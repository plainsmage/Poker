#!/usr/bin/env bash
set -e

mkdir -p solver examples tests .github/workflows

cat > solver/__init__.py <<'EOT'
__version__ = "0.1.0"
EOT

cat > solver/core.py <<'EOT'
def solve_hand(state):
    """
    Minimal placeholder solver.
    Replace with your algorithm.
    Input: state dict describing game (players, stacks, board, pot, history)
    Output: dict with keys 'action' and 'ev'
    """
    return {"action": "fold", "ev": 0.0}
EOT

cat > solver/cli.py <<'EOT'
import sys, json
from solver.core import solve_hand

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            state = json.load(f)
    else:
        state = json.load(sys.stdin)
    print(json.dumps(solve_hand(state), indent=2))

if __name__ == "__main__":
    main()
EOT

cat > examples/run_example.py <<'EOT'
from solver.core import solve_hand

if __name__ == "__main__":
    state = {
        "hero": {"stack": 100, "cards": ["As", "Kd"]},
        "villain": {"stack": 100},
        "pot": 1,
        "board": [],
        "history": []
    }
    print(solve_hand(state))
EOT

cat > tests/test_core.py <<'EOT'
from solver.core import solve_hand

def test_solve_hand_returns_dict():
    out = solve_hand({"dummy": True})
    assert isinstance(out, dict)
    assert "action" in out
EOT

cat > requirements.txt <<'EOT'
pytest
black
flake8
EOT

cat > pyproject.toml <<'EOT'
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "poker-solver"
version = "0.1.0"
description = "A minimal poker solver"
authors = [{name = "plainsmage"}]
dependencies = []
EOT

cat > .gitignore <<'EOT'
__pycache__/
*.py[cod]
.venv
venv/
.vscode/
.idea/
.DS_Store
Thumbs.db
EOT

cat > .gitattributes <<'EOT'
*.pt filter=lfs diff=lfs merge=lfs -text
*.pth filter=lfs diff=lfs merge=lfs -text
*.bin filter=lfs diff=lfs merge=lfs -text
*.h5 filter=lfs diff=lfs merge=lfs -text
EOT

cat > .github/workflows/ci.yml <<'EOT'
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: pytest -q
      - name: Lint
        run: |
          pip install black flake8
          black --check .
          flake8 .
EOT

echo "Skeleton created"
