"""
smoke_test.py

Objetivo del script: 
Smoke test real con LLM — verifica el grafo end-to-end.
Requiere OPENAI_API_KEY válida en .env o entorno.

Uso: uv run python scripts/smoke_test.py

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import HumanMessage
from rich.console import Console
from rich.table import Table

from cinematic_intelligence.graph import make_cultural_graph

QUERIES = [
    ("nolan",   "Explica la técnica narrativa de Memento"),
    ("king",    "¿Cuáles son los temas recurrentes en It de Stephen King?"),
    ("davis",   "Describe el impacto de Kind of Blue en el jazz modal"),
    ("general", "¿Qué es la inteligencia artificial?"),  # fallback domain
]

console = Console()

def run():
    graph = make_cultural_graph()
    table = Table(title="Smoke Test — LLM Real", show_lines=True)
    table.add_column("Dominio esperado", style="cyan")
    table.add_column("Dominio obtenido", style="green")
    table.add_column("Final answer (primeros 120 chars)", style="white")
    table.add_column("OK", style="bold")

    errors = []
    for expected_domain, query in QUERIES:
        console.print(f"\n[bold]Query:[/bold] {query}")
        try:
            result = graph.invoke({"messages": [HumanMessage(content=query)]})
            got_domain = result["domain"].value if hasattr(result["domain"], "value") else str(result["domain"])
            final = result.get("final_response")
            answer = (final.final_answer if final else "")[:120]
            ok = "✓" if answer else "✗ (respuesta vacía)"
            if not answer:
                errors.append(f"{query}: respuesta vacía")
            table.add_row(expected_domain, got_domain, answer, ok)
        except Exception as e:
            errors.append(f"{query}: {e}")
            table.add_row(expected_domain, "ERROR", str(e)[:120], "✗")

    console.print(table)
    if errors:
        console.print(f"\n[red]FALLÓ {len(errors)} query(s):[/red]")
        for e in errors:
            console.print(f"  • {e}")
        sys.exit(1)
    else:
        console.print("\n[green]✓ Todas las queries completadas con respuestas no vacías[/green]")

if __name__ == "__main__":
    run()
