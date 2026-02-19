"""Vector DB utilities built on top of ChromaDB."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

import chromadb

from .common import chunk_comic_records, embed_documents, embed_query, load_comic_records


class ComicsVectorDB:
    """Small wrapper around ChromaDB focused on educational notebooks."""

    def __init__(
        self,
        collection_name: str,
        persist_dir: Path | str,
    ) -> None:
        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(self.persist_dir))
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def reset_collection(self) -> None:
        """Delete and recreate collection to ensure deterministic notebook runs."""
        try:
            self.client.delete_collection(name=self.collection_name)
        except Exception:  # noqa: BLE001
            pass
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def index_chunks(
        self,
        chunks: list[dict[str, Any]],
        embedding_model: str = "text-embedding-3-small",
    ) -> dict[str, Any]:
        """Upsert chunk list into Chroma collection using selected embedding backend."""
        if not chunks:
            raise ValueError("Chunk list is empty")

        ids = [str(chunk["id"]) for chunk in chunks]
        documents = [str(chunk["text"]) for chunk in chunks]
        metadatas = [dict(chunk["metadata"]) for chunk in chunks]

        embeddings, provider = embed_documents(documents, model=embedding_model)
        self.collection.upsert(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)
        return {
            "collection": self.collection_name,
            "indexed_chunks": len(chunks),
            "embedding_provider": provider,
        }

    def query(
        self,
        query_text: str,
        n_results: int = 4,
        embedding_model: str = "text-embedding-3-small",
    ) -> tuple[list[dict[str, Any]], str]:
        """Query vector DB and return normalized result list + embedding provider."""
        query_embedding, provider = embed_query(query_text, model=embedding_model)
        raw = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
        )

        documents = raw.get("documents", [[]])[0]
        metadatas = raw.get("metadatas", [[]])[0]
        distances = raw.get("distances", [[]])[0]

        output: list[dict[str, Any]] = []
        for idx, (doc, metadata, distance) in enumerate(zip(documents, metadatas, distances), start=1):
            output.append(
                {
                    "rank": idx,
                    "text": doc,
                    "metadata": metadata,
                    "distance": float(distance),
                }
            )
        return output, provider


def describe_chunks(chunks: list[dict[str, Any]]) -> dict[str, Any]:
    """Simple diagnostics to support vector DB design decisions."""
    char_lengths = [len(chunk["text"]) for chunk in chunks]
    source_ids = [chunk["metadata"]["source_id"] for chunk in chunks]
    themes = [chunk["metadata"]["tema"] for chunk in chunks]
    personas = [chunk["metadata"]["personaje"] for chunk in chunks]

    return {
        "chunk_count": len(chunks),
        "unique_sources": len(set(source_ids)),
        "avg_chars_per_chunk": round(sum(char_lengths) / max(len(char_lengths), 1), 2),
        "max_chars_per_chunk": max(char_lengths) if char_lengths else 0,
        "themes_distribution": dict(Counter(themes)),
        "hero_distribution": dict(Counter(personas)),
    }


def build_index_from_json(
    json_path: Path | str,
    persist_dir: Path | str,
    collection_name: str,
    chunk_size: int = 800,
    chunk_overlap: int = 120,
    embedding_model: str = "text-embedding-3-small",
) -> tuple[ComicsVectorDB, list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    """Convenience helper for notebook setup: load -> chunk -> index."""
    records = load_comic_records(json_path)
    chunks = chunk_comic_records(
        records,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    db = ComicsVectorDB(collection_name=collection_name, persist_dir=persist_dir)
    db.reset_collection()
    index_stats = db.index_chunks(chunks=chunks, embedding_model=embedding_model)
    chunk_stats = describe_chunks(chunks)
    return db, chunks, index_stats, chunk_stats
