from schema.document import DocumentSchema

from .s3 import S3Client


class KnowledgeClient:
    """検索機能を提供するクライアント"""

    def __init__(self, s3_client: S3Client | None = None):
        self.s3 = s3_client or S3Client()

    def find(self, query: str) -> DocumentSchema:
        """指定されたクエリに対して最小限のスタブ検索結果を返す"""
        # TODO: スタブを実際の検索ロジック（ベクタDB等）に置き換える
        raw_data = {"id": "stub-1", "text": f"result for {query}"}
        return DocumentSchema(**raw_data)
