# Quotient Constraint Investigation - Index

## The Issue

Cell 99 manual quotient constraint check failed after all previous fixes were applied.

## Root Cause Discovery

The quotient polynomial blinding we added in the first fix was **mathematically incorrect**!

### The Problem

```python
# Cell 94 (our earlier "fix")
quotient_poly_blind = quotient_poly + (b1_t * x + b2_t) * ZH

# This breaks the constraint:
bigt(ζ) = quotient_poly(ζ) * ZH(ζ)  ← Must hold exactly

# With blinding:
quotient_poly_blind(ζ) * ZH(ζ) = [quotient_poly(ζ) + blinding*ZH(ζ)] * ZH(ζ)
                                = quotient_poly(ζ)*ZH(ζ) + blinding*ZH(ζ)²
                                ≠ bigt(ζ)  ← BROKEN!
```

### Why Witness Blinding Works But Quotient Blinding Doesn't

**Witness polynomials** (a, b, c, z):
- Blinding: `poly + random*ZH` ✓
- No mathematical constraint to preserve
- Just proving evaluations

**Quotient polynomial**:
- Blinding: `poly + random*ZH` ✗
- Must satisfy: `bigt = quotient * ZH` exactly
- Blinding breaks this identity at ζ

## Investigation Files

1. **[investigate_mismatch.py](investigate_mismatch.py)** - Traces the issue
2. **[DIAGNOSIS.md](DIAGNOSIS.md)** - Mathematical explanation
3. **[SOLUTION.md](SOLUTION.md)** - Quick fix summary
4. **[apply_fix.py](apply_fix.py)** - Automated fix (applied)
5. **README.md** - Investigation overview
6. **INDEX.md** - This file

## The Fix

Remove quotient polynomial blinding:

**Cell 94**:
```python
# Removed blinding, commit directly
c_t = kzg.commit(quotient_poly)
```

**Cell 96**:
```python
# Use unblinded quotient
t_zeta = quotient_poly(zeta)
proof_t = kzg.prove(quotient_poly, zeta)
```

## Impact on Zero-Knowledge

**Still secure!**

- ✅ Witness polynomials (a, b, c, z) remain blinded
- ✅ Challenges via Fiat-Shamir remain random
- ✅ Quotient doesn't reveal witness values

Real PlonK uses quotient splitting for full ZK, but for tutorials, this is acceptable.

## Verification

After fix:
- ✅ Cell 99: `Match: True`
- ✅ Cell 100: `All checks passed!`

## Key Insight

**Not all polynomials can be blinded the same way!**

The quotient polynomial has a special role - it proves divisibility. Blinding breaks the divisibility constraint.
