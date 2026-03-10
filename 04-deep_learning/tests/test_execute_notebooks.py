from __future__ import annotations

from pathlib import Path

from tools.execute_notebooks import NOTEBOOK_GROUPS, ROOT, notebook_paths


def test_notebook_groups_have_expected_keys() -> None:
    assert sorted(NOTEBOOK_GROUPS) == ["all", "core", "nlp", "transformers"]


def test_notebook_paths_exist() -> None:
    for group in NOTEBOOK_GROUPS:
        for notebook in notebook_paths(group):
            assert notebook.exists()
            assert notebook.suffix == ".ipynb"
            assert notebook.is_relative_to(ROOT)


def test_runner_root_points_to_module() -> None:
    assert (Path(ROOT) / "README.md").exists()
