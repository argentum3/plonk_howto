#!/bin/bash
# Helper script to run Python scripts with the repository's virtual environment
# Usage: ./run.sh <script_path> [args...]
#
# Examples:
#   ./run.sh sageless/solutions/exercise6/exercise6.py
#   ./run.sh sageless/kzg.py

# Get the directory where this script is located (repo root)
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$REPO_ROOT/.venv/bin/python"

# Check if venv exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "Error: Virtual environment not found at $VENV_PYTHON"
    echo "Please create it first with: python3 -m venv .venv"
    echo "Then install dependencies: .venv/bin/pip install py_ecc numpy"
    exit 1
fi

# Check if a script was provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <script_path> [args...]"
    echo ""
    echo "Examples:"
    echo "  $0 sageless/solutions/exercise1/constraints.py"
    echo "  $0 sageless/solutions/exercise6/exercise6.py"
    echo "  $0 sageless/kzg.py"
    exit 1
fi

# Run the script with venv Python
exec "$VENV_PYTHON" "$@"
