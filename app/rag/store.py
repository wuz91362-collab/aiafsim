from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class KnowledgeChunk:
    chunk_id: str
    category: str
    content: str
    keywords: list[str]


class LocalKnowledgeStore:
    """Simple keyword retriever placeholder for vector DB."""

    def __init__(self, knowledge_file: str) -> None:
        self.knowledge_file = Path(knowledge_file)
        self._chunks = self._load_chunks()

    def _load_chunks(self) -> list[KnowledgeChunk]:
        if not self.knowledge_file.exists():
            return []
        raw = json.loads(self.knowledge_file.read_text(encoding="utf-8"))
        return [
            KnowledgeChunk(
                chunk_id=item["chunk_id"],
                category=item["category"],
                content=item["content"],
                keywords=item["keywords"],
            )
            for item in raw
        ]

    def retrieve(self, query: str, top_k: int = 3) -> list[KnowledgeChunk]:
        lowered = query.lower()
        scored: list[tuple[int, KnowledgeChunk]] = []
        for chunk in self._chunks:
            score = sum(1 for kw in chunk.keywords if kw.lower() in lowered)
            if score > 0:
                scored.append((score, chunk))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:top_k]]
