"""Scrapbox → S3 → ベクトルDB のETL処理"""

import logging
from datetime import datetime
from typing import Any

from core.clients.embeddings import EmbeddingsClient
try:
    from core.clients.pinecone import PineConeClient
except ImportError:
    PineConeClient = None
from core.clients.s3 import S3Client
from core.clients.scrapbox import ScrapboxClient
from infrastructure.config.config import CONFIG
from schema.vector import VectorMetadata

logger = logging.getLogger(__name__)


class ScrapboxETLProcessor:
    """ScrapboxページのETL処理を行うプロセッサ"""

    def __init__(
        self,
        scrapbox_client: ScrapboxClient | None = None,
        s3_client: S3Client | None = None,
        embeddings_client: EmbeddingsClient | None = None,
        pinecone_client = None,
    ):
        self.scrapbox = scrapbox_client or ScrapboxClient(
            project=CONFIG.scrapbox_project,
            api_token=CONFIG.scrapbox_api_token,
        )
        self.s3 = s3_client or S3Client()
        self.embeddings = embeddings_client or EmbeddingsClient()
        self.pinecone = pinecone_client

    def process_page(self, page_title: str) -> dict[str, Any]:
        """単一のScrapboxページを処理する

        Args:
            page_title: 処理対象のページタイトル

        Returns:
            処理結果の辞書
        """
        result = {
            "page_title": page_title,
            "success": False,
            "steps": {},
        }

        try:
            # 1. Scrapboxからページを取得
            logger.info(f"Fetching page: {page_title}")
            page_data = self.scrapbox.get_page_content(page_title)
            result["steps"]["fetch"] = "completed"

            # 2. S3に保存（元データ）
            s3_key = f"scrapbox/{CONFIG.scrapbox_project}/{page_title}.json"
            logger.info(f"Saving to S3: {s3_key}")
            self.s3.upload_json_file(
                bucket=CONFIG.s3_bucket, key=s3_key, data=page_data
            )
            result["steps"]["s3_upload"] = "completed"

            # 3. テキスト抽出とベクトル化
            page_text = self._extract_text_from_page(page_data)
            logger.info(f"Generating embeddings for page: {page_title}")
            embeddings = self.embeddings.embed_text(page_text)
            result["steps"]["embeddings"] = "completed"

            # 4. メタデータ準備
            metadata = self._prepare_metadata(page_data, s3_key)

            # 5. Pineconeに保存（オプション）
            if self.pinecone:
                vector_id = f"{CONFIG.scrapbox_project}#{page_title}"
                logger.info(f"Upserting to Pinecone: {vector_id}")
                self.pinecone.upsert_one(
                    id=vector_id, values=embeddings, metadata=metadata
                )
                result["steps"]["pinecone_upsert"] = "completed"

            # 6. メタデータをS3に保存
            metadata_key = f"metadata/{CONFIG.scrapbox_project}/{page_title}.json"
            metadata_dict = {
                "vector_id": f"{CONFIG.scrapbox_project}#{page_title}",
                "embeddings_model": self.embeddings.get_model_info(),
                "metadata": metadata.model_dump(),
                "processed_at": datetime.utcnow().isoformat(),
            }
            self.s3.upload_metadata_file(
                bucket=CONFIG.s3_bucket, key=metadata_key, metadata=metadata_dict
            )
            result["steps"]["metadata_upload"] = "completed"

            result["success"] = True
            logger.info(f"Successfully processed page: {page_title}")

        except Exception as e:
            logger.error(f"Error processing page {page_title}: {e}")
            result["error"] = str(e)

        return result

    def process_all_pages(self) -> dict[str, Any]:
        """プロジェクトの全ページを処理する"""
        results = {
            "project": CONFIG.scrapbox_project,
            "total_pages": 0,
            "successful": 0,
            "failed": 0,
            "pages": [],
        }

        try:
            # 全ページのリストを取得
            logger.info(f"Fetching all pages from project: {CONFIG.scrapbox_project}")
            pages = self.scrapbox.get_pages()
            results["total_pages"] = len(pages)

            # 各ページを処理
            for page in pages:
                page_title = page.get("title", "")
                if not page_title:
                    continue

                logger.info(
                    f"Processing page {results['successful'] + results['failed'] + 1}/{len(pages)}: {page_title}"
                )
                page_result = self.process_page(page_title)

                if page_result["success"]:
                    results["successful"] += 1
                else:
                    results["failed"] += 1

                results["pages"].append(page_result)

        except Exception as e:
            logger.error(f"Error in batch processing: {e}")
            results["error"] = str(e)

        return results

    def _extract_text_from_page(self, page_data: dict[str, Any]) -> str:
        """Scrapboxページからテキストを抽出する

        Args:
            page_data: Scrapbox API から取得したページデータ

        Returns:
            抽出したテキスト
        """
        # タイトル
        title = page_data.get("title", "")

        # 本文（各行のテキストを結合）
        lines = page_data.get("lines", [])
        body_lines = []
        for line in lines:
            text = line.get("text", "")
            if text:
                body_lines.append(text)

        body = "\n".join(body_lines)

        # タイトルと本文を結合
        full_text = f"{title}\n\n{body}"

        return full_text

    def _prepare_metadata(
        self, page_data: dict[str, Any], s3_key: str
    ) -> VectorMetadata:
        """ベクトルDBに保存するメタデータを準備する

        Args:
            page_data: Scrapboxページデータ
            s3_key: S3に保存したキー

        Returns:
            VectorMetadata インスタンス
        """
        # ページの説明文を取得（最初の数行）
        descriptions = page_data.get("descriptions", [])
        description = " ".join(descriptions[:3]) if descriptions else ""

        # タグを抽出（リンクから）
        links = page_data.get("links", [])
        tags = links[:10] if links else []  # 最大10個のタグ

        metadata = VectorMetadata(
            source="scrapbox",
            project_name=CONFIG.scrapbox_project,
            page_title=page_data.get("title", ""),
            page_id=page_data.get("id", ""),
            content_preview=description[:500],  # 最大500文字
            url=f"https://scrapbox.io/{CONFIG.scrapbox_project}/{page_data.get('title', '')}",
            s3_key=s3_key,
            created_at=page_data.get("created", 0),
            updated_at=page_data.get("updated", 0),
            tags=tags,
            character_count=page_data.get("charsCount", 0),
            lines_count=page_data.get("linesCount", 0),
        )

        return metadata
