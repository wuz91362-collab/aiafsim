from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from app.config import settings


@dataclass
class KnowledgeChunk:
    """表示一个可检索的 DSL 知识片段。"""

    chunk_id: str
    category: str
    content: str
    keywords: list[str]


class KnowledgeRetriever(Protocol):
    """定义检索器需要实现的最小接口。"""

    def retrieve(self, query: str, top_k: int = 3) -> list[KnowledgeChunk]:
        """按查询语义返回知识片段列表。"""


class LocalKnowledgeStore:
    """本地关键词检索器，占位替代向量数据库。"""

    def __init__(self, knowledge_file: str) -> None:
        """初始化知识库文件路径并预加载全部片段。"""
        self.knowledge_file = Path(knowledge_file)
        self._chunks = self._load_chunks()

    def _load_chunks(self) -> list[KnowledgeChunk]:
        """从 JSON 文件加载知识片段，不存在时返回空列表。"""
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
        """按关键词命中分数检索最相关的知识片段。"""
        lowered = query.lower()
        scored: list[tuple[int, KnowledgeChunk]] = []
        for chunk in self._chunks:
            score = sum(1 for kw in chunk.keywords if kw.lower() in lowered)
            if score > 0:
                scored.append((score, chunk))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:top_k]]


class ChromaKnowledgeStore:
    """Chroma 向量检索实现，支持由 JSON 启动初始化。"""

    def __init__(
        self,
        persist_directory: str,
        collection_name: str,
        bootstrap_file: str | None = None,
        enable_bootstrap: bool = True,
    ) -> None:
        """初始化 Chroma 客户端并确保集合可用。"""
        import chromadb

        self.bootstrap_file = Path(bootstrap_file) if bootstrap_file else None
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        if enable_bootstrap:
            self._bootstrap_if_needed()

    def _bootstrap_if_needed(self) -> None:
        """当集合为空时，从 JSON 片段导入初始语料。"""
        if not self.bootstrap_file or not self.bootstrap_file.exists():
            return
        if self.collection.count() > 0:
            return
        raw = json.loads(self.bootstrap_file.read_text(encoding="utf-8"))
        ids: list[str] = []
        documents: list[str] = []
        metadatas: list[dict] = []
        for item in raw:
            ids.append(item["chunk_id"])
            documents.append(item["content"])
            metadatas.append(
                {
                    "chunk_id": item["chunk_id"],
                    "category": item["category"],
                    "keywords": ",".join(item.get("keywords", [])),
                }
            )
        if ids:
            self.collection.add(ids=ids, documents=documents, metadatas=metadatas)

    def retrieve(self, query: str, top_k: int = 3) -> list[KnowledgeChunk]:
        """从 Chroma 中按向量相似度检索知识片段。"""
        result = self.collection.query(query_texts=[query], n_results=top_k)
        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        chunks: list[KnowledgeChunk] = []
        for idx, doc in enumerate(documents):
            metadata = metadatas[idx] if idx < len(metadatas) else {}
            chunks.append(
                KnowledgeChunk(
                    chunk_id=metadata.get("chunk_id", f"chroma_{idx}"),
                    category=metadata.get("category", "unknown"),
                    content=doc,
                    keywords=metadata.get("keywords", "").split(",") if metadata.get("keywords") else [],
                )
            )
        return chunks


def build_knowledge_store() -> KnowledgeRetriever:
    """按配置返回 JSON 或 Chroma 检索器。"""
    if settings.rag_backend.lower() == "chroma":
        return ChromaKnowledgeStore(
            persist_directory=settings.chroma_persist_directory,
            collection_name=settings.chroma_collection_name,
            bootstrap_file=settings.knowledge_file,
            enable_bootstrap=settings.chroma_enable_bootstrap,
        )
    return LocalKnowledgeStore(settings.knowledge_file)
