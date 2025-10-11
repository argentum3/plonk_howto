# Exercise 13: Verifying Exact Division - Zero Remainder

## Overview

This exercise verifies that the gate constraint polynomial t(x) is **exactly divisible** by the vanishing polynomial Z(x), with **zero remainder**. This is a crucial verification step in the PlonK protocol.

## The Division

We need to verify:
```
t(x) = Q(x) · Z(x) + R(x)
```

Where:
- **t(x) = qM·a·b + qL·a + qR·b - c** (gate constraint polynomial)
- **Z(x) = x^4 - 1** (vanishing polynomial for Ω)
- **Q(x)** is the quotient
- **R(x)** is the remainder

**Goal:** Prove that **R(x) = 0** (exact division)

## Why This Matters

### Efficiency Advantage:

**Before (naive approach):**
- Check t(ω^1) = 0
- Check t(ω^2) = 0
- Check t(ω^3) = 0
- Check t(ω^4) = 0
→ **4 evaluations** (O(n) for n gates)

**Now (with vanishing polynomial):**
- Compute t(x) ÷ Z(x)
- Check if remainder R(x) = 0
→ **1 division** (O(1) for the check, though division itself is O(n²))

For large circuits with thousands of gates, this approach is more amenable to further optimizations using FFT.

### Mathematical Insight:

If **R(x) = 0**, then:
```
t(x) = Q(x) · Z(x)
```

Since **Z(ω^i) = 0** for all ω^i ∈ Ω, we have:
```
t(ω^i) = Q(ω^i) · Z(ω^i) = Q(ω^i) · 0 = 0
```

This proves all constraints are satisfied!

## Implementation

```python
# Gate constraint polynomial
t = qM*a*b + qL*a + qR*b - c

# Vanishing polynomial (constant time!)
Z = (x * x * x * x) - 1  # x^4 - 1

# Perform division
Quo, Rem = t.quo_rem(Z)

# Verify remainder is zero
assert Rem == 0
```

## Results

### Gate Constraint Polynomial:
```
t(x) = qM(x)·a(x)·b(x) + qL(x)·a(x) + qR(x)·b(x) - c(x)
Degree: 9
```

This combines both addition and multiplication gates:
- **Multiplication gates**: qM·a·b
- **Addition gates**: qL·a + qR·b - c

### Vanishing Polynomial:
```
Z(x) = x^4 - 1
Degree: 4
Coefficients: [-1, 0, 0, 0, 1]
```

Much simpler than Z(x) = (x-ω)(x-ω^2)(x-ω^3)(x-1)!

### Division Result:
```
Quotient Q(x) degree: 5
Remainder R(x): 0

✓ Division is EXACT!
```

## Verification Steps

### 1. Verify Z(x) vanishes on Ω:
```
Z(ω^1) = 0 ✓
Z(ω^2) = 0 ✓
Z(ω^3) = 0 ✓
Z(ω^4) = 0 ✓
```

### 2. Verify t(x) vanishes on Ω:
```
Gate 1: t(ω^1) = 0 ✓  →  0·0·1 + 1·0 + 1·1 - 1 = 0
Gate 2: t(ω^2) = 0 ✓  →  0·1·1 + 1·1 + 1·1 - 2 = 0
Gate 3: t(ω^3) = 0 ✓  →  0·1·2 + 1·1 + 1·2 - 3 = 0
Gate 4: t(ω^4) = 0 ✓  →  1·3·3 + 0·3 + 0·3 - 9 = 0
```

All gate constraints satisfied!

### 3. Verify remainder is zero:
```
Remainder R(x) = 0 ✓
```

### 4. Verify reconstruction:
```
t(x) = Q(x) · Z(x) ✓
```

## Key Insights

### 1. Constant-Time Vanishing Polynomial

With multiplicative domain:
```
Z(x) = x^n - 1
```

This is computed in **O(1)** time, versus O(n) for the additive approach.

### 2. Single Check Instead of Many

Instead of checking n individual constraints, we:
1. Compute one polynomial t(x)
2. Perform one division t(x) ÷ Z(x)
3. Check one condition: R(x) = 0

### 3. Foundation for ZK-SNARKs

This exact division property is fundamental to:
- **PlonK**: Polynomial commitments and verification
- **Groth16**: QAP divisibility
- **Other SNARKs**: Polynomial-based proofs

## Running the Exercise

```bash
# From repository root
./run.sh sageless/solutions/exercise13/exercise13.py

# Or from solutions directory
cd sageless/solutions
../../run.sh exercise13/exercise13.py
```

## Expected Output

```
======================================================================
VERIFICATION: IS REMAINDER ZERO?
======================================================================

Remainder R(x) = 0

Is remainder zero? True

✓ SUCCESS! The division is EXACT

  This proves:
    t(x) = Q(x) · Z(x)

  Since Z(x) divides t(x) exactly, and Z(ω^i) = 0 for all ω^i ∈ Ω,
  we have confirmed that t(ω^i) = 0 for all domain points.

  ✓ All gate constraints are satisfied!

======================================================================
VERIFICATION: RECONSTRUCT t(x) FROM Q(x) AND Z(x)
======================================================================

Reconstruction:
  t(x) = Q(x) · Z(x)

Do they match? True
✓ Reconstruction successful!
```

## Mathematical Proof

**Theorem:** If all constraints are satisfied, then Z(x) divides t(x).

**Proof:**
1. The constraints are satisfied ⟺ t(ω^i) = 0 for all ω^i ∈ Ω
2. If t(ω^i) = 0 for all ω^i ∈ Ω, then (x - ω^i) divides t(x) for each i
3. Since the (x - ω^i) are pairwise coprime, their product Z(x) = ∏(x - ω^i) divides t(x)
4. For multiplicative domain: Z(x) = x^n - 1 = ∏(x - ω^i)
5. Therefore: t(x) = Q(x) · Z(x) for some polynomial Q(x)
6. The remainder R(x) = 0 ✓

## Next Steps

This exact division property will be used in subsequent exercises to:
- Generate quotient polynomials efficiently
- Create ZK proofs using polynomial commitments
- Verify constraints without revealing witness values
- Build the complete PlonK protocol

## Files

- `exercise13.py` - Complete implementation with verification
- `README.md` - This file
- `../../PlonK-Tutorial.ipynb` - Cell 51 contains the solution

## Key Takeaways

✓ t(x) = Q(x) · Z(x) with zero remainder
✓ All gate constraints satisfied at every domain point
✓ Multiplicative domain enables Z(x) = x^n - 1 (constant time)
✓ Single division check replaces n individual checks
✓ Foundation for efficient ZK-SNARK protocols

---

**PlonK Tutorial by zkSecurity**
