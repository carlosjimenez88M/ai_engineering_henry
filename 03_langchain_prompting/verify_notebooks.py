"""Script de verificación de notebooks extendidos."""
import json
import ast
from pathlib import Path

def verify_notebook(notebook_path: Path) -> dict:
    """Verifica que un notebook esté bien formado."""
    results = {
        "path": str(notebook_path),
        "valid_json": False,
        "total_cells": 0,
        "code_cells": 0,
        "markdown_cells": 0,
        "syntax_errors": [],
        "import_issues": [],
    }

    try:
        # Leer notebook
        with open(notebook_path, 'r') as f:
            nb = json.load(f)
        results["valid_json"] = True

        # Contar celdas
        results["total_cells"] = len(nb.get("cells", []))

        # Verificar cada celda
        for i, cell in enumerate(nb.get("cells", [])):
            cell_type = cell.get("cell_type")

            if cell_type == "code":
                results["code_cells"] += 1

                # Verificar sintaxis de código
                source = ''.join(cell.get("source", []))
                if source.strip():
                    try:
                        ast.parse(source)
                    except SyntaxError as e:
                        results["syntax_errors"].append({
                            "cell": i,
                            "error": str(e),
                            "preview": source[:100]
                        })

                    # Verificar imports
                    if 'from' in source or 'import' in source:
                        # Detectar imports problemáticos
                        if 'cot_langgraph_02' in source or 'react_langgraph_02' in source:
                            results["import_issues"].append({
                                "cell": i,
                                "issue": "Import incorrecto (debería ser 02_*)"
                            })

            elif cell_type == "markdown":
                results["markdown_cells"] += 1

    except json.JSONDecodeError as e:
        results["syntax_errors"].append({"error": f"Invalid JSON: {e}"})
    except Exception as e:
        results["syntax_errors"].append({"error": f"Unexpected error: {e}"})

    return results


def main():
    """Verifica ambos notebooks."""
    print("=" * 80)
    print("VERIFICACION DE NOTEBOOKS EXTENDIDOS")
    print("=" * 80)

    # Verificar CoT
    cot_notebook = Path(__file__).parent / "COT_LangChain" / "Notebooks" / "02_cot_langgraph.ipynb"
    print(f"\n1. Verificando: {cot_notebook.name}")
    print("-" * 80)

    cot_results = verify_notebook(cot_notebook)
    print(f"   Valid JSON: {'[OK]' if cot_results['valid_json'] else '[FAIL]'}")
    print(f"   Total celdas: {cot_results['total_cells']}")
    print(f"   - Código: {cot_results['code_cells']}")
    print(f"   - Markdown: {cot_results['markdown_cells']}")

    if cot_results['syntax_errors']:
        print(f"   [FAIL] Errores de sintaxis: {len(cot_results['syntax_errors'])}")
        for err in cot_results['syntax_errors'][:3]:
            print(f"     - Celda {err.get('cell', 'N/A')}: {err['error'][:80]}")
    else:
        print("   [OK] Sin errores de sintaxis")

    if cot_results['import_issues']:
        print(f"   [FAIL] Issues de imports: {len(cot_results['import_issues'])}")
        for issue in cot_results['import_issues']:
            print(f"     - Celda {issue['cell']}: {issue['issue']}")
    else:
        print("   [OK] Imports correctos")

    # Verificar ReAct
    react_notebook = Path(__file__).parent / "ReAct_LangChain" / "Notebooks" / "02_react_langgraph.ipynb"
    print(f"\n2. Verificando: {react_notebook.name}")
    print("-" * 80)

    react_results = verify_notebook(react_notebook)
    print(f"   Valid JSON: {'[OK]' if react_results['valid_json'] else '[FAIL]'}")
    print(f"   Total celdas: {react_results['total_cells']}")
    print(f"   - Código: {react_results['code_cells']}")
    print(f"   - Markdown: {react_results['markdown_cells']}")

    if react_results['syntax_errors']:
        print(f"   [FAIL] Errores de sintaxis: {len(react_results['syntax_errors'])}")
        for err in react_results['syntax_errors'][:3]:
            print(f"     - Celda {err.get('cell', 'N/A')}: {err['error'][:80]}")
    else:
        print("   [OK] Sin errores de sintaxis")

    if react_results['import_issues']:
        print(f"   [FAIL] Issues de imports: {len(react_results['import_issues'])}")
        for issue in react_results['import_issues']:
            print(f"     - Celda {issue['cell']}: {issue['issue']}")
    else:
        print("   [OK] Imports correctos")

    # Resumen final
    print("\n" + "=" * 80)
    print("RESUMEN")
    print("=" * 80)

    all_good = (
        cot_results['valid_json'] and
        react_results['valid_json'] and
        not cot_results['syntax_errors'] and
        not react_results['syntax_errors'] and
        not cot_results['import_issues'] and
        not react_results['import_issues']
    )

    if all_good:
        print("[OK] Todos los notebooks están bien formados y listos para ejecutar")
        print("\nPróximos pasos:")
        print("  1. Verificar que los imports funcionen correctamente")
        print("  2. Ejecutar celdas de setup (imports)")
        print("  3. Verificar que las herramientas se carguen correctamente")
        print("  4. Ejecutar ejemplos completos")
    else:
        print("[FAIL] Se encontraron issues que necesitan corrección")
        print("\nRevisa los detalles arriba y corrige los errores")

    print("=" * 80)


if __name__ == "__main__":
    main()
