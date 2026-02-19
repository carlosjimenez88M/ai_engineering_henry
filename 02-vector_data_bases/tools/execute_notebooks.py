"""Execute notebooks for the Batman vector DB orchestration module."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = [
    ROOT / "batman_vector_db_orchestration" / "01_diseno_vector_db_batman.ipynb",
    ROOT / "batman_vector_db_orchestration" / "02_rag_vs_agentic_rag_batman.ipynb",
    ROOT / "batman_vector_db_orchestration" / "03_routing_orquestacion_simple.ipynb",
]


def run_notebook(path: Path) -> Path:
    with path.open("r", encoding="utf-8") as fh:
        nb = nbformat.read(fh, as_version=4)

    client = NotebookClient(
        nb,
        timeout=900,
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
            raise FileNotFoundError(f"Notebook not found: {notebook}")
        executed.append(run_notebook(notebook))

    print("Batman module notebooks executed successfully:")
    for item in executed:
        print(f"- {item}")


if __name__ == "__main__":
    main()
