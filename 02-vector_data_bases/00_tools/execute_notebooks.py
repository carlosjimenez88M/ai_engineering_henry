"""Execute notebooks in-place for the vector data bases module."""

from __future__ import annotations

import argparse
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]

BATMAN_NOTEBOOKS = [
    ROOT / "batman_vector_db_orchestration" / "01_diseno_vector_db_batman.ipynb",
    ROOT / "batman_vector_db_orchestration" / "02_rag_vs_agentic_rag_batman.ipynb",
    ROOT / "batman_vector_db_orchestration" / "03_routing_orquestacion_simple.ipynb",
    ROOT / "batman_vector_db_orchestration" / "04_ejercicio_agent2agent_batman_rag.ipynb",
    ROOT / "batman_vector_db_orchestration" / "05_agent2agent_roles_router_batman.ipynb",
]

DATABASE_NOTEBOOKS = [
    ROOT / "databases" / "01-bases-vectoriales-fundamentos.ipynb",
    ROOT / "databases" / "02-bases-vectoriales-produccion.ipynb",
    ROOT / "databases" / "03-comparacion-modelos-embeddings-rayuela.ipynb",
]

INTRO_NOTEBOOKS = [
    ROOT / "intro" / "01_rag_tfidf.ipynb",
]

ALL_NOTEBOOKS = DATABASE_NOTEBOOKS + INTRO_NOTEBOOKS + BATMAN_NOTEBOOKS


def run_notebook(path: Path, timeout: int = 900) -> Path:
    """Execute a notebook in-place, saving outputs back to the same file."""
    with path.open("r", encoding="utf-8") as fh:
        nb = nbformat.read(fh, as_version=4)

    client = NotebookClient(
        nb,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
    )
    client.execute()

    with path.open("w", encoding="utf-8") as fh:
        nbformat.write(nb, fh)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Execute notebooks in-place")
    parser.add_argument(
        "group",
        nargs="?",
        default="all",
        choices=["all", "batman", "databases", "intro"],
        help="Which group of notebooks to execute (default: all)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=900,
        help="Timeout per notebook in seconds (default: 900)",
    )
    args = parser.parse_args()

    groups = {
        "all": ALL_NOTEBOOKS,
        "batman": BATMAN_NOTEBOOKS,
        "databases": DATABASE_NOTEBOOKS,
        "intro": INTRO_NOTEBOOKS,
    }
    notebooks = groups[args.group]

    executed = []
    for notebook in notebooks:
        if not notebook.exists():
            raise FileNotFoundError(f"Notebook not found: {notebook}")
        print(f"Executing: {notebook.relative_to(ROOT)} ...")
        run_notebook(notebook, timeout=args.timeout)
        executed.append(notebook)
        print(f"  Done: {notebook.name}")

    print(f"\n{len(executed)} notebooks executed successfully (in-place):")
    for item in executed:
        print(f"  - {item.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
