"""
data_loader.py

Objetivo del script: 
Data loader for Cultural Intelligence JSON datasets.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cinematic_intelligence.config import settings


class DataLoader:
    """
    Loads and caches cultural domain data from JSON files.

    Supports lazy loading with an LRU cache per domain.
    """

    def __init__(self, data_dir: Path | None = None) -> None:
        self._data_dir = data_dir or settings.data_dir
        self._cache: dict[str, list[dict[str, Any]]] = {}

    def _load(self, filename: str) -> list[dict[str, Any]]:
        """Load a JSON file, raising FileNotFoundError with a clear message."""
        if filename in self._cache:
            return self._cache[filename]

        path = Path(self._data_dir) / filename
        if not path.exists():
            raise FileNotFoundError(
                f"Dataset file not found: {path}\n"
                f"Expected location: {path.resolve()}\n"
                f"Please ensure the 00_datos/ directory contains {filename}."
            )

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        self._cache[filename] = data
        return data

    def get_nolan_films(self) -> list[dict[str, Any]]:
        """Return all Nolan films data."""
        return self._load("nolan_films.json")

    def get_king_books(self) -> list[dict[str, Any]]:
        """Return all Stephen King books data."""
        return self._load("king_books.json")

    def get_davis_albums(self) -> list[dict[str, Any]]:
        """Return all Miles Davis albums data."""
        return self._load("davis_albums.json")

    def search_nolan(self, query: str) -> list[dict[str, Any]]:
        """Keyword search across Nolan films."""
        query_lower = query.lower()
        films = self.get_nolan_films()
        results = []
        for film in films:
            text = " ".join([
                film.get("titulo", ""),
                " ".join(film.get("temas", [])),
                film.get("sinopsis", ""),
                " ".join(film.get("frases_clave", [])),
            ]).lower()
            if any(word in text for word in query_lower.split()):
                results.append(film)
        return results or films[:3]  # fallback to first 3 if no match

    def search_king(self, query: str) -> list[dict[str, Any]]:
        """Keyword search across King books."""
        query_lower = query.lower()
        books = self.get_king_books()
        results = []
        for book in books:
            text = " ".join([
                book.get("titulo", ""),
                " ".join(book.get("temas", [])),
                book.get("sinopsis", ""),
                book.get("escenario", ""),
            ]).lower()
            if any(word in text for word in query_lower.split()):
                results.append(book)
        return results or books[:3]

    def search_davis(self, query: str) -> list[dict[str, Any]]:
        """Keyword search across Davis albums."""
        query_lower = query.lower()
        albums = self.get_davis_albums()
        results = []
        for album in albums:
            text = " ".join([
                album.get("titulo", ""),
                " ".join(album.get("epocas", [])),
                album.get("descripcion", ""),
                " ".join(album.get("tecnicas", [])),
            ]).lower()
            if any(word in text for word in query_lower.split()):
                results.append(album)
        return results or albums[:3]


# Global loader instance
_loader: DataLoader | None = None


def get_loader(data_dir: Path | None = None) -> DataLoader:
    """Get or create the global DataLoader instance."""
    global _loader
    if _loader is None or data_dir is not None:
        _loader = DataLoader(data_dir)
    return _loader
