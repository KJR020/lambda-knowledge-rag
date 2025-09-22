resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

resource "aws_s3_bucket" "scrapbox_documents" {
  bucket = "${var.project_name}-scrapbox-rag-${random_string.bucket_suffix.result}"
  tags   = var.tags
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

resource "aws_s3_bucket_public_access_block" "scrapbox_documents" {
  bucket = aws_s3_bucket.scrapbox_documents.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}