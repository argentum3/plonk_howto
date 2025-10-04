# Exercise 3: Polynomial Interpolation

Interpolates witness and selector vectors as polynomials over finite field F_p.

## Problem

Transform discrete circuit values into polynomials:
- Witness values: LI, RI, O → polynomials a(x), b(x), c(x)
- Selector values: SL, SR, SM → polynomials qL(x), qR(x), qM(x)

## Method

Uses **Lagrange interpolation** to create polynomials that pass through given points.

For points (x₁, y₁), (x₂, y₂), ..., (xₙ, yₙ):

```
f(x) = Σ yⱼ · Lⱼ(x)

where Lⱼ(x) = ∏(i≠j) (x - xᵢ)/(xⱼ - xᵢ)
```

## Running

```bash
cd exercise3
python3 exercise3.py
```

## Output

```
Exercise 3 Solution: Polynomial Interpolation
✓ All polynomials have degree 3
✓ Evaluations match original values
✓ Gate constraint polynomial verified
```

## Important

This file contains the complete `Polynomial` class implementation. All other exercises import from `lib/polynomials.py` (which is a copy of this file).
