# Exercise 12: Polynomial Interpolation over Multiplicative Domain

## Overview

This exercise re-interpolates the witness polynomials (a, b, c) and selector polynomials (qL, qR, qM) over the **multiplicative domain Ω** instead of the additive indices I.

This is a key step in transitioning to more efficient polynomial operations used in modern ZK-SNARKs like PlonK.

## The Change

### Before (Exercises 1-10):
```python
I = [1, 2, 3, 4]  # Additive indices
a = interpolate(I, list(LI.values()))
# a(1) = LI[1], a(2) = LI[2], a(3) = LI[3], a(4) = LI[4]
```

### Now (Exercise 12):
```python
Ω = [ω, ω^2, ω^3, ω^4]  # Multiplicative domain (roots of unity)
a = interpolate(Ω, list(LI.values()))
# a(ω) = LI[1], a(ω^2) = LI[2], a(ω^3) = LI[3], a(ω^4) = LI[4]
```

## Domain Mapping

The circuit has 4 gates, now mapped to multiplicative domain:

| Gate | Old Domain (I) | New Domain (Ω) | Witness Values |
|------|---------------|----------------|----------------|
| 1    | 1             | ω              | LI[1]=0, RI[1]=1, O[1]=1 |
| 2    | 2             | ω^2            | LI[2]=1, RI[2]=1, O[2]=2 |
| 3    | 3             | ω^3            | LI[3]=1, RI[3]=2, O[3]=3 |
| 4    | 4             | ω^4 = 1        | LI[4]=3, RI[4]=3, O[4]=9 |

## Value Vectors

### Witness Vectors (Circuit Execution):
```python
LI = {1: 0, 2: 1, 3: 1, 4: 3}  # Left inputs
RI = {1: 1, 2: 1, 3: 2, 4: 3}  # Right inputs
O  = {1: 1, 2: 2, 3: 3, 4: 9}  # Outputs
```

Representing:
- Gate 1: 0 + 1 = 1 (addition)
- Gate 2: 1 + 1 = 2 (addition)
- Gate 3: 1 + 2 = 3 (addition)
- Gate 4: 3 × 3 = 9 (multiplication)

### Selector Vectors (Gate Types):
```python
SL = {1: 1, 2: 1, 3: 1, 4: 0}  # Left addition selector
SR = {1: 1, 2: 1, 3: 1, 4: 0}  # Right addition selector
SM = {1: 0, 2: 0, 3: 0, 4: 1}  # Multiplication selector
```

## Interpolated Polynomials

### Witness Polynomials:
```python
a = interpolate(Ω, [0, 1, 1, 3])  # Left inputs
b = interpolate(Ω, [1, 1, 2, 3])  # Right inputs
c = interpolate(Ω, [1, 2, 3, 9])  # Outputs
```

All have degree 3 (one less than domain size 4).

### Selector Polynomials:
```python
qL = interpolate(Ω, [1, 1, 1, 0])  # Addition left selector
qR = interpolate(Ω, [1, 1, 1, 0])  # Addition right selector
qM = interpolate(Ω, [0, 0, 0, 1])  # Multiplication selector
```

All have degree 3.

## Verification

### Evaluation Verification

The script verifies that the interpolated polynomials evaluate correctly at all domain points:

```
Witness polynomials (a, b, c):
  i  | Domain Point | a(ω^i) = LI[i] | b(ω^i) = RI[i] | c(ω^i) = O[i]
  ---------------------------------------------------------------------------
  1  | ω^1          |    0 =    0 ✓ |    1 =    1 ✓ |    1 =    1 ✓
  2  | ω^2          |    1 =    1 ✓ |    1 =    1 ✓ |    2 =    2 ✓
  3  | ω^3          |    1 =    1 ✓ |    2 =    2 ✓ |    3 =    3 ✓
  4  | ω^4          |    3 =    3 ✓ |    3 =    3 ✓ |    9 =    9 ✓

Selector polynomials (qL, qR, qM):
  i  | qL(ω^i) = SL[i] | qR(ω^i) = SR[i] | qM(ω^i) = SM[i]
  ------------------------------------------------------------
  1  |    1 =    1 ✓   |    1 =    1 ✓   |    0 =    0 ✓
  2  |    1 =    1 ✓   |    1 =    1 ✓   |    0 =    0 ✓
  3  |    1 =    1 ✓   |    1 =    1 ✓   |    0 =    0 ✓
  4  |    0 =    0 ✓   |    0 =    0 ✓   |    1 =    1 ✓
```

✓ All polynomial evaluations match expected values!

### Coefficient Validation

The script also validates that the exact coefficients match the expected values from the tutorial.

**Expected coefficients for a(x) over Ω:**
```
a(x) = 16416182153879456417786784551517017277046601793284012108757927423286461067892 * x^3
     + 5472060717959818805561601436314318772137091100104008585924551046643952123905 * x^2
     + 5472060717959818804459621193740257811501762607132022234940276763289347427726 * x
     + 16416182153879456416684804308942956316411273300312025757773653139931856371714
```

**Validation result:**
```
Coefficient comparison:
  x^0: ✓
  x^1: ✓
  x^2: ✓
  x^3: ✓

✓ All coefficients match expected values!
```

This confirms our interpolation is producing exactly the correct polynomial for the multiplicative domain.

## Key Insight: Different Polynomials, Same Values

The polynomials interpolated over Ω have **different coefficients** than those over I, but they encode the **same witness values** at the corresponding domain points.

Example with polynomial a(x):

**Over additive domain I = [1, 2, 3, 4]:**
```python
a.coeffs = [21888242871839275222246405745257275088548364400416034343698204186575808495612,
            8,
            10944121435919637611123202872628637544274182200208017171849102093287904247805,
            10944121435919637611123202872628637544274182200208017171849102093287904247809]
```

**Over multiplicative domain Ω = [ω, ω^2, ω^3, 1]:**
```python
a.coeffs = [16416182153879456416684804308942956316411273300312025757773653139931856371714,
            5472060717959818804459621193740257811501762607132022234940276763289347427726,
            5472060717959818805561601436314318772137091100104008585924551046643952123905,
            16416182153879456417786784551517017277046601793284012108757927423286461067892]
```

→ **Different polynomials**, but a(ω) = 0, a(ω^2) = 1, a(ω^3) = 1, a(1) = 3 ✓

## Why Use Multiplicative Domain?

### Advantages:

1. **Constant-time Vanishing Polynomial:**
   - Additive: Z(x) = (x-1)(x-2)(x-3)(x-4) requires O(n) operations
   - Multiplicative: Z(x) = x^4 - 1 computed in O(1) time!

2. **FFT/NTT Compatibility:**
   - Roots of unity enable Fast Fourier Transform
   - O(n log n) polynomial evaluation/interpolation instead of O(n^2)

3. **Cleaner Math:**
   - All elements satisfy (ω^i)^n = 1
   - Better algebraic structure for proofs

4. **Standard in ZK-SNARKs:**
   - PlonK, Groth16, and others use multiplicative domains
   - Essential for efficient polynomial commitments

## Running the Exercise

```bash
# From repository root
./run.sh sageless/solutions/exercise12/exercise12.py

# Or from solutions directory
cd sageless/solutions
../../run.sh exercise12/exercise12.py
```

## Expected Output

```
======================================================================
EXERCISE 12: INTERPOLATION OVER MULTIPLICATIVE DOMAIN
======================================================================

Step 1: Computing generator ω and domain Ω...
  Generator: ω = 21888242871839275217838484774961031246007050428528088939761107053157389710902

Domain Ω = {ω, ω^2, ω^3, ω^4}
    ω^1 = 21888242871839275217838484774961031246007050428528088939761107053157389710902
    ω^2 = 21888242871839275222246405745257275088548364400416034343698204186575808495616
    ω^3 = 4407920970296243842541313971887945403937097133418418784715
    ω^4 = 1

✓ Interpolated a(x) with degree 3
✓ Interpolated b(x) with degree 3
✓ Interpolated c(x) with degree 3
✓ Interpolated qL(x) with degree 3
✓ Interpolated qR(x) with degree 3
✓ Interpolated qM(x) with degree 3

✓ All polynomial evaluations match expected values!
```

## Next Steps

These polynomials over Ω will be used in subsequent exercises to:
- Check constraints using the vanishing polynomial Z(x) = x^4 - 1
- Compute quotient polynomials efficiently
- Prepare for PlonK's permutation argument
- Leverage FFT for faster operations

## Files

- `exercise12.py` - Complete implementation with verification
- `README.md` - This file
- `../../PlonK-Tutorial.ipynb` - Cell 49 contains the solution

## Key Takeaways

✓ Successfully interpolated all 6 polynomials over multiplicative domain Ω
✓ Domain mapping: Gate i → ω^i
✓ Same witness values, different polynomial coefficients
✓ Ready to use Z(x) = x^4 - 1 for efficient vanishing polynomial
✓ Foundation for FFT-based polynomial operations

---

**PlonK Tutorial by zkSecurity**
