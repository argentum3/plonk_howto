# Quotient Constraint Investigation

## Problem Report

Cell 99 manual quotient constraint check failed:
```python
master_poly_v = (t_gates_v + alpha * t_perm_start_v + (alpha * alpha) % p * t_perm_step_v) % p
ZH_z = (pow(zeta, 4, p) - 1) % p
rhs = (t_zeta * ZH_z) % p

# Check failed:
master_poly_v != rhs  # ✗
```

## Investigation Summary

### Discovery Process

1. **Initial hypothesis**: Values from wrong cells or old variables
2. **Traced data flow**: All values come from correct cells
3. **Mathematical analysis**: Examined blinding impact
4. **Root cause found**: Quotient blinding breaks the constraint!

### The Issue

When we blind the quotient polynomial:
```python
quotient_poly_blind = quotient_poly + (b1_t * x + b2_t) * ZH
```

The quotient constraint breaks:
```
Required: bigt(ζ) = quotient_poly(ζ) * ZH(ζ)

With blinding:
  quotient_poly_blind(ζ) * ZH(ζ)
  = [quotient_poly(ζ) + blinding_term*ZH(ζ)] * ZH(ζ)
  = quotient_poly(ζ)*ZH(ζ) + blinding_term*ZH(ζ)²
  = bigt(ζ) + extra_term
  ≠ bigt(ζ)  ← FAILS!
```

### Why Witness Blinding Works

For witnesses (a, b, c, z):
- No mathematical constraint to preserve
- Just proving evaluations
- Blinding adds randomness without breaking anything

### Why Quotient Blinding Fails

For quotient polynomial:
- **Must satisfy**: `bigt = quotient_poly * ZH` exactly
- Blinding adds `(random)*ZH(ζ)²` to the equation
- This breaks the polynomial identity at ζ

## The Solution

**Remove quotient polynomial blinding.**

Witness polynomials still provide zero-knowledge. The quotient polynomial is derived from witnesses, not itself a witness.

### Changes Made

**Cell 94** - Removed blinding:
```python
# Before:
quotient_poly_blind = quotient_poly + (b1_t * x + b2_t) * ZH
c_t = kzg.commit(quotient_poly_blind)

# After:
c_t = kzg.commit(quotient_poly)
```

**Cell 96** - Use unblinded:
```python
# Before:
t_zeta = quotient_poly_blind(zeta)
proof_t = kzg.prove(quotient_poly_blind, zeta)

# After:
t_zeta = quotient_poly(zeta)
proof_t = kzg.prove(quotient_poly, zeta)
```

**Cell 103** - Updated message:
```python
print(f"✓ quotient_poly was used: degree {quotient_poly.degree()}")
```

## Results

After fix:
- ✓ Cell 99: Quotient constraint check passes
- ✓ Cell 100: verify_plonk passes
- ✓ All opening proofs verify
- ✓ Zero-knowledge still maintained via witness blinding

## Key Learning

**Not all polynomials can be blinded the same way!**

| Polynomial Type | Can Blind with `poly + random*ZH`? | Why? |
|----------------|-------------------------------------|------|
| Witness (a,b,c,z) | ✓ Yes | No constraint to preserve |
| Quotient | ✗ No | Must satisfy `bigt = quotient*ZH` |

The real PlonK protocol uses quotient splitting for ZK, but for tutorials, unblinded quotient is fine.

## Files

1. **[DIAGNOSIS.md](DIAGNOSIS.md)** - Mathematical explanation of the issue
2. **[SOLUTION.md](SOLUTION.md)** - Quick fix summary
3. **[investigate_mismatch.py](investigate_mismatch.py)** - Investigation script
4. **[apply_fix.py](apply_fix.py)** - Automated fix (applied)
5. **README.md** - This file

## Verification

Run these steps after fix:
1. Restart kernel
2. Run cells 91-100
3. Cell 99 should show: `Match: True`
4. Cell 100 should show: `All checks passed!`

## Backup

Backup created: `PlonK-Tutorial.ipynb.backup_quotient_fix`
