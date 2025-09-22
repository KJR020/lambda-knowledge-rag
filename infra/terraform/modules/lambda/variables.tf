variable "project_name" {
  description = "プロジェクト名"
  type        = string
}

variable "aws_region" {
  description = "AWSリージョン"
  type        = string
}

variable "lambda_function_name" {
  description = "Lambda関数名"
  type        = string
}

variable "lambda_zip_path" {
  description = "LambdaデプロイメントパッケージのZIPファイルパス"
  type        = string
}

variable "s3_bucket_arn" {
  description = "S3バケットARN"
  type        = string
}

variable "s3_bucket_name" {
  description = "S3バケット名"
  type        = string
}

variable "knowledge_base_arn" {
  description = "Bedrock Knowledge BaseのARN"
  type        = string
}

variable "knowledge_base_id" {
  description = "Bedrock Knowledge BaseのID"
  type        = string
}

variable "data_source_id" {
  description = "Bedrock Knowledge BaseのデータソースID"
  type        = string
}

variable "scrapbox_secret_arn" {
  description = "Scrapbox APIトークンのSecret ARN"
  type        = string
}

variable "scrapbox_secret_name" {
  description = "Scrapbox APIトークンのSecret名"
  type        = string
}

variable "tags" {
  description = "リソースタグ"
  type        = map(string)
  default     = {}
}