from typing import Any

from pydantic import BaseModel


class QueryRequest(BaseModel):
    """ナレッジ検索リクエストのスキーマ"""

    query: str


class QueryResponse(BaseModel):
    """ナレッジ検索レスポンスのスキーマ"""

    query: str
    document: dict[str, Any]


class ErrorResponse(BaseModel):
    """エラー応答のスキーマ"""

    error: str
    message: str
    status_code: int
