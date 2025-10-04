# Exercise 5 Solution Summary

## Problem Statement

Verify polynomial equalities using the Schwartz-Zippel lemma with random challenge points instead of expensive polynomial multiplication. This makes the verification **succinct** (fast and efficient).

## The Schwartz-Zippel Lemma

**Key Insight:** Two different polynomials of degree d can agree at most d points. So if we check equality at a random point γ:
- If polynomials are equal → check always passes ✓
- If polynomials are different → check fails with probability ≥ 1 - d/p

**Security:** For our circuit with degree ≤ 9 and field size p ≈ 2²⁵⁴:
```
Probability of false positive ≤ 9/(2^254) ≈ 10^-75
```

This is negligibly small - less likely than guessing someone's private key!

## Three Equality Checks

Instead of checking polynomial equalities directly:
```
t(x) = Q(x) · Z(x)      (expensive: multiply deg-5 × deg-4 polynomials)
f1(x) = Q1(x) · Z1(x)   (expensive: multiply deg-1 × deg-2 polynomials)
f2(x) = Q2(x) · Z1(x)   (expensive: multiply deg-1 × deg-2 polynomials)
```

We check at random points (cheap: just evaluate and multiply numbers):
```
t(γ1) = Q(γ1) · Z(γ1)
f1(γ2) = Q1(γ2) · Z1(γ2)
f2(γ3) = Q2(γ3) · Z1(γ3)
```

## Solution

### Challenge Values
```python
γ1 = 42
γ2 = 74102
γ3 = 987654321987654321
```

### Check 1: Gate Constraints
```python
t_γ1 = t(γ1)    # Evaluate constraint polynomial at γ1
Q_γ1 = Q(γ1)    # Evaluate quotient at γ1
Z_γ1 = Z(γ1)    # Evaluate vanishing polynomial at γ1

# Verify equality
assert t_γ1 == (Q_γ1 * Z_γ1) % p
```

**Result:**
```
t(42) = Q(42) · Z(42) = 21888242871839275222246405745257275088548364400416034343698204183303103172977
```
✓ Check passes!

### Check 2: Wiring Constraint 1
```python
f1_γ2 = f1(γ2)
Q1_γ2 = Q1(γ2)
Z1_γ2 = Z1(γ2)

assert f1_γ2 == (Q1_γ2 * Z1_γ2) % p
```

**Result:**
```
f1(74102) = Q1(74102) · Z1(74102) = 271248759392650
```
✓ Check passes!

### Check 3: Wiring Constraint 2
```python
f2_γ3 = f2(γ3)
Q2_γ3 = Q2(γ3)
Z1_γ3 = Z1(γ3)

assert f2_γ3 == (Q2_γ3 * Z1_γ3) % p
```

**Result:**
```
f2(987654321987654321) = Q2(987654321987654321) · Z1(987654321987654321)
                       = 21888242871839275222245442326925691337956137906799110242993653357780575606177
```
✓ Check passes!

## Why This Matters

### Before (Expensive):
To verify t(x) = Q(x) · Z(x):
1. Multiply Q(x) · Z(x) → O(d²) operations
2. Compare all 10 coefficients of result with t(x)
3. Total: ~45 field multiplications + 10 comparisons

### After (Cheap with Schwartz-Zippel):
1. Evaluate t(42) → O(d) operations
2. Evaluate Q(42) → O(d) operations
3. Evaluate Z(42) → O(d) operations
4. Multiply two numbers: Q(42) · Z(42)
5. Compare: one equality check
6. Total: ~27 field operations + 1 comparison

**Speedup:** ~60% fewer operations, and scales better for larger circuits!

## Verification vs Security Trade-off

| Method | Cost | Security |
|--------|------|----------|
| Full polynomial check | O(d²) | 100% (deterministic) |
| Schwartz-Zippel | O(d) | 1 - 10⁻⁷⁵ ≈ 100% (probabilistic) |

The security loss is negligible but the efficiency gain is substantial!

## Complete Solution Code

```python
γ1 = 42
γ2 = 74102
γ3 = 987654321987654321

# Check 1: Gate constraints
t_γ1 = t(γ1)
Q_γ1 = Q(γ1)
Z_γ1 = Z(γ1)
assert t_γ1 == (Q_γ1 * Z_γ1) % p
print(f"t(γ1) = Q(γ1)·Z(γ1) = {t_γ1}")

# Check 2: Wiring constraint 1
f1_γ2 = f1(γ2)
Q1_γ2 = Q1(γ2)
Z1_γ2 = Z1(γ2)
assert f1_γ2 == (Q1_γ2 * Z1_γ2) % p
print(f"f1(γ2) = Q1(γ2)·Z1(γ2) = {f1_γ2}")

# Check 3: Wiring constraint 2
f2_γ3 = f2(γ3)
Q2_γ3 = Q2(γ3)
Z1_γ3 = Z1(γ3)
assert f2_γ3 == (Q2_γ3 * Z1_γ3) % p
print(f"f2(γ3) = Q2(γ3)·Z1(γ3) = {f2_γ3}")

print("✓ All Schwartz-Zippel checks passed!")
```

## Expected Output

```
t(γ1) = Q(γ1)·Z(γ1) = 21888242871839275222246405745257275088548364400416034343698204183303103172977
f1(γ2) = Q1(γ2)·Z1(γ2) = 271248759392650
f2(γ3) = Q2(γ3)·Z1(γ3) = 21888242871839275222245442326925691337956137906799110242993653357780575606177
✓ All Schwartz-Zippel checks passed!
```

## Key Takeaways

1. **Schwartz-Zippel enables succinct verification** - O(d) instead of O(d²)
2. **Security trade-off is negligible** - error probability ≈ 10⁻⁷⁵
3. **Uses random challenges** - γ values prevent cheating
4. **Foundation for PLONK** - this is what makes zero-knowledge proofs practical!

## Files

- **sageless/solutions/SCHWARTZ_ZIPPEL_EXPLAINED.md** - Simple explanation of the lemma
- **sageless/solutions/exercise5.py** - Complete solution with verification
- **sageless/PlonK-Tutorial.ipynb** - Cell 23 now contains the solution

## Running the Solution

```bash
cd sageless/solutions
python3 exercise5.py
```

Expected: All three checks pass with matching values!

## Connection to PLONK

This exercise demonstrates the **second protocol version** in PLONK:
- Prover sends polynomials (or commitments to them)
- Verifier picks random challenges γ₁, γ₂, γ₃
- Prover evaluates at those points
- Verifier checks equalities with negligible error probability

This is much more efficient than the first protocol which required looping through all circuit gates!
