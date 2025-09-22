module "storage" {
  source = "./modules/storage"

  project_name = var.project_name
  tags         = var.tags
}

module "secrets" {
  source = "./modules/secrets"

  project_name       = var.project_name
  scrapbox_api_token = var.scrapbox_api_token
  scrapbox_project   = var.scrapbox_project
  pinecone_api_key   = var.pinecone_api_key
  tags               = var.tags
}

module "knowledge_base" {
  source = "./modules/knowledge-base"

  project_name                   = var.project_name
  aws_region                     = var.aws_region
  s3_bucket_arn                  = module.storage.bucket_arn
  pinecone_connection_string     = var.pinecone_connection_string
  pinecone_credentials_secret_arn = module.secrets.pinecone_secret_arn
  tags                           = var.tags
}

module "lambda" {
  source = "./modules/lambda"

  project_name         = var.project_name
  aws_region           = var.aws_region
  lambda_function_name = var.lambda_function_name
  lambda_zip_path      = var.lambda_zip_path
  s3_bucket_arn        = module.storage.bucket_arn
  s3_bucket_name       = module.storage.bucket_name
  knowledge_base_arn   = module.knowledge_base.knowledge_base_arn
  knowledge_base_id    = module.knowledge_base.knowledge_base_id
  data_source_id       = module.knowledge_base.data_source_id
  scrapbox_secret_arn  = module.secrets.scrapbox_secret_arn
  scrapbox_secret_name = module.secrets.scrapbox_secret_name
  tags                 = var.tags
}

