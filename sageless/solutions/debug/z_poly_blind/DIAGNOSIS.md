# z_poly_blind Verification Failure Diagnosis

## Problem

After applying the quotient constraint fixes, Cell 96 (Exercise 22) now shows:

```
Verify z_poly_blind(ζ) = ...: False
Verify z_poly_blind(ζ·ω) = ...: False
```

## Root Cause

**Cell 92 commits to the wrong polynomial!**

```python
# Cell 92 (Exercise 20) - CURRENT CODE
z_poly_blind = z_poly + random_polynomial(degree=k-1, modulus=p) * ZH
c_z = kzg.commit(z_poly)  # ❌ WRONG - commits to unblinded z_poly
```

**Cell 96 generates proofs for the blinded polynomial:**

```python
# Cell 96 (Exercise 22) - CURRENT CODE
z_zeta = z_poly_blind(zeta)              # ✓ Uses blinded
proof_z = kzg.prove(z_poly_blind, zeta)  # ✓ Proves blinded
```

**The verification fails because:**
- `c_z` = commitment to `z_poly` (unblinded)
- `proof_z` = proof for `z_poly_blind` (blinded)
- `z_zeta` = evaluation of `z_poly_blind` (blinded)

KZG verification checks: "Does commitment `c_z` commit to a polynomial that evaluates to `z_zeta` at `zeta`?"

The answer is NO because:
- `c_z` commits to `z_poly`
- `z_zeta` is the evaluation of `z_poly_blind`
- `z_poly ≠ z_poly_blind`

## The Fix

**Cell 92 (Exercise 20) - Line ~3623**

Change:
```python
c_z = kzg.commit(z_poly)
```

To:
```python
c_z = kzg.commit(z_poly_blind)
```

## Why This Fix Works

After the fix:
1. `c_z = kzg.commit(z_poly_blind)` - commitment to blinded polynomial
2. `proof_z = kzg.prove(z_poly_blind, zeta)` - proof for blinded polynomial
3. `z_zeta = z_poly_blind(zeta)` - evaluation of blinded polynomial

All three use the **same polynomial** (`z_poly_blind`), so verification passes!

## Impact

This is the same issue we had with `quotient_poly_blind`:
- We created blinded versions for zero-knowledge
- But forgot to update the commitments to use the blinded versions
- Commitments must match the polynomials used in proofs

## Files

- `diagnose_commitment_mismatch.py` - Detailed diagnostic explanation
- `DIAGNOSIS.md` - This file (summary)
- `FIX.md` - Step-by-step fix instructions
