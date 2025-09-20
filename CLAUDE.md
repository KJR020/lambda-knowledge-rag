# Claude Code 開発設定・記録

## プロジェクト概要

Lambda Knowledge RAG システムの開発プロジェクト。

Scrapboxのナレッジベースを、AWS Bedrock Knowledge Baseを活用したRAGシステムとして構築。

## 設計・実装方針

### アーキテクチャ

- **クリーンアーキテクチャ**を採用
- **Bedrock Knowledge Base**中心の設計
- **MCPプロトコル**による外部LLM連携

### 設計書スタイルガイド

#### Mermaid図について

- **styleの使用禁止**: 可読性を優先し、Mermaid図でのstyle設定は使用しない
- 色やスタイルによる装飾は避け、シンプルで見やすい図を心がける

例：
```mermaid
# ❌ 避けるべき
graph TB
    A[Node A]
    B[Node B]
    style A fill:#f9f,stroke:#333,stroke-width:2px

# ✅ 推奨
graph TB
    A[Node A]
    B[Node B]
```

### 開発フロー

1. 設計書の更新・レビュー
2. ドメイン層の実装
3. アプリケーション層の実装
4. インフラストラクチャ層の実装
5. 統合テスト

## 技術スタック

### 主要技術

- **言語**: Python 3.11+
- **フレームワーク**: AWS Lambda
- **外部サービス**: 
  - Scrapbox API
  - AWS Bedrock Knowledge Base
  - Amazon S3
  - Pinecone (Bedrock KB経由)

### 開発ツール

- **テスト**: pytest
- **リンター**: ruff
- **タイプチェック**: mypy
- **IaC**: Terraform

## ディレクトリ構造

```
src/
├── domain/                 # ビジネスロジック層
│   ├── entities/
│   ├── values/
│   └── policies/
├── application/            # アプリケーション層
│   ├── usecases/
│   └── ports/
├── infrastructure/         # インフラストラクチャ層
│   ├── adapters/
│   ├── lambda/
│   └── config/
└── shared/                 # 共有コンポーネント
```

## 環境変数

### 必須設定

- `AWS_REGION`: AWSリージョン
- `SCRAPBOX_PROJECT`: Scrapboxプロジェクト名
- `SCRAPBOX_API_TOKEN`: Scrapbox APIトークン
- `S3_BUCKET`: Knowledge Base用S3バケット名
- `KNOWLEDGE_BASE_ID`: Bedrock Knowledge BaseのID
- `DATA_SOURCE_ID`: Bedrock KB内のデータソースID

## 注意事項

### Embedding処理について

- Embeddingの生成は**Bedrock Knowledge Baseが自動実行**
- Lambda側でのEmbedding処理は**実装不要**
- PineconeへのインデックスもBedrock KB経由で自動実行

### RAGPortについて

- 検索と生成を統合したインターフェース
- `RetrieverPort`と`GeneratorPort`は統合済み
- `BedrockKBAdapter`が実装

## 開発履歴

### 2025-09-20

- DESIGN.mdの設計を見直し、クリーンアーキテクチャ版に更新
- RAGPortへの統合により、RetrieverPortとGeneratorPortを統合
- システムアーキテクチャ章を全体像→詳細の流れに再構成
- Mermaid図のstyle使用を禁止に設定