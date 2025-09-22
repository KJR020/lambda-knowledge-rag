resource "aws_secretsmanager_secret" "scrapbox_token" {
  name        = "${var.project_name}-scrapbox-api-token"
  description = "Scrapbox API token for ETL process"
  tags        = var.tags
}

resource "aws_secretsmanager_secret_version" "scrapbox_token" {
  secret_id = aws_secretsmanager_secret.scrapbox_token.id
  secret_string = jsonencode({
    token   = var.scrapbox_api_token
    project = var.scrapbox_project
  })
}

resource "aws_secretsmanager_secret" "pinecone_credentials" {
  name        = "${var.project_name}-pinecone-credentials"
  description = "Pinecone credentials for Bedrock Knowledge Base"
  tags        = var.tags
}

resource "aws_secretsmanager_secret_version" "pinecone_credentials" {
  secret_id = aws_secretsmanager_secret.pinecone_credentials.id
  secret_string = jsonencode({
    apiKey = var.pinecone_api_key
  })
}