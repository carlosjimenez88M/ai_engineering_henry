"""Execute all class 04 LangGraph notebooks and persist executed artifacts."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parents[2]
NOTEBOOKS = [
    ROOT / "04_langchain_langgraph" / "01_prompt_chaining" / "Notebooks" / "prompt_chaining_langgraph.ipynb",
    ROOT / "04_langchain_langgraph" / "02_parallelization" / "Notebooks" / "parallelization_langgraph.ipynb",
    ROOT / "04_langchain_langgraph" / "03_orchestrator_worker" / "Notebooks" / "orchestrator_worker_langgraph.ipynb",
    ROOT / "04_langchain_langgraph" / "04_evaluator_optimizer" / "Notebooks" / "evaluator_optimizer_langgraph.ipynb",
    ROOT / "04_langchain_langgraph" / "05_routing" / "Notebooks" / "routing_langgraph.ipynb",
    ROOT / "04_langchain_langgraph" / "06_agent_feedback" / "Notebooks" / "agent_feedback_langgraph.ipynb",
]


def run_notebook(path: Path) -> Path:
    with path.open("r", encoding="utf-8") as fh:
        nb = nbformat.read(fh, as_version=4)

    client = NotebookClient(nb, timeout=360, kernel_name="python3")
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

    print("Notebooks clase 04 ejecutadas correctamente:")
    for item in executed:
        print(f"- {item}")


if __name__ == "__main__":
    main()
