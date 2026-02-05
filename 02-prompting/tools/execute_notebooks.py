"""Ejecuta notebooks de la clase 02 y guarda artefactos de validacion."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parents[2]
NOTEBOOKS = [
    ROOT / "02-prompting" / "COT" / "Notebooks" / "cot_recomendador_aplicado.ipynb",
    ROOT / "02-prompting" / "ReAct" / "Notebooks" / "react_agente_aplicado.ipynb",
]


def run_notebook(path: Path) -> Path:
    with path.open("r", encoding="utf-8") as fh:
        nb = nbformat.read(fh, as_version=4)

    client = NotebookClient(nb, timeout=180, kernel_name="python3")
    client.execute()

    out_path = path.with_name(path.stem + ".executed.ipynb")
    with out_path.open("w", encoding="utf-8") as fh:
        nbformat.write(nb, fh)
    return out_path


def main() -> None:
    executed = []
    for notebook in NOTEBOOKS:
        if not notebook.exists():
            raise FileNotFoundError(f"Notebook no encontrada: {notebook}")
        executed_path = run_notebook(notebook)
        executed.append(executed_path)

    print("Notebooks ejecutadas correctamente:")
    for path in executed:
        print(f"- {path}")


if __name__ == "__main__":
    main()
