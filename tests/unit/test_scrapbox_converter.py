"""Tests for Scrapbox markdown converter."""

from core.converter import ScrapboxMarkdownConverter


class TestScrapboxMarkdownConverter:
    """Test cases for ScrapboxMarkdownConverter."""

    def setup_method(self):
        """Set up test fixtures."""
        self.converter = ScrapboxMarkdownConverter("test-project")

    def test_convert_empty_text(self):
        """Test converting empty text."""
        result = self.converter.convert("")
        assert result == ""

    def test_convert_headers(self):
        """Test converting Scrapbox headers to Markdown."""
        scrapbox_text = "[* Header 1]\n[** Header 2]\n[*** Header 3]"
        result = self.converter.convert(scrapbox_text)

        expected = "# Header 1\n## Header 2\n### Header 3"
        assert result == expected

    def test_convert_links(self):
        """Test converting Scrapbox links to Markdown."""
        scrapbox_text = "Check out [[My Page]] for more info"
        result = self.converter.convert(scrapbox_text)

        expected = "Check out [My Page](https://scrapbox.io/test-project/My%20Page) for more info"
        assert result == expected

    def test_convert_code_blocks(self):
        """Test converting Scrapbox code blocks."""
        scrapbox_text = "code:python\nprint('hello')"
        result = self.converter.convert(scrapbox_text)

        expected = "```python\nprint('hello')"
        assert result == expected

    def test_convert_with_metadata(self):
        """Test converting with metadata frontmatter."""
        scrapbox_text = "Some content"
        metadata = {
            "id": "page-123",
            "title": "Test Page",
            "updated": 1640995200,  # 2022-01-01 00:00:00 UTC
        }

        result = self.converter.convert(scrapbox_text, metadata)

        assert "---" in result
        assert "title: Test Page" in result
        assert "page_id: page-123" in result
        assert "url: https://scrapbox.io/test-project/Test%20Page" in result
        assert "updated_at: 2022-01-01T00:00:00Z" in result
        assert "# Test Page" in result
        assert "Some content" in result

    def test_complex_conversion(self):
        """Test converting complex Scrapbox markup."""
        scrapbox_text = """[* Introduction]
This is a page about [[Programming]].

[** Python Examples]
Here's some code:
code:python
def hello():
    return "world"

Check out [[Other Page]] too!"""

        result = self.converter.convert(scrapbox_text)

        assert "# Introduction" in result
        assert "## Python Examples" in result
        assert "[Programming](https://scrapbox.io/test-project/Programming)" in result
        assert "[Other Page](https://scrapbox.io/test-project/Other%20Page)" in result
        assert "```python" in result
