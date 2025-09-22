# Terraform変数定義

variable "project_name" {
  description = "プロジェクト名"
  type        = string
  default     = "lambda-knowledge-rag"
}

variable "aws_region" {
  description = "AWSリージョン"
  type        = string
  default     = "us-east-1"
}


variable "pinecone_connection_string" {
  description = "Pineconeの接続文字列"
  type        = string
}

variable "pinecone_credentials_secret_arn" {
  description = "PineconeクレデンシャルのAWS Secrets Manager ARN"
  type        = string
}

variable "scrapbox_project" {
  description = "Scrapboxプロジェクト名"
  type        = string
}

variable "scrapbox_api_token" {
  description = "Scrapbox APIトークン"
  type        = string
  sensitive   = true
}

variable "lambda_function_name" {
  description = "Lambda関数名"
  type        = string
  default     = "lambda-knowledge-rag"
}

variable "tags" {
  description = "リソースタグ"
  type        = map(string)
  default = {
    Project     = "lambda-knowledge-rag"
    Environment = "dev"
    ManagedBy   = "terraform"
  }
}