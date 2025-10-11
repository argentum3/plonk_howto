# Exercise 15: Numerator and Denominator for Grand Product Argument

## Overview

This exercise implements the **numerator** and **denominator** functions used in PlonK's **grand product argument** for verifying copy constraints (permutation checks).

## The Grand Product Argument

### Motivation

We need to verify that the permutation σ correctly encodes copy constraints:

**Property to check:** ∀i: f(i) = f(σ(i))

where f represents the wire values in the circuit.

### Hash-Based Intuition

Consider a cryptographic hash function h. If we compute:

$$GP = \prod_{i=1}^n \frac{h(i, f(i))}{h(i, f(\sigma(i)))}$$

Then GP = 1 if and only if f(σ(i)) = f(i) for all i.

### Key Observation

We can rewrite this as:

$$GP = \prod_{i=1}^n \frac{h(i, f(i))}{h(\sigma(i), f(i))}$$

This avoids polynomial composition f(σ(i)) which is expensive!

### Efficient "Hash" Function

Instead of a cryptographic hash, we use:

$$h(i, f(i)) = i + \beta \cdot f(i) + \gamma$$

where β and γ are random challenges. By Schwartz-Zippel lemma, this behaves like a hash function with high probability.

## Formulas

### Numerator

$$\text{numerator}(i, \text{column}, f, \sigma, \beta, \gamma) = \text{pos}(\text{column}, i) + \beta \cdot f(\omega^i) + \gamma$$

### Denominator

$$\text{denominator}(i, \text{column}, f, \sigma, \beta, \gamma) = \sigma(\text{pos}(\text{column}, i)) + \beta \cdot f(\omega^i) + \gamma$$

### Parameters

- **i**: Gate index (can be > n since ω has finite order)
- **column**: Column number (1=a, 2=b, 3=c)
- **f**: Polynomial for this column
- **σ**: Permutation encoding copy constraints
- **β, γ**: Random challenges from verifier
- **ω**: Generator of multiplicative domain

### Position Function

```python
pos(column, i) = (column - 1) * n + i
```

Maps (column, gate index) to global position [1..12].

## Implementation

```python
def numerator(i, column, f, sigma, beta, gamma):
    position = pos(column, i)
    ω_to_i = pow(ω, i, p)
    f_of_ω_i = f(ω_to_i)
    value = (position + beta * f_of_ω_i + gamma) % p
    return value

def denominator(i, column, f, sigma, beta, gamma):
    position = pos(column, i)
    sigma_position = sigma[position]
    ω_to_i = pow(ω, i, p)
    f_of_ω_i = f(ω_to_i)
    value = (sigma_position + beta * f_of_ω_i + gamma) % p
    return value
```

## Key Differences

| Function | Uses | Meaning |
|----------|------|---------|
| **numerator** | pos(column, i) | Original position |
| **denominator** | σ(pos(column, i)) | Where position maps to in permutation |

Both evaluate the **same** polynomial value f(ω^i), but use different position identifiers.

## Example

With β=42, γ=42:

### Test 1: Position 3 (a[3])

```
numerator(3, 1, a, σ, 42, 42):
  pos(1, 3) = 3
  a(ω³) = 1
  Result: 3 + 42·1 + 42 = 87

denominator(3, 1, a, σ, 42, 42):
  pos(1, 3) = 3
  σ(3) = 6
  a(ω³) = 1
  Result: 6 + 42·1 + 42 = 90
```

### Test 2: Position 10 (i=6, column 2)

Note: i=6 > n=4 is valid! Since ω⁴=1, we have ω⁶ = ω².

```
numerator(6, 2, b, σ, 42, 42):
  pos(2, 6) = (2-1)·4 + 6 = 10
  b(ω⁶) = b(ω²) = 1
  Result: 10 + 42·1 + 42 = 94

denominator(6, 2, b, σ, 42, 42):
  pos(2, 6) = 10
  σ(10) = 7
  b(ω⁶) = b(ω²) = 1
  Result: 7 + 42·1 + 42 = 91
```

## Cycle Verification Example

For cycle (3, 6, 9) with value 1:

| Position | Column | num | den | Ratio |
|----------|--------|-----|-----|-------|
| 3 (a[3]) | 1 | 87 | 90 | 87/90 |
| 6 (b[2]) | 2 | 90 | 93 | 90/93 |
| 9 (c[1]) | 3 | 93 | 87 | 93/87 |

**Product of numerators:** 728,190
**Product of denominators:** 728,190

The products match! This is the key property: for a valid permutation, the grand product equals 1.

## Grand Product

The complete grand product across all positions and columns:

$$GP = \prod_{\text{all positions}} \frac{\text{numerator}}{\text{denominator}}$$

If the permutation is valid (copy constraints satisfied), then **GP = 1**.

## Why This Works

1. **Numerator terms** = all positions with their original IDs
2. **Denominator terms** = all positions with their permuted IDs

Since σ is a permutation (bijection), every position ID appears exactly once in both numerator and denominator, just in different orders.

If the wire values match within each cycle, the products cancel out perfectly, giving GP = 1.

## Running the Exercise

```bash
# From repo root
./run.sh sageless/solutions/exercise15/exercise15.py

# Or with venv activated
cd sageless/solutions/exercise15
./exercise15.py
```

## Output

```
======================================================================
EXERCISE 15: NUMERATOR AND DENOMINATOR FUNCTIONS
======================================================================

Test 1: numerator(3, 1, a, σ, 42, 42)
  Position: pos(1, 3) = 3
  Result: 87
  ✓ PASS

Test 2: denominator(3, 1, a, σ, 42, 42)
  Position: pos(1, 3) = 3
  σ(3) = 6
  Result: 90
  ✓ PASS

Test 3: numerator(6, 2, b, σ, 42, 42)
  Position: pos(2, 6) = 10
  Result: 94
  ✓ PASS

Test 4: denominator(6, 2, b, σ, 42, 42)
  Position: pos(2, 6) = 10
  σ(10) = 7
  Result: 91
  ✓ PASS

✓ Exercise 15 Complete!
```

## What's Next?

**Exercise 16** will implement **accumulator functions** that compute partial products of numerators and denominators, building up to the full grand product argument.

---

**PlonK Tutorial - Exercise 15**
**Grand product argument: numerator and denominator functions ✓**
