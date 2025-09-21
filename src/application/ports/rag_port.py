from abc import ABC, abstractmethod
from typing import Any


class RAGPort(ABC):
    """検索拡張生成（RAG）システムのインターフェース"""

    @abstractmethod
    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """ベクトル検索を実行

        Args:
            query: 検索クエリ
            top_k: 取得する結果数

        Returns:
            検索結果のリスト
        """
        ...

    @abstractmethod
    def search_and_generate(self, query: str, top_k: int = 5) -> dict[str, Any]:
        """検索拡張生成（RAG）を実行

        Args:
            query: 検索クエリ
            top_k: 検索する結果数

        Returns:
            検索結果と生成された回答を含む辞書
        """
        ...

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """RAGシステムの状態を取得

        Returns:
            システム状態の辞書
        """
        ...
