"""
ETL処理の動作確認テスト

注意: Embedding処理はBedrock Knowledge Baseが自動実行するため、
このテストはS3保存機能のみをテストします。
"""

import pytest


@pytest.fixture(autouse=True)
def setup_env(monkeypatch):
    """monkeypatch を使って環境変数を安全に設定する"""
    monkeypatch.setenv("SCRAPBOX_PROJECT", "test-project")
    monkeypatch.setenv("SCRAPBOX_API_TOKEN", "test-token")
    monkeypatch.setenv("S3_BUCKET", "test-bucket")
    monkeypatch.setenv("AWS_REGION", "us-east-1")


def test_etl_basic():
    """ETL処理の基本動作をテスト（初期化と基本属性確認）"""

    from infrastructure.adapters.etl import ScrapboxETLProcessor

    # プロセッサの初期化テスト
    processor = ScrapboxETLProcessor()

    # 属性が正しく初期化されていることを検証
    assert hasattr(processor, "scrapbox")
    assert hasattr(processor, "s3")
    # 注意: Embedding処理は削除済み（Bedrock KB自動処理）


def test_index_function_imports():
    """upsert_scrapbox_page が import できることを確認"""
    from index import upsert_scrapbox_page

    # 関数が呼び出せること（実際の処理は呼ばない）
    assert callable(upsert_scrapbox_page)


def test_s3_client_basic():
    """S3Client の基本動作を検証"""
    from infrastructure.adapters.s3 import S3Client

    client = S3Client()
    # S3クライアントが初期化されていることを確認
    assert hasattr(client, "s3")
    
    # 注意: EmbeddingsClient は削除済み（Bedrock KB自動処理のため）
