"""
config.py

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

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    model: str = os.getenv("OPENAI_MODEL", "gpt-5-mini")
    api_key: str | None = os.getenv("OPENAI_API_KEY")

    @staticmethod
    def default_dataset(module_root: Path) -> Path:
        return module_root / "05_llmops" / "00_data" / "tickets_eval.jsonl"

    @staticmethod
    def default_output_dir(module_root: Path) -> Path:
        return module_root / "05_llmops" / "outputs"
