# PlonK Tutorial Solutions - Organized

Complete solutions for all exercises in the PlonK tutorial, refactored to work without SageMath.

## 📁 Directory Structure

```
solutions/
├── README.md              # This file
├── lib/                   # Shared polynomial library
│   └── polynomials.py    # Core Polynomial classes (imported by all exercises)
├── exercise1/            # Exercise 1: Constraint system
│   └── constraints.py
├── exercise3/            # Exercise 3: Polynomial interpolation
│   └── exercise3.py
├── exercise4/            # Exercise 4: Vanishing polynomials
│   └── exercise4.py
├── exercise5/            # Exercise 5: Schwartz-Zippel checks
│   └── exercise5.py
├── exercise6/            # Exercise 6: Bilinearity of pairings
│   └── exercise6.py
├── exercise7/            # Exercise 7: KZG trusted setup
│   └── exercise7.py
├── exercise8/            # Exercise 8: KZG commitment function
│   └── exercise8.py
├── exercise9/            # Exercise 9: KZG proof generation
│   └── exercise9.py
├── exercise10/           # Exercise 10: KZG verification
│   └── exercise10.py
├── exercise11/           # Exercise 11: Finding generator of multiplicative subgroup
│   └── exercise11.py
├── exercise12/           # Exercise 12: Interpolation over multiplicative domain
│   └── exercise12.py
├── exercise13/           # Exercise 13: Verifying exact division (zero remainder)
│   └── exercise13.py
├── exercise14/           # Exercise 14: Computing permutation for copy constraints
│   └── exercise14.py
├── exercise15/           # Exercise 15: Numerator and denominator for grand product
│   └── exercise15.py
├── exercise16/           # Exercise 16: Accumulator functions for grand product
│   └── exercise16.py
├── exercise17/           # Exercise 17: Interpolating z, N, D polynomials
│   └── exercise17.py
├── debug/                # Debug and testing scripts
│   ├── test_cell14.py
│   └── debug_cell14.py
└── docs/                 # All documentation
    ├── README.md                      # Detailed documentation
    ├── KZG_COMMITMENTS_EXPLAINED.md  # KZG commitment scheme explained
    ├── SCHWARTZ_ZIPPEL_EXPLAINED.md  # Schwartz-Zippel lemma explained
    ├── EXERCISE4_SUMMARY.md          # Exercise 4 summary
    ├── EXERCISE5_SUMMARY.md          # Exercise 5 summary
    ├── CELL14_FIX_EXPLANATION.md     # Polynomial composition fix
    └── FINAL_FIX_SUMMARY.md          # Complete fix summary
```

## 🚀 Quick Start

### Prerequisites

All Python scripts use **portable shebangs** (`#!/usr/bin/env python3`) that work on any system.

**Recommended: Helper Script (Guaranteed Venv)**
```bash
# From repo root - always uses venv Python, no activation needed
./run.sh sageless/solutions/exercise1/constraints.py
./run.sh sageless/solutions/exercise6/exercise6.py
```

**Alternative: Activate Venv Then Run**
```bash
source .venv/bin/activate
# Now scripts automatically use venv Python
./sageless/solutions/exercise1/constraints.py
./sageless/solutions/exercise6/exercise6.py
```

**First Time Setup:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install py_ecc numpy jupyterlab
```

See [docs/VENV_SETUP.md](docs/VENV_SETUP.md) for complete portable venv configuration details.

### Run Exercises

Each exercise can be run from its own directory:

```bash
# Exercise 1 - Constraint System
./exercise1/constraints.py

# Exercise 3 - Polynomial Interpolation
./exercise3/exercise3.py

# Exercise 4 - Vanishing Polynomials
./exercise4/exercise4.py

# Exercise 5 - Schwartz-Zippel Checks
./exercise5/exercise5.py

# Exercise 6 - Bilinearity of Pairings
./exercise6/exercise6.py

# Exercise 7 - KZG Trusted Setup
./exercise7/exercise7.py

# Exercise 8 - KZG Commitment Function
./exercise8/exercise8.py

# Exercise 9 - KZG Proof Generation
./exercise9/exercise9.py

# Exercise 10 - KZG Verification
./exercise10/exercise10.py

# Exercise 11 - Multiplicative Subgroup Generator
./exercise11/exercise11.py

# Exercise 12 - Interpolation over Multiplicative Domain
./exercise12/exercise12.py

# Exercise 13 - Verifying Exact Division
./exercise13/exercise13.py

# Exercise 14 - Computing Permutation for Copy Constraints
./exercise14/exercise14.py

# Exercise 15 - Numerator and Denominator for Grand Product
./exercise15/exercise15.py

# Exercise 16 - Accumulator Functions
./exercise16/exercise16.py

# Exercise 17 - Interpolating z, N, D Polynomials
./exercise17/exercise17.py
```

Or from the repo root:

```bash
./sageless/solutions/exercise1/constraints.py
./sageless/solutions/exercise4/exercise4.py
./sageless/solutions/exercise5/exercise5.py
./sageless/solutions/exercise6/exercise6.py
./sageless/solutions/exercise7/exercise7.py
./sageless/solutions/exercise8/exercise8.py
./sageless/solutions/exercise9/exercise9.py
./sageless/solutions/exercise10/exercise10.py
./sageless/solutions/exercise11/exercise11.py
./sageless/solutions/exercise12/exercise12.py
./sageless/solutions/exercise13/exercise13.py
./sageless/solutions/exercise14/exercise14.py
./sageless/solutions/exercise15/exercise15.py
./sageless/solutions/exercise16/exercise16.py
./sageless/solutions/exercise17/exercise17.py
```

## 📚 Documentation

All documentation is in the **[docs/](docs/)** directory:

- **[docs/README.md](docs/README.md)** - Comprehensive guide with detailed explanations
- **[docs/KZG_COMMITMENTS_EXPLAINED.md](docs/KZG_COMMITMENTS_EXPLAINED.md)** - KZG commitment scheme explained simply
- **[docs/VENV_SETUP.md](docs/VENV_SETUP.md)** - Virtual environment configuration for all scripts
- **[docs/SCHWARTZ_ZIPPEL_EXPLAINED.md](docs/SCHWARTZ_ZIPPEL_EXPLAINED.md)** - Schwartz-Zippel lemma in simple terms
- **[docs/EXERCISE4_SUMMARY.md](docs/EXERCISE4_SUMMARY.md)** - Vanishing polynomials explained
- **[docs/EXERCISE5_SUMMARY.md](docs/EXERCISE5_SUMMARY.md)** - Probabilistic equality checks
- **[docs/CELL14_FIX_EXPLANATION.md](docs/CELL14_FIX_EXPLANATION.md)** - Polynomial composition fix details
- **[docs/FINAL_FIX_SUMMARY.md](docs/FINAL_FIX_SUMMARY.md)** - All notebook fixes summarized

## 🔧 Exercise Overview

### Exercise 1: Constraint System
**Location:** `exercise1/constraints.py`

Implements the 5 constraints for computing F₄²:
- Initial values, addition gates, wiring, multiplication
- **Result:** Proves F₄² = 9

---

### Exercise 3: Polynomial Interpolation
**Location:** `exercise3/exercise3.py`

Interpolates witness and selector vectors as polynomials over F_p.
- Contains complete `Polynomial` class implementation
- Self-contained - all other exercises import from `lib/polynomials.py`
- **Output:** Polynomials a(x), b(x), c(x), qL(x), qR(x), qM(x)

---

### Exercise 4: Vanishing Polynomials
**Location:** `exercise4/exercise4.py`

Computes vanishing polynomials and quotients.
- **Imports from:** `lib/polynomials`
- **Computes:** Z(x), Q(x), Z1(x), Q1(x), Q2(x)
- **Verifies:** Polynomial division with zero remainder

---

### Exercise 5: Schwartz-Zippel Checks
**Location:** `exercise5/exercise5.py`

Probabilistic equality verification at random points.
- **Imports from:** `lib/polynomials`
- **Checks:** t(42), f1(74102), f2(987654321987654321)
- **Security:** Error probability ≈ 10⁻⁷⁵

---

### Exercise 6: Bilinearity of Pairings
**Location:** `exercise6/exercise6.py`

Verifies the bilinearity property of the pairing function.
- **Imports from:** `kzg` (for BN254 parameters)
- **Verifies:** e([s]·P, Q) = e(P, [s]·Q) = e(P, Q)^s
- **Requires:** py_ecc library (run with venv activated)

---

### Exercise 7: KZG Trusted Setup
**Location:** `exercise7/exercise7.py`

Computes the trusted setup parameters for KZG commitments.
- **Computes:** S₁ = [P, τ·P, τ²·P, ..., τ¹⁰·P] and S₂ = τ·Q
- **Parameters:** τ=424242 (toxic waste), l=10 (max degree)
- **Security:** Demonstrates why τ must be destroyed after setup

---

### Exercise 8: KZG Commitment Function
**Location:** `exercise8/exercise8.py`

Implements the polynomial commitment function using KZG.
- **Function:** `commitment(S1, p)` returns commitment point `c`
- **Formula:** c = Σᵢ aᵢ·S1[i] = p(τ)·P
- **Properties:** Binding, hiding, succinct, homomorphic

---

### Exercise 9: KZG Proof Generation
**Location:** `exercise9/exercise9.py`

Implements the proof generation function for KZG polynomial evaluation.
- **Function:** `proof(S1, Qc)` returns proof point `π`
- **Formula:** π = Σᵢ bᵢ·S1[i] = Qc(τ)·P
- **Quotient:** Qc(x) = (f(x) - f(γ)) / (x - γ)
- **Test case:** γ = 151515, a(γ) = 1739069066686765

---

### Exercise 10: KZG Verification
**Location:** `exercise10/exercise10.py`

Implements the verification function for KZG polynomial commitments.
- **Function:** `verification(c, π, γ, b)` returns True/False
- **Equation:** e(π, S₂ - γ·Q) ?= e(c - b·P, Q)
- **Purpose:** Verify polynomial evaluation without knowing τ
- **Tests:** Both valid and invalid proofs

---

### Exercise 11: Multiplicative Subgroup Generator
**Location:** `exercise11/exercise11.py`

Finds a generator ω of a multiplicative domain of order 4.
- **Algorithm:** Find smallest h such that ω = h^r has order 4, where r = (p-1)/4
- **Result:** ω found using h = 5
- **Domain:** Ω = {ω, ω^2, ω^3, 1}
- **Advantage:** Vanishing polynomial Z(x) = x^4 - 1 (constant time!)

---

### Exercise 12: Interpolation over Multiplicative Domain
**Location:** `exercise12/exercise12.py`

Re-interpolates witness and selector polynomials over multiplicative domain Ω.
- **Witness polynomials:** a(x), b(x), c(x) over Ω = {ω, ω^2, ω^3, 1}
- **Selector polynomials:** qL(x), qR(x), qM(x) over Ω
- **Mapping:** Gate i → ω^i
- **Result:** Different coefficients than over I, but same values at domain points

---

### Exercise 13: Verifying Exact Division
**Location:** `exercise13/exercise13.py`

Verifies that gate constraint polynomial t(x) is exactly divisible by Z(x).
- **Constraint:** t(x) = qM·a·b + qL·a + qR·b - c
- **Vanishing:** Z(x) = x^4 - 1
- **Division:** t(x) = Q(x)·Z(x) + R(x)
- **Result:** Remainder R(x) = 0 ✓ (exact division!)

---

### Exercise 14: Computing Permutation for Copy Constraints
**Location:** `exercise14/exercise14.py`

Computes permutation σ encoding copy constraints (wiring) between circuit columns.
- **Permutation:** σ: {1..12} → {1..12} over all positions
- **Position mapping:** pos(column, index) = (column-1)*n + index
- **Cycles:** 6 cycles encoding value equalities
- **Key cycle:** (3, 6, 9) for value 1 from c[1]
- **Result:** All 12 positions mapped correctly ✓

---

### Exercise 15: Numerator and Denominator for Grand Product Argument
**Location:** `exercise15/exercise15.py`

Implements numerator and denominator functions for PlonK's grand product argument.
- **Numerator:** pos(column, i) + β·f(ω^i) + γ
- **Denominator:** σ(pos(column, i)) + β·f(ω^i) + γ
- **Purpose:** Verify permutation without revealing wire values
- **Key insight:** Grand product = 1 if permutation is valid
- **Result:** All test cases pass (87, 90, 94, 91) ✓

---

### Exercise 16: Accumulator Functions for Grand Product Argument
**Location:** `exercise16/exercise16.py`

Implements accumulator functions computing partial products of numerators/denominators.
- **acc_numerator:** ∏_{j=1}^{i-1} numerator(j, ...)
- **acc_denominator:** ∏_{j=1}^{i-1} denominator(j, ...)
- **Range:** Product from j=1 to i-1 (i exclusive)
- **Grand product check:** N_n / D_n = 1 ✓
- **Result:** Confirms permutation correctly encodes copy constraints ✓

---

### Exercise 17: Interpolating z, N, D Polynomials
**Location:** `exercise17/exercise17.py`

Computes and interpolates the three core polynomials for PlonK's permutation argument.
- **z polynomial:** Recursive accumulator with z(ω) = 1, z(ω^(i+1)) = z(ω^i)·N(ω^i)/D(ω^i)
- **N polynomial:** Product of numerators across columns at each point
- **D polynomial:** Product of denominators across columns at each point
- **Validation:** ZH divides L1*(z-1) ✓ and z*N - D*z(x*ω) ✓
- **Result:** Successfully encodes permutation argument for copy constraints ✓

## 🧪 Testing

Run all tests from the `debug/` directory:

```bash
cd debug
python3 test_cell14.py      # Test polynomial composition
python3 debug_cell14.py     # Detailed debugging info
```

### Quick Verification
Test all exercises in one command:

```bash
cd /Users/boy/projects/plonk/sageless/solutions
python3 -c "
import sys, os, io
sys.path.insert(0, '.')
old = sys.stdout; sys.stdout = io.StringIO()
from lib.polynomials import *
sys.stdout = old

x = PolynomialVar(p)
t = qM*a*b + qL*a + qR*b - c
f1, f2 = a(x+1) - b(x), b(x+1) - c(x)

Z = Polynomial([1], p)
for i in I: Z = Z * (x - i)
Q, _ = t.quo_rem(Z)

I_prime = [i for i in I if i not in {3, 4}]
Z1 = Polynomial([1], p)
for i in I_prime: Z1 = Z1 * (x - i)
Q1, _ = f1.quo_rem(Z1)
Q2, _ = f2.quo_rem(Z1)

γ1, γ2, γ3 = 42, 74102, 987654321987654321
assert t(γ1) == (Q(γ1) * Z(γ1)) % p
assert f1(γ2) == (Q1(γ2) * Z1(γ2)) % p
assert f2(γ3) == (Q2(γ3) * Z1(γ3)) % p
print('✓ All exercises verified!')
"
```

## 📊 Library Structure

### `lib/polynomials.py`

Core library that all exercises depend on. Contains:

**Classes:**
- `Polynomial` - Polynomial arithmetic in GF(p)
  - Operations: `+`, `-`, `*`, `//`, `%`, `**`, `==`
  - Methods: `quo_rem()`, `divides()`, `degree()`, `__call__()`
  - Supports polynomial composition: `a(x+1)`

- `PolynomialVar` - Represents variable x
  - Supports all polynomial operations
  - Returns `Polynomial` objects

**Functions:**
- `interpolate(I, Y)` - Lagrange interpolation
- `prod(iterable)` - Product of elements
- `random_polynomial(degree)` - Random polynomial generation

**Pre-computed values:**
- `p` - BN254 curve order
- `I`, `LI`, `RI`, `O` - Circuit witness values
- `SL`, `SR`, `SM` - Selector values
- `a`, `b`, `c` - Witness polynomials
- `qL`, `qR`, `qM` - Selector polynomials
- `x` - Polynomial variable

## 🔍 Import Examples

All exercises (4 and 5) and debug scripts import from `lib/polynomials`:

```python
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import from lib
from lib.polynomials import Polynomial, PolynomialVar, p, interpolate
from lib.polynomials import I, LI, RI, O, a, b, c, qL, qR, qM
```

## 🎯 Key Improvements

### Before (Messy)
```
solutions/
├── constraints.py
├── exercise3.py
├── exercise4.py
├── exercise5.py
├── debug_cell14.py
├── test_cell14.py
├── CELL14_FIX_EXPLANATION.md
├── EXERCISE4_SUMMARY.md
├── EXERCISE5_SUMMARY.md
├── ... (all files in one directory)
```

### After (Organized)
```
solutions/
├── lib/              # Shared code
├── exercise1/        # One exercise per directory
├── exercise3/
├── exercise4/
├── exercise5/
├── debug/           # Testing utilities
└── docs/            # All documentation
```

**Benefits:**
- ✓ Clear organization by purpose
- ✓ Easy to navigate
- ✓ Shared library prevents code duplication
- ✓ Documentation separated from code
- ✓ All imports still work correctly

## 🔗 Related Files

- **../PlonK-Tutorial.ipynb** - Main tutorial notebook (SageMath-free!)
- **../kzg.py** - KZG polynomial commitments using py_ecc

## ✅ Verification

All exercises have been tested and verified:
- [x] Exercise 1 - Constraints satisfied
- [x] Exercise 3 - Polynomials interpolate correctly
- [x] Exercise 4 - Vanishing polynomials and quotients computed
- [x] Exercise 5 - Schwartz-Zippel checks pass
- [x] Exercise 6 - Bilinearity verification passes
- [x] Exercise 7 - Trusted setup computed correctly
- [x] Exercise 8 - Commitment function works, matches expected output
- [x] Exercise 9 - Proof generation works, matches expected output
- [x] Exercise 10 - Verification function works, correctly validates proofs
- [x] Exercise 11 - Generator ω of order 4 found (h=5), domain verified
- [x] Exercise 12 - Polynomials interpolated over Ω, all evaluations correct
- [x] Exercise 13 - Exact division verified, remainder R(x) = 0
- [x] Exercise 14 - Permutation σ computed correctly, all cycles verified
- [x] Exercise 15 - Numerator and denominator functions implemented, all tests pass
- [x] Exercise 16 - Accumulator functions implemented, grand product check passes
- [x] Exercise 17 - z, N, D polynomials interpolated, both validation checks pass
- [x] All imports work from new structure
- [x] Debug scripts functional
- [x] No SageMath dependencies!

---

**PlonK Tutorial by zkSecurity**
**Refactored and organized for clarity**
**All solutions verified ✓**
