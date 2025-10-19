# CRITICAL ISSUE: verify_plonk Missing Variable Extraction

## The Problem

The `verify_plonk` function at line 4628-4633 uses variables:
- `a_zeta`
- `b_zeta`
- `c_zeta`
- `z_zeta`
- `z_zeta_omega`
- `t_zeta`

**BUT THESE VARIABLES ARE NEVER EXTRACTED FROM proof_dictionary!**

## Evidence

Line 4628:
```python
t_gates_v = (qM_z*a_zeta*b_zeta + qL_z*a_zeta+qR_z*b_zeta-c_zeta) % p
```

Line 4632-4633:
```python
t_perm_start_v = (z_zeta - 1) * L1_z
t_perm_step_v = (z_zeta * N_z - D_z * z_zeta_omega) % p
```

Line 4648:
```python
if master_poly_v == t_zeta * ZH_z:
```

## The verify_plonk function structure:

1. Lines 4564-4592: Regenerate challenges (beta_v, gamma_v, alpha_v, zeta_v) ✓
2. Lines 4596-4618: Perform pairing checks ✓
3. Lines 4620-4625: Compute selector polynomials at zeta_v ✓
4. Lines 4628-4648: **USE UNDEFINED VARIABLES** ✗

## Why This Breaks

The variables `a_zeta`, `b_zeta`, `c_zeta`, `z_zeta`, `z_zeta_omega`, `t_zeta`
are defined in earlier cells (from Exercise 22) but they are **global notebook variables**,
not extracted from the proof_dictionary.

This means:
1. verify_plonk is using stale values from the notebook environment
2. If you call verify_plonk with a different proof, it will use the old values
3. The function is NOT self-contained

## What Should Happen

After the pairing checks (line 4618), we need to extract these values:

```python
# Extract evaluated values from proof dictionary
a_zeta = proof_dictionary['evaluations']['a_zeta']
b_zeta = proof_dictionary['evaluations']['b_zeta']
c_zeta = proof_dictionary['evaluations']['c_zeta']
z_zeta = proof_dictionary['evaluations']['z_zeta']
z_zeta_omega = proof_dictionary['evaluations']['z_zeta_omega']
t_zeta = proof_dictionary['evaluations']['t_zeta']
```

## Investigation Needed

We need to:
1. Check what's actually in proof_dictionary
2. Verify the key names match what we're trying to extract
3. Add the extraction code to verify_plonk
4. Ensure all modular arithmetic is correct

## Impact

This is why verify_plonk is failing - it's using the wrong values for the constraint checks!
