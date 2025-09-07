# Scrapbox→S3 ETL MVP要件定義（requirements-mvp.md）

## 0. ドキュメント情報

* **目的**: ScrapboxのページをRAG用にS3に配置する最小機能のETLを定義する
* **対象読者**: 個人開発者
* **前提**: Scrapboxプロジェクトが公開またはAPI Token経由でアクセス可能

---

## 1. 背景・目的

* 個人ナレッジ（Scrapbox）を**AI検索/RAG**に活用するため、最小限の機能でスタート
* **動くものを早く作る**ことを優先

---

## 2. スコープ

**IN**
* Scrapboxページの**取得**
* **Markdown変換**（基本形式のみ）
* **S3配置**
* **手動実行での同期**
* **基本メタデータ付与**

**OUT**
* 差分同期（毎回フル取得）
* 添付ファイル処理
* 定期実行
* 複雑な監視・アラート
* 複数環境対応

---

## 3. アーキテクチャ

```
Scrapbox API → Lambda → S3
```

* **Lambda**: 単一関数で全処理
* **実行**: 手動（AWS Console / CLI）
* **認証**: Scrapbox API Token
* **出力**: S3バケット単一

---

## 4. 機能要件（MVP）

| ID    | 要件         | 詳細                      | 受け入れ基準                     |
|-------|--------------|---------------------------|--------------------------------|
| FR-01 | ページ取得      | 指定プロジェクトの全ページを取得     | 全ページが正常に取得される             |
| FR-02 | Markdown変換 | Scrapbox記法→基本Markdown | 見出し・リンク・コードブロックが変換される      |
| FR-03 | S3配置       | 変換済みファイルをS3に保存       | ページごとに.mdファイルが作成される          |
| FR-04 | メタデータ付与    | 基本的なpage情報を含める      | title, url, updated_atが保存される |
| FR-05 | 手動実行     | AWS Consoleから実行可能     | ボタン一つで同期が開始される            |

---

## 5. 入出力定義

### 5.1 入力（Scrapbox API）
```json
{
  "pageId": "string",
  "title": "string", 
  "text": "Scrapbox markup...",
  "updated": 1234567890
}
```

### 5.2 出力（S3）

**バケット**: `my-scrapbox-rag-{random}`
**ファイル構成**:
```
pages/
  ├── page1.md
  ├── page2.md
  └── metadata.json
```

**個別ページファイル**:
```markdown
---
title: ページタイトル
url: https://scrapbox.io/project/ページタイトル  
updated_at: 2025-09-10T12:34:56Z
page_id: pageId
---

# ページタイトル

本文のMarkdown...
```

---

## 6. 変換ルール（最小限）

* **見出し**: `[* 見出し]` → `# 見出し`
* **リンク**: `[[ページ名]]` → `[ページ名](https://scrapbox.io/{project}/ページ名)`
* **コード**: `code:python` → ````python` 
* **箇条書き**: そのまま維持
* **その他**: プレーンテキスト化

---

## 7. 設定

```python
# 環境変数で設定
SCRAPBOX_PROJECT = "your-project"
SCRAPBOX_API_TOKEN = "your-token"  # Secrets Manager推奨
S3_BUCKET = "my-scrapbox-rag-bucket"
```

---

## 8. 技術スタック

* **Runtime**: Python 3.13
* **Libraries**: 
  - `requests` (Scrapbox API)
  - `boto3` (S3)
  - `re` (正規表現変換)
* **AWS Services**:
  - Lambda（単一関数）
  - S3（ストレージ）
  - Secrets Manager（トークン保存）

---

## 9. Lambda構成

```python
def lambda_handler(event, context):
    # 1. Scrapboxからページ一覧取得
    # 2. 各ページの詳細取得
    # 3. Markdown変換
    # 4. S3アップロード
    # 5. 実行結果を返す
    pass
```

**タイムアウト**: 5分
**メモリ**: 512MB
**環境変数**: PROJECT, TOKEN, BUCKET

---

## 10. デプロイ方法

* **手動**: Lambda関数を直接作成・更新
* **推奨**: 簡単なCloudFormationまたはTerraform
* **コード**: zipファイルまたはGitHub連携

---

## 11. 受け入れ基準

1. **インフラ**: Terraformで必要なAWSリソースが作成される
   - S3バケット（ドキュメント保存用）
   - Lambda関数（ETL処理用）
   - Secrets Manager（API Token保存用）
   - IAMロール・ポリシー（最小権限）

2. **機能**: 
   - Scrapboxの指定プロジェクトから全ページが取得できる
   - 基本的なMarkdown変換が正しく行われる
   - S3に.mdファイルとmetadata.jsonが作成される
   - 手動実行で同期が完了する

3. **統合**: RAGシステムが生成されたファイルを読み込める

4. **運用**: 既存のCI/CDパイプラインでテスト・デプロイが可能

---

## 12. 次段階での拡張予定

* 差分同期機能
* 定期実行（EventBridge）
* より高度なMarkdown変換
* 画像・添付ファイル対応
* エラー処理・リトライ
* CloudWatch監視
* **既存のRAGパイプラインとの統合**（ETL→ベクトル化→Pinecone自動更新）

---

## 13. 制約・前提

* 個人利用想定（大量データは対象外）
* Scrapboxプロジェクトは公開または適切なトークンでアクセス可能
* AWSアカウント利用可能
* 初期はフル同期のみ（差分なし）
