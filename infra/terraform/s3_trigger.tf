# S3トリガーによる自動同期設定

# データソース同期用のLambda関数のIAMロール
resource "aws_iam_role" "sync_lambda_role" {
  name = "${var.project_name}-sync-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

}

# Lambda実行用の基本ポリシー
resource "aws_iam_role_policy_attachment" "sync_lambda_basic_execution" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.sync_lambda_role.name
}

# Bedrock Knowledge Base同期用のポリシー
resource "aws_iam_policy" "sync_lambda_policy" {
  name        = "${var.project_name}-sync-lambda-policy"
  description = "Policy for Lambda to sync Bedrock Knowledge Base data source"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:StartIngestionJob",
          "bedrock:GetIngestionJob",
          "bedrock:ListIngestionJobs"
        ]
        Resource = [
          aws_bedrockagent_knowledge_base.main.arn,
          "${aws_bedrockagent_knowledge_base.main.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:GetObjectVersion"
        ]
        Resource = "${aws_s3_bucket.scrapbox_documents.arn}/*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "sync_lambda_policy_attachment" {
  policy_arn = aws_iam_policy.sync_lambda_policy.arn
  role       = aws_iam_role.sync_lambda_role.name
}

# データソース同期用のLambda関数
resource "aws_lambda_function" "sync_data_source" {
  filename      = "sync_lambda.zip"
  function_name = "${var.project_name}-sync-data-source"
  role          = aws_iam_role.sync_lambda_role.arn
  handler       = "sync_handler.lambda_handler"
  runtime       = "python3.11"
  timeout       = 300

  environment {
    variables = {
      KNOWLEDGE_BASE_ID = aws_bedrockagent_knowledge_base.main.id
      DATA_SOURCE_ID    = aws_bedrockagent_data_source.s3_data_source.data_source_id
    }
  }


  depends_on = [
    aws_iam_role_policy_attachment.sync_lambda_basic_execution,
    aws_iam_role_policy_attachment.sync_lambda_policy_attachment,
  ]
}

# S3バケット通知設定用のLambda許可
resource "aws_lambda_permission" "allow_s3_invoke" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.sync_data_source.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.scrapbox_documents.arn
}

# S3バケット通知設定（外部で管理されているS3バケットの場合）
# 注意: 既存のS3バケットの場合は手動で設定するか、aws_s3_bucket_notificationを使用
# S3バケット通知設定
resource "aws_s3_bucket_notification" "sync_notification" {
  bucket = aws_s3_bucket.scrapbox_documents.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.sync_data_source.arn
    events              = ["s3:ObjectCreated:*", "s3:ObjectRemoved:*"]
    filter_prefix       = "scrapbox/"
    filter_suffix       = ".json"
  }

  depends_on = [aws_lambda_permission.allow_s3_invoke]
}