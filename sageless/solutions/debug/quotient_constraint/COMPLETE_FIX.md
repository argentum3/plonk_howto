# Complete Fix: Cell 94 Uses Wrong Polynomial

## The Real Problem

**Cell 94 (Exercise 21) uses `z_poly` instead of `z_poly_blind` when building the master polynomial!**

## What the Diagnostic Revealed

```
master_poly(ζ) = 18019780481302730032116641672764688116579078714796190459725174446154238444939
bigt(ζ) direct = 10377191041174401129614098168019476770558042062426031968427002113321734186927
Match: False ✗
```

These are completely different values! This means `bigt` is built incorrectly.

## Root Cause

Cell 94 had these lines:
```python
# ❌ WRONG - uses z_poly (unblinded)
t_perm_start = (z_poly - 1) * L1
z_shifted = z_poly(x * ω)
t_perm_step = z_poly * N_poly - D_poly * z_shifted
bigt = t_gates + alpha * t_perm_start + (alpha * alpha) * t_perm_step
```

But it should use `z_poly_blind` because:
1. Cell 92 defines and commits to `z_poly_blind`
2. Cell 96 evaluates `z_poly_blind(zeta)`
3. All constraints must use the SAME polynomial

## Why This Broke

The flow should be:
```
Cell 92: Create z_poly_blind, commit c_z
Cell 94: Build bigt using z_poly_blind, compute quotient
Cell 96: Evaluate z_poly_blind(ζ), quotient_poly(ζ)
Cell 99: Check bigt(ζ) = quotient_poly(ζ) * ZH(ζ)
```

But Cell 94 used `z_poly` instead of `z_poly_blind`, so:
```
bigt uses z_poly (unblinded)
z_zeta from z_poly_blind(ζ) (blinded)
→ bigt(ζ) ≠ master_poly_v computed from z_zeta
```

## The Fix Applied

Changed Cell 94 to use `z_poly_blind`:

```python
# ✓ CORRECT - uses z_poly_blind (blinded)
t_perm_start = (z_poly_blind - 1) * L1
z_shifted = z_poly_blind(x * ω)
t_perm_step = z_poly_blind * N_poly - D_poly * z_shifted
bigt = t_gates + alpha * t_perm_start + (alpha * alpha) * t_perm_step
```

## Summary of All Fixes to Cell 94

### Change 1: Remove quotient_poly_blind (earlier fix)
- Was: `quotient_poly_blind = quotient_poly + blinding * ZH`
- Now: Commit directly to `quotient_poly`

### Change 2: Use z_poly_blind (current fix)
- Was: `t_perm_start = (z_poly - 1) * L1`
- Now: `t_perm_start = (z_poly_blind - 1) * L1`

- Was: `z_shifted = z_poly(x * ω)`
- Now: `z_shifted = z_poly_blind(x * ω)`

- Was: `t_perm_step = z_poly * N_poly - D_poly * z_shifted`
- Now: `t_perm_step = z_poly_blind * N_poly - D_poly * z_shifted`

## Why This Works

Now all cells use consistent polynomials:

| Cell | Polynomial Used |
|------|----------------|
| Cell 92 | Defines `z_poly_blind`, commits `c_z = commit(z_poly_blind)` |
| Cell 94 | Uses `z_poly_blind` in constraints, builds `bigt` |
| Cell 96 | Evaluates `z_poly_blind(ζ)` |
| Cell 99 | Computes `master_poly_v` from `z_zeta = z_poly_blind(ζ)` |

All based on `z_poly_blind`! ✓

## Complete Fix History

1. ❌ Added `quotient_poly_blind` (broke quotient constraint)
2. ✅ Removed `quotient_poly_blind`
3. ❌ Cell 99 modular arithmetic issue
4. ✅ Fixed Cell 99 modular arithmetic
5. ❌ Cell 94 used `z_poly` instead of `z_poly_blind`
6. ✅ Fixed Cell 94 to use `z_poly_blind` (THIS FIX)

## Backups Created

1. `.backup_quotient_fix` - After removing quotient_poly_blind
2. `.backup_cell99_fix` - After fixing Cell 99 modular arithmetic
3. `.backup_cell94_z_poly_fix` - After fixing Cell 94 z_poly_blind (current)

## How to Apply

1. **Close and reopen** notebook in Jupyter
2. **Restart kernel**
3. **Run cells 91-100**

## Expected Results

Cell 94 output should show:
```
Computing t_perm_start...
Computing z_shifted and t_perm_step...
Computing master polynomial bigt...
  bigt = t_gates + α·t_perm_start + α²·t_perm_step
```
(Code uses `z_poly_blind` internally)

Cell 99 output:
```
Quotient constraint check:
  LHS (master_poly): [value]
  RHS (t_zeta*ZH):   [value]
  Match: True  ✓
```

Cell 100 output:
```
Quotient constraint holds.
Verifier result: True All checks passed!
```
