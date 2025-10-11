# Exercise 18: Blinding Polynomials for Zero-Knowledge

## Overview

This exercise implements **polynomial blinding** to achieve zero-knowledge properties in PlonK. By adding random multiples of the vanishing polynomial, we hide witness values from potentially malicious verifiers while preserving all polynomial constraints.

## The Zero-Knowledge Problem

Even with a sound proof system, a malicious verifier could:
- Choose adaptive off-domain evaluation points
- Collude across multiple proof instances
- Extract intermediate witness values or private inputs

**Solution:** Blind the polynomials to hide sensitive information!

## Blinding via Vanishing Polynomial Multiples

### Formula

$$f_{\text{blind}}(x) = f(x) + p(x) \cdot ZH(x)$$

Where:
- **f(x)**: Original polynomial (witness or accumulator)
- **p(x)**: Random polynomial of degree k-1
- **ZH(x) = x^n - 1**: Vanishing polynomial for domain Ω
- **k**: Maximum number of openings (queries)

### Key Property

$$f_{\text{blind}}(\omega^i) = f(\omega^i) \text{ for all } \omega^i \in \Omega$$

**Why?** Because $ZH(\omega^i) = (\omega^i)^n - 1 = 1 - 1 = 0$ for all $\omega^i$ in the domain!

### Security Intuition

- **At domain points:** Blinded polynomial = original polynomial (preserves correctness)
- **Everywhere else:** Blinded polynomial is randomized (hides information)
- **Verifier only evaluates at domain points** → Cannot learn witness values
- **Random p(x) changes each proof** → No information leakage across proofs

## Exercise 18 Tasks

### 1. Blind witness polynomials b and c

Following the pattern from cell 81 where a was blinded:

```python
k = 2  # At most 2 openings

# Blind b(x)
p_b = random_polynomial(degree=k-1, modulus=p)
b_blind = b + p_b * ZH

# Blind c(x)
p_c = random_polynomial(degree=k-1, modulus=p)
c_blind = c + p_c * ZH
```

### 2. Interpolate z, N, D with blinded polynomials

Use the blinded witness polynomials in the interpolation:

```python
beta = gamma = 42
z_poly, N_poly, D_poly = interpolate_z_N_D(a_blind, b_blind, c_blind, beta, gamma, Ω)
```

**Note:** N_poly and D_poly are computed from blinded witnesses but are not themselves blinded.

### 3. Blind the z polynomial

The accumulator z also needs blinding:

```python
p_z = random_polynomial(degree=k-1, modulus=p)
z_poly_blind = z_poly + p_z * ZH
```

## Implementation

```python
def random_polynomial(degree, modulus):
    """Generate a random polynomial of given degree"""
    coeffs = [random.randint(0, modulus - 1) for _ in range(degree + 1)]
    return Polynomial(coeffs, modulus)

# Blinding parameters
k = 2  # Max openings
beta = gamma = 42

# Blind witness polynomials
b_blind = b + random_polynomial(degree=k-1, modulus=p) * ZH
c_blind = c + random_polynomial(degree=k-1, modulus=p) * ZH

# Interpolate with blinded polynomials
z_poly, N_poly, D_poly = interpolate_z_N_D(a_blind, b_blind, c_blind, beta, gamma, Ω)

# Blind z polynomial
z_poly_blind = z_poly + random_polynomial(degree=k-1, modulus=p) * ZH
```

## Validation

The constraint check from cell 85 must still pass:

```python
assert ZH.divides(z_poly_blind * N_poly - D_poly * z_poly_blind(x*ω)) == True
```

This works because:
1. At domain points Ω, blinded and unblinded polynomials are equal
2. The recursive constraint is evaluated at domain points
3. Therefore, blinding doesn't affect the constraint satisfaction

## Degree Analysis

### Before Blinding
```
deg(a) = 3
deg(b) = 3
deg(c) = 3
deg(z_poly) = 3
```

### After Blinding (k=2)
```
deg(a_blind) = deg(a) + deg(ZH) + deg(p) = 3 + 4 + 1 = 5
deg(b_blind) = 5
deg(c_blind) = 5
deg(z_poly_blind) = 5
```

**General formula:** $\text{deg}(f_{\text{blind}}) = \text{deg}(f) + n + (k-1)$

Where:
- deg(f): Original polynomial degree
- n: Domain size
- k-1: Degree of random blinding polynomial

## Security Guarantees

### What Does Blinding Protect?

✅ **Witness values** (a, b, c values) are hidden
✅ **Intermediate computations** cannot be extracted
✅ **Cross-proof correlations** are eliminated (fresh randomness each time)
✅ **Private inputs** remain confidential

### What Is NOT Hidden?

- Circuit structure (public)
- Public inputs/outputs (intentionally public)
- Polynomial degrees (bounded by protocol)

## Example Output

```
======================================================================
BLINDING WITNESS POLYNOMIALS
======================================================================

1. Blinding a(x):
   deg(a) = 3, deg(a_blind) = 5

2. Blinding b(x):
   deg(b) = 3, deg(b_blind) = 5

3. Blinding c(x):
   deg(c) = 3, deg(c_blind) = 5

✓ All blinded polynomials match originals at domain points Ω

======================================================================
BLINDING z POLYNOMIAL
======================================================================

Blinding z_poly (assuming at most k=2 openings):
   deg(z_poly) = 3, deg(z_poly_blind) = 5

✓ z_poly_blind matches z_poly at all domain points

======================================================================
VALIDATION CHECK
======================================================================

Checking: ZH divides z_poly_blind*N_poly - D_poly*z_poly_blind(x*ω)
  ✓ PASS: Recursive constraint still satisfied with blinded polynomials!
```

## Running the Exercise

```bash
# From repo root
./run.sh sageless/solutions/exercise18/exercise18.py

# Or with venv activated
cd sageless/solutions/exercise18
./exercise18.py
```

## Why This Achieves Zero-Knowledge

### The Simulator Test

A proof system is zero-knowledge if a simulator can generate "fake" proofs that are indistinguishable from real proofs, without knowing the witness.

With blinding:
- **Simulator** can choose random p(x) polynomials
- Creates blinded polynomials that satisfy all constraints
- Indistinguishable from real prover's blinded polynomials
- Therefore: No information leakage! ✓

### Intuitive Security

Think of blinding as "adding noise":
- Original polynomial: Signal
- Random multiple of ZH: Noise
- At evaluation points in Ω: Noise cancels out (ZH = 0)
- Everywhere else: Signal buried in noise

**Result:** Verifier gets correct answers at domain points but learns nothing about the polynomial's "shape" between those points.

## Connection to Full PlonK Protocol

In the complete PlonK protocol:
1. **Prover blinds** witness polynomials (a, b, c)
2. **Prover blinds** accumulator (z)
3. **Prover commits** to blinded polynomials using KZG
4. **Verifier challenges** with random points
5. **Prover opens** at challenged points
6. **Verifier checks** polynomial identities

Blinding ensures step 5 (opening) reveals no sensitive information!

---

**PlonK Tutorial - Exercise 18**
**Polynomial blinding for zero-knowledge ✓**
