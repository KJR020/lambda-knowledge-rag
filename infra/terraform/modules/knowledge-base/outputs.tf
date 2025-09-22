output "knowledge_base_id" {
  description = "Bedrock Knowledge BaseのID"
  value       = aws_bedrockagent_knowledge_base.main.id
}

output "knowledge_base_arn" {
  description = "Bedrock Knowledge BaseのARN"
  value       = aws_bedrockagent_knowledge_base.main.arn
}

output "data_source_id" {
  description = "Bedrock Knowledge BaseのデータソースID"
  value       = aws_bedrockagent_data_source.s3_data_source.data_source_id
}

output "knowledge_base_role_arn" {
  description = "Knowledge Base用IAMロールのARN"
  value       = aws_iam_role.knowledge_base_role.arn
}