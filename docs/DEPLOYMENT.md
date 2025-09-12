# Scrapbox ETL デプロイメントガイド

## 前提条件

- AWS CLI設定済み（`aws configure`完了）
- Terraform >= 1.2.0
- uv（Python package manager）
- Scrapbox API トークン取得済み
- Scrapboxプロジェクトにアクセス権限あり

## 🚀 ワンコマンドデプロイ

```bash
# 1. terraform.tfvarsファイルを作成
cp infra/terraform/terraform.tfvars.example infra/terraform/terraform.tfvars

# 2. terraform.tfvarsを編集（実際の値を設定）
# aws_region = "us-east-1"
# scrapbox_project = "your-scrapbox-project"
# scrapbox_api_token = "your-api-token"

# 3. 全自動デプロイ実行
./scripts/deploy.sh
```

## 手動デプロイ手順

### 1. インフラストラクチャのデプロイ

```bash
cd infra/terraform/

# terraform.tfvarsファイルを作成
cp terraform.tfvars.example terraform.tfvars

# terraform.tfvarsを編集
# aws_region = "us-east-1"
# scrapbox_project = "your-scrapbox-project"
# scrapbox_api_token = "your-api-token"
```

```bash
# Terraformの初期化
terraform init

# プランの確認
terraform plan

# インフラのデプロイ
terraform apply
```

### 2. Lambda関数のデプロイ

```bash
# プロジェクトルートに戻る
cd ../../

# Lambdaパッケージの作成（uvを使用）
./scripts/build-lambda.sh

# Lambda関数のデプロイ
aws lambda create-function \
  --function-name scrapbox-etl \
  --runtime python3.11 \
  --role $(terraform -chdir=infra/terraform output -raw lambda_role_arn) \
  --handler handlers.scrapbox_etl.lambda_handler \
  --zip-file fileb://lambda-package.zip \
  --timeout 300 \
  --memory-size 512 \
  --environment Variables='{
    "AWS_REGION":"us-east-1",
    "S3_BUCKET":"'$(terraform -chdir=infra/terraform output -raw s3_bucket_name)'",
    "SCRAPBOX_SECRET_NAME":"'$(terraform -chdir=infra/terraform output -raw secrets_manager_secret_name)'"
  }'
```

### 3. 実行テスト

```bash
# Lambda関数を手動実行
aws lambda invoke \
  --function-name scrapbox-etl \
  --payload '{}' \
  response.json

# レスポンス確認
cat response.json
```

### 4. S3の確認

```bash
# デプロイされたファイルを確認
aws s3 ls s3://$(terraform -chdir=infra/terraform output -raw s3_bucket_name)/pages/
```

## 環境変数

Lambda関数は以下の環境変数を使用します：

- `AWS_REGION`: AWSリージョン
- `S3_BUCKET`: ドキュメント保存用S3バケット名
- `SCRAPBOX_SECRET_NAME`: Secrets Managerのシークレット名（オプション）
- `SCRAPBOX_PROJECT`: Scrapboxプロジェクト名（Secrets Managerがない場合）
- `SCRAPBOX_API_TOKEN`: Scrapbox APIトークン（Secrets Managerがない場合）

## 出力ファイル構造

```
s3://bucket-name/
├── pages/
│   ├── page1.md
│   ├── page2.md
│   └── metadata.json
```

各.mdファイルにはYAMLフロントマターが含まれます：

```markdown
---
title: ページタイトル
url: https://scrapbox.io/project/ページタイトル
page_id: page_id
updated_at: 2025-01-01T00:00:00Z
---

# ページタイトル

変換されたMarkdownコンテンツ...
```