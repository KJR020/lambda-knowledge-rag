import dataclasses
import json
import os

import boto3


@dataclasses.dataclass
class Config:
    @property
    def aws_region(self) -> str:
        return os.environ["AWS_REGION"]

    @property
    def scrapbox_project(self) -> str:
        """Get Scrapbox project name from Secrets Manager or environment."""
        return self._get_scrapbox_config().get(
            "project", os.environ.get("SCRAPBOX_PROJECT")
        )

    @property
    def scrapbox_api_token(self) -> str:
        """Get Scrapbox API token from Secrets Manager or environment."""
        return self._get_scrapbox_config().get(
            "token", os.environ.get("SCRAPBOX_API_TOKEN")
        )

    @property
    def s3_bucket(self) -> str:
        return os.environ["S3_BUCKET"]

    def _get_scrapbox_config(self) -> dict:
        """Get Scrapbox configuration from Secrets Manager."""
        secret_name = os.environ.get("SCRAPBOX_SECRET_NAME", "scrapbox-api-token")

        try:
            session = boto3.session.Session()
            client = session.client(
                service_name="secretsmanager", region_name=self.aws_region
            )

            response = client.get_secret_value(SecretId=secret_name)
            return json.loads(response["SecretString"])
        except Exception:
            # Fallback to empty dict if secret is not available
            return {}


CONFIG = Config()
