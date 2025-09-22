# Terraform バックエンド設定とバージョン制約
terraform {
  # ローカル開発時はコメントアウト、本番環境では有効化
  # backend "s3" {
  #   bucket = "your-terraform-state-bucket"
  #   key    = "lambda-knowledge-rag/terraform.tfstate"
  #   region = "us-east-1"
  # }

  required_version = ">= 1.2.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1"
    }
  }
}