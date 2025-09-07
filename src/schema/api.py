"""API request and response schemas."""

from typing import Any

from pydantic import BaseModel


class QueryRequest(BaseModel):
    """Schema for knowledge query requests."""
    query: str


class QueryResponse(BaseModel):
    """Schema for knowledge query responses."""
    query: str
    document: dict[str, Any]


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    error: str
    message: str
    status_code: int
