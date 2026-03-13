"""
execute_notebooks.py

Objetivo del script: 
Ejecuta notebooks del modulo Deep Learning y guarda artefactos de validacion.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = ROOT / ".artifacts" / "executed_notebooks"

NOTEBOOK_GROUPS = {
    "core": [
        ROOT / "01_fundamentos_redes_neuronales" / "01_anns_desde_cero.ipynb",
        ROOT / "02_pytorch_fundamentos" / "01_pytorch_pipeline_entrenamiento.ipynb",
        ROOT / "03_entrenamiento_redes_profundas" / "01_estabilidad_y_regularizacion.ipynb",
        ROOT / "04_vision_por_computadora_cnns" / "01_cnns_y_reconocimiento_visual.ipynb",
        ROOT / "05_modelado_de_secuencias" / "01_rnns_lstm_gru_y_cnns_temporales.ipynb",
    ],
    "nlp": [
        ROOT / "06_nlp_con_atencion" / "01_nlp_con_atencion_las_mil_y_una_noches.ipynb",
    ],
    "transformers": [
        ROOT / "07_transformers_y_chatbots" / "01_transformers_y_chat_local.ipynb",
    ],
}
NOTEBOOK_GROUPS["all"] = (
    NOTEBOOK_GROUPS["core"] + NOTEBOOK_GROUPS["nlp"] + NOTEBOOK_GROUPS["transformers"]
)


def notebook_paths(group: str = "all") -> list[Path]:
    if group not in NOTEBOOK_GROUPS:
        raise KeyError(f"Grupo invalido: {group}")
    return NOTEBOOK_GROUPS[group]


def run_notebook(path: Path, timeout: int = 1200, output_dir: Path | None = None) -> Path:
    with path.open("r", encoding="utf-8") as fh:
        notebook = nbformat.read(fh, as_version=4)

    client = NotebookClient(
        notebook,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
    )
    client.execute()

    target_dir = output_dir or ARTIFACTS_DIR
    out_path = target_dir / path.relative_to(ROOT)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        nbformat.write(notebook, fh)
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Ejecuta notebooks del modulo 04-deep_learning")
    parser.add_argument(
        "group",
        nargs="?",
        default="all",
        choices=sorted(NOTEBOOK_GROUPS),
        help="Grupo de notebooks a ejecutar",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=1200,
        help="Timeout por notebook en segundos",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Activa HENRY_DL_SMOKE=1 antes de ejecutar",
    )
    args = parser.parse_args()

    os.environ.setdefault("MPLBACKEND", "Agg")
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    if args.smoke:
        os.environ["HENRY_DL_SMOKE"] = "1"
    os.environ.setdefault("HENRY_DL_ONLINE_MODE", "0")

    executed = []
    for notebook in notebook_paths(args.group):
        if not notebook.exists():
            raise FileNotFoundError(f"Notebook no encontrada: {notebook}")
        print(f"Ejecutando: {notebook.relative_to(ROOT)}")
        executed.append(run_notebook(notebook, timeout=args.timeout))

    print("\nNotebooks ejecutadas correctamente:")
    for item in executed:
        print(f"- {item.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
