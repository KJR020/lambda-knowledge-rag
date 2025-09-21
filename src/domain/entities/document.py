"""
ドキュメントのドメインエンティティ
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Document:
    """ドキュメントエンティティ"""

    id: str
    title: str
    content: str
    source: str
    project_name: str
    url: str
    created_at: datetime
    updated_at: datetime

    # メタデータ
    tags: list[str]
    character_count: int
    lines_count: int
    content_preview: str

    # 検索関連
    search_score: float | None = None

    def __post_init__(self):
        """初期化後の処理"""
        if not self.content_preview:
            self.content_preview = self._generate_preview()

    def _generate_preview(self, max_length: int = 200) -> str:
        """コンテンツのプレビューを生成"""
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length] + "..."

    def is_from_scrapbox(self) -> bool:
        """Scrapboxからのドキュメントかどうか"""
        return self.source == "scrapbox"

    def has_tag(self, tag: str) -> bool:
        """指定されたタグを持っているかどうか"""
        return tag in self.tags

    def get_age_days(self) -> int:
        """最終更新からの経過日数"""
        return (datetime.utcnow() - self.updated_at).days

    def is_recent(self, days: int = 30) -> bool:
        """最近更新されたドキュメントかどうか"""
        return self.get_age_days() <= days
