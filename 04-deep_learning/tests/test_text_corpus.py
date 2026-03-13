"""
test_text_corpus.py

Objetivo del script: 
Script description goes here.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations

from tools.text_corpus import (
    build_vocabulary,
    chunk_text,
    corpus_stats,
    load_corpus_text,
    simple_tokenize,
)


def test_chunk_text_is_stable_and_non_empty() -> None:
    text = load_corpus_text()
    chunks = chunk_text(text, chunk_size=40, overlap=10)
    assert chunks
    assert all(len(chunk.split()) >= 35 for chunk in chunks[:3])


def test_simple_tokenize_and_vocabulary() -> None:
    tokens = simple_tokenize("El rey hablo con la princesa y el visir.")
    vocab = build_vocabulary(tokens)
    encoded = vocab.encode(tokens)
    assert tokens[0] == "el"
    assert vocab.decode(encoded[:3]) == tokens[:3]
    assert vocab.stoi["<pad>"] == 0


def test_corpus_stats_unique_tokens() -> None:
    stats = corpus_stats()
    assert stats["unique_tokens"] >= 100
