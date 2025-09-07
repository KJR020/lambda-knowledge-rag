import hashlib
import hmac
import json
import logging
from typing import Any

from src.core.clients import KnowledgeClient
from src.schema import QueryRequest

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event: dict, context: Any) -> dict:
    """Lambda function entry point with signature verification and inference."""
    logger.info("Event: %s", json.dumps(event))

    # シグネチャの検証
    signature = event.get("headers", {}).get("x-signature")
    if not signature:
        logger.warning("Missing signature")
        return {"statusCode": 400, "body": "Missing signature"}

    # 期待されるシグネチャの計算
    secret = "my_secret"
    expected_signature = hmac.new(
        secret.encode(), json.dumps(event).encode(), hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(signature, expected_signature):
        logger.warning("Invalid signature")
        return {"statusCode": 403, "body": "Invalid signature"}

    logger.info("Signature verified")

    try:
        # ナレッジ推論の実行
        request = QueryRequest(**event)
        knowledge_client = KnowledgeClient()
        # 既にDocumentSchemaオブジェクト
        document = knowledge_client.find(request.query)

        return {
            "statusCode": 200,
            "body": {
                "query": request.query,
                "document": document.model_dump(),  # 辞書に変換
            },
        }
    except Exception as e:
        logger.error("Error processing request: %s", str(e))
        return {"statusCode": 500, "body": {"error": "Internal server error"}}
