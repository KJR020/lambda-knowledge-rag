"""Document domain schemas."""

from pydantic import BaseModel


class DocumentSchema(BaseModel):
    """Schema for knowledge documents."""

    id: str
    text: str


class DocumentSearchResult(BaseModel):
    """Schema for document search results."""

    documents: list[DocumentSchema]
    total_count: int
    query: str
