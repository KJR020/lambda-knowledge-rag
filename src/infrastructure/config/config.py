import dataclasses
import os


@dataclasses.dataclass
class Config:
    @property
    def aws_region(self) -> str:
        return os.environ.get("AWS_REGION")

    @property
    def scrapbox_api_token(self) -> str:
        return os.environ.get("SCRAPBOX_API_TOKEN")

    @property
    def scrapbox_project(self) -> str:
        return os.environ.get("SCRAPBOX_PROJECT")

    @property
    def s3_bucket(self) -> str:
        return os.environ.get("S3_BUCKET")

    @property
    def pinecone_api_key(self) -> str:
        return os.environ.get("PINECONE_API_KEY")

    @property
    def pinecone_environment(self) -> str:
        return os.environ.get("PINECONE_ENVIRONMENT")

    @property
    def pinecone_index_name(self) -> str:
        return os.environ.get("PINECONE_INDEX_NAME")

    @property
    def pinecone_namespace(self) -> str:
        return os.environ.get("PINECONE_NAMESPACE")

    @property
    def knowledge_base_id(self) -> str:
        return os.environ.get("KNOWLEDGE_BASE_ID")

    @property
    def data_source_id(self) -> str:
        return os.environ.get("DATA_SOURCE_ID")

    @property
    def bedrock_model_id(self) -> str:
        return os.environ.get(
            "BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"
        )

    @property
    def webhook_secret(self) -> str:
        return os.environ.get("WEBHOOK_SECRET")

    # Embedding関連の設定
    @property
    def embedding_model_id(self) -> str:
        return os.environ.get("EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v1")

    @property
    def embedding_batch_size(self) -> int:
        return int(os.environ.get("EMBEDDING_BATCH_SIZE", "10"))

    @property
    def embedding_max_retries(self) -> int:
        return int(os.environ.get("EMBEDDING_MAX_RETRIES", "3"))

    @property
    def embedding_timeout_seconds(self) -> int:
        return int(os.environ.get("EMBEDDING_TIMEOUT_SECONDS", "30"))

    @property
    def use_bedrock_embeddings(self) -> bool:
        return os.environ.get("USE_BEDROCK_EMBEDDINGS", "true").lower() in (
            "true",
            "1",
            "yes",
        )


CONFIG = Config()
