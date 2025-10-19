# Fix Instructions for Quotient Constraint Failure

## Root Cause

The diagnostic revealed **TWO BUGS**:

1. **Cell 94 (Exercise 21)**: Does NOT create `quotient_poly_blind`, only `quotient_poly`
2. **Cell 96 (Exercise 22)**: Uses unblinded `z_poly` and `quotient_poly` instead of blinded versions

## Why This Matters

The master polynomial `bigt` is constructed from **blinded** polynomials:
```python
bigt = t_gates + alpha * t_perm_start + alpha^2 * t_perm_step
```

Where:
- `t_gates` uses `a_blind`, `b_blind`, `c_blind`
- `t_perm_start` uses `z_poly_blind`
- `t_perm_step` uses `z_poly_blind`, `N_poly`, `D_poly`

Therefore, the quotient polynomial should be:
```python
quotient_poly = bigt / ZH  # This is based on BLINDED polynomials
```

And evaluations must use the blinded version.

## The Evidence

Your diagnostic showed:
```
Current z_zeta_omega: 15426623832310455175124265049380216935164090373349890937272801789861857222680
Should be z_poly_blind(ζ·ω): 3940837869981039717610763274790657016477022911600274195300739646073818338082
Match: False
```

This mismatch causes the quotient constraint to fail.

## Fix #1: Cell 94 (Exercise 21)

**Current code** (line ~3825):
```python
# Commit to quotient
c_t = kzg.commit(quotient_poly)
```

**Add BEFORE that line**:
```python
# Blind the quotient polynomial (for zero-knowledge)
# We add random multiples of ZH since quotient_poly * ZH = bigt
# and bigt is already based on blinded witness polynomials
b1_t, b2_t = 55555, 66666  # Random blinding factors
quotient_poly_blind = quotient_poly + (b1_t * x + b2_t) * ZH

print(f"\nBlinding quotient polynomial:")
print(f"  quotient_poly_blind = quotient_poly + ({b1_t}·x + {b2_t}) · ZH")
print(f"  quotient_poly_blind: degree {quotient_poly_blind.degree()}")
```

**Then change the commitment line to**:
```python
# Commit to blinded quotient
c_t = kzg.commit(quotient_poly_blind)
```

### Complete Cell 94 Fix

Find the section that says:
```python
# Commit to quotient
c_t = kzg.commit(quotient_poly)
print(f"\nCommitment to quotient:")
print(f"  c_t = {c_t}")
```

Replace with:
```python
# Blind the quotient polynomial (for zero-knowledge)
b1_t, b2_t = 55555, 66666
quotient_poly_blind = quotient_poly + (b1_t * x + b2_t) * ZH

print(f"\nBlinding quotient polynomial:")
print(f"  quotient_poly_blind = quotient_poly + ({b1_t}·x + {b2_t}) · ZH")
print(f"  quotient_poly_blind: degree {quotient_poly_blind.degree()}")

# Commit to blinded quotient
c_t = kzg.commit(quotient_poly_blind)
print(f"\nCommitment to blinded quotient:")
print(f"  c_t = {c_t}")
```

## Fix #2: Cell 96 (Exercise 22)

**Current code** (lines ~3963-3973):
```python
z_zeta = z_poly(zeta)
print(f"z_zeta = z_poly(ζ) = {z_zeta}")

t_zeta = quotient_poly(zeta)
print(f"t_zeta = quotient_poly(ζ) = {t_zeta}")

# Evaluate z_poly at ζ·ω
zeta_omega = (zeta * ω) % p
print(f"\nζ·ω = {zeta_omega}")

z_zeta_omega = z_poly(zeta_omega)
print(f"z_zeta_omega = z_poly(ζ·ω) = {z_zeta_omega}")
```

**Change to**:
```python
z_zeta = z_poly_blind(zeta)
print(f"z_zeta = z_poly_blind(ζ) = {z_zeta}")

t_zeta = quotient_poly_blind(zeta)
print(f"t_zeta = quotient_poly_blind(ζ) = {t_zeta}")

# Evaluate z_poly_blind at ζ·ω
zeta_omega = (zeta * ω) % p
print(f"\nζ·ω = {zeta_omega}")

z_zeta_omega = z_poly_blind(zeta_omega)
print(f"z_zeta_omega = z_poly_blind(ζ·ω) = {z_zeta_omega}")
```

**Also update the proof generation** (lines ~3992-3998):
```python
# OLD
proof_z = kzg.prove(z_poly, zeta)
print(f"  ✓ proof_z = prove(z_poly, ζ)")

proof_t = kzg.prove(quotient_poly, zeta)
print(f"  ✓ proof_t = prove(quotient_poly, ζ)")

proof_z_omega = kzg.prove(z_poly, zeta_omega)
print(f"  ✓ proof_z_omega = prove(z_poly, ζ·ω)")
```

**Change to**:
```python
# NEW
proof_z = kzg.prove(z_poly_blind, zeta)
print(f"  ✓ proof_z = prove(z_poly_blind, ζ)")

proof_t = kzg.prove(quotient_poly_blind, zeta)
print(f"  ✓ proof_t = prove(quotient_poly_blind, ζ)")

proof_z_omega = kzg.prove(z_poly_blind, zeta_omega)
print(f"  ✓ proof_z_omega = prove(z_poly_blind, ζ·ω)")
```

## Summary of Changes

### Cell 94 - Add blinding for quotient polynomial
- Create `quotient_poly_blind = quotient_poly + (b1_t * x + b2_t) * ZH`
- Commit to `quotient_poly_blind` instead of `quotient_poly`

### Cell 96 - Use blinded polynomials everywhere
- Change `z_poly(zeta)` → `z_poly_blind(zeta)`
- Change `quotient_poly(zeta)` → `quotient_poly_blind(zeta)`
- Change `z_poly(zeta_omega)` → `z_poly_blind(zeta_omega)`
- Change all `kzg.prove(z_poly, ...)` → `kzg.prove(z_poly_blind, ...)`
- Change `kzg.prove(quotient_poly, ...)` → `kzg.prove(quotient_poly_blind, ...)`

## After Applying Fixes

Run cells in order:
1. Cell 92 (Exercise 20) - defines `z_poly_blind`
2. Cell 94 (Exercise 21) - now defines `quotient_poly_blind` ✓
3. Cell 96 (Exercise 22) - now uses blinded versions ✓
4. Cell 98 - assembles proof
5. Cell 100 - verify_plonk should now pass ✓

## Why This Works

The verifier checks:
```
master_poly(ζ) == t_zeta * ZH(ζ)
```

Where:
- Left side: Computed from constraint polynomials at ζ
- Right side: `t_zeta * ZH(ζ)`

If `t_zeta` comes from unblinded `quotient_poly(ζ)`, but the master polynomial is built from blinded witness polynomials, they won't match.

The blinding factors add `random * ZH` terms. When divided by `ZH`, these become `random` terms in the quotient. Both sides must use the same blinding to match.

## Verification

After fixes, you should see:
```
Quotient constraint holds.
Verifier result: True All checks passed!
```
