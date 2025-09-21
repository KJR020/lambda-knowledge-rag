"""
ダミーのEmbeddingsクライアント

将来的にAWS Bedrock Titan Embeddingsに置き換え予定
現在はテスト用のダミーベクトルを生成
"""

import hashlib
import logging

import numpy as np

logger = logging.getLogger(__name__)


class EmbeddingsClient:
    """テキストのベクトル化を行うクライアント"""

    def __init__(self, model_id: str = "dummy-embeddings-v1", dimension: int = 1536):
        """
        初期化

        Args:
            model_id: 使用するモデルID（将来的にBedrock用）
            dimension: ベクトルの次元数
        """
        self.model_id = model_id
        self.dimension = dimension
        logger.info(
            f"EmbeddingsClient initialized with model: {model_id}, dimension: {dimension}"
        )

    def embed_text(self, text: str) -> list[float]:
        """
        テキストをベクトル化

        Args:
            text: ベクトル化するテキスト

        Returns:
            ベクトル（float配列）
        """
        # テキストのハッシュを基にダミーベクトルを生成
        # 同じテキストからは常に同じベクトルが生成される（決定的）
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        seed = int(text_hash[:8], 16)
        np.random.seed(seed)

        # -1から1の範囲で正規化されたベクトルを生成
        vector = np.random.randn(self.dimension).astype(np.float32)
        # L2正規化
        vector = vector / np.linalg.norm(vector)

        logger.debug(f"Generated embedding for text (length: {len(text)})")
        return vector.tolist()

    def embed_batch(
        self, texts: list[str], batch_size: int | None = None
    ) -> list[list[float]]:
        """
        複数のテキストをバッチでベクトル化

        Args:
            texts: ベクトル化するテキストのリスト
            batch_size: バッチサイズ（将来的な実装用）

        Returns:
            ベクトルのリスト
        """
        logger.info(f"Embedding batch of {len(texts)} texts")
        embeddings = []

        for text in texts:
            embedding = self.embed_text(text)
            embeddings.append(embedding)

        return embeddings

    def compute_similarity(
        self, embedding1: list[float], embedding2: list[float]
    ) -> float:
        """
        2つのベクトル間のコサイン類似度を計算

        Args:
            embedding1: ベクトル1
            embedding2: ベクトル2

        Returns:
            コサイン類似度（-1から1）
        """
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        # コサイン類似度計算
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        similarity = dot_product / (norm1 * norm2)
        return float(similarity)

    def get_model_info(self) -> dict:
        """
        使用中のモデル情報を取得

        Returns:
            モデル情報の辞書
        """
        return {
            "model_id": self.model_id,
            "dimension": self.dimension,
            "type": "dummy_embeddings",
        }


class BedrockEmbeddingsClient(EmbeddingsClient):
    """
    AWS Bedrock Titan Embeddingsを使用するクライアント（将来の実装用）
    """

    def __init__(
        self, model_id: str = "amazon.titan-embed-text-v1", dimension: int = 1536
    ):
        """
        初期化

        Args:
            model_id: Bedrockのモデル ID
            dimension: ベクトルの次元数
        """
        super().__init__(model_id, dimension)
        # TODO: boto3クライアントの初期化
        logger.info("BedrockEmbeddingsClient initialized (placeholder)")

    def embed_text(self, text: str) -> list[float]:
        """
        Bedrockを使用してテキストをベクトル化

        Args:
            text: ベクトル化するテキスト

        Returns:
            ベクトル
        """
        # TODO: 実際のBedrock API呼び出し実装
        # 現在はダミー実装を使用
        logger.warning(
            "BedrockEmbeddingsClient.embed_text is not implemented yet, using dummy implementation"
        )
        return super().embed_text(text)

    def get_model_info(self) -> dict:
        """
        Bedrockモデル情報を取得

        Returns:
            モデル情報の辞書
        """
        return {
            "model_id": self.model_id,
            "dimension": self.dimension,
            "type": "bedrock_embeddings",
        }
