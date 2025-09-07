import dataclasses
import os


@dataclasses.dataclass
class Config:
    @property
    def aws_region(self) -> str:
        return os.environ["AWS_REGION"]

    @property
    def scrapbox_api_token(self) -> str:
        return os.environ.get("SCRAPBOX_API_TOKEN")

    @property
    def s3_bucket(self) -> str:
        return os.environ["S3_BUCKET"]


CONFIG = Config()
