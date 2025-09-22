output "scrapbox_secret_arn" {
  description = "Scrapbox APIトークンのSecret ARN"
  value       = aws_secretsmanager_secret.scrapbox_token.arn
}

output "scrapbox_secret_name" {
  description = "Scrapbox APIトークンのSecret名"
  value       = aws_secretsmanager_secret.scrapbox_token.name
}

output "pinecone_secret_arn" {
  description = "Pinecone認証情報のSecret ARN"
  value       = aws_secretsmanager_secret.pinecone_credentials.arn
}

output "pinecone_secret_name" {
  description = "Pinecone認証情報のSecret名"
  value       = aws_secretsmanager_secret.pinecone_credentials.name
}