from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from rich.console import Console
from rich.table import Table

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "las_mil_y_una_noches"
TOKEN_PATTERN = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)?|[.,;:!?()-]")


@dataclass(frozen=True)
class Vocabulary:
    stoi: dict[str, int]
    itos: list[str]
    pad_token: str = "<pad>"
    unk_token: str = "<unk>"
    bos_token: str = "<bos>"
    eos_token: str = "<eos>"

    def encode(self, tokens: Iterable[str]) -> list[int]:
        unk_id = self.stoi[self.unk_token]
        return [self.stoi.get(token, unk_id) for token in tokens]

    def decode(self, ids: Iterable[int]) -> list[str]:
        return [self.itos[index] for index in ids]


def corpus_files() -> list[Path]:
    return sorted(DATA_DIR.glob("*.txt"))


def normalize_text(text: str) -> str:
    text = text.replace("\ufeff", "")
    text = text.lower()
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def load_documents() -> list[dict[str, str]]:
    documents = []
    for path in corpus_files():
        documents.append(
            {"name": path.stem, "text": normalize_text(path.read_text(encoding="utf-8"))}
        )
    return documents


def load_corpus_text(separator: str = "\n\n") -> str:
    return separator.join(document["text"] for document in load_documents())


def simple_tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(normalize_text(text))


def token_windows(tokens: list[str], window_size: int, stride: int) -> list[list[str]]:
    if window_size <= 0:
        raise ValueError("window_size debe ser positivo")
    if stride <= 0:
        raise ValueError("stride debe ser positivo")
    windows = []
    for start in range(0, max(len(tokens) - window_size + 1, 1), stride):
        window = tokens[start : start + window_size]
        if len(window) == window_size:
            windows.append(window)
    return windows


def chunk_text(text: str, chunk_size: int = 80, overlap: int = 20) -> list[str]:
    if overlap >= chunk_size:
        raise ValueError("overlap debe ser menor que chunk_size")
    tokens = simple_tokenize(text)
    stride = chunk_size - overlap
    windows = token_windows(tokens, window_size=chunk_size, stride=stride)
    return [" ".join(window) for window in windows]


def build_vocabulary(tokens: Iterable[str], min_freq: int = 1) -> Vocabulary:
    if min_freq <= 0:
        raise ValueError("min_freq debe ser mayor que cero")
    counter = Counter(tokens)
    specials = ["<pad>", "<unk>", "<bos>", "<eos>"]
    words = [token for token, freq in counter.items() if freq >= min_freq]
    ordered = specials + sorted(words)
    stoi = {token: index for index, token in enumerate(ordered)}
    return Vocabulary(stoi=stoi, itos=ordered)


def corpus_stats() -> dict[str, int]:
    documents = load_documents()
    text = load_corpus_text()
    tokens = simple_tokenize(text)
    chunks = chunk_text(text, chunk_size=80, overlap=20)
    return {
        "documents": len(documents),
        "characters": len(text),
        "tokens": len(tokens),
        "chunks": len(chunks),
        "unique_tokens": len(set(tokens)),
    }


def print_corpus_report() -> None:
    console = Console()
    stats = corpus_stats()
    table = Table(title="Corpus local: Las mil y una noches")
    table.add_column("Check")
    table.add_column("Valor")
    for key, value in stats.items():
        table.add_row(key, str(value))
    console.print(table)


def main() -> None:
    if not corpus_files():
        raise FileNotFoundError(f"No se encontraron archivos .txt en {DATA_DIR}")
    print_corpus_report()


if __name__ == "__main__":
    main()
