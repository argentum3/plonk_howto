# Debugging Quotient Constraint Failure

## Problem

After running the notebook cells chronologically, `verify_plonk()` fails with:
```
Verifier result: False
Quotient constraint check failed!
```

## Debug Approach

Since you've confirmed cells are run in order, we need to check the actual values being computed in the notebook environment.

## Step-by-Step Debugging

### Option 1: Run Inline Checker (RECOMMENDED)

Add a **new cell** in your notebook right after cell 98 (before cell 100), and paste this code:

```python
%run sageless/solutions/debug/verify_plonk/check_notebook_values_inline.py
```

This will:
1. Check that all required variables (N_poly, D_poly, etc.) are defined
2. Compute the verifier's values step-by-step
3. Compare LHS (master_poly) vs RHS (t_zeta * ZH)
4. Show exactly where the mismatch occurs

### Option 2: Copy-Paste Debug Code

If you prefer, create a new cell and paste the code from:
```
sageless/solutions/debug/verify_plonk/check_notebook_values.py
```

This file contains the inline code you can copy directly.

### Option 3: Manual Inspection

Add a new cell after cell 98 and run:

```python
# Check the critical values
print("Challenges:")
print(f"  zeta = {zeta}")
print(f"  alpha = {alpha}")
print(f"  beta = {beta}")
print(f"  gamma = {gamma}")

# Check if N_poly and D_poly exist
print("\nPermutation polynomials:")
try:
    print(f"  N_poly(zeta) = {N_poly(zeta)}")
    print(f"  D_poly(zeta) = {D_poly(zeta)}")
except NameError as e:
    print(f"  ERROR: {e}")

# Check the quotient constraint manually
qL_z = qL(zeta)
qR_z = qR(zeta)
qM_z = qM(zeta)
L1_z = L1(zeta)
N_z = N_poly(zeta)
D_z = D_poly(zeta)
zeta_omega = (zeta * ω) % p

t_gates_v = (qM_z * a_zeta * b_zeta + qL_z * a_zeta + qR_z * b_zeta - c_zeta) % p
t_perm_start_v = ((z_zeta - 1) * L1_z) % p
t_perm_step_v = (z_zeta * N_z - D_z * z_zeta_omega) % p

master_poly_v = (t_gates_v + alpha * t_perm_start_v + (alpha * alpha) % p * t_perm_step_v) % p
ZH_z = (pow(zeta, 4, p) - 1) % p
rhs = (t_zeta * ZH_z) % p

print(f"\nQuotient constraint check:")
print(f"  LHS (master_poly): {master_poly_v}")
print(f"  RHS (t_zeta*ZH):   {rhs}")
print(f"  Match: {master_poly_v == rhs}")

if master_poly_v != rhs:
    print(f"\nDifference: {(master_poly_v - rhs) % p}")
```

## What to Look For

The debug output will show:

1. **If N_poly/D_poly are undefined**: Means cell 92 wasn't run or kernel was restarted
   - **Solution**: Re-run cells 91-92

2. **If values mismatch**: Will show exact component that's wrong
   - Check `t_gates(ζ)` vs direct polynomial evaluation
   - Check `t_perm_start(ζ)` vs direct polynomial evaluation
   - Check `t_perm_step(ζ)` vs direct polynomial evaluation

3. **If LHS ≠ RHS**: Will show the difference
   - This indicates an issue with how the quotient polynomial was computed or blinded

## Common Issues

### Issue 1: Blinding Randomness Mismatch

If the blinding factors used for `quotient_poly_blind` don't match between prover and verifier, the check will fail.

**Check**: In cell 94 (Exercise 21), verify that `quotient_poly_blind` is created correctly:
```python
quotient_poly_blind = quotient_poly + random_poly_t * ZH
```

### Issue 2: z_poly vs z_poly_blind Confusion

The verifier uses `z_zeta` from the proof, which should be `z_poly_blind(zeta)`, not `z_poly(zeta)`.

**Check**: In cell 96 (Exercise 22), verify:
```python
z_zeta = z_poly_blind(zeta)  # Should use BLIND version
```

### Issue 3: N_poly and D_poly Computed with Wrong Polynomial

N_poly and D_poly should be computed from **blinded** witness polynomials.

**Check**: In cell 92 (Exercise 20), verify:
```python
z_poly, N_poly, D_poly = interpolate_z_N_D(a_blind, b_blind, c_blind, beta, gamma, Ω)
```

NOT from unblinded `a`, `b`, `c`.

### Issue 4: Modular Arithmetic Overflow

Python can compute large integers without overflow, but if intermediate values aren't reduced modulo p, you might get wrong results.

**Check**: Look for operations like:
```python
# WRONG - no modulo
result = a * b * c + d * e * f

# RIGHT - with modulo
result = (a * b % p * c % p + d * e % p * f % p) % p
```

## Files in This Directory

- `check_notebook_values_inline.py` - Run from notebook with `%run`
- `check_notebook_values.py` - Contains copy-pasteable code
- `debug_quotient_constraint.py` - Standalone reconstruction (shows it SHOULD work)
- `debug_quotient_detailed.py` - Detailed standalone debug (incomplete)
- `QUOTIENT_DIAGNOSIS.md` - Architectural explanation of the issue
- `README_QUOTIENT_DEBUG.md` - This file

## Next Steps

1. Run the inline checker in your notebook
2. Share the output with me
3. We'll identify the exact source of the mismatch

The fact that `debug_quotient_constraint.py` passes when run standalone suggests the issue is likely:
- A variable scope issue (wrong polynomial being used)
- A blinding factor mismatch
- An unblinded vs blinded polynomial confusion
