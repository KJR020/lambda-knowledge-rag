# AWSプロバイダー設定
provider "aws" {
  region = var.aws_region

  # デフォルトタグを設定
  default_tags {
    tags = {
      Project     = var.project_name
      Environment = "dev"
      ManagedBy   = "terraform"
    }
  }
}

# Random プロバイダー設定
provider "random" {
  # デフォルト設定を使用
}