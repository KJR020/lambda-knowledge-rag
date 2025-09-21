import hashlib
import hmac
import json
import logging
from typing import Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event: dict, context: Any) -> dict:
    """Lambdaのエントリポイント"""
    logger.info("Event: %s", json.dumps(event))

    # シグネチャの検証
    actual_signature = event.get("headers", {}).get("x-signature")
    secret = "dummy_secret"  # 実際には安全に管理されたシークレットを使用
    expected_signature = hash_event(event, secret)

    is_valid_signature = verify_signature(actual_signature, expected_signature)

    if not is_valid_signature:
        return {"statusCode": 401, "body": {"error": "Invalid signature"}}

    logger.info("Signature verified")

    return {}


def upsert_scrapbox_page(page_title: str, content: str) -> dict:
    """更新処理
    scrapboxのページを取得
    S3に保存
    KBでベクトル化する
    pineconeに保存

    Args:
        page_title: Scrapboxページタイトル
        content: ページコンテンツ（今回は使用せず、ScrapboxETLProcessorが取得）

    Returns:
        処理結果の辞書
    """
    from infrastructure.adapters.etl import ScrapboxETLProcessor

    try:
        # ETLプロセッサでページを処理
        processor = ScrapboxETLProcessor()
        result = processor.process_page(page_title)

        logger.info(f"Page processing result: {result}")
        return result

    except Exception as e:
        logger.error(f"Error in upsert_scrapbox_page: {e}")
        return {"page_title": page_title, "success": False, "error": str(e)}


def hash_event(event: dict, secret: str) -> str:
    """期待されるシグネチャの計算"""
    expected_signature = hmac.new(
        secret.encode(), json.dumps(event).encode(), hashlib.sha256
    ).hexdigest()
    return expected_signature


def verify_signature(signature: str, expected_signature: str) -> bool:
    """シグネチャの検証"""
    if not hmac.compare_digest(signature, expected_signature):
        logger.warning("Invalid signature")
        return False
    return True
