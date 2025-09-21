"""
検索クエリの値オブジェクト
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SearchQuery:
    """検索クエリの値オブジェクト"""

    text: str
    top_k: int = 5
    filters: list[str] | None = None
    include_metadata: bool = True

    def __post_init__(self):
        """バリデーション"""
        if not self.text.strip():
            raise ValueError("検索クエリが空です")

        if self.top_k <= 0 or self.top_k > 100:
            raise ValueError("top_kは1-100の範囲で指定してください")

        if self.filters is None:
            object.__setattr__(self, "filters", [])

    @property
    def normalized_text(self) -> str:
        """正規化されたクエリテキスト"""
        return self.text.strip().lower()

    def is_simple_query(self) -> bool:
        """シンプルなクエリかどうか（フィルターなし）"""
        return not self.filters

    def has_filter(self, filter_name: str) -> bool:
        """指定されたフィルターを持っているかどうか"""
        return filter_name in (self.filters or [])


@dataclass(frozen=True)
class DocumentId:
    """ドキュメントIDの値オブジェクト"""

    project: str
    page_title: str

    def __post_init__(self):
        """バリデーション"""
        if not self.project.strip():
            raise ValueError("プロジェクト名が空です")

        if not self.page_title.strip():
            raise ValueError("ページタイトルが空です")

    @property
    def full_id(self) -> str:
        """完全なドキュメントID"""
        return f"{self.project}#{self.page_title}"

    @classmethod
    def from_string(cls, id_string: str) -> "DocumentId":
        """文字列からDocumentIdを生成"""
        if "#" not in id_string:
            raise ValueError(
                "ドキュメントIDの形式が正しくありません。'project#title'の形式で指定してください"
            )

        project, page_title = id_string.split("#", 1)
        return cls(project=project, page_title=page_title)
