from pydantic import BaseModel


class DocumentSchema(BaseModel):
    """ナレッジドキュメントのスキーマ"""

    id: str
    text: str


class DocumentSearchResult(BaseModel):
    """ドキュメント検索結果のスキーマ"""

    documents: list[DocumentSchema]
    total_count: int
    query: str
