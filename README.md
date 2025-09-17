# lambda-knowledge-rag

## プロジェクト概要

Scrapboxで管理されているナレッジベースを、ベクトル検索可能なRAG（Retrieval-Augmented Generation）システムとして構築し、Claude CodeやGitHub Copilot等のLLMツールから利用可能にするプロジェクト

### 主要機能
- Scrapboxプロジェクトからの知識抽出とS3への自動保存
- AWS Bedrock Knowledge Baseによる自動RAGパイプライン構築
- MCPプロトコルによるLLMツールとの連携（Claude Code、GitHub Copilot等）

## 主な技術・構成要素

### AWSインフラ
- AWS Lambda
- Amazon S3
- Amazon API Gateway
- Amazon Bedrock Knowledge Base
- AWS Secrets Manager

### ベクトルデータベース
- Pinecone

### 言語・ランタイム
- Python

### 開発ツール
- uv
- tox
- pytest
- ruff

### インフラ管理
- Terraform

## ディレクトリ構成

```
├── infra/              # インフラ構成
│   ├── terraform/      # Terraform定義
│   └── docker/         # Dockerイメージ定義
│       ├── package_deploy/
│       └── tests/
├── src/                # Lambdaソースコード
│   ├── core/           # コアロジック
│   └── handlers/       # Lambdaハンドラー
├── tests/              # テストコード
├── pyproject.toml
├── tox.ini
└── uv.lock
```

## セットアップ

```bash
# 依存関係のインストール
uv sync
```

## テスト実行

```bash
# toxでテスト・Lintを実行
uv run tox

# 特定の環境のみ実行
uv run tox -e py313       # テストのみ
uv run tox -e lint        # Lintのみ
uv run tox -e format-check  # フォーマットチェックのみ
```

## CI（Docker + tox）

GitHub Actionsで、`infra/docker/tests/Dockerfile` を使いテスト用イメージをビルドし、uv run toxでテスト・Lintを自動実行

ローカルで同じCIを試す場合：
```bash
docker build -f infra/docker/tests/Dockerfile -t lambda-knowledge-rag:ci .
docker run --rm lambda-knowledge-rag:ci
```

## テスト・Lint

- テスト: pytest（`tests/unit/` 配下）
- Lint: ruff
- フォーマット: ruff format
