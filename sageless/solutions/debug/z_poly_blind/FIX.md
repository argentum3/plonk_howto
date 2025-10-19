# Fix for z_poly_blind Verification Failure

## Quick Fix

**Cell 92 (Exercise 20) - ONE LINE CHANGE**

Find this line (around line 3623):
```python
c_z = kzg.commit(z_poly)
```

Change to:
```python
c_z = kzg.commit(z_poly_blind)
```

That's it! This single character change fixes both verification failures.

## Detailed Steps

### Step 1: Open Cell 92 in the notebook

### Step 2: Find this section:
```python
# Commit to z polynomial
c_z = kzg.commit(z_poly)
print(f"\nCommitment to z:")
print(f"  c_z = {c_z}")
```

### Step 3: Change to:
```python
# Commit to blinded z polynomial
c_z = kzg.commit(z_poly_blind)
print(f"\nCommitment to z_poly_blind:")
print(f"  c_z = {c_z}")
```

### Step 4: Re-run cells in order
1. Re-run Cell 92 (Exercise 20) - generates new c_z commitment
2. Re-run Cell 94 (Exercise 21) - uses c_z in transcript
3. Re-run Cell 96 (Exercise 22) - generates proofs
4. Re-run Cell 98 - assembles proof dictionary
5. Re-run Cell 100 - verify_plonk

### Step 5: Verify the fix worked

Cell 96 should now show:
```
Verify z_poly_blind(ζ) = ...: True
Verify z_poly_blind(ζ·ω) = ...: True
✓✓✓ ALL OPENING PROOFS VERIFIED SUCCESSFULLY ✓✓✓
```

Cell 100 should show:
```
Quotient constraint holds.
Verifier result: True All checks passed!
```

## Why Only One Line?

The commitment is the only thing that was wrong. Everything else already uses `z_poly_blind`:

✓ Cell 92 creates `z_poly_blind` correctly
✓ Cell 94 uses `z_poly_blind` in constraint equations
✓ Cell 96 evaluates `z_poly_blind(zeta)`
✓ Cell 96 generates proofs for `z_poly_blind`

Only the commitment was using the wrong polynomial!

## Pattern

This is the same issue as with `quotient_poly_blind`:

| Polynomial | Created | Committed | Used in Proofs | Status |
|------------|---------|-----------|----------------|--------|
| `a_blind` | ✓ | ✓ | ✓ | Working |
| `b_blind` | ✓ | ✓ | ✓ | Working |
| `c_blind` | ✓ | ✓ | ✓ | Working |
| `z_poly_blind` | ✓ | ❌ → ✓ | ✓ | **Fixed** |
| `quotient_poly_blind` | ✓ | ✓ | ✓ | Fixed earlier |

The pattern: **Always commit to the blinded version if you use the blinded version in proofs!**
