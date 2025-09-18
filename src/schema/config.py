from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    """データベース接続設定のスキーマ"""

    host: str
    port: int
    database: str
    username: str
    password: str


class S3Config(BaseModel):
    """S3 関連設定のスキーマ"""

    bucket_name: str
    region: str
    access_key_id: str | None = None
    secret_access_key: str | None = None
