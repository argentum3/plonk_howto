# Cell 103 verify_plonk Modular Arithmetic Issue

## Problem

Cell 103 (verify_plonk function) is failing the quotient constraint check even though all the fixes have been applied.

## Root Cause

The `verify_plonk` function has the SAME modular arithmetic bug we fixed in Cell 99!

### Line 4637:
```python
master_poly_v = t_gates_v + alpha_v * t_perm_start_v + alpha_v**2 * t_perm_step_v
```

This computes:
- `alpha_v * t_perm_start_v` → very large number
- `alpha_v**2 * t_perm_step_v` → even larger number
- Adds them without reducing modulo p
- No final `% p` operation

### Also Missing Modulo in Lines 4628, 4633:
```python
t_gates_v = qM_z*a_zeta*b_zeta + qL_z*a_zeta+qR_z*b_zeta-c_zeta
t_perm_step_v = z_zeta * N_z - D_z * z_zeta_omega
```

These also create large intermediate values without reduction.

## The Issue

In field arithmetic over a prime p, all operations should be reduced modulo p:
```python
(a + b) mod p ≠ (a mod p + b mod p) mod p  (sometimes, due to overflow)
```

When working with very large numbers (cryptographic field elements), we must reduce frequently to avoid:
1. Integer overflow (Python handles this, but...)
2. Precision issues with comparisons
3. Incorrect results when not properly reduced

## The Fix

Change line 4628:
```python
# FROM:
t_gates_v = qM_z*a_zeta*b_zeta + qL_z*a_zeta+qR_z*b_zeta-c_zeta

# TO:
t_gates_v = (qM_z*a_zeta*b_zeta + qL_z*a_zeta+qR_z*b_zeta-c_zeta) % p
```

Change line 4633:
```python
# FROM:
t_perm_step_v = z_zeta * N_z - D_z * z_zeta_omega

# TO:
t_perm_step_v = (z_zeta * N_z - D_z * z_zeta_omega) % p
```

Change line 4637:
```python
# FROM:
master_poly_v = t_gates_v + alpha_v * t_perm_start_v + alpha_v**2 * t_perm_step_v

# TO:
alpha_v_squared = pow(alpha_v, 2, p)
term1 = t_gates_v
term2 = (alpha_v * t_perm_start_v) % p
term3 = (alpha_v_squared * t_perm_step_v) % p
master_poly_v = (term1 + term2 + term3) % p
```

Or more compactly:
```python
# TO (compact):
master_poly_v = (t_gates_v + alpha_v * t_perm_start_v + pow(alpha_v, 2, p) * t_perm_step_v) % p
```

## Why We Need This

The verifier computes:
```
LHS = master_poly_v (from constraints)
RHS = t_zeta * ZH_z (from proof)
```

If LHS isn't properly reduced modulo p, the comparison `LHS == RHS` will fail even though they're equivalent in the field.

## Same Issue as Cell 99

We fixed this exact issue in Cell 99 (line 4189). Now we need to fix it in verify_plonk (Cell 103, line 4637).

This is the last remaining modular arithmetic bug!
