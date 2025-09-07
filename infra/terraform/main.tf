terraform {
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

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "scrapbox_project" {
  type        = string
  description = "Scrapbox project name"
}

variable "scrapbox_api_token" {
  type        = string
  description = "Scrapbox API token"
  sensitive   = true
}

resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

resource "aws_iam_role" "lambda_exec" {
  name               = "lambda_knowledge_rag_exec"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_s3_bucket" "scrapbox_documents" {
  bucket = "my-scrapbox-rag-${random_string.bucket_suffix.result}"
}

resource "aws_s3_bucket_versioning" "scrapbox_documents" {
  bucket = aws_s3_bucket.scrapbox_documents.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "scrapbox_documents" {
  bucket = aws_s3_bucket.scrapbox_documents.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_secretsmanager_secret" "scrapbox_token" {
  name        = "scrapbox-api-token"
  description = "Scrapbox API token for ETL process"
}

resource "aws_secretsmanager_secret_version" "scrapbox_token" {
  secret_id     = aws_secretsmanager_secret.scrapbox_token.id
  secret_string = jsonencode({
    token   = var.scrapbox_api_token
    project = var.scrapbox_project
  })
}

resource "aws_iam_role_policy" "lambda_s3_policy" {
  name = "lambda_s3_access"
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = "${aws_s3_bucket.scrapbox_documents.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket"
        ]
        Resource = aws_s3_bucket.scrapbox_documents.arn
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_secrets_policy" {
  name = "lambda_secrets_access"
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = aws_secretsmanager_secret.scrapbox_token.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_exec.name
}

output "lambda_role_name" {
  value = aws_iam_role.lambda_exec.name
}

output "lambda_role_arn" {
  value = aws_iam_role.lambda_exec.arn
}

output "s3_bucket_name" {
  value = aws_s3_bucket.scrapbox_documents.bucket
}

output "secrets_manager_secret_name" {
  value = aws_secretsmanager_secret.scrapbox_token.name
}
