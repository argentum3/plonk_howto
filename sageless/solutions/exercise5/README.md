# Exercise 5: Schwartz-Zippel Probabilistic Equality Checks

Uses the Schwartz-Zippel lemma for efficient probabilistic polynomial equality verification.

## Problem

Instead of expensive polynomial multiplication and comparison:
```
t(x) = Q(x) · Z(x)  (expensive: O(d²))
```

Check equality at random points:
```
t(γ) = Q(γ) · Z(γ)  (cheap: O(d))
```

## Schwartz-Zippel Lemma

For different polynomials f(x) ≠ g(x) of degree ≤ d:
```
Pr[f(γ) = g(γ)] ≤ d/p ≈ 9/(2²⁵⁴) ≈ 10⁻⁷⁵
```

**Security:** Negligibly small error probability!

## Challenge Values

```python
γ1 = 42
γ2 = 74102
γ3 = 987654321987654321
```

## Three Checks

1. **Gate constraints:** t(γ₁) = Q(γ₁) · Z(γ₁)
2. **Wiring constraint 1:** f₁(γ₂) = Q₁(γ₂) · Z₁(γ₂)
3. **Wiring constraint 2:** f₂(γ₃) = Q₂(γ₃) · Z₁(γ₃)

## Running

```bash
cd exercise5
python3 exercise5.py
```

## Dependencies

Imports from `lib/polynomials`:
- All polynomial classes and functions
- Pre-computed values from exercises 3 and 4

## Output

Shows each check with computed values and verifies against expected results.

## Why This Matters

This is what makes PLONK **succinct** - verifier only checks numbers at random points instead of processing entire polynomials!
