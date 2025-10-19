# PlonK Zero-Knowledge Proof Tutorial

Educational implementation of the PlonK zero-knowledge proof system with KZG polynomial commitments on the BN254 curve.

**Original Tutorial:** [zkSecurity PlonK Tutorial](https://github.com/zksecurity/plonk-by-finger-exercise)

## Key Features

- ✅ **SageMath-Free** - Refactored to use pure Python with `py_ecc` library. 
- ✅ **Portable** - Works on any system without hardcoded paths. 
- ✅ **Complete Solutions** - All exercises solved and verified. 
- ✅ **Well-Documented** - Comprehensive explanations and examples

## Quick Start

### 1. Setup Virtual Environment

```bash
# Clone the repository
git clone <repo-url>
cd plonk

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install py_ecc numpy jupyterlab
```

### 2. Run the Jupyter Notebook

```bash
source .venv/bin/activate
jupyter lab
# Open sageless/PlonK-Tutorial.ipynb
```

### 3. Run Exercise Solutions

**Option A: Using Helper Script (Recommended)**
```bash
# Automatically uses venv Python
./run.sh sageless/solutions/exercise1/constraints.py
./run.sh sageless/solutions/exercise6/exercise6.py
```

**Option B: After Activating Venv**
```bash
source .venv/bin/activate
./sageless/solutions/exercise1/constraints.py
./sageless/solutions/exercise6/exercise6.py
```

## Directory Structure

```
plonk/
├── run.sh                          # Helper script to run with venv
├── sageless/                       # SageMath-free implementations
│   ├── kzg.py                     # KZG commitments using py_ecc
│   ├── PlonK-Tutorial.ipynb       # Main tutorial notebook (Python 3 kernel)
│   ├── BEFORE_AFTER_EXAMPLES.md   # SageMath → Python refactoring guide
│   └── solutions/                 # Exercise solutions (all 22 exercises)
│       ├── exercise1-22/          # Individual exercise solutions
│       ├── lib/                   # Shared polynomial library
│       ├── debug/                 # Debugging & verification
│       │   ├── ALL_FIXES_SUMMARY.md    # Complete fix documentation
│       │   ├── cell14/            # Cell 14 debugging
│       │   ├── cell98/            # Cell 98 debugging
│       │   ├── verify_plonk/      # verify_plonk fixes
│       │   └── ...                # Other debug directories
│       └── docs/                  # Comprehensive documentation
│           ├── MODULO_P_EXPLAINED.md   # Why modulo p is critical
│           └── ...                # 15+ other docs
└── notebook/                      # Original SageMath version (archived)
```

## Exercises Completed

All 22 exercises from the PlonK tutorial have been completed and verified:

- ✅ **Exercises 1-6** - Core concepts (constraints, interpolation, vanishing polynomials, Schwartz-Zippel, pairings)
- ✅ **Exercises 7-12** - Advanced polynomial techniques and KZG commitments
- ✅ **Exercises 13-18** - PlonK protocol implementation
- ✅ **Exercises 19-22** - Complete proof generation and verification

**Status:** ✅ Fully working with all verification checks passing

**Major Debugging Completed:**
- Fixed 4 critical issues in the tutorial (see [debug/ALL_FIXES_SUMMARY.md](sageless/solutions/debug/ALL_FIXES_SUMMARY.md))
- All PlonK proof verification now passes correctly
- Comprehensive documentation of fixes and explanations

## Documentation

### Main Documentation
- **[sageless/solutions/README.md](sageless/solutions/README.md)** - Complete solutions guide for all 22 exercises
- **[sageless/BEFORE_AFTER_EXAMPLES.md](sageless/BEFORE_AFTER_EXAMPLES.md)** - SageMath → Python refactoring examples

### Key Technical Docs
- **[sageless/solutions/docs/MODULO_P_EXPLAINED.md](sageless/solutions/docs/MODULO_P_EXPLAINED.md)** - Why `pow(base, exp, p)` is critical ⭐
- **[sageless/solutions/docs/SCHWARTZ_ZIPPEL_EXPLAINED.md](sageless/solutions/docs/SCHWARTZ_ZIPPEL_EXPLAINED.md)** - Probabilistic equality testing
- **[sageless/solutions/docs/VENV_SETUP.md](sageless/solutions/docs/VENV_SETUP.md)** - Portable venv configuration

### Debugging & Fixes
- **[sageless/solutions/debug/ALL_FIXES_SUMMARY.md](sageless/solutions/debug/ALL_FIXES_SUMMARY.md)** - All 4 major issues fixed ⭐
- **[sageless/solutions/debug/INDEX.md](sageless/solutions/debug/INDEX.md)** - Debug navigation guide
- **[sageless/solutions/debug/final_comparison/](sageless/solutions/debug/final_comparison/)** - verify_plonk before/after

### All Documentation
- **[sageless/solutions/docs/](sageless/solutions/docs/)** - 16 comprehensive technical documents

## What's Different from Original?

### No SageMath Required!
- Original used SageMath kernel (complex installation)
- This version uses pure Python 3 with `py_ecc` library
- All polynomial operations implemented in Python

### Portable Configuration
- No hardcoded absolute paths
- Helper script (`run.sh`) for guaranteed venv usage
- Portable shebangs (`#!/usr/bin/env python3`)
- Works on any system where repo is cloned

### Complete Solutions
- All 22 exercises solved and verified
- 4 critical bugs fixed in original tutorial
- Detailed explanations and documentation
- Debug utilities and test scripts
- Before/after comparison of all changes

## Running Scripts

### Helper Script (Portable, Guaranteed Venv)

The `run.sh` helper ensures scripts always use the venv Python:

```bash
./run.sh <script_path> [args...]
```

Examples:
```bash
./run.sh sageless/solutions/exercise1/constraints.py
./run.sh sageless/solutions/exercise6/exercise6.py
./run.sh sageless/kzg.py
```

Benefits:
- ✓ Works from any directory
- ✓ No need to activate venv
- ✓ Always uses correct Python interpreter
- ✓ Clear error messages if venv missing

### Direct Execution (Requires Venv Activation)

```bash
source .venv/bin/activate
./sageless/solutions/exercise6/exercise6.py
```

## Dependencies

Installed via `pip install py_ecc numpy jupyterlab`:

- **py_ecc** (8.0.0) - BN254/BN128 elliptic curve operations and pairings
- **numpy** - Numerical computations
- **jupyterlab** - Notebook environment
- Auto-installed: eth-typing, eth-utils, cytoolz, pydantic

## Technical Details

### BN254 Curve Parameters
- **Field modulus (p):** `21888242871839275222246405745257275088696311157297823662689037894645226208583`
- **Curve order (n):** `21888242871839275222246405745257275088548364400416034343698204186575808495617`
- **Security level:** ~128 bits

### Polynomial Operations
- Custom `Polynomial` class in `lib/polynomials.py`
- Supports composition: `a(x+1)` where `x` is polynomial variable
- Field arithmetic in GF(p) using modular arithmetic
- Lagrange interpolation
- **Critical:** Use `pow(base, exp, p)` for field element exponentiation, not `**`

### KZG Commitments
- Polynomial commitments using bilinear pairings
- G1 (affine): (1, 2)
- G2 (F_p²): See kzg.py for full coordinates
- Pairing: G1 × G2 → GT (F_p¹²)

## Troubleshooting

### `ModuleNotFoundError: No module named 'py_ecc'`

Ensure venv is activated and dependencies installed:
```bash
source .venv/bin/activate
pip install py_ecc numpy
```

Or use the helper script which handles this automatically:
```bash
./run.sh sageless/solutions/exercise6/exercise6.py
```

### Helper Script Says "venv not found"

Create the virtual environment first:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install py_ecc numpy jupyterlab
```

### Notebook Kernel Issues

Make sure to:
1. Activate venv: `source .venv/bin/activate`
2. Install ipykernel: `pip install ipykernel`
3. Launch Jupyter from activated venv: `jupyter lab`
4. Select "Python 3" kernel (not "SageMath")

## Testing

Run exercise solutions to verify setup:

```bash
# Core exercises
./run.sh sageless/solutions/exercise1/constraints.py
./run.sh sageless/solutions/exercise4/exercise4.py
./run.sh sageless/solutions/exercise5/exercise5.py
./run.sh sageless/solutions/exercise6/exercise6.py

# Debug verification tests
./run.sh sageless/solutions/debug/test_cell14.py
```

All should complete without errors and display verification messages.

**Full Tutorial Verification:**
Open the Jupyter notebook and run all cells:
```bash
source .venv/bin/activate
jupyter lab
# Open sageless/PlonK-Tutorial.ipynb and run all cells
```

All 22 exercises and verification checks should pass.

## Contributing

This is an educational repository. Feel free to:
- Report issues or bugs
- Suggest documentation improvements
- Add additional exercises or examples

## Credits

- **Original Tutorial:** [zkSecurity](https://github.com/zksecurity)
- **BN254 Implementation:** [py_ecc library](https://github.com/ethereum/py_ecc)
- **PlonK Protocol:** [Gabizon, Williamson, Ciobotaru (2019)](https://eprint.iacr.org/2019/953)

## License

Educational use - see original tutorial for license details.

---

**Ready to learn PlonK? Start with the Jupyter notebook!**

```bash
source .venv/bin/activate
jupyter lab
# Open sageless/PlonK-Tutorial.ipynb
```

**Last Updated:** October 19, 2025
**Status:** ✅ Fully Working - All 22 exercises complete, all verification checks passing
