# lambda-knowledge-rag

## プロジェクト概要

AWS Lambdaを用いたRetrieval-Augmented Generation (RAG) の最小構成サンプルです。S3に保存したドキュメントをベクトル化し、質問応答APIを提供します。インフラはTerraformで管理します。

## 主な技術・構成要素

- AWS Lambda
- Amazon S3
- Amazon API Gateway
- Pinecone
- Python
- Terraform
- uv（高速Pythonパッケージ管理）
- tox, pytest, ruff（テスト・Lint・CI）

## ディレクトリ構成

```
├── DESIGN.md
├── lambda-image-resize-tutorial.md
├── pyproject.toml
├── README.md
├── requirements.txt
├── tox.ini
├── uv.lock
├── infra/
│   └── terraform/
│       └── main.tf
├── src/
│   ├── __init__.py
│   ├── index.py
│   ├── requirements-dev.txt
│   ├── requirements.txt
│   ├── core/
│   │   ├── __init__.py
│   │   ├── clients.py
│   │   ├── config.py
│   │   ├── retriever.py
│   └── docker/
│       ├── package_deploy/
│       │   └── Dockerfile
│       └── tests/
│           └── Dockerfile
│   └── handlers/
│       └── knowledge_infer.py
├── tests/
│   ├── conftest.py
│   └── unit/
│       └── test_retriever.py
```

## セットアップ（uv を使用）

このプロジェクトでは `uv` を使った環境管理・パッケージインストールを推奨します。

1. リポジトリをクローンし作業ディレクトリへ移動

```bash
git clone <repo-url>
cd lambda-knowledge-rag
```

1. uv をインストール（システムに uv がない場合）

```bash
pip install uv
```

1. 依存関係をインストール

```bash
# プロジェクトルートにある uv.lock を使用してインストール
uv sync

# 開発用依存を追加で入れる場合
uv pip install -r src/requirements-dev.txt
```

1. テスト実行

```bash
pytest -q
```

## CI（Docker + tox）

GitHub Actionsで、`src/docker/tests/Dockerfile` を使いテスト用イメージをビルドし、toxでテスト・Lintを自動実行します。

ローカルで同じCIを試す場合：
```bash
docker build -f src/docker/tests/Dockerfile -t lambda-knowledge-rag:ci .
docker run --rm lambda-knowledge-rag:ci
```

## テスト・Lint

- テスト: pytest（`tests/unit/` 配下）
- Lint: ruff
- フォーマット: ruff format

## 注意事項

- 秘密情報（APIキー等）はコミットしないでください。AWS Secrets Managerや環境変数を利用してください。
