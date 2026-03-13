"""
doctor.py

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
import platform
import sys
from pathlib import Path

import torch
from rich.console import Console
from rich.table import Table


def detect_default_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    mps_backend = getattr(torch.backends, "mps", None)
    if mps_backend is not None and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def main() -> None:
    console = Console()
    table = Table(title="Deep Learning Doctor")
    table.add_column("Check")
    table.add_column("Value")

    table.add_row("Python", sys.version.split()[0])
    table.add_row("Platform", platform.platform())
    table.add_row("Torch", torch.__version__)
    table.add_row("CUDA available", str(torch.cuda.is_available()))
    mps_backend = getattr(torch.backends, "mps", None)
    mps_available = bool(mps_backend is not None and torch.backends.mps.is_available())
    table.add_row("MPS available", str(mps_available))
    table.add_row("Default device", detect_default_device())
    table.add_row("Smoke mode", os.getenv("HENRY_DL_SMOKE", "0"))
    table.add_row("Online mode", os.getenv("HENRY_DL_ONLINE_MODE", "0"))
    table.add_row(
        "Corpus dir",
        str(Path(__file__).resolve().parents[1] / "data" / "las_mil_y_una_noches"),
    )

    console.print(table)


if __name__ == "__main__":
    main()
