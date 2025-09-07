from typing import Any

import requests

from core.config import CONFIG


class ScrapboxClient:
    """Scrapbox APIとやり取りするためのクライアント"""

    def __init__(self, project: str, api_token: str):
        self.project = CONFIG.scrapbox_project
        self.api_token = CONFIG.scrapbox_api_token
        self.base_url = "https://scrapbox.io/api"
        self.session = requests.Session()

        if self.api_token:
            self.session.headers.update({"Cookie": f"connect.sid={self.api_token}"})

    def get_pages(self) -> list[dict[str, Any]]:
        """Scrapboxプロジェクトからすべてのページを取得する"""
        url = f"{self.base_url}/pages/{self.project}"
        response = self.session.get(url)
        response.raise_for_status()

        data = response.json()
        return data.get("pages", [])

    def get_page_content(self, title: str) -> dict[str, Any]:
        """特定のページの詳細なコンテンツを取得する"""
        url = f"{self.base_url}/pages/{self.project}/{title}"
        response = self.session.get(url)
        response.raise_for_status()

        return response.json()
