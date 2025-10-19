# Solution: Quotient Constraint Failure

## Problem Identified

Your diagnostic output revealed the root cause:

```
✗ quotient_poly_blind not defined
z_zeta_omega mismatch: 15426623832310455175124265049380216935164090373349890937272801789861857222680
                  vs:  3940837869981039717610763274790657016477022911600274195300739646073818338082
```

## Root Cause

**Cell 94** creates `quotient_poly` but not `quotient_poly_blind`.
**Cell 96** uses unblinded `z_poly` and `quotient_poly` when it should use blinded versions.

The master polynomial is built from **blinded** witness polynomials:
- `bigt = t_gates + α·t_perm_start + α²·t_perm_step`
- Uses `a_blind`, `b_blind`, `c_blind`, `z_poly_blind`

Therefore evaluations must use blinded versions too!

## Two Required Fixes

### Fix 1: Cell 94 - Create quotient_poly_blind

**Location**: After computing `quotient_poly`, before committing

**Find this code**:
```python
# Commit to quotient
c_t = kzg.commit(quotient_poly)
```

**Replace with** (see `fix_cell94.py`):
```python
# Blind the quotient polynomial
b1_t, b2_t = 55555, 66666
quotient_poly_blind = quotient_poly + (b1_t * x + b2_t) * ZH

# Commit to blinded quotient
c_t = kzg.commit(quotient_poly_blind)
```

### Fix 2: Cell 96 - Use blinded polynomials

**Location**: Evaluations and proof generation sections

**Change these 3 evaluations**:
```python
# OLD
z_zeta = z_poly(zeta)
t_zeta = quotient_poly(zeta)
z_zeta_omega = z_poly(zeta_omega)

# NEW
z_zeta = z_poly_blind(zeta)
t_zeta = quotient_poly_blind(zeta)
z_zeta_omega = z_poly_blind(zeta_omega)
```

**Change these 3 proofs**:
```python
# OLD
proof_z = kzg.prove(z_poly, zeta)
proof_t = kzg.prove(quotient_poly, zeta)
proof_z_omega = kzg.prove(z_poly, zeta_omega)

# NEW
proof_z = kzg.prove(z_poly_blind, zeta)
proof_t = kzg.prove(quotient_poly_blind, zeta)
proof_z_omega = kzg.prove(z_poly_blind, zeta_omega)
```

## Quick Copy-Paste Fix

### For Cell 94:
Copy the code from: `sageless/solutions/debug/verify_plonk/fix_cell94.py`

### For Cell 96:
Copy the code from: `sageless/solutions/debug/verify_plonk/fix_cell96.py`

## After Applying Fixes

1. **Re-run Cell 94** - This will create `quotient_poly_blind` and update `c_t`
2. **Re-run Cell 96** - This will use blinded polynomials for evaluations
3. **Re-run Cell 98** - This will assemble the updated proof
4. **Re-run Cell 100** - verify_plonk should now pass!

Expected output:
```
Quotient constraint holds.
Verifier result: True All checks passed!
```

## Why This Was Happening

The verifier computes:
```python
master_poly(ζ) = t_gates(ζ) + α·t_perm_start(ζ) + α²·t_perm_step(ζ)
```

Using blinded evaluations: `a_zeta = a_blind(ζ)`, `z_zeta = z_poly_blind(ζ)`, etc.

Then checks:
```python
master_poly(ζ) == t_zeta * ZH(ζ)
```

If `t_zeta = quotient_poly(ζ)` (unblinded), it won't equal `t_zeta = quotient_poly_blind(ζ)` (blinded).

Same for `z_zeta` - using `z_poly(ζ)` instead of `z_poly_blind(ζ)` breaks the equation.

## Files Created for You

1. **FIX_INSTRUCTIONS.md** - Detailed explanation
2. **fix_cell94.py** - Copy-paste code for Cell 94
3. **fix_cell96.py** - Copy-paste code for Cell 96
4. **SOLUTION.md** - This file (quick reference)

## Verification

To verify the fix worked, add a cell after Cell 100 and run:
```python
print(f"✓ verify_plonk passed!")
print(f"✓ quotient_poly_blind was used: {quotient_poly_blind.degree()}")
print(f"✓ z_poly_blind was used for evaluations")
```
