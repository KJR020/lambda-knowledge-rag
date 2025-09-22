variable "project_name" {
  description = "プロジェクト名"
  type        = string
}

variable "scrapbox_api_token" {
  description = "Scrapbox APIトークン"
  type        = string
  sensitive   = true
}

variable "scrapbox_project" {
  description = "Scrapboxプロジェクト名"
  type        = string
}

variable "pinecone_api_key" {
  description = "Pinecone APIキー"
  type        = string
  sensitive   = true
}

variable "tags" {
  description = "リソースタグ"
  type        = map(string)
  default     = {}
}