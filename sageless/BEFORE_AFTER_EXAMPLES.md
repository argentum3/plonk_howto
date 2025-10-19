# Before/After Examples: SageMath to Python Refactoring

This document shows concrete examples of code transformations from SageMath to pure Python.

---

## Example 1: Polynomial Setup (Cell 10)

### BEFORE (SageMath)
```python
from sage.all import *

p = 21888242871839275222246405745257275088548364400416034343698204186575808495617
F = GF(p)
R.<x> = PolynomialRing(F, 'x')

# Create polynomials
qL = interpolate(I, list(SL.values()))
a = interpolate(I, list(LI.values()))
```

### AFTER (Python)
```python
import numpy as np
from functools import reduce
import random

p = 21888242871839275222246405745257275088548364400416034343698204186575808495617

class Polynomial:
    """Polynomial with coefficients in GF(p)"""
    def __init__(self, coeffs, modulus=p):
        self.modulus = modulus
        # ... (full implementation)

    def __call__(self, x):
        """Evaluate polynomial at x"""
        result = 0
        x_power = 1
        for coeff in self.coeffs:
            result = (result + coeff * x_power) % self.modulus
            x_power = (x_power * x) % self.modulus
        return result

    # ... more methods

x = PolynomialVar()

# Create polynomials (same API!)
qL = interpolate(I, list(SL.values()))
a = interpolate(I, list(LI.values()))
```

**Key Difference**: Instead of importing SageMath, we implement a custom `Polynomial` class that provides the same API.

---

## Example 2: Polynomial Arithmetic

### BEFORE (SageMath)
```python
# Polynomial operations
t = qM*a*b + qL*a + qR*b - c
Z = x^4 - 1
Q, R = t.quo_rem(Z)

# Check divisibility
if Z.divides(t):
    print("Divisible!")
```

### AFTER (Python)
```python
# Polynomial operations (same syntax!)
t = qM*a*b + qL*a + qR*b - c
Z = x**4 - 1
Q, R = t.quo_rem(Z)

# Check divisibility (same method!)
if Z.divides(t):
    print("Divisible!")
```

**Key Difference**: Syntax is nearly identical! Only change is `x^4` → `x**4` (Python exponentiation operator).

**Important Note**: For modular exponentiation with field elements (not polynomial variables), always use `pow(base, exp, p)` instead of `**` to ensure correct modular reduction and avoid overflow.

---

## Example 3: Polynomial Evaluation

### BEFORE (SageMath)
```python
# Evaluate polynomial at a point
for i in I:
    assert a(i) == LI[i]
    assert b(i) == RI[i]
```

### AFTER (Python)
```python
# Evaluate polynomial at a point (identical!)
for i in I:
    assert a(i) == LI[i]
    assert b(i) == RI[i]
```

**Key Difference**: None! The `__call__` method makes evaluation identical.

---

## Example 4: Lagrange Interpolation

### BEFORE (SageMath)
```python
def interpolate(I, Y):
    """Lagrange interpolation (SageMath builtin)"""
    # SageMath provides this automatically
    return lagrange_polynomial(zip(I, Y))
```

### AFTER (Python)
```python
def interpolate(I, Y):
    """Lagrange interpolation polynomial"""
    n = len(I)
    result = Polynomial([0], p)

    for i in range(n):
        # Build Lagrange basis L_i(x)
        numerator = Polynomial([1], p)
        denominator = 1

        for j in range(n):
            if i != j:
                numerator = numerator * (x - I[j]).poly
                denominator = (denominator * (I[i] - I[j])) % p

        # L_i(x) = numerator / denominator (mod p)
        denominator_inv = pow(denominator, p - 2, p)
        basis = numerator * denominator_inv
        result = result + (basis * Y[i])

    return result
```

**Key Difference**: We implement Lagrange interpolation manually, but it provides the same output.

---

## Example 5: Display Output

### BEFORE (SageMath)
```python
show("Q=", Q)
show("P:", P)
show(e(P,Q))
```

### AFTER (Python)
```python
print("Q=", Q)
print("P:", P)
print("e(P,Q):", e(P,Q))
```

**Key Difference**: `show()` → `print()`. The Polynomial `__repr__` method formats output nicely.

---

## Example 6: Elliptic Curve Pairing

### BEFORE (SageMath)
```python
def e(P, Q):
    q = 21888242871839275222246405745257275088696311157297823662689037894645226208583
    n = Integer(21888242871839275222246405745257275088548364400416034343698204186575808495617)
    k = 12
    t = 6*pow(4965661367192848881, 2) + 1
    return P.ate_pairing(Q, n, k, t, q)
```

### AFTER (Python)
```python
from py_ecc.bn128 import pairing

def e(P, Q):
    """
    Compute pairing using py_ecc library
    Note: py_ecc expects (G2, G1) order
    """
    return pairing(Q, P)
```

**Key Difference**: Use py_ecc library instead of SageMath's ate_pairing. Much simpler!

---

## Example 7: Product Function

### BEFORE (SageMath)
```python
# SageMath has built-in prod()
L1 = prod((x - ω**m)//(ω - ω**m) for m in range(2, n+1))
```

### AFTER (Python)
```python
# Custom prod() using functools.reduce
from functools import reduce

def prod(iterable):
    """Product of all elements"""
    return reduce(lambda a, b: a * b, iterable, 1)

L1 = prod((x - ω**m)//(ω - ω**m) for m in range(2, n+1))
```

**Key Difference**: Define custom `prod()`, but usage is identical.

---

## Example 8: Random Polynomial

### BEFORE (SageMath)
```python
k = 2
p = R.random_element(degree=k-1)
print("p(x) =", p)
```

### AFTER (Python)
```python
def random_polynomial(degree, modulus=p):
    """Generate random polynomial of given degree"""
    coeffs = [random.randint(0, modulus - 1) for _ in range(degree + 1)]
    return Polynomial(coeffs, modulus)

k = 2
p_poly = random_polynomial(degree=k-1, modulus=p)
print("p(x) =", p_poly)
```

**Key Difference**: Custom `random_polynomial()` function instead of SageMath method.

---

## Example 9: Polynomial Division

### BEFORE (SageMath)
```python
# Division with remainder
quotient, remainder = f.quo_rem(g)

# Floor division
q = f // g

# Check divisibility
if g.divides(f):
    print("g divides f")
```

### AFTER (Python)
```python
# Division with remainder (same!)
quotient, remainder = f.quo_rem(g)

# Floor division (same!)
q = f // g

# Check divisibility (same!)
if g.divides(f):
    print("g divides f")
```

**Key Difference**: None! Our Polynomial class implements the same methods.

---

## Example 10: Integer Type Conversion

### BEFORE (SageMath)
```python
s = Integer(randrange(1, p))
n = Integer(21888242871839275222246405745257275088548364400416034343698204186575808495617)
```

### AFTER (Python)
```python
s = int(randrange(1, p))
n = 21888242871839275222246405745257275088548364400416034343698204186575808495617
```

**Key Difference**: `Integer()` → `int()` (or just use the literal directly).

---

## Summary of Changes

| SageMath Construct | Python Equivalent | Difficulty |
|-------------------|-------------------|------------|
| `GF(p)` | Modular arithmetic with `% p` | Easy |
| `R.<x> = PolynomialRing(F, 'x')` | `x = PolynomialVar()` | Medium |
| `x^n` (polynomial var) | `x**n` | Trivial |
| `a^n` (field element) | `pow(a, n, p)` | Easy |
| `show()` | `print()` | Trivial |
| `Integer()` | `int()` | Trivial |
| `prod()` | `functools.reduce(...)` | Easy |
| `.quo_rem()` | Custom implementation | Hard |
| `.divides()` | Custom implementation | Medium |
| `.random_element()` | Custom function | Easy |
| `ate_pairing()` | `py_ecc.bn128.pairing()` | Medium |

---

## Example 11: Modular Exponentiation (Critical for Finite Fields)

### BEFORE (SageMath)
```python
# SageMath automatically handles modular arithmetic in GF(p)
F = GF(p)
ω = F(some_value)
result = ω^n  # Automatically computed in GF(p)
ZH_z = zeta_v^n - 1
```

### AFTER (Python)
```python
# Must explicitly use pow() for modular exponentiation
ω = some_value
result = pow(ω, n, p)  # Efficient modular exponentiation
ZH_z = (pow(zeta_v, n, p) - 1) % p

# WRONG - causes overflow and incorrect results:
# result = (ω ** n) % p  # Don't do this!
# ZH_z = zeta_v**n - 1   # Don't do this!
```

**Key Difference**: `pow(base, exp, p)` is critical for field element exponentiation.

**Why This Matters**:
- `pow(ω, n, p)` computes `(ω^n) mod p` efficiently using modular exponentiation
- `(ω ** n) % p` first computes huge intermediate value, then reduces (slow and can overflow)
- Without `% p`, values can become 150+ digits and break verification
- This was the **most critical bug** we fixed in verify_plonk

**When to Use Each**:
- **Polynomial variables** (`x`): Use `x**n` (handled by Polynomial class)
- **Field elements** (integers mod p): Use `pow(base, n, p)`
- **Small constants**: Either works, but `pow()` is more consistent

---

## Performance Notes

The Python implementation should have similar performance to SageMath for most operations:

- **Polynomial arithmetic**: Comparable (both use Python integers with modular arithmetic)
- **Pairing operations**: Comparable or better (py_ecc is optimized)
- **Startup time**: Much faster (no SageMath overhead)
- **Memory usage**: Lower (no SageMath runtime)

---

## Compatibility Notes

The refactored code maintains **API compatibility** with the original SageMath version:

✓ Same function names
✓ Same method names
✓ Same operator overloading
✓ Same evaluation syntax
✓ Same polynomial representation

This means that most of the tutorial code remains **unchanged** after refactoring!
