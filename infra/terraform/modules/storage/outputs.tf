output "bucket_name" {
  description = "S3バケット名"
  value       = aws_s3_bucket.scrapbox_documents.bucket
}

output "bucket_arn" {
  description = "S3バケットARN"
  value       = aws_s3_bucket.scrapbox_documents.arn
}

output "bucket_id" {
  description = "S3バケットID"
  value       = aws_s3_bucket.scrapbox_documents.id
}