"""Simple retriever stub used for local tests."""

from typing import Any


class Retriever:
    def __init__(self):
        pass

    def find(self, query: str) -> Any:
        # Placeholder: in real project this would query vector DB or search index
        return {"id": "stub-1", "text": f"result for {query}"}
