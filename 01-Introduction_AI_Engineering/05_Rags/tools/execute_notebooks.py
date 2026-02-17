"""Ejecuta notebooks de la clase 05 y guarda artefactos de validacion."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parents[2]
NOTEBOOKS = [
    ROOT / "05_Rags" / "Notebooks" / "01_bases_datos_vectoriales.ipynb",
    ROOT / "05_Rags" / "Notebooks" / "02_rag_pipeline.ipynb",
    ROOT / "05_Rags" / "Notebooks" / "03_rag_prompt_chaining.ipynb",
    ROOT / "05_Rags" / "Notebooks" / "04_rag_routing.ipynb",
]


def run_notebook(path: Path) -> Path:
    with path.open("r", encoding="utf-8") as fh:
        nb = nbformat.read(fh, as_version=4)

    client = NotebookClient(
        nb,
        timeout=420,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
    )
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
        executed.append(run_notebook(notebook))

    print("Notebooks clase 05 ejecutadas correctamente:")
    for path in executed:
        print(f"- {path}")


if __name__ == "__main__":
    main()
