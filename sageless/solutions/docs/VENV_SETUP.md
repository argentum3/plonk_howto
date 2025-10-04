# Virtual Environment Setup for All Python Scripts

## Overview

All Python scripts in the `sageless/` directory use **portable shebangs** and can be run with the repository's virtual environment in multiple ways.

## What Was Changed

### 1. Added Portable Shebang Lines

Every `.py` file now starts with:
```python
#!/usr/bin/env python3
```

**Why portable?** This shebang:
- Works on any system (no hardcoded paths)
- Uses whatever Python 3 is in the current PATH
- Automatically uses venv Python when venv is activated
- Falls back to system Python if venv not activated

### 2. Created Helper Script (`run.sh`)

A portable helper script in the repo root that automatically runs scripts with the venv Python:

```bash
./run.sh sageless/solutions/exercise6/exercise6.py
```

The helper script:
- Finds the repo root automatically (works from any clone location)
- Uses `.venv/bin/python` relative to repo root
- Works on any machine without hardcoded paths

### 3. Made Scripts Executable

All scripts have been given executable permissions:
```bash
chmod +x sageless/**/*.py
```

## Files Updated

### Core Files
- `sageless/kzg.py` - KZG polynomial commitments (requires py_ecc)
- `sageless/refactor_notebook.py` - Notebook refactoring utility

### Solution Scripts
- `sageless/solutions/exercise1/constraints.py` - Constraint verification
- `sageless/solutions/exercise3/exercise3.py` - Polynomial interpolation
- `sageless/solutions/exercise4/exercise4.py` - Vanishing polynomials
- `sageless/solutions/exercise5/exercise5.py` - Schwartz-Zippel checks
- `sageless/solutions/exercise6/exercise6.py` - Bilinearity verification

### Library and Debug
- `sageless/solutions/lib/polynomials.py` - Shared polynomial library
- `sageless/solutions/debug/test_cell14.py` - Cell 14 tests
- `sageless/solutions/debug/debug_cell14.py` - Cell 14 debugging

## Usage Options

### Option 1: Helper Script (Recommended for Guaranteed Venv)

```bash
# From repo root, run any script with venv Python
./run.sh sageless/solutions/exercise6/exercise6.py
./run.sh sageless/kzg.py
./run.sh sageless/solutions/exercise1/constraints.py
```

**Pros:**
- ✓ Always uses venv Python
- ✓ No need to activate venv
- ✓ Works from any directory
- ✓ Portable across systems

### Option 2: Activate Venv Then Run Directly

```bash
# Activate venv once
source .venv/bin/activate

# Run scripts directly
./sageless/solutions/exercise6/exercise6.py
./sageless/solutions/exercise1/constraints.py

# Or with python command
python sageless/solutions/exercise6/exercise6.py
```

**Pros:**
- ✓ Traditional Python workflow
- ✓ Venv Python used for all commands
- ✓ Can run multiple scripts without repeating activation

### Option 3: Direct Execution (Uses System Python if Venv Not Activated)

```bash
# Direct execution uses whatever python3 is in PATH
./sageless/solutions/exercise1/constraints.py
```

**Pros:**
- ✓ Quick and simple
- ✓ Uses venv Python if activated
- ✓ Falls back to system Python

**Cons:**
- ⚠️  May use system Python if venv not activated
- ⚠️  May fail if dependencies not in system Python

## Benefits

### ✓ Portable
- No hardcoded paths (works on any machine)
- Works regardless of where repo is cloned
- Compatible with all Unix-like systems (Linux, macOS, WSL)

### ✓ Flexible
- Three usage options to fit different workflows
- Works with or without venv activation
- IDE-compatible

### ✓ Safe
- Helper script guarantees venv usage
- No system package pollution
- All dependencies isolated in venv

### ✓ Convenient
- Direct script execution when venv activated
- Helper script when venv not activated
- No manual path configuration needed

## Setup for New Users

1. **Clone the repository** (anywhere on their system):
   ```bash
   git clone <repo-url>
   cd plonk
   ```

2. **Create and activate venv**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install py_ecc numpy jupyterlab
   ```

4. **Run scripts** (choose any method):
   ```bash
   # Method 1: Helper script
   ./run.sh sageless/solutions/exercise6/exercise6.py

   # Method 2: Direct (venv already activated)
   ./sageless/solutions/exercise6/exercise6.py

   # Method 3: Python command
   python sageless/solutions/exercise6/exercise6.py
   ```

## Verification

All scripts tested and working with both methods:

```bash
✓ ./run.sh sageless/solutions/exercise1/constraints.py
✓ ./run.sh sageless/solutions/exercise4/exercise4.py
✓ ./run.sh sageless/solutions/exercise5/exercise5.py
✓ ./run.sh sageless/solutions/exercise6/exercise6.py
✓ ./run.sh sageless/solutions/debug/test_cell14.py

# Also works with venv activated:
✓ source .venv/bin/activate && ./sageless/solutions/exercise1/constraints.py
```

## Dependencies in venv

The virtual environment includes:
- `py_ecc` (8.0.0) - BN254 curve operations and pairings
- `numpy` - Numerical operations
- `jupyterlab` - Notebook environment
- All required dependencies (eth-typing, eth-utils, etc.)

## Why This Approach?

### Portability First
- No hardcoded paths like `/Users/boy/projects/plonk/`
- Works on any machine where repo is cloned
- Compatible with CI/CD systems

### User-Friendly
- Multiple usage options for different workflows
- Clear error messages from `run.sh` if venv missing
- No magic - users understand what's happening

### Best Practices
- Virtual environment isolation
- Standard Python shebang patterns
- Executable scripts follow Unix conventions

## Note for Notebook

The Jupyter notebook (`sageless/PlonK-Tutorial.ipynb`) should be run through JupyterLab with activated venv:

```bash
source .venv/bin/activate
jupyter lab
```

Or using the helper:
```bash
source .venv/bin/activate  # Still needed for jupyter
jupyter lab
```

---

**All Python scripts now use portable configuration that works anywhere!**
