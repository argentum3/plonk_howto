# Exercise 4 Solution Summary

## Problem Statement

Compute vanishing polynomials and quotient polynomials using polynomial division to verify zero-equality constraints more efficiently than looping through all indices.

## Mathematical Background

A polynomial $t(x)$ vanishes at points in set $I$ if and only if the **vanishing polynomial** $Z(x) = \prod_{i \in I} (x-i)$ divides $t(x)$.

This means: $t(x) = Q(x) \cdot Z(x)$ for some quotient polynomial $Q(x)$.

## Solution

### 1. Vanishing Polynomial Z(x) for I = {1, 2, 3, 4}

```python
Z = Polynomial([1], p)  # Start with constant 1
for i in I:
    Z = Z * (x - i)
```

**Result:**
- $Z(x) = (x-1)(x-2)(x-3)(x-4)$
- Degree: 4
- $Z(i) = 0$ for all $i \in I$ ✓

### 2. Quotient Polynomial Q(x) from t(x) = Q(x)·Z(x)

```python
Q, _ = t.quo_rem(Z)
```

**Result:**
- Degree: 5
- Coefficients match expected values from cell 17 ✓
- Division is exact (remainder = 0) ✓
- Verification: $t(x) = Q(x) \cdot Z(x)$ ✓

**Note:** The constraint polynomial $t$ uses the FULL gate formula:
```python
t = qM*a*b + qL*a + qR*b - c
```
Not just `a + b - c`. This is why $t$ has degree 9 and $Q$ has degree 5.

### 3. Vanishing Polynomial Z1(x) for I' = I\{3,4} = {1, 2}

```python
I_prime = [i for i in I if i not in {3, 4}]
Z1 = Polynomial([1], p)
for i in I_prime:
    Z1 = Z1 * (x - i)
```

**Result:**
- $Z1(x) = (x-1)(x-2)$
- Degree: 2
- $Z1(i) = 0$ for $i \in \{1, 2\}$ ✓

### 4. Quotient Q1(x) from f1(x) = Q1(x)·Z1(x)

Wiring constraint: $f_1(x) = a(x+1) - b(x)$

```python
Q1, _ = f1.quo_rem(Z1)
```

**Result:**
- Degree: 1
- Division is exact (remainder = 0) ✓
- Verification: $f_1(x) = Q_1(x) \cdot Z1(x)$ ✓

### 5. Quotient Q2(x) from f2(x) = Q2(x)·Z1(x)

Wiring constraint: $f_2(x) = b(x+1) - c(x)$

```python
Q2, _ = f2.quo_rem(Z1)
```

**Result:**
- Degree: 1
- Division is exact (remainder = 0) ✓
- Verification: $f_2(x) = Q_2(x) \cdot Z1(x)$ ✓

## Key Insights

1. **Efficiency:** Instead of checking $t(i) = 0$ for each $i \in I$ (4 checks), we compute one polynomial division and verify $t(x) = Q(x) \cdot Z(x)$.

2. **Polynomial Division:** The `quo_rem` method uses long division with modular arithmetic:
   - Compute leading coefficient: $c = \frac{\text{lead}(\text{dividend})}{\text{lead}(\text{divisor})} \mod p$
   - Subtract: $\text{dividend} - c \cdot x^{\text{deg}} \cdot \text{divisor}$
   - Repeat until degree of dividend < degree of divisor

3. **Vanishing Polynomials:** For a set $I = \{i_1, i_2, ..., i_n\}$, the vanishing polynomial is:
   $$Z(x) = (x-i_1)(x-i_2)\cdots(x-i_n)$$

## Complete Solution Code

```python
# Compute Z(x) = vanishing polynomial for I = {1,2,3,4}
Z = Polynomial([1], p)
for i in I:
    Z = Z * (x - i)

# Compute Q(x) from t(x) = Q(x)·Z(x)
Q, _ = t.quo_rem(Z)

# Compute Z1(x) = vanishing polynomial for I' = I\{3,4} = {1,2}
I_prime = [i for i in I if i not in {3, 4}]
Z1 = Polynomial([1], p)
for i in I_prime:
    Z1 = Z1 * (x - i)

# Compute Q1(x) from f1(x) = Q1(x)·Z1(x)
Q1, _ = f1.quo_rem(Z1)

# Compute Q2(x) from f2(x) = Q2(x)·Z1(x)
Q2, _ = f2.quo_rem(Z1)

# Verify
assert t == Q * Z
assert f1 == Q1 * Z1
assert f2 == Q2 * Z1
```

## Files

- **sageless/solutions/exercise4.py** - Complete solution with verification
- **sageless/PlonK-Tutorial.ipynb** - Cell 16 now contains the solution

## Running the Solution

```bash
cd sageless/solutions
python3 exercise4.py
```

Expected output shows all polynomials computed correctly with degree verification and division checks passing.
