"""Unit tests for the DataLoader class."""

from __future__ import annotations

import pytest

from cinematic_intelligence.data_loader import DataLoader


class TestDataLoader:
    def test_loads_nolan_films(self, tmp_data_dir):
        loader = DataLoader(data_dir=tmp_data_dir)
        films = loader.get_nolan_films()
        assert len(films) >= 1
        assert "titulo" in films[0]

    def test_loads_king_books(self, tmp_data_dir):
        loader = DataLoader(data_dir=tmp_data_dir)
        books = loader.get_king_books()
        assert len(books) >= 1
        assert "titulo" in books[0]

    def test_loads_davis_albums(self, tmp_data_dir):
        loader = DataLoader(data_dir=tmp_data_dir)
        albums = loader.get_davis_albums()
        assert len(albums) >= 1
        assert "titulo" in albums[0]

    def test_cache_hit(self, tmp_data_dir):
        loader = DataLoader(data_dir=tmp_data_dir)
        films1 = loader.get_nolan_films()
        films2 = loader.get_nolan_films()
        assert films1 is films2  # same object from cache

    def test_file_not_found_raises_clear_error(self, tmp_path):
        loader = DataLoader(data_dir=tmp_path)
        with pytest.raises(FileNotFoundError, match="nolan_films.json"):
            loader.get_nolan_films()

    def test_search_nolan_returns_results(self, tmp_data_dir):
        loader = DataLoader(data_dir=tmp_data_dir)
        results = loader.search_nolan("Memento")
        assert len(results) >= 1

    def test_search_nolan_fallback_on_no_match(self, tmp_data_dir):
        loader = DataLoader(data_dir=tmp_data_dir)
        # Unlikely keyword
        results = loader.search_nolan("xyzzy_nonexistent_term_12345")
        assert len(results) >= 1  # fallback returns first 3

    def test_search_king_returns_results(self, tmp_data_dir):
        loader = DataLoader(data_dir=tmp_data_dir)
        results = loader.search_king("horror")
        assert len(results) >= 1

    def test_search_davis_returns_results(self, tmp_data_dir):
        loader = DataLoader(data_dir=tmp_data_dir)
        results = loader.search_davis("jazz")
        assert len(results) >= 1
