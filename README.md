# PlonK Zero-Knowledge Proof Tutorial

Educational implementation of the PlonK zero-knowledge proof system with KZG polynomial commitments on the BN254 curve.

**Original Tutorial:** [zkSecurity PlonK Tutorial](https://github.com/zksecurity/plonk-by-finger-exercise)

## Key Features

✅ **SageMath-Free** - Refactored to use pure Python with `py_ecc` library
✅ **Portable** - Works on any system without hardcoded paths
✅ **Complete Solutions** - All exercises solved and verified
✅ **Well-Documented** - Comprehensive explanations and examples

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
│   └── solutions/                 # Exercise solutions
│       ├── exercise1/             # Constraint verification
│       ├── exercise3/             # Polynomial interpolation
│       ├── exercise4/             # Vanishing polynomials
│       ├── exercise5/             # Schwartz-Zippel checks
│       ├── exercise6/             # Pairing bilinearity
│       ├── lib/                   # Shared polynomial library
│       ├── debug/                 # Testing utilities
│       └── docs/                  # Comprehensive documentation
└── notebook/                      # Original SageMath version (archived)
```

## Exercises Completed

- ✅ **Exercise 1** - Fibonacci squared constraint system (F₄² = 9)
- ✅ **Exercise 3** - Polynomial interpolation using Lagrange
- ✅ **Exercise 4** - Vanishing polynomials and quotient computation
- ✅ **Exercise 5** - Schwartz-Zippel probabilistic equality checks
- ✅ **Exercise 6** - Bilinearity verification of BN254 pairings

## Documentation

- **[sageless/solutions/README.md](sageless/solutions/README.md)** - Complete solutions guide
- **[sageless/solutions/docs/VENV_SETUP.md](sageless/solutions/docs/VENV_SETUP.md)** - Portable venv configuration
- **[sageless/solutions/docs/SCHWARTZ_ZIPPEL_EXPLAINED.md](sageless/solutions/docs/SCHWARTZ_ZIPPEL_EXPLAINED.md)** - Lemma explanation
- **[sageless/solutions/docs/](sageless/solutions/docs/)** - All technical documentation

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
- All 6 exercises solved and verified
- Detailed explanations and documentation
- Debug utilities and test scripts

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
- Field arithmetic in GF(p)
- Lagrange interpolation

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

Run all exercise solutions to verify setup:

```bash
./run.sh sageless/solutions/exercise1/constraints.py
./run.sh sageless/solutions/exercise4/exercise4.py
./run.sh sageless/solutions/exercise5/exercise5.py
./run.sh sageless/solutions/exercise6/exercise6.py
./run.sh sageless/solutions/debug/test_cell14.py
```

All should complete without errors and display verification messages.

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
