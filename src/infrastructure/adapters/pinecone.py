from collections.abc import Sequence
from typing import Any

import pinecone  # type: ignore

from schema.vector import SearchFilter, SearchResult, VectorData, VectorMetadata


class PineConeClient:
    def __init__(
        self,
        api_key: str | None = None,
        environment: str | None = None,
        index_name: str | None = None,
        namespace: str | None = None,
    ) -> None:
        """Pinecone接続とIndexバインドを初期化する。"""
        api_key = api_key
        environment = environment
        index_name = index_name
        self.namespace = namespace

        # SDK初期化 & Indexバインド
        pinecone.init(api_key=api_key, environment=environment)
        self.index = pinecone.Index(index_name)

    def upsert(self, vectors: list[VectorData]) -> dict[str, int]:
        """ベクトルをupsertする"""
        # VectorDataからPinecone形式に変換
        pinecone_vectors = []
        for vector in vectors:
            pinecone_vectors.append(
                {
                    "id": vector.id,
                    "values": vector.values,
                    "metadata": vector.metadata.model_dump(),
                }
            )

        result = self.index.upsert(vectors=pinecone_vectors, namespace=self.namespace)
        return {"upserted_count": result.get("upserted_count", 0)}

    def upsert_one(
        self,
        id: str,
        values: Sequence[float],
        metadata: VectorMetadata,
    ) -> dict[str, int]:
        """1件だけupsertするユーティリティ。"""
        vector_data = VectorData(
            id=id,
            values=list(values),
            metadata=metadata,
        )
        return self.upsert([vector_data])

    # --- R(ead): 類似検索 ---
    def query(
        self,
        vector: Sequence[float],
        top_k: int = 5,
        filter: SearchFilter | None = None,
    ) -> list[SearchResult]:
        """クエリベクトルで類似検索する。"""
        pinecone_filter = filter.to_pinecone_filter() if filter else None

        results = self.index.query(
            vector=list(vector),
            top_k=top_k,
            namespace=self.namespace,
            filter=pinecone_filter,
            include_metadata=True,
        )

        # SearchResultのリストに変換
        search_results = []
        for match in results.get("matches", []):
            metadata = match.get("metadata", {})
            search_result = SearchResult(
                id=match["id"],
                score=match["score"],
                metadata=VectorMetadata(**metadata),
            )
            search_results.append(search_result)

        return search_results

    def fetch(self, ids: list[str]) -> Any:
        """id指定でレコードを取得する。"""
        return self.index.fetch(ids=ids, namespace=self.namespace)

    def delete(
        self,
        ids: list[str] | None = None,
        *,
        delete_all: bool = False,
        filter: dict[str, Any] | None = None,
    ) -> Any:
        """レコードを削除する。id指定 / フィルタ / 全削除 をサポート"""
        return self.index.delete(
            ids=ids,
            delete_all=delete_all,
            filter=filter,
            namespace=self.namespace,
        )
