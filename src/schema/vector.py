from typing import Any

from pydantic import BaseModel, Field


class VectorMetadata(BaseModel):
    """ベクトルに付与するメタデータ"""

    text: str = Field(..., description="元のテキスト内容")
    source: str = Field(..., description="データソース（例: scrapbox, s3）")
    source_id: str = Field(..., description="ソース内でのユニークID")
    title: str | None = Field(None, description="ドキュメントタイトル")
    url: str | None = Field(None, description="参照URL")
    created_at: str | None = Field(None, description="作成日時")
    updated_at: str | None = Field(None, description="更新日時")
    tags: list[str] | None = Field(default_factory=list, description="タグリスト")
    chunk_index: int | None = Field(
        None, description="分割されたチャンクのインデックス"
    )
    total_chunks: int | None = Field(None, description="総チャンク数")


class VectorData(BaseModel):
    """Pineconeに登録するベクトルデータ"""

    id: str = Field(..., description="ベクトルのユニークID")
    values: list[float] = Field(..., description="Embeddingベクトル")
    metadata: VectorMetadata = Field(..., description="メタデータ")


class SearchResult(BaseModel):
    """検索結果"""

    id: str = Field(..., description="ベクトルID")
    score: float = Field(..., description="類似度スコア（0-1）")
    metadata: VectorMetadata = Field(..., description="メタデータ")


class SearchFilter(BaseModel):
    """検索フィルター条件"""

    source: str | None = Field(None, description="データソースでフィルタ")
    tags: list[str] | None = Field(None, description="タグでフィルタ")
    created_after: str | None = Field(None, description="作成日時の下限")
    created_before: str | None = Field(None, description="作成日時の上限")

    def to_pinecone_filter(self) -> dict[str, Any] | None:
        """Pinecone用のフィルター形式に変換"""
        conditions = []

        if self.source:
            conditions.append({"source": {"$eq": self.source}})

        if self.tags:
            conditions.append({"tags": {"$in": self.tags}})

        if self.created_after:
            conditions.append({"created_at": {"$gte": self.created_after}})

        if self.created_before:
            conditions.append({"created_at": {"$lte": self.created_before}})

        if not conditions:
            return None

        return {"$and": conditions} if len(conditions) > 1 else conditions[0]
