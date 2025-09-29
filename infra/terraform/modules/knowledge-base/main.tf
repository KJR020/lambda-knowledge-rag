data "aws_caller_identity" "current" {}

resource "aws_iam_role" "knowledge_base_role" {
  name = "${var.project_name}-knowledge-base-role"
  tags = var.tags

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "bedrock.amazonaws.com"
        }
        Condition = {
          StringEquals = {
            "aws:SourceAccount" = data.aws_caller_identity.current.account_id
          }
        }
      }
    ]
  })
}

resource "aws_iam_policy" "knowledge_base_policy" {
  name        = "${var.project_name}-knowledge-base-policy"
  description = "Policy for Bedrock Knowledge Base access to S3, Bedrock, and Secrets Manager"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          var.s3_bucket_arn,
          "${var.s3_bucket_arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel"
        ]
        Resource = [
          "arn:aws:bedrock:*::foundation-model/amazon.titan-embed-text-v1"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = [
          var.pinecone_credentials_secret_arn
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "knowledge_base_policy_attachment" {
  role       = aws_iam_role.knowledge_base_role.name
  policy_arn = aws_iam_policy.knowledge_base_policy.arn
}

resource "aws_bedrockagent_knowledge_base" "main" {
  name     = "${var.project_name}-knowledge-base"
  role_arn = aws_iam_role.knowledge_base_role.arn
  tags     = var.tags

  description = "Scrapboxナレッジベースの検索拡張生成システム"

  knowledge_base_configuration {
    vector_knowledge_base_configuration {
      embedding_model_arn = "arn:aws:bedrock:${var.aws_region}::foundation-model/amazon.titan-embed-text-v1"
    }
    type = "VECTOR"
  }

  storage_configuration {
    type = "PINECONE"

    pinecone_configuration {
      connection_string      = var.pinecone_connection_string
      credentials_secret_arn = var.pinecone_credentials_secret_arn
      field_mapping {
        metadata_field = "metadata"
        text_field     = "text"
      }
    }
  }
}

resource "aws_bedrockagent_data_source" "s3_data_source" {
  knowledge_base_id = aws_bedrockagent_knowledge_base.main.id
  name              = "${var.project_name}-s3-data-source"
  description       = "ScrapboxページのS3データソース"

  data_source_configuration {
    type = "S3"

    s3_configuration {
      bucket_arn         = var.s3_bucket_arn
      inclusion_prefixes = ["scrapbox/"]
    }
  }

  vector_ingestion_configuration {
    chunking_configuration {
      chunking_strategy = "FIXED_SIZE"

      fixed_size_chunking_configuration {
        max_tokens         = 300
        overlap_percentage = 20
      }
    }
  }
}
