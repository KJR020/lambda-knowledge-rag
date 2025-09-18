from typing import Any

from pydantic import BaseModel


class ScrapboxPage(BaseModel):
    """API レスポンスから返されるScrapboxページのスキーマ"""

    id: str
    title: str
    updated: int
    views: int | None = None
    linked: int | None = None
    commitId: str | None = None


class ScrapboxPageContent(BaseModel):
    """行単位のコンテンツを含むScrapboxページのスキーマ"""

    id: str
    title: str
    updated: int
    lines: list[dict[str, Any]]
    links: list[str] | None = None
    icons: list[str] | None = None


class MarkdownDocument(BaseModel):
    """変換済みのMarkdownドキュメントのスキーマ"""

    page_id: str
    title: str
    content: str
    metadata: dict[str, Any]
    s3_key: str
    processed_at: str


class ETLResult(BaseModel):
    """ETL処理の結果を表すスキーマ"""

    total_pages: int
    successful: int
    failed: int
    errors: list[str]
    processed_at: str
