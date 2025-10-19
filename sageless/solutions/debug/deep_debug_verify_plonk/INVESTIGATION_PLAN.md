# Deep Debug verify_plonk - Investigation Plan

## Critical Issue Discovered

The `verify_plonk` function (Cell 103) uses variables like `a_zeta`, `b_zeta`, `c_zeta`, `z_zeta`, `z_zeta_omega`, `t_zeta` **without extracting them from proof_dictionary**.

This means it's using global notebook variables, not the values from the proof!

## What I've Done

1. **Created comprehensive diagnostic cell** - Inserted after Cell 98 (proof_dictionary creation)
2. **Diagnostic will show**:
   - All keys in proof_dictionary
   - Values extracted from proof_dictionary['evaluations']
   - Global notebook variables
   - Comparison: are they the same?
   - Constraint computations using both sets of values
   - Exact breakdown of master_poly_v computation
   - Where the quotient constraint fails

## What to Look For

When you run the diagnostic cell, check:

### Scenario 1: Values Match
If `proof_dictionary['evaluations']` values match global variables:
- The issue is likely modular arithmetic in verify_plonk
- Look at section 11 of diagnostic (modular arithmetic check)
- Specifically check if `t_perm_start_v` needs `% p`

### Scenario 2: Values Don't Match
If they don't match:
- This confirms verify_plonk is using wrong values
- Need to extract values from proof_dictionary
- Fix: Add extraction code after line 4618 in verify_plonk

### Scenario 3: Quotient Constraint Passes with Proof Values
If section 9 shows "MATCH (using proof values): True":
- The proof is actually valid!
- verify_plonk just needs to extract values correctly
- Simple fix: add variable extraction

### Scenario 4: Quotient Constraint Fails with Both
If both proof and global values fail:
- Problem is in proof generation (Cells 92-96)
- Look at section 10 for exact difference
- Check if t_perm_start_v computation is wrong

## Most Likely Issue

Based on the code structure, I believe the issue is:

**verify_plonk needs to extract variables from proof_dictionary**

Add this code at line 4619 (after pairing checks, before constraint checks):

```python
# Extract evaluated values from proof dictionary
a_zeta = proof_dictionary['evaluations']['a_zeta']
b_zeta = proof_dictionary['evaluations']['b_zeta']
c_zeta = proof_dictionary['evaluations']['c_zeta']
z_zeta = proof_dictionary['evaluations']['z_zeta']
z_zeta_omega = proof_dictionary['evaluations']['z_zeta_omega']
t_zeta = proof_dictionary['evaluations']['t_zeta']
```

## Additional Issues to Check

1. **Modular arithmetic on line 4632** (t_perm_start_v):
   ```python
   # Current:
   t_perm_start_v = (z_zeta - 1) * L1_z

   # Should be:
   t_perm_start_v = ((z_zeta - 1) * L1_z) % p
   ```

2. **Modular arithmetic on line 4648** (final comparison):
   ```python
   # Current:
   if master_poly_v == t_zeta * ZH_z:

   # Should be:
   if master_poly_v == (t_zeta * ZH_z) % p:
   ```

## Next Steps After Running Diagnostic

1. **Run the diagnostic cell** and save the output
2. **Analyze the output** to determine which scenario above applies
3. **Create targeted fix** based on findings:
   - If values match: fix modular arithmetic
   - If values don't match: add extraction code
   - If constraint passes with proof values: just add extraction
4. **Apply fix** to verify_plonk
5. **Test** that verify_plonk passes

## Files in This Debug Directory

- `README.md` - Overview
- `CRITICAL_ISSUE_FOUND.md` - Initial analysis
- `INVESTIGATION_PLAN.md` - This file
- `diagnostic_comprehensive.py` - Diagnostic code (for reference)
- `insert_diagnostic.py` - Script that inserted diagnostic cell
- `fix_verify_plonk_final.py` - Will create after seeing diagnostic output

## Core PlonK Logic

**IMPORTANT**: All fixes must preserve PlonK correctness:

1. ✓ Don't blind quotient polynomial (we already fixed this)
2. ✓ Use z_poly_blind consistently (we already fixed this)
3. ✓ All field arithmetic must reduce modulo p
4. ✓ verify_plonk must use values from proof_dictionary, not globals
5. ✓ Fiat-Shamir transcript must be reconstructed identically

The quotient constraint MUST hold:
```
master_poly(ζ) = quotient_poly(ζ) * ZH(ζ)
```

Where:
```
master_poly(ζ) = t_gates(ζ) + α·t_perm_start(ζ) + α²·t_perm_step(ζ)
```

This is the fundamental PlonK identity that proves the computation is correct.
