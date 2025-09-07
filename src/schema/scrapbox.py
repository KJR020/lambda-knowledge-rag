"""Scrapbox-related schemas."""

from typing import Any

from pydantic import BaseModel


class ScrapboxPage(BaseModel):
    """Schema for Scrapbox page from API response."""

    id: str
    title: str
    updated: int
    views: int | None = None
    linked: int | None = None
    commitId: str | None = None


class ScrapboxPageContent(BaseModel):
    """Schema for Scrapbox page content with lines."""

    id: str
    title: str
    updated: int
    lines: list[dict[str, Any]]
    links: list[str] | None = None
    icons: list[str] | None = None


class MarkdownDocument(BaseModel):
    """Schema for converted markdown document."""

    page_id: str
    title: str
    content: str
    metadata: dict[str, Any]
    s3_key: str
    processed_at: str


class ETLResult(BaseModel):
    """Schema for ETL process result."""

    total_pages: int
    successful: int
    failed: int
    errors: list[str]
    processed_at: str
