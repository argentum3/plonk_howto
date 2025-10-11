# Exercise 16: Accumulator Functions for Grand Product Argument

## Overview

This exercise implements **accumulator functions** that compute partial products of numerators and denominators. These accumulators are essential for building the grand product step-by-step in PlonK's permutation argument.

## Formulas

### Accumulator for Numerator

$$\text{acc\_numerator}(i, \text{column}, f, \sigma, \beta, \gamma) = \prod_{j=1}^{i-1} \text{numerator}(j, \text{column}, f, \sigma, \beta, \gamma)$$

### Accumulator for Denominator

$$\text{acc\_denominator}(i, \text{column}, f, \sigma, \beta, \gamma) = \prod_{j=1}^{i-1} \text{denominator}(j, \text{column}, f, \sigma, \beta, \gamma)$$

## Key Properties

### Product Range

The product runs from **j = 1 to i-1** (i is exclusive):

| i value | Product range | Result |
|---------|---------------|--------|
| i = 1 | Empty (no j values) | 1 (empty product) |
| i = 2 | j = 1 | numerator(1, ...) |
| i = 3 | j = 1, 2 | numerator(1, ...) × numerator(2, ...) |
| i = n+1 | j = 1, 2, ..., n | Product of all n terms |

### Why i-1?

Using **i-1** as the upper bound allows:
- `acc_*(1, ...)` = 1 (identity element)
- `acc_*(i+1, ...)` = `acc_*(i, ...)` × `numerator(i, ...)`

This creates a **recursive structure** useful for the z polynomial in later exercises.

## Implementation

```python
def acc_numerator(i, column, f, sigma, beta, gamma):
    value = 1
    for j in range(1, i):
        value = (value * numerator(j, column, f, sigma, beta, gamma)) % p
    return value

def acc_denominator(i, column, f, sigma, beta, gamma):
    value = 1
    for j in range(1, i):
        value = (value * denominator(j, column, f, sigma, beta, gamma)) % p
    return value
```

## Example Calculations

With β=42, γ=42, column 1 (polynomial a):

### Empty Product (i=1)

```
acc_numerator(1, 1, a, σ, 42, 42) = 1 (empty product)
acc_denominator(1, 1, a, σ, 42, 42) = 1 (empty product)
```

### Single Term (i=2)

```
numerator(1, 1, a, σ, 42, 42) = 43

acc_numerator(2, 1, a, σ, 42, 42) = numerator(1, ...) = 43
acc_denominator(2, 1, a, σ, 42, 42) = denominator(1, ...) = 43
```

### Two Terms (i=3)

```
numerator(1, ...) = 43
numerator(2, ...) = 86

acc_numerator(3, 1, a, σ, 42, 42) = 43 × 86 = 3,698 (mod p)
```

### All Terms (i=n+1=5)

```
Product of numerator(1, ...) through numerator(4, ...):

acc_numerator(5, 1, a, σ, 42, 42) = 55,336,872
acc_denominator(5, 1, a, σ, 42, 42) = 60,619,680
```

## Grand Product Verification

The key property: **If the permutation is valid, the grand product equals 1.**

### Computing N_n and D_n

Multiply accumulators across all three columns:

```python
N_n = acc_numerator(n+1, 1, a, σ, β, γ) ×
      acc_numerator(n+1, 2, b, σ, β, γ) ×
      acc_numerator(n+1, 3, c, σ, β, γ)

D_n = acc_denominator(n+1, 1, a, σ, β, γ) ×
      acc_denominator(n+1, 2, b, σ, β, γ) ×
      acc_denominator(n+1, 3, c, σ, β, γ)
```

### Results

```
N_n (column a): 55,336,872
N_n (column b): 187,498,080
N_n (column c): 978,044,544
N_n (total): 10,147,757,162,457,520,077,373,440

D_n (column a): 60,619,680
D_n (column b): 194,703,312
D_n (column c): 859,771,584
D_n (total): 10,147,757,162,457,520,077,373,440

N_n / D_n = 1 ✓
```

### Why Does This Work?

The grand product equals 1 because:

1. **Numerator terms**: Each position contributes `pos + β·f(ω^i) + γ`
2. **Denominator terms**: Each position contributes `σ(pos) + β·f(ω^i) + γ`

Since σ is a **permutation** (bijection):
- Every position ID appears exactly once in numerators
- Every position ID appears exactly once in denominators
- Just in different orders!

If wire values match within cycles (copy constraints satisfied), the products cancel perfectly:

$$\frac{N_n}{D_n} = \frac{\prod_i (pos_i + \beta \cdot f(i) + \gamma)}{\prod_i (\sigma(pos_i) + \beta \cdot f(i) + \gamma)} = 1$$

## Recursive Structure

The accumulator functions have a recursive property:

```
acc_*(i+1, ...) = acc_*(i, ...) × numerator(i, ...)
```

This will be exploited in later exercises to define the **z polynomial** efficiently.

## Running the Exercise

```bash
# From repo root
./run.sh sageless/solutions/exercise16/exercise16.py

# Or with venv activated
cd sageless/solutions/exercise16
./exercise16.py
```

## Output

```
======================================================================
EXERCISE 16: ACCUMULATOR FUNCTIONS
======================================================================

Test 1: Empty product (i=1)
  acc_numerator(1, 1, a, ...) = 1
  acc_denominator(1, 1, a, ...) = 1
  ✓ Both equal 1 (correct)

Test 2: Single term (i=2, includes j=1)
  numerator(1, 1, a, ...) = 43
  acc_numerator(2, 1, a, ...) = 43
  ✓ Accumulators match single terms

Test 3: Multiple terms (i=3, includes j=1,2)
  Expected product: 3698
  acc_numerator(3, ...) = 3698
  ✓ Accumulator matches product

Test 4: Full accumulator (i=n+1=5)
  acc_numerator(n+1, 1, a, ...) = 55336872
  ✓ Matches manual calculation

======================================================================
GRAND PRODUCT CHECK
======================================================================

  N_n // D_n = 1
  Check: N_n // D_n == 1? True
  ✓ PASS: Grand product equals 1!

  This confirms the permutation σ correctly encodes
  the copy constraints in the circuit.

✓ Exercise 16 Complete!
```

## What's Next?

The accumulator functions will be used to define the **recursive z polynomial** in Exercise 17, which captures the cumulative product structure needed for the PlonK permutation argument.

## Mathematical Insight

### Why Partial Products Matter

Instead of computing the full grand product directly:

```python
GP = ∏(all numerators) / ∏(all denominators)
```

We can build it incrementally using accumulators:

```python
GP_partial(i) = ∏_{j=1}^{i} numerator(j) / ∏_{j=1}^{i} denominator(j)
```

This allows:
1. **Incremental verification**: Check partial products at each step
2. **Efficient polynomial encoding**: Turn products into polynomial evaluations
3. **Succinct proofs**: Commit to z polynomial instead of all individual values

### Connection to Z Polynomial

In upcoming exercises, the z polynomial will satisfy:

$$z(\omega^{i+1}) = z(\omega^i) \cdot \frac{\text{numerator}(i, ...)}{\text{denominator}(i, ...)}$$

with boundary condition z(1) = 1, ensuring z(ω^{n+1}) = 1 if the permutation is valid.

---

**PlonK Tutorial - Exercise 16**
**Accumulator functions for grand product argument ✓**
