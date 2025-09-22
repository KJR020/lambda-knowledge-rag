variable "project_name" {
  description = "プロジェクト名"
  type        = string
}

variable "aws_region" {
  description = "AWSリージョン"
  type        = string
}

variable "s3_bucket_arn" {
  description = "S3バケットARN"
  type        = string
}

variable "pinecone_connection_string" {
  description = "Pineconeの接続文字列"
  type        = string
}

variable "pinecone_credentials_secret_arn" {
  description = "PineconeクレデンシャルのAWS Secrets Manager ARN"
  type        = string
}

variable "tags" {
  description = "リソースタグ"
  type        = map(string)
  default     = {}
}