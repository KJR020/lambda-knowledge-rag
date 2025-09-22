# Lambda Knowledge RAG - Terraform Infrastructure

このディレクトリには、Lambda Knowledge RAGシステムのAWSインフラストラクチャをTerraformで管理するためのコードが含まれています。

## 📋 概要

Scrapboxのナレッジベースを、AWS Bedrock Knowledge Baseを活用したRAGシステムとして構築するためのインフラストラクチャです。

### 主要なAWSリソース

- **S3バケット**: Scrapboxドキュメントの保存用
- **Bedrock Knowledge Base**: RAG処理の中核（Embedding生成、Pinecone管理を自動化）
- **Lambda関数**: ETL処理と検索API
- **IAMロール・ポリシー**: 各サービス間の権限管理
- **Secrets Manager**: 機密情報（Scrapbox、Pinecone認証情報）の管理

> **注意**: このシステムではベクトルデータベースとしてPineconeを使用し、Bedrock Knowledge Baseが全ての管理を自動化するため、DynamoDBテーブルは不要です。

## 🏗️ アーキテクチャ

このインフラストラクチャはモジュール化アーキテクチャを採用しており、以下の特徴があります：

- **明確な責務分離**: 各モジュールが単一の責務を持つ
- **高い再利用性**: 環境間でモジュールを再利用可能
- **依存関係の明確化**: モジュール間の依存がインターフェースで明確

### ディレクトリ構造

```
infra/terraform/
├── main.tf                # ルートモジュール（モジュールの組み合わせ）
├── variables.tf           # プロジェクト全体の変数定義
├── outputs.tf             # プロジェクト全体の出力
├── terraform.tf           # Terraformバージョン・プロバイダー要件
├── providers.tf           # プロバイダー設定
├── terraform.tfvars       # 環境変数値（gitignore対象）
├── terraform.tfvars.example # 設定例
└── modules/               # 再利用可能なモジュール
    ├── storage/           # S3ストレージモジュール
    ├── secrets/           # シークレット管理モジュール
    ├── knowledge-base/    # Bedrock Knowledge Baseモジュール
    └── lambda/            # Lambda関数モジュール
```

## 🚀 セットアップ

### 1. 前提条件

- Terraform >= 1.0
- AWS CLI設定済み
- Pineconeアカウントとインデックス作成済み

### 2. 環境変数の設定

```bash
# terraform.tfvars.exampleをコピー
cp terraform.tfvars.example terraform.tfvars

# 必要な値を設定
vi terraform.tfvars
```

#### 必須設定項目

```hcl
# プロジェクト設定
project_name = "lambda-knowledge-rag"
aws_region   = "us-east-1"

# Scrapbox設定
scrapbox_project   = "your-scrapbox-project-name"
scrapbox_api_token = "your-scrapbox-api-token"

# Pinecone設定
pinecone_connection_string = "https://your-index-name-xxxxxxxx.svc.environment.pinecone.io"
pinecone_api_key          = "your-pinecone-api-key"

# Lambda設定
lambda_function_name = "lambda-knowledge-rag"
lambda_zip_path     = "../lambda/deployment.zip"
```

### 3. デプロイ

```bash
# Terraformの初期化
terraform init

# 実行計画の確認
terraform plan

# インフラストラクチャのデプロイ
terraform apply
```

## 📦 モジュール詳細

### Storage モジュール (`modules/storage/`)

**責務**: S3バケットとバケットポリシー管理

- ドキュメント保存用S3バケット
- バージョニング有効化
- 暗号化設定
- パブリックアクセスブロック

### Secrets モジュール (`modules/secrets/`)

**責務**: シークレット管理

- Scrapbox APIトークン（Secrets Manager）
- Pinecone認証情報（Secrets Manager）

### Knowledge Base モジュール (`modules/knowledge-base/`)

**責務**: Bedrock Knowledge Base関連リソースとIAM管理

- Bedrock Knowledge Base
- S3データソース
- IAMロール・ポリシー
- Pinecone接続設定

> **重要**: Bedrock Knowledge BaseがPineconeへの自動インデックス作成・管理を実行し、Embedding生成からベクトル保存まで全てを自動化します。

### Lambda モジュール (`modules/lambda/`)

**責務**: メインLambda関数とIAM管理

**主要機能**:
1. **ETL処理**: Scrapboxからデータ取得してS3に保存
2. **RAG機能**: Knowledge Baseを使った検索・回答生成

**主要リソース**:
- メインLambda関数
- IAMロール・ポリシー（S3、Secrets Manager、Bedrock権限）

## 🔧 運用

### 環境変数の確認

デプロイ後、以下のコマンドで重要な出力値を確認できます：

```bash
terraform output
```

### リソースの更新

設定を変更した場合：

```bash
terraform plan
terraform apply
```

### リソースの削除

```bash
terraform destroy
```

## 🔒 セキュリティ

- 全ての機密情報はAWS Secrets Managerで管理
- S3バケットはパブリックアクセスブロック有効
- IAMロールは最小権限の原則に従って設定
- terraform.tfvarsファイルはgitignore対象

## 📝 注意事項

1. **Lambda ZIPファイル**: デプロイ前に`../lambda/deployment.zip`が存在することを確認してください
2. **Pineconeインデックス**: 事前にPineconeでインデックスを作成しておく必要があります
3. **Scrapbox API**: 適切なアクセス権限を持つAPIトークンを使用してください

## 🤝 トラブルシューティング

### よくある問題

**Q: Lambda関数のデプロイが失敗する**
- A: `lambda_zip_path`で指定したZIPファイルが存在することを確認してください

**Q: Bedrock Knowledge Baseの作成が失敗する**
- A: Pineconeの接続文字列とクレデンシャルが正しいことを確認してください

**Q: IAM権限エラーが発生する**
- A: AWS CLIの設定とTerraformを実行するユーザーの権限を確認してください

## 📄 ライセンス

このプロジェクトは[ライセンス名]でライセンスされています。