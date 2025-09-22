# Terraform出力定義

# 基本リソースの出力
output "lambda_role_name" {
  description = "Lambda実行ロール名"
  value       = aws_iam_role.lambda_exec.name
}

output "lambda_role_arn" {
  description = "Lambda実行ロールARN"
  value       = aws_iam_role.lambda_exec.arn
}

output "s3_bucket_name" {
  description = "Scrapboxドキュメント用S3バケット名"
  value       = aws_s3_bucket.scrapbox_documents.bucket
}

output "s3_bucket_arn" {
  description = "Scrapboxドキュメント用S3バケットARN"
  value       = aws_s3_bucket.scrapbox_documents.arn
}

output "secrets_manager_secret_name" {
  description = "Secrets Manager シークレット名"
  value       = aws_secretsmanager_secret.scrapbox_token.name
}

# Bedrock Knowledge Base関連の出力

output "knowledge_base_id" {
  description = "Bedrock Knowledge BaseのID"
  value       = aws_bedrockagent_knowledge_base.main.id
}

output "knowledge_base_arn" {
  description = "Bedrock Knowledge BaseのARN"
  value       = aws_bedrockagent_knowledge_base.main.arn
}

output "data_source_id" {
  description = "データソースのID"
  value       = aws_bedrockagent_data_source.s3_data_source.data_source_id
}

output "knowledge_base_role_arn" {
  description = "Knowledge Base用IAMロールのARN"
  value       = aws_iam_role.knowledge_base_role.arn
}

output "embedding_model_arn" {
  description = "使用するEmbeddingモデルのARN"
  value       = "arn:aws:bedrock:${var.aws_region}::foundation-model/amazon.titan-embed-text-v1"
}

# Lambda関数で使用する環境変数
output "lambda_environment_variables" {
  description = "Lambda関数で使用する環境変数"
  value = {
    KNOWLEDGE_BASE_ID = aws_bedrockagent_knowledge_base.main.id
    DATA_SOURCE_ID    = aws_bedrockagent_data_source.s3_data_source.data_source_id
    AWS_REGION        = var.aws_region
    S3_BUCKET         = aws_s3_bucket.scrapbox_documents.bucket
    SCRAPBOX_PROJECT  = var.scrapbox_project
  }
}