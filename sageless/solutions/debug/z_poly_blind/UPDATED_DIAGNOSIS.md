# Updated Diagnosis: z_poly_blind Not Defined

## The Real Problem

The user correctly identified that **`z_poly_blind` is NOT defined in Cell 92 (Exercise 20)**!

### What Cell 92 Currently Has

```python
# Cell 92 - CURRENT (Exercise 20)
z_poly, N_poly, D_poly = interpolate_z_N_D(a_blind, b_blind, c_blind, beta, gamma, Ω)

# ❌ MISSING: z_poly_blind definition

# Then we try to commit to z_poly_blind (which doesn't exist!)
c_z = kzg.commit(z_poly_blind)  # ❌ NameError!
```

### What Cell 92 Should Have

```python
# Cell 92 - CORRECT (Exercise 20)
z_poly, N_poly, D_poly = interpolate_z_N_D(a_blind, b_blind, c_blind, beta, gamma, Ω)

# ✓ ADD: Blind z_poly for zero-knowledge
b1_z, b2_z = 98765, 43210  # Random blinding factors
z_poly_blind = z_poly + (b1_z * x + b2_z) * ZH

# ✓ Now c_z commitment will work
c_z = kzg.commit(z_poly_blind)
```

## Why This Wasn't Caught Earlier

There's an earlier cell (around line 3342) that has:
```python
z_poly_blind = z_poly + random_polynomial(degree=k-1, modulus=p) * ZH
```

This is from the **tutorial demonstration**, not from Exercise 20!

When we run the notebook:
1. Earlier tutorial cell defines `z_poly_blind`
2. Cell 92 (Exercise 20) redefines `z_poly` but NOT `z_poly_blind`
3. Cell 92 tries to commit to `z_poly_blind` from the old tutorial cell
4. This creates a mismatch!

## The Complete Fix

Cell 92 (Exercise 20) needs to:

1. **Compute z_poly** (already done ✓)
2. **Blind z_poly** (MISSING - need to add)
3. **Commit to z_poly_blind** (already updated ✓)

### Code to Add

After this line in Cell 92:
```python
z_poly, N_poly, D_poly = interpolate_z_N_D(a_blind, b_blind, c_blind, beta, gamma, Ω)
```

Add:
```python
# Blind z_poly for zero-knowledge (at most 2 openings)
b1_z, b2_z = 98765, 43210
z_poly_blind = z_poly + (b1_z * x + b2_z) * ZH

print(f"\nBlinding z_poly:")
print(f"  z_poly_blind = z_poly + ({b1_z}·x + {b2_z}) · ZH")
print(f"  z_poly_blind: degree {z_poly_blind.degree()}")
```

## Impact

Without this fix:
- Cell 92 commits to an old `z_poly_blind` from the tutorial
- Cell 96 generates proofs for `z_poly_blind` (the old one)
- The commitments and proofs are all based on the WRONG z_poly!

With this fix:
- Cell 92 creates NEW `z_poly_blind` based on the current `z_poly`
- Cell 92 commits to the NEW `z_poly_blind`
- Cell 96 generates proofs for the NEW `z_poly_blind`
- Everything is consistent!

## Why We Need Blinding

The blinding factors `b1_z * x + b2_z` multiplied by `ZH` add randomness without changing:
- The values at the domain points Ω (since ZH = 0 at all Ω points)
- The constraint equations (since ZH divides everything)

But they make the polynomial unpredictable to the verifier, achieving zero-knowledge.

We use degree k-1 blinding (2 coefficients: b1_z and b2_z) because we open z_poly at 2 points:
- ζ (the random challenge point)
- ζ·ω (for the permutation check)

This follows the standard pattern: if you open at k points, blind with degree k-1 polynomial.
