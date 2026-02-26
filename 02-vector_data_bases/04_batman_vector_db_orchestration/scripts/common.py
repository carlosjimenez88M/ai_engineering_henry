"""Shared helpers for the Batman vector DB notebooks."""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

import numpy as np
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9_\u00e1\u00e9\u00ed\u00f3\u00fa\u00f1]+")


def load_comic_records(path: Path | str) -> list[dict[str, Any]]:
    """Load records from a JSON file."""
    with Path(path).open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, list):
        raise TypeError("Expected a list of comic records")
    return payload


def chunk_comic_records(
    records: list[dict[str, Any]],
    chunk_size: int = 800,
    chunk_overlap: int = 120,
) -> list[dict[str, Any]]:
    """Split comic long-form content into retrieval chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )
    chunks: list[dict[str, Any]] = []
    for record in records:
        source_id = str(record.get("id", "unknown"))
        persona = str(record.get("personaje", "desconocido"))
        arco = str(record.get("arco", "sin_arco"))
        tema = str(record.get("tema", "general"))
        titulo = str(record.get("titulo", "sin_titulo"))
        contenido = str(record.get("contenido", ""))
        text_chunks = splitter.split_text(contenido)

        for idx, text in enumerate(text_chunks):
            chunk_id = f"{source_id}_chunk_{idx:03d}"
            chunks.append(
                {
                    "id": chunk_id,
                    "text": text,
                    "metadata": {
                        "source_id": source_id,
                        "personaje": persona,
                        "arco": arco,
                        "tema": tema,
                        "titulo": titulo,
                        "chunk_index": idx,
                    },
                }
            )
    return chunks


def tokenize(text: str) -> list[str]:
    """Simple normalized tokenizer for overlap metrics and routing."""
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


def _hash_embedding(text: str, dim: int = 256) -> list[float]:
    """Local deterministic embedding fallback when OpenAI is unavailable."""
    vector = np.zeros(dim, dtype=np.float32)
    for token in tokenize(text):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        idx = int.from_bytes(digest[:4], "big") % dim
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        weight = 1.0 + (digest[5] / 255.0)
        vector[idx] += sign * weight

    norm = float(np.linalg.norm(vector))
    if norm == 0.0:
        return vector.tolist()
    return (vector / norm).tolist()


def _use_openai() -> bool:
    return bool(os.getenv("OPENAI_API_KEY"))


def embed_documents(
    texts: list[str],
    model: str = "text-embedding-3-small",
) -> tuple[list[list[float]], str]:
    """Embed a batch of documents with OpenAI, fallback to local hash embeddings."""
    if _use_openai():
        try:
            embeddings = OpenAIEmbeddings(
                model=model,
                max_retries=1,
                request_timeout=20,
            )
            vectors = embeddings.embed_documents(texts)
            return vectors, f"openai:{model}"
        except Exception as exc:  # noqa: BLE001
            print(f"[WARN] OpenAI embeddings failed, using local fallback: {exc}")

    vectors = [_hash_embedding(text) for text in texts]
    return vectors, "local:hash-embedding"


def embed_query(
    text: str,
    model: str = "text-embedding-3-small",
) -> tuple[list[float], str]:
    """Embed a query with OpenAI, fallback to local hash embeddings."""
    if _use_openai():
        try:
            embeddings = OpenAIEmbeddings(
                model=model,
                max_retries=1,
                request_timeout=20,
            )
            vector = embeddings.embed_query(text)
            return vector, f"openai:{model}"
        except Exception as exc:  # noqa: BLE001
            print(f"[WARN] OpenAI query embedding failed, using local fallback: {exc}")

    return _hash_embedding(text), "local:hash-embedding"


def _fallback_summary(query: str, contexts: list[str], max_items: int = 3) -> str:
    """Produce a deterministic local response when LLM calls are unavailable."""
    query_tokens = set(tokenize(query))
    scored_sentences: list[tuple[int, str, int]] = []

    for doc_idx, context in enumerate(contexts, start=1):
        sentences = [segment.strip() for segment in context.split(".") if segment.strip()]
        for sentence in sentences:
            sentence_tokens = set(tokenize(sentence))
            overlap = len(query_tokens & sentence_tokens)
            scored_sentences.append((overlap, sentence, doc_idx))

    scored_sentences.sort(key=lambda item: item[0], reverse=True)
    top_items = [item for item in scored_sentences if item[0] > 0][:max_items]
    if not top_items:
        top_items = [(0, contexts[0][:220], 1)] if contexts else [(0, "No context available.", 0)]

    bullets = [f"- {sentence.strip()} [D{doc_idx}]" for _, sentence, doc_idx in top_items]
    intro = "Respuesta local fallback (sin llamada a OpenAI):"
    return intro + "\n" + "\n".join(bullets)


def generate_answer(
    query: str,
    contexts: list[str],
    model: str = "gpt-5-mini",
    system_prompt: str | None = None,
    temperature: float = 0.0,
) -> tuple[str, str]:
    """Generate an answer with OpenAI Chat API, fallback to local summary."""
    prompt = system_prompt or (
        "Responde en espanol, de forma clara y didactica. "
        "Usa solo el contexto entregado y agrega citas [D#] cuando corresponda."
    )
    joined_context = "\n\n".join(f"[D{idx}] {ctx}" for idx, ctx in enumerate(contexts, start=1))

    if _use_openai():
        try:
            llm = ChatOpenAI(
                model=model,
                temperature=temperature,
                timeout=20,
                max_retries=1,
            )
            response = llm.invoke(
                [
                    SystemMessage(content=prompt + "\n\nContexto:\n" + joined_context),
                    HumanMessage(content=query),
                ]
            )
            content = response.content if isinstance(response.content, str) else str(response.content)
            return content.strip(), f"openai:{model}"
        except Exception as exc:  # noqa: BLE001
            print(f"[WARN] OpenAI chat failed, using local fallback: {exc}")

    return _fallback_summary(query=query, contexts=contexts), "local:fallback-summary"
