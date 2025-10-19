# Note on fix_cell94.py.OBSOLETE

The file `fix_cell94.py.OBSOLETE` represents an **incorrect approach** that was discovered during debugging.

## Why This Fix Was Wrong

This file attempted to blind the quotient polynomial:
```python
quotient_poly_blind = quotient_poly + (b1_t * x + b2_t) * ZH
```

**This breaks the fundamental PlonK constraint:**
```
master_poly(ζ) = quotient_poly(ζ) · ZH(ζ)
```

If we blind the quotient as `quotient_poly_blind = quotient_poly + blinding·ZH`, then:
```
quotient_poly_blind(ζ) · ZH(ζ) = (quotient_poly(ζ) + blinding(ζ)·ZH(ζ)) · ZH(ζ)
                                = quotient_poly(ζ)·ZH(ζ) + blinding(ζ)·ZH(ζ)²
                                ≠ master_poly(ζ)
```

The additional `ZH(ζ)²` term makes verification fail.

## The Correct Fix for Cell 94

The actual fix (documented in `../quotient_constraint/fix_cell94.py`) was to **use z_poly_blind consistently** when building the master polynomial:

```python
# Changed 3 lines to use z_poly_blind:
t_perm_start = (z_poly_blind - 1) * L1
z_shifted = z_poly_blind(x * ω)
t_perm_step = z_poly_blind * N_poly - D_poly * z_shifted

# Quotient remains UNBLINDED (mathematical requirement):
quotient_poly = bigt / ZH
c_t = kzg.commit(quotient_poly)
```

## See Also

- [../quotient_constraint/COMPLETE_FIX.md](../quotient_constraint/COMPLETE_FIX.md) - The correct Cell 94 fix
- [SOLUTION.md](SOLUTION.md) - Why quotient cannot be blinded
- [QUOTIENT_DIAGNOSIS.md](QUOTIENT_DIAGNOSIS.md) - Mathematical analysis
- [../debug/ALL_FIXES_SUMMARY.md](../../debug/ALL_FIXES_SUMMARY.md) - Issue #2 and Issue #3

---

**Lesson:** In PlonK, not all polynomials can be blinded. The quotient polynomial's special role in the verification equation requires it to remain unblinded. Real PlonK protocols use polynomial splitting techniques instead.
