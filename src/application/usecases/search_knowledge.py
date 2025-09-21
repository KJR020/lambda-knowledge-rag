import logging
from typing import Any

from application.ports.rag_port import RAGPort

logger = logging.getLogger(__name__)


class SearchKnowledgeUseCase:
    """ナレッジベースを検索するユースケース"""

    def __init__(self, rag_port: RAGPort):
        self.rag_port = rag_port
        logger.info("SearchKnowledgeUseCase initialized")

    def search_documents(self, query: str, top_k: int = 5) -> dict[str, Any]:
        """ドキュメントのベクトル検索を実行

        Args:
            query: 検索クエリ
            top_k: 取得する結果数

        Returns:
            検索結果を含む辞書
        """
        try:
            logger.info(f"Searching documents for query: {query[:50]}...")

            # バリデーション
            if not query.strip():
                raise ValueError("検索クエリが空です")

            if top_k <= 0 or top_k > 20:
                raise ValueError("top_kは1-20の範囲で指定してください")

            # RAGポートで検索実行
            search_results = self.rag_port.search(query, top_k)

            result = {
                "query": query,
                "results": search_results,
                "total_count": len(search_results),
                "status": "success",
            }

            logger.info(f"Found {len(search_results)} documents")
            return result

        except Exception as e:
            logger.error(f"Error in search_documents: {e}")
            return {
                "query": query,
                "results": [],
                "total_count": 0,
                "status": "error",
                "error": str(e),
            }

    def search_and_answer(self, query: str, top_k: int = 5) -> dict[str, Any]:
        """検索拡張生成（RAG）で質問に回答

        Args:
            query: 質問
            top_k: 検索する結果数

        Returns:
            回答と参照情報を含む辞書
        """
        try:
            logger.info(f"Generating answer for query: {query[:50]}...")

            # バリデーション
            if not query.strip():
                raise ValueError("質問が空です")

            if top_k <= 0 or top_k > 20:
                raise ValueError("top_kは1-20の範囲で指定してください")

            # RAGポートで回答生成
            rag_result = self.rag_port.search_and_generate(query, top_k)

            result = {
                "query": query,
                "answer": rag_result.get("answer", ""),
                "citations": rag_result.get("citations", []),
                "metadata": rag_result.get("metadata", {}),
                "session_id": rag_result.get("session_id"),
                "status": "success",
            }

            logger.info("Answer generated successfully")
            return result

        except Exception as e:
            logger.error(f"Error in search_and_answer: {e}")
            return {
                "query": query,
                "answer": "",
                "citations": [],
                "metadata": {},
                "status": "error",
                "error": str(e),
            }

    def get_system_status(self) -> dict[str, Any]:
        """システム状態を取得

        Returns:
            システム状態の辞書
        """
        try:
            status = self.rag_port.get_status()
            return {"status": "success", "system_info": status}
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {"status": "error", "error": str(e), "system_info": {}}
