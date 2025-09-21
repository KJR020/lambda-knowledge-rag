"""
共有ユーティリティ関数
"""

import hashlib
import hmac
import json
import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


def verify_signature(actual_signature: str, expected_signature: str) -> bool:
    """HMACシグネチャの検証

    Args:
        actual_signature: 実際のシグネチャ
        expected_signature: 期待されるシグネチャ

    Returns:
        検証結果
    """
    if not actual_signature or not expected_signature:
        return False

    return hmac.compare_digest(actual_signature, expected_signature)


def calculate_signature(event: dict[str, Any], secret: str) -> str:
    """イベントからHMACシグネチャを計算

    Args:
        event: イベントデータ
        secret: シークレットキー

    Returns:
        計算されたシグネチャ
    """
    message = json.dumps(event, sort_keys=True)
    signature = hmac.new(
        secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    return signature


def generate_document_id(project: str, title: str) -> str:
    """ドキュメントIDを生成

    Args:
        project: プロジェクト名
        title: ドキュメントタイトル

    Returns:
        ドキュメントID
    """
    return f"{project}#{title}"


def parse_document_id(doc_id: str) -> tuple[str, str]:
    """ドキュメントIDを解析

    Args:
        doc_id: ドキュメントID

    Returns:
        (プロジェクト名, タイトル)のタプル
    """
    if "#" not in doc_id:
        raise ValueError(f"Invalid document ID format: {doc_id}")

    project, title = doc_id.split("#", 1)
    return project, title


def format_datetime(dt: datetime) -> str:
    """datetime を ISO 形式の文字列に変換

    Args:
        dt: datetime オブジェクト

    Returns:
        ISO形式の文字列
    """
    return dt.isoformat()


def parse_datetime(dt_str: str) -> datetime:
    """ISO 形式の文字列を datetime に変換

    Args:
        dt_str: ISO形式の文字列

    Returns:
        datetime オブジェクト
    """
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))


def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """テキストを指定した長さで切り詰める

    Args:
        text: 元のテキスト
        max_length: 最大長
        suffix: 切り詰め時の接尾辞

    Returns:
        切り詰められたテキスト
    """
    if len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)] + suffix


def safe_get_nested_value(
    data: dict[str, Any], keys: list[str], default: Any = None
) -> Any:
    """ネストした辞書から安全に値を取得

    Args:
        data: データ辞書
        keys: キーのリスト
        default: デフォルト値

    Returns:
        取得した値またはデフォルト値
    """
    current = data

    try:
        for key in keys:
            current = current[key]
        return current
    except (KeyError, TypeError):
        return default
