output "lambda_function_name" {
  description = "Lambda関数名"
  value       = aws_lambda_function.main.function_name
}

output "lambda_function_arn" {
  description = "Lambda関数ARN"
  value       = aws_lambda_function.main.arn
}

output "lambda_role_arn" {
  description = "Lambda実行ロールARN"
  value       = aws_iam_role.lambda_exec.arn
}