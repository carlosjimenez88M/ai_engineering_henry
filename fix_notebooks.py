#!/usr/bin/env python3
"""Fix all notebooks by removing repo_root finding code."""
import json
from pathlib import Path

def fix_notebook(nb_path: Path) -> bool:
    """Fix a single notebook."""
    if '.executed' in nb_path.name:
        return False

    with open(nb_path, 'r') as f:
        nb = json.load(f)

    modified = False
    for i, cell in enumerate(nb['cells']):
        if cell.get('cell_type') != 'code':
            continue

        source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']

        if 'find_repo_root' in source or 'repo_root = Path.cwd()' in source:
            # Remove the problematic code
            new_source = source

            # Remove find_repo_root function definition
            if 'def find_repo_root' in source:
                lines = source.split('\n')
                new_lines = []
                skip = False
                for line in lines:
                    if 'def find_repo_root' in line:
                        skip = True
                    elif skip and line and not line[0].isspace():
                        skip = False
                    if not skip:
                        new_lines.append(line)
                new_source = '\n'.join(new_lines)

            # Replace repo_root finding with simple sys.path insertion
            if 'ROOT = find_repo_root' in new_source or 'repo_root = Path.cwd()' in new_source:
                # Simple setup that just adds parent directories to path
                setup_code = """# Setup
import sys
from pathlib import Path

# Add project root to path
project_root = Path.cwd()
while not (project_root / "pyproject.toml").exists() and project_root != project_root.parent:
    project_root = project_root.parent

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
"""
                # Keep only imports and the rest
                lines = new_source.split('\n')
                import_lines = []
                other_lines = []
                in_setup = False

                for line in lines:
                    if 'import' in line and ('from' in line or line.strip().startswith('import')):
                        if 'find_repo_root' not in line and 'importlib' not in line:
                            import_lines.append(line)
                    elif 'ROOT = find_repo_root' in line or 'repo_root = Path.cwd()' in line:
                        in_setup = True
                    elif 'print(' in line and ('ROOT' in line or 'root' in line):
                        continue
                    elif not in_setup:
                        other_lines.append(line)
                    elif line and not line[0].isspace():
                        in_setup = False
                        other_lines.append(line)

                new_source = setup_code + '\n' + '\n'.join(import_lines + other_lines)

            cell['source'] = new_source
            modified = True
            print(f"  Fixed cell {i}")

    if modified:
        with open(nb_path, 'w') as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
        return True

    return False


def main():
    """Fix all notebooks."""
    repo_root = Path(__file__).parent
    notebooks = sorted(repo_root.glob("**/*.ipynb"))
    notebooks = [nb for nb in notebooks if ".executed" not in nb.name]

    print(f"Checking {len(notebooks)} notebooks")
    print("=" * 80)

    fixed_count = 0
    for nb_path in notebooks:
        rel_path = nb_path.relative_to(repo_root)

        if 'find_repo_root' in nb_path.read_text() or 'repo_root = Path.cwd()' in nb_path.read_text():
            print(f"\nFixing: {rel_path}")
            if fix_notebook(nb_path):
                fixed_count += 1
                print(f"  [OK] Fixed")

    print("\n" + "=" * 80)
    print(f"Fixed {fixed_count} notebooks")


if __name__ == "__main__":
    main()
