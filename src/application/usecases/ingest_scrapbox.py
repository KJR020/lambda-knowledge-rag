import logging
from typing import Any

from infrastructure.adapters.etl import ScrapboxETLProcessor

logger = logging.getLogger(__name__)


class IngestScrapboxUseCase:
    """Scrapboxページの取り込みを行うユースケース"""

    def __init__(self, etl_processor: ScrapboxETLProcessor = None):
        self.etl_processor = etl_processor or ScrapboxETLProcessor()
        logger.info("IngestScrapboxUseCase initialized")

    def ingest_page(self, page_title: str) -> dict[str, Any]:
        """単一のScrapboxページを取り込み

        Args:
            page_title: ページタイトル

        Returns:
            取り込み結果を含む辞書
        """
        try:
            logger.info(f"Starting ingest for page: {page_title}")

            # バリデーション
            if not page_title.strip():
                raise ValueError("ページタイトルが空です")

            # ETLプロセッサで処理実行
            result = self.etl_processor.process_page(page_title)

            # 結果を整理
            response = {
                "page_title": page_title,
                "success": result.get("success", False),
                "steps_completed": list(result.get("steps", {}).keys()),
                "status": "completed" if result.get("success") else "failed",
            }

            if not result.get("success"):
                response["error"] = result.get("error", "Unknown error")

            logger.info(
                f"Ingest completed for page: {page_title}, success: {response['success']}"
            )
            return response

        except Exception as e:
            logger.error(f"Error in ingest_page: {e}")
            return {
                "page_title": page_title,
                "success": False,
                "steps_completed": [],
                "status": "error",
                "error": str(e),
            }

    def ingest_all_pages(self) -> dict[str, Any]:
        """プロジェクトの全ページを取り込み

        Returns:
            取り込み結果を含む辞書
        """
        try:
            logger.info("Starting batch ingest for all pages")

            # ETLプロセッサで全ページ処理
            result = self.etl_processor.process_all_pages()

            # 結果を整理
            response = {
                "project": result.get("project"),
                "total_pages": result.get("total_pages", 0),
                "successful": result.get("successful", 0),
                "failed": result.get("failed", 0),
                "success_rate": 0.0,
                "status": "completed",
            }

            # 成功率を計算
            if response["total_pages"] > 0:
                response["success_rate"] = (
                    response["successful"] / response["total_pages"]
                )

            if result.get("error"):
                response["error"] = result["error"]
                response["status"] = "error"

            logger.info(
                f"Batch ingest completed: {response['successful']}/{response['total_pages']} pages successful"
            )
            return response

        except Exception as e:
            logger.error(f"Error in ingest_all_pages: {e}")
            return {
                "project": None,
                "total_pages": 0,
                "successful": 0,
                "failed": 0,
                "success_rate": 0.0,
                "status": "error",
                "error": str(e),
            }

    def get_ingest_status(self, page_title: str = None) -> dict[str, Any]:
        """取り込み状態を取得

        Args:
            page_title: 特定のページタイトル（省略時は全体の状態）

        Returns:
            状態情報を含む辞書
        """
        try:
            # TODO: 実際の状態確認ロジックを実装
            # S3やデータベースから取り込み状況を確認

            if page_title:
                # 特定ページの状態
                return {
                    "page_title": page_title,
                    "status": "unknown",
                    "last_updated": None,
                    "error": "Status check not implemented yet",
                }
            else:
                # 全体の状態
                return {
                    "total_ingested": 0,
                    "last_ingest_time": None,
                    "status": "unknown",
                    "error": "Status check not implemented yet",
                }

        except Exception as e:
            logger.error(f"Error getting ingest status: {e}")
            return {"status": "error", "error": str(e)}
