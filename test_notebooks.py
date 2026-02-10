#!/usr/bin/env python3
"""Script to execute all notebooks and report errors."""
import json
import sys
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

def execute_notebook(notebook_path: Path) -> dict:
    """Execute a notebook and return execution results."""
    result = {
        "path": str(notebook_path),
        "success": False,
        "error": None,
        "failed_cell": None
    }

    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)

        client = NotebookClient(
            nb,
            timeout=600,
            kernel_name='python3',
            allow_errors=False
        )

        client.execute()
        result["success"] = True

    except CellExecutionError as e:
        result["error"] = str(e)
        result["failed_cell"] = e.cell_index if hasattr(e, 'cell_index') else None
    except Exception as e:
        result["error"] = str(e)

    return result

def main():
    """Execute all notebooks and report results."""
    repo_root = Path(__file__).parent

    notebooks = sorted(repo_root.glob("**/*.ipynb"))
    notebooks = [nb for nb in notebooks if ".executed" not in nb.name]

    print(f"Found {len(notebooks)} notebooks to test")
    print("=" * 80)

    results = []
    for nb_path in notebooks:
        rel_path = nb_path.relative_to(repo_root)
        print(f"\nTesting: {rel_path}")

        result = execute_notebook(nb_path)
        results.append(result)

        if result["success"]:
            print(f"  [OK] Executed successfully")
        else:
            print(f"  [FAIL] Execution failed")
            if result["failed_cell"] is not None:
                print(f"    Failed at cell: {result['failed_cell']}")
            print(f"    Error: {result['error'][:200]}")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    success_count = sum(1 for r in results if r["success"])
    fail_count = len(results) - success_count

    print(f"Total: {len(results)}")
    print(f"Success: {success_count}")
    print(f"Failed: {fail_count}")

    if fail_count > 0:
        print("\nFailed notebooks:")
        for r in results:
            if not r["success"]:
                print(f"  - {Path(r['path']).relative_to(repo_root)}")
                if r['failed_cell'] is not None:
                    print(f"    Cell: {r['failed_cell']}")
                print(f"    Error: {r['error'][:150]}")

    return 0 if fail_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
