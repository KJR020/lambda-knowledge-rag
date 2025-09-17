"""Configuration schemas."""

from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    """Database configuration schema."""

    host: str
    port: int
    database: str
    username: str
    password: str


class S3Config(BaseModel):
    """S3 configuration schema."""

    bucket_name: str
    region: str
    access_key_id: str | None = None
    secret_access_key: str | None = None
