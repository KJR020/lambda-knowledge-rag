"""
AWS Bedrock Knowledge BaseのRAGPort実装
"""

import logging
from typing import Any

try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:
    boto3 = None
    ClientError = Exception

from application.ports.rag_port import RAGPort

logger = logging.getLogger(__name__)


class BedrockKBAdapter(RAGPort):
    """AWS Bedrock Knowledge BaseのRAGPort実装"""

    def __init__(
        self,
        knowledge_base_id: str,
        region_name: str = "us-east-1",
        model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0",
    ):
        """
        初期化

        Args:
            knowledge_base_id: Bedrock Knowledge BaseのID
            region_name: AWSリージョン
            model_id: 使用するLLMモデルID
        """
        if boto3 is None:
            raise ImportError("boto3が必要です。pip install boto3を実行してください。")

        self.knowledge_base_id = knowledge_base_id
        self.region_name = region_name
        self.model_id = model_id

        # Bedrock Knowledge Baseクライアントを初期化
        self.bedrock_agent_runtime = boto3.client(
            "bedrock-agent-runtime", region_name=region_name
        )

        logger.info(f"BedrockKBAdapter initialized with KB ID: {knowledge_base_id}")

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """
        Bedrock Knowledge Baseでベクトル検索を実行

        Args:
            query: 検索クエリ
            top_k: 取得する結果数

        Returns:
            検索結果のリスト
        """
        try:
            response = self.bedrock_agent_runtime.retrieve(
                knowledgeBaseId=self.knowledge_base_id,
                retrievalQuery={"text": query},
                retrievalConfiguration={
                    "vectorSearchConfiguration": {"numberOfResults": top_k}
                },
            )

            results = []
            for item in response.get("retrievalResults", []):
                result = {
                    "id": item.get("metadata", {}).get(
                        "x-amz-bedrock-kb-source-uri", ""
                    ),
                    "score": item.get("score", 0.0),
                    "content": item.get("content", {}).get("text", ""),
                    "metadata": item.get("metadata", {}),
                    "location": item.get("location", {}),
                }
                results.append(result)

            logger.info(f"Retrieved {len(results)} results for query: {query[:50]}...")
            return results

        except ClientError as e:
            logger.error(f"Bedrock Knowledge Base search error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in search: {e}")
            raise

    def search_and_generate(self, query: str, top_k: int = 5) -> dict[str, Any]:
        """
        検索拡張生成（RAG）を実行

        Args:
            query: 検索クエリ
            top_k: 検索する結果数

        Returns:
            検索結果と生成された回答を含む辞書
        """
        try:
            response = self.bedrock_agent_runtime.retrieve_and_generate(
                input={"text": query},
                retrieveAndGenerateConfiguration={
                    "type": "KNOWLEDGE_BASE",
                    "knowledgeBaseConfiguration": {
                        "knowledgeBaseId": self.knowledge_base_id,
                        "modelArn": f"arn:aws:bedrock:{self.region_name}::foundation-model/{self.model_id}",
                        "retrievalConfiguration": {
                            "vectorSearchConfiguration": {"numberOfResults": top_k}
                        },
                    },
                },
            )

            # レスポンスを整理
            result = {
                "query": query,
                "answer": response.get("output", {}).get("text", ""),
                "citations": [],
                "session_id": response.get("sessionId"),
                "metadata": {
                    "model_id": self.model_id,
                    "knowledge_base_id": self.knowledge_base_id,
                    "top_k": top_k,
                },
            }

            # 引用情報を追加
            for citation in response.get("citations", []):
                for reference in citation.get("retrievedReferences", []):
                    citation_info = {
                        "content": reference.get("content", {}).get("text", ""),
                        "location": reference.get("location", {}),
                        "metadata": reference.get("metadata", {}),
                    }
                    result["citations"].append(citation_info)

            logger.info(f"Generated answer for query: {query[:50]}...")
            return result

        except ClientError as e:
            logger.error(f"Bedrock RAG error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in search_and_generate: {e}")
            raise

    def get_status(self) -> dict[str, Any]:
        """
        Bedrock Knowledge Baseの状態を取得

        Returns:
            システム状態の辞書
        """
        try:
            # Knowledge Baseの詳細情報を取得
            bedrock_agent = boto3.client("bedrock-agent", region_name=self.region_name)

            response = bedrock_agent.get_knowledge_base(
                knowledgeBaseId=self.knowledge_base_id
            )

            kb_info = response.get("knowledgeBase", {})

            status = {
                "knowledge_base_id": self.knowledge_base_id,
                "status": kb_info.get("status"),
                "name": kb_info.get("name"),
                "description": kb_info.get("description"),
                "model_id": self.model_id,
                "region": self.region_name,
                "created_at": kb_info.get("createdAt"),
                "updated_at": kb_info.get("updatedAt"),
            }

            return status

        except ClientError as e:
            logger.error(f"Error getting Knowledge Base status: {e}")
            return {
                "knowledge_base_id": self.knowledge_base_id,
                "status": "ERROR",
                "error": str(e),
                "model_id": self.model_id,
                "region": self.region_name,
            }
        except Exception as e:
            logger.error(f"Unexpected error getting status: {e}")
            return {
                "knowledge_base_id": self.knowledge_base_id,
                "status": "ERROR",
                "error": str(e),
                "model_id": self.model_id,
                "region": self.region_name,
            }
