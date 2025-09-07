"""Tests for Scrapbox client."""

from unittest.mock import Mock, patch

import pytest
import requests

from core.clients import ScrapboxClient


class TestScrapboxClient:
    """Test cases for ScrapboxClient."""

    def setup_method(self):
        """Set up test fixtures."""
        with patch("core.clients.CONFIG") as mock_config:
            # コンフィグをモックする
            mock_config.scrapbox_project = "test-project"
            mock_config.scrapbox_api_token = "test-token"

            self.client = ScrapboxClient()

    @patch("core.clients.requests.Session.get")
    def test_get_pages_success(self, mock_get):
        """Test successful page retrieval."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "pages": [
                {"id": "page1", "title": "Test Page 1", "updated": 1640995200},
                {"id": "page2", "title": "Test Page 2", "updated": 1640995300},
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        pages = self.client.get_pages()

        assert len(pages) == 2
        assert pages[0]["id"] == "page1"
        assert pages[0]["title"] == "Test Page 1"
        mock_get.assert_called_once_with("https://scrapbox.io/api/pages/test-project")

    @patch("core.clients.requests.Session.get")
    def test_get_pages_api_error(self, mock_get):
        """Test API error handling for get_pages."""
        mock_get.side_effect = requests.HTTPError("API Error")

        with pytest.raises(requests.HTTPError):
            self.client.get_pages()

    @patch("core.clients.requests.Session.get")
    def test_get_page_content_success(self, mock_get):
        """Test successful page content retrieval."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "page1",
            "title": "Test Page",
            "lines": [
                {"text": "[* Title]"},
                {"text": "Some content here"},
                {"text": "[[Linked Page]]"},
            ],
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        content = self.client.get_page_content("Test Page")

        assert content["id"] == "page1"
        assert content["title"] == "Test Page"
        assert len(content["lines"]) == 3
        mock_get.assert_called_once_with(
            "https://scrapbox.io/api/pages/test-project/Test Page"
        )

    @patch("core.clients.requests.Session.get")
    def test_get_page_content_api_error(self, mock_get):
        """Test API error handling for get_page_content."""
        mock_get.side_effect = requests.HTTPError("API Error")

        with pytest.raises(requests.HTTPError):
            self.client.get_page_content("Test Page")

    def test_initialization_with_params(self):
        """Test client initialization with custom parameters."""
        client = ScrapboxClient(project="custom-project", api_token="custom-token")

        assert client.project == "custom-project"
        assert client.api_token == "custom-token"
        assert "connect.sid=custom-token" in str(
            client.session.headers.get("Cookie", "")
        )

    def test_initialization_without_token(self):
        """Test client initialization without API token."""
        with patch("core.clients.CONFIG") as mock_config:
            mock_config.scrapbox_project = "test-project"
            mock_config.scrapbox_api_token = None
            client = ScrapboxClient()

            assert client.project == "test-project"
            assert client.api_token is None
            assert "Cookie" not in client.session.headers
