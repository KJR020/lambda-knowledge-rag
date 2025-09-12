from typing import Any

import boto3
import requests

from core.config import CONFIG
from schema.document import DocumentSchema


class S3Client:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            region_name=CONFIG.aws_region,
        )

    def upload_markdown_file(self, bucket: str, key: str, content: str) -> None:
        """マークダウンファイルをS3にアップロードする"""
        self.s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=content.encode("utf-8"),
            ContentType="text/markdown",
        )

    def upload_metadata_file(
        self, bucket: str, key: str, metadata: dict[str, Any]
    ) -> None:
        """メタデータJSONファイルをS3にアップロードする"""
        import json

        self.s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps(metadata, indent=2).encode("utf-8"),
            ContentType="application/json",
        )

    def list_objects(self, bucket: str, prefix: str = "") -> list[str]:
        """指定されたプレフィックスでS3バケット内のオブジェクトをリストする"""
        response = self.s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        return [obj["Key"] for obj in response.get("Contents", [])]


class ScrapboxClient:
    """Scrapbox APIとやり取りするためのクライアント"""

    def __init__(self, project: str = None, api_token: str = None):
        self.project = project or CONFIG.scrapbox_project
        self.api_token = api_token or CONFIG.scrapbox_api_token
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


class KnowledgeClient:
    """検索機能を提供するクライアント"""

    def __init__(self, s3_client: S3Client | None = None):
        self.s3 = s3_client or S3Client()

    def find(self, query: str) -> DocumentSchema:
        """指定されたクエリに対して最小限のスタブ検索結果を返す"""
        # TODO: replace stub with real retrieval logic (vector DB, etc.)
        raw_data = {"id": "stub-1", "text": f"result for {query}"}
        return DocumentSchema(**raw_data)
