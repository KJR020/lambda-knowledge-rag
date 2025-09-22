# S3 Storage Outputs
output "s3_bucket_name" {
  description = "S3バケット名"
  value       = module.storage.bucket_name
}

output "s3_bucket_arn" {
  description = "S3バケットARN"
  value       = module.storage.bucket_arn
}

# Knowledge Base Outputs
output "knowledge_base_id" {
  description = "Bedrock Knowledge BaseのID"
  value       = module.knowledge_base.knowledge_base_id
}

output "knowledge_base_arn" {
  description = "Bedrock Knowledge BaseのARN"
  value       = module.knowledge_base.knowledge_base_arn
}

output "data_source_id" {
  description = "Bedrock Knowledge BaseのデータソースID"
  value       = module.knowledge_base.data_source_id
}

# Lambda Outputs
output "lambda_function_name" {
  description = "Lambda関数名"
  value       = module.lambda.lambda_function_name
}

output "lambda_function_arn" {
  description = "Lambda関数ARN"
  value       = module.lambda.lambda_function_arn
}

output "lambda_role_arn" {
  description = "Lambda実行ロールARN"
  value       = module.lambda.lambda_role_arn
}

# Secrets Outputs
output "scrapbox_secret_name" {
  description = "Scrapbox APIトークンのSecret名"
  value       = module.secrets.scrapbox_secret_name
}

output "pinecone_secret_name" {
  description = "Pinecone認証情報のSecret名"
  value       = module.secrets.pinecone_secret_name
}

# Lambda関数で使用する環境変数
output "lambda_environment_variables" {
  description = "Lambda関数で使用する環境変数"
  value = {
    KNOWLEDGE_BASE_ID = module.knowledge_base.knowledge_base_id
    DATA_SOURCE_ID    = module.knowledge_base.data_source_id
    AWS_REGION        = var.aws_region
    S3_BUCKET         = module.storage.bucket_name
    SCRAPBOX_PROJECT  = var.scrapbox_project
  }
}