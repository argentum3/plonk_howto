# PlonK Tutorial Solutions

This directory contains complete solutions for all exercises in the PlonK tutorial, refactored to work without SageMath.

## 📚 Documentation

### Core Concepts
- **[SCHWARTZ_ZIPPEL_EXPLAINED.md](SCHWARTZ_ZIPPEL_EXPLAINED.md)** - Simple explanation of the Schwartz-Zippel lemma with intuitive examples
- **[CELL14_FIX_EXPLANATION.md](CELL14_FIX_EXPLANATION.md)** - Detailed explanation of polynomial composition fix
- **[FINAL_FIX_SUMMARY.md](FINAL_FIX_SUMMARY.md)** - Complete summary of all notebook fixes

### Exercise Summaries
- **[EXERCISE4_SUMMARY.md](EXERCISE4_SUMMARY.md)** - Vanishing polynomials and polynomial division
- **[EXERCISE5_SUMMARY.md](EXERCISE5_SUMMARY.md)** - Schwartz-Zippel probabilistic equality checks

## 🔧 Solution Scripts

### Exercise Solutions
1. **[constraints.py](constraints.py)** - Solution to Exercise 1 (constraint system)
2. **[exercise3.py](exercise3.py)** - Solution to Exercise 3 (polynomial interpolation)
   - Contains complete Polynomial and PolynomialVar classes
   - Implements Lagrange interpolation
   - All other exercises import from this file
3. **[exercise4.py](exercise4.py)** - Solution to Exercise 4 (vanishing polynomials)
4. **[exercise5.py](exercise5.py)** - Solution to Exercise 5 (Schwartz-Zippel checks)

### Testing & Debugging
- **[test_cell14.py](test_cell14.py)** - Tests for polynomial composition functionality
- **[debug_cell14.py](debug_cell14.py)** - Detailed debugging script for cell 14 issues

## 🚀 Running the Solutions

### Prerequisites
```bash
pip install py_ecc numpy
```

### Run Individual Exercises
```bash
cd /Users/boy/projects/plonk/sageless/solutions

# Exercise 1
python3 constraints.py

# Exercise 3
python3 exercise3.py

# Exercise 4
python3 exercise4.py

# Exercise 5
python3 exercise5.py
```

### Quick Verification
```bash
# Test all exercises in sequence
python3 -c "
import sys, io
old = sys.stdout; sys.stdout = io.StringIO()
from exercise3 import *
sys.stdout = old

x = PolynomialVar(p)
t = qM*a*b + qL*a + qR*b - c
f1 = a(x+1) - b(x)
f2 = b(x+1) - c(x)

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

## 📊 Exercise Overview

### Exercise 1: Constraint System
**File:** `constraints.py`

Implements the 5 constraints for computing F₄²:
1. Initial values: LI(1)=0, RI(1)=1
2. Addition gates: LI(i) + RI(i) = O(i) for i ∈ {1,2,3}
3. Wiring: Values propagate correctly between gates
4. Multiplication input: LI(4) = RI(4) = O(3)
5. Multiplication gate: LI(4) * RI(4) = O(4)

**Result:** Proves F₄² = 9 through circuit constraints

---

### Exercise 3: Polynomial Interpolation
**File:** `exercise3.py`

Interpolates witness and selector vectors as polynomials over F_p:
- **Witness polynomials:** a(x), b(x), c(x) from LI, RI, O
- **Selector polynomials:** qL(x), qR(x), qM(x) from SL, SR, SM

**Key Features:**
- Custom Polynomial class with full arithmetic in GF(p)
- Lagrange interpolation implementation
- Polynomial composition support for a(x+1), b(x+1)
- All polynomials are degree 3

**Verification:** a(i) = LI[i], b(i) = RI[i], c(i) = O[i] for all i ∈ I

---

### Exercise 4: Vanishing Polynomials
**File:** `exercise4.py`

Computes vanishing polynomials and quotients using polynomial division:

**Computed:**
- Z(x) = (x-1)(x-2)(x-3)(x-4) - degree 4
- Q(x) from t(x) = Q(x)·Z(x) - degree 5
- Z1(x) = (x-1)(x-2) - degree 2
- Q1(x) from f1(x) = Q1(x)·Z1(x) - degree 1
- Q2(x) from f2(x) = Q2(x)·Z1(x) - degree 1

**Key Insight:** Instead of checking t(i)=0 for each i, we check if Z(x) divides t(x), which is more efficient for large circuits.

---

### Exercise 5: Schwartz-Zippel Checks
**File:** `exercise5.py`

Probabilistic equality verification at random challenge points:

**Checks:**
1. t(42) = Q(42)·Z(42) → Gate constraints
2. f1(74102) = Q1(74102)·Z1(74102) → Wiring constraint 1
3. f2(987654321987654321) = Q2(...)·Z1(...) → Wiring constraint 2

**Security:** Error probability ≤ 9/(2²⁵⁴) ≈ 10⁻⁷⁵ (negligible!)

**Result:** All three checks pass, proving correct computation!

## 🎯 Key Concepts Demonstrated

### 1. Polynomial Arithmetic in Finite Fields
- All operations modulo prime p (BN254 curve order)
- Modular inverse for division: a⁻¹ = a^(p-2) mod p
- Efficient implementation without external libraries

### 2. Lagrange Interpolation
Transform discrete points into polynomial:
```
Given: (1,0), (2,1), (3,1), (4,3)
Output: a(x) with a(1)=0, a(2)=1, a(3)=1, a(4)=3
```

### 3. Polynomial Composition
Evaluate polynomial at another polynomial:
```
a(x+1) means: substitute (x+1) for x in a(x)
Returns a new polynomial, not a number!
```

### 4. Polynomial Division
Compute quotient and remainder:
```
t(x) = Q(x)·Z(x) + r(x)
If r(x)=0, then Z(x) divides t(x)
```

### 5. Schwartz-Zippel Lemma
Probabilistic polynomial equality:
```
If f(x) ≠ g(x) and deg(f-g) ≤ d,
then Pr[f(γ) = g(γ)] ≤ d/p
```

## 🔍 Troubleshooting

### ImportError: No module named 'py_ecc'
```bash
pip install py_ecc
```

### Jupyter kernel issues
If notebook still shows errors after fixes:
1. Kernel → Restart Kernel
2. Run all cells from beginning
3. Old class definitions are cached in memory

### Polynomial composition errors
Make sure you're using the fixed version of exercise3.py with:
- `__call__` method that handles both int and Polynomial arguments
- `__mul__` method that handles PolynomialVar objects
- `__eq__` method for proper polynomial equality

## 📈 Complexity Analysis

| Operation | Before Schwartz-Zippel | After Schwartz-Zippel |
|-----------|----------------------|---------------------|
| Gate check | O(n) evaluations | O(d) single evaluation |
| Wiring checks | O(n) evaluations | O(d) single evaluations |
| Polynomial multiply | O(d²) | Not needed! |
| Total verification | O(n + d²) | O(d) |

For larger circuits: **massive speedup!**

## 🎓 Learning Path

1. Start with **SCHWARTZ_ZIPPEL_EXPLAINED.md** for intuition
2. Run **constraints.py** to understand the circuit
3. Study **exercise3.py** for polynomial interpolation
4. Run **exercise4.py** to see vanishing polynomials
5. Complete with **exercise5.py** for probabilistic checks
6. Read summaries for deeper understanding

## ✅ Verification Checklist

- [x] All constraints satisfied (Exercise 1)
- [x] Polynomials interpolate correctly (Exercise 3)
- [x] Vanishing polynomials computed (Exercise 4)
- [x] Quotients exist with zero remainder (Exercise 4)
- [x] Schwartz-Zippel checks pass (Exercise 5)
- [x] Results match expected values
- [x] No SageMath dependencies!

## 🔗 Related Files

- **../PlonK-Tutorial.ipynb** - Main tutorial notebook (now SageMath-free!)
- **../kzg.py** - KZG polynomial commitments using py_ecc
- **../.gitignore** - Git ignore file for Python projects

## 📝 Notes

- All solutions use the BN254 elliptic curve (same as Ethereum)
- Field prime: p = 21888242871839275222246405745257275088548364400416034343698204186575808495617
- Polynomial degrees are small (≤9) for this example circuit
- Real PLONK circuits can have millions of gates!

---

**Created for the PlonK tutorial by zkSecurity**
**Refactored to remove SageMath dependencies**
**All solutions verified and tested ✓**
