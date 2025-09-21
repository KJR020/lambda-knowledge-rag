"""
Bedrock Knowledge Base データソース同期用のLambda関数
S3にファイルが追加/更新された際に自動的にKnowledge Baseのデータソースを同期する
"""

import json
import logging
import os
from typing import Any

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 環境変数から設定を取得
KNOWLEDGE_BASE_ID = os.environ.get("KNOWLEDGE_BASE_ID")
DATA_SOURCE_ID = os.environ.get("DATA_SOURCE_ID")

# Bedrockクライアントを初期化
bedrock_agent = boto3.client("bedrock-agent")


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """
    S3イベントをトリガーにKnowledge Baseのデータソースを同期

    Args:
        event: S3イベント
        context: Lambda context

    Returns:
        実行結果
    """
    logger.info(f"Received event: {json.dumps(event)}")

    if not KNOWLEDGE_BASE_ID or not DATA_SOURCE_ID:
        logger.error("Required environment variables not set")
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"error": "KNOWLEDGE_BASE_ID and DATA_SOURCE_ID must be set"}
            ),
        }

    try:
        # S3イベントを解析
        s3_events = []

        if "Records" in event:
            for record in event["Records"]:
                if record.get("eventSource") == "aws:s3":
                    bucket = record["s3"]["bucket"]["name"]
                    key = record["s3"]["object"]["key"]
                    event_name = record["eventName"]

                    s3_events.append(
                        {"bucket": bucket, "key": key, "event": event_name}
                    )

        if not s3_events:
            logger.info("No S3 events found")
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "No S3 events to process"}),
            }

        logger.info(f"Processing {len(s3_events)} S3 events")

        # Knowledge Baseデータソースの同期を開始
        sync_result = start_data_source_sync()

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "Data source sync initiated",
                    "sync_job_id": sync_result.get("ingestionJobId"),
                    "processed_events": len(s3_events),
                    "s3_events": s3_events,
                }
            ),
        }

    except Exception as e:
        logger.error(f"Error processing S3 event: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}


def start_data_source_sync() -> dict[str, Any]:
    """
    Bedrock Knowledge Baseのデータソース同期を開始

    Returns:
        同期ジョブの情報
    """
    try:
        # 既存の実行中ジョブをチェック
        list_response = bedrock_agent.list_ingestion_jobs(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            dataSourceId=DATA_SOURCE_ID,
            maxResults=10,
        )

        # 実行中のジョブがあるかチェック
        running_jobs = [
            job
            for job in list_response.get("ingestionJobSummaries", [])
            if job.get("status") in ["STARTING", "IN_PROGRESS"]
        ]

        if running_jobs:
            logger.info(
                f"Ingestion job already running: {running_jobs[0]['ingestionJobId']}"
            )
            return running_jobs[0]

        # 新しい同期ジョブを開始
        response = bedrock_agent.start_ingestion_job(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            dataSourceId=DATA_SOURCE_ID,
            description="Automatic sync triggered by S3 event",
        )

        job_id = response.get("ingestionJob", {}).get("ingestionJobId")
        logger.info(f"Started ingestion job: {job_id}")

        return response.get("ingestionJob", {})

    except ClientError as e:
        logger.error(f"Bedrock API error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error starting sync: {e}")
        raise


def get_ingestion_job_status(job_id: str) -> dict[str, Any]:
    """
    同期ジョブの状態を取得（デバッグ用）

    Args:
        job_id: ジョブID

    Returns:
        ジョブの状態情報
    """
    try:
        response = bedrock_agent.get_ingestion_job(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            dataSourceId=DATA_SOURCE_ID,
            ingestionJobId=job_id,
        )

        return response.get("ingestionJob", {})

    except ClientError as e:
        logger.error(f"Error getting ingestion job status: {e}")
        raise
