from typing import Any

import boto3

from infrastructure.config.config import CONFIG


class S3Client:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            region_name=CONFIG.aws_region,
        )

    def upload_json_file(self, bucket: str, key: str, data: dict[str, Any]) -> None:
        """JSONファイルをS3にアップロードする"""
        import json

        self.s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"),
            ContentType="application/json",
        )

    def upload_metadata_file(
        self, bucket: str, key: str, metadata: dict[str, Any]
    ) -> None:
        """メタデータJSONファイルをS3にアップロードする"""
        import json

        self.s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps(metadata, indent=2).encode("utf-8"),
            ContentType="application/json",
        )

    def list_objects(self, bucket: str, prefix: str = "") -> list[str]:
        """指定されたプレフィックスでS3バケット内のオブジェクトをリストする"""
        response = self.s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        return [obj["Key"] for obj in response.get("Contents", [])]
