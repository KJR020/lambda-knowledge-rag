variable "project_name" {
  description = "プロジェクト名"
  type        = string
}

variable "tags" {
  description = "リソースタグ"
  type        = map(string)
  default     = {}
}