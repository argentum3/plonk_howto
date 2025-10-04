# Exercise 4: Vanishing Polynomials and Polynomial Division

Computes vanishing polynomials and uses polynomial division to verify constraint satisfaction.

## Problem

Instead of checking constraints at each point, use polynomial division:
- If t(i) = 0 for all i ∈ I, then Z(x) divides t(x)
- Compute quotient Q(x) such that t(x) = Q(x) · Z(x)

## Computed Values

1. **Z(x)** - Vanishing polynomial for I = {1, 2, 3, 4}
   - Z(x) = (x-1)(x-2)(x-3)(x-4)
   - Degree: 4

2. **Q(x)** - Quotient from t(x) = Q(x)·Z(x)
   - Degree: 5

3. **Z1(x)** - Vanishing polynomial for I' = {1, 2}
   - Z1(x) = (x-1)(x-2)
   - Degree: 2

4. **Q1(x), Q2(x)** - Quotients for wiring constraints
   - Both degree: 1

## Running

```bash
cd exercise4
python3 exercise4.py
```

## Dependencies

Imports from `lib/polynomials`:
- Polynomial classes
- Pre-computed polynomials (a, b, c, qL, qR, qM)

## Output

Shows polynomial degrees, coefficients, and verifies division is exact (zero remainder).
