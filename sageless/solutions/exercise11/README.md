# Exercise 11: Finding a Generator of a Multiplicative Subgroup

## Overview

This exercise finds a **generator ω** of a multiplicative domain of order 4. This domain will replace the additive indices I = {1, 2, 3, 4} used in previous exercises, providing better efficiency for polynomial operations.

## Problem Statement

Find a generator ω such that:
- **ω^4 = 1** (ω is a 4th root of unity)
- **ω^i ≠ 1** for i ∈ {1, 2, 3} (order is EXACTLY 4, not a divisor)

The domain will be: **Ω = {ω, ω^2, ω^3, ω^4=1}**

## Algorithm

### Step 1: Compute r = (p-1)/4
```python
r = (p - 1) // 4
```

Since the multiplicative group F_p* has order p-1, and we want an element of order 4, we use:
- By Lagrange's theorem: h^(p-1) = 1 for all h ≠ 0
- If ω = h^r where r = (p-1)/4, then ω^4 = h^(p-1) = 1

### Step 2: Find smallest h such that ω = h^r has order 4
```python
h = 1
while h < p:
    ω = pow(h, r, p)
    if has_order_4(ω, p):
        break
    h += 1
```

### Step 3: Verify order is exactly 4
```python
def has_order_4(omega, modulus):
    # ω^4 = 1 (is a 4th root of unity)
    if pow(omega, 4, modulus) != 1:
        return False

    # ω^i ≠ 1 for i ∈ {1, 2, 3}
    for i in [1, 2, 3]:
        if pow(omega, i, modulus) == 1:
            return False

    return True
```

## Results

### Found Generator:
```
h = 5
ω = 21888242871839275217838484774961031246007050428528088939761107053157389710902
```

### Powers of ω:
```
ω^1 = 21888242871839275217838484774961031246007050428528088939761107053157389710902  ≠ 1
ω^2 = 21888242871839275222246405745257275088548364400416034343698204186575808495616  ≠ 1
ω^3 = 4407920970296243842541313971887945403937097133418418784715                     ≠ 1
ω^4 = 1                                                                               = 1 ✓
```

### The Domain:
```
Ω = {ω, ω^2, ω^3, 1}
```

All four elements are distinct, and ω^4 = 1, confirming ω has multiplicative order 4.

## Why Multiplicative Domains?

### Advantages over Additive Indices:

1. **Constant-Time Vanishing Polynomial:**
   - Additive (I = {1, 2, 3, 4}): Z(x) = (x-1)(x-2)(x-3)(x-4) — requires O(n) multiplications
   - Multiplicative (Ω): Z(x) = x^4 - 1 — computed in O(1) time!

2. **Mathematical Properties:**
   - Each element ω^i is an n-th root of unity: (ω^i)^n = 1
   - Closed under multiplication within the domain
   - Better structure for FFT/NTT operations

3. **Efficiency:**
   - No need to multiply (x - ωⁱ) for each element
   - Faster polynomial evaluation and interpolation
   - More efficient quotient polynomial computation

4. **Scalability:**
   - Works for domains of size n = 2^k (power of 2)
   - Standard in ZK-SNARKs and other cryptographic protocols

## Vanishing Polynomial

For a multiplicative domain of order n:

```
Z(x) = x^n - 1
```

For our domain of order 4:
```
Z(x) = x^4 - 1
```

Verification that Z(ω^i) = 0 for all i:
```
Z(ω^1) = (ω^1)^4 - 1 = 1 - 1 = 0 ✓
Z(ω^2) = (ω^2)^4 - 1 = 1 - 1 = 0 ✓
Z(ω^3) = (ω^3)^4 - 1 = 1 - 1 = 0 ✓
Z(ω^4) = (ω^4)^4 - 1 = 1 - 1 = 0 ✓
```

## Mathematical Background

### Roots of Unity

An **n-th root of unity** is a complex (or field) element α such that α^n = 1.

A **primitive n-th root of unity** is an element ω such that:
- ω^n = 1
- ω^k ≠ 1 for all 0 < k < n

In our case, ω is a primitive 4th root of unity.

### Why r = (p-1)/4 Works

The multiplicative group F_p* = {1, 2, ..., p-1} has order p-1.

By **Fermat's Little Theorem**: h^(p-1) ≡ 1 (mod p) for all h ≠ 0.

If we set r = (p-1)/4 and ω = h^r, then:
```
ω^4 = (h^r)^4 = h^(4r) = h^(p-1) = 1
```

So ω^4 = 1 is guaranteed. However, not every h gives an ω of order exactly 4:
- If h = 1, then ω = 1^r = 1, which has order 1 (fails!)
- If ω^2 = 1, then ω has order 2, not 4 (fails!)

We search for the smallest h that gives ω with order exactly 4.

## Running the Exercise

```bash
# From repository root
./run.sh sageless/solutions/exercise11/exercise11.py

# Or from solutions directory
cd sageless/solutions
../../run.sh exercise11/exercise11.py
```

## Expected Output

```
======================================================================
EXERCISE 11: FINDING A GENERATOR OF ORDER 4
======================================================================

Step 1: Compute r = (p-1)/4
  r = 5472060717959818805561601436314318772137091100104008585924551046643952123904
  ✓ Verified: 4 divides (p-1)

Step 2: Find smallest h such that ω = h^r has multiplicative order 4
  ✓ Found h = 5
    ω = 21888242871839275217838484774961031246007050428528088939761107053157389710902

======================================================================
✓ SUCCESS! ω has multiplicative order 4
======================================================================

Domain Ω = {ω, ω^2, ω^3, 1}
Vanishing polynomial: Z(x) = x^4 - 1
```

## Next Steps

This generator ω and domain Ω will be used in subsequent exercises to:
- Re-interpolate polynomials using multiplicative domain
- Compute vanishing polynomials efficiently
- Improve constraint checking
- Prepare for PlonK's permutation argument

The multiplicative domain is a key optimization in modern ZK-SNARKs!

## Files

- `exercise11.py` - Complete implementation with verification
- `README.md` - This file
- `../../PlonK-Tutorial.ipynb` - Cell 46 contains the solution

## Key Takeaways

✓ Found generator ω of order 4 using h = 5
✓ Domain Ω = {ω, ω^2, ω^3, 1} has 4 distinct elements
✓ Vanishing polynomial Z(x) = x^4 - 1 (constant time!)
✓ Much more efficient than additive indices
✓ Foundation for FFT/NTT and modern ZK-SNARKs

---

**PlonK Tutorial by zkSecurity**
