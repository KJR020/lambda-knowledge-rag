"""
Scrapboxページのドメインエンティティ
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from domain.entities.document import Document


@dataclass
class ScrapboxPage:
    """Scrapboxページエンティティ"""

    id: str
    title: str
    lines: list[str]
    project: str
    descriptions: list[str]
    links: list[str]

    # タイムスタンプ（Unix timestamp）
    created: int
    updated: int

    # 統計情報
    chars_count: int
    lines_count: int

    # APIから取得した生データ
    raw_data: dict[str, Any] | None = None

    def __post_init__(self):
        """初期化後の処理"""
        if not self.lines:
            self.lines = []
        if not self.descriptions:
            self.descriptions = []
        if not self.links:
            self.links = []

    @property
    def url(self) -> str:
        """ScrapboxページのURL"""
        return f"https://scrapbox.io/{self.project}/{self.title}"

    @property
    def content(self) -> str:
        """ページの全文コンテンツ"""
        return "\n".join(self.lines)

    @property
    def created_at(self) -> datetime:
        """作成日時（datetime）"""
        return datetime.fromtimestamp(self.created)

    @property
    def updated_at(self) -> datetime:
        """更新日時（datetime）"""
        return datetime.fromtimestamp(self.updated)

    def get_preview(self, max_length: int = 200) -> str:
        """ページの概要を取得"""
        if self.descriptions:
            preview = " ".join(self.descriptions[:3])
        else:
            preview = self.content

        if len(preview) <= max_length:
            return preview
        return preview[:max_length] + "..."

    def to_document(self) -> Document:
        """Documentエンティティに変換"""
        return Document(
            id=f"{self.project}#{self.title}",
            title=self.title,
            content=self.content,
            source="scrapbox",
            project_name=self.project,
            url=self.url,
            created_at=self.created_at,
            updated_at=self.updated_at,
            tags=self.links[:10],  # 最大10個のリンクをタグとして使用
            character_count=self.chars_count,
            lines_count=self.lines_count,
            content_preview=self.get_preview(),
        )

    def has_content(self) -> bool:
        """コンテンツがあるかどうか"""
        return bool(self.lines and any(line.strip() for line in self.lines))

    def is_recent(self, days: int = 30) -> bool:
        """最近更新されたページかどうか"""
        age_days = (datetime.utcnow() - self.updated_at).days
        return age_days <= days

    def has_link(self, link: str) -> bool:
        """指定されたリンクを持っているかどうか"""
        return link in self.links

    @classmethod
    def from_api_response(cls, data: dict[str, Any], project: str) -> "ScrapboxPage":
        """Scrapbox APIのレスポンスからエンティティを生成"""
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            lines=[line.get("text", "") for line in data.get("lines", [])],
            project=project,
            descriptions=data.get("descriptions", []),
            links=data.get("links", []),
            created=data.get("created", 0),
            updated=data.get("updated", 0),
            chars_count=data.get("charsCount", 0),
            lines_count=data.get("linesCount", 0),
            raw_data=data,
        )
