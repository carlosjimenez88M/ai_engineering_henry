"""
test_execute_notebooks.py

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
