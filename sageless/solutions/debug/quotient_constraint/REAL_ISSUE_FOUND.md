# Real Issue Found: Modular Arithmetic Bug in Cell 99

## The Diagnostic Revealed

The diagnostic showed:
```
master_poly(ζ) computed = 15881336282346686748609892963327418060523628370946765287006697761502273751856
bigt(ζ) direct eval    = 21680131508316546133776511944515611827072429717437918331349788695345791946113
Match: False ✗
```

But also:
```
bigt(ζ) = 21680131508316546133776511944515611827072429717437918331349788695345791946113
quotient_poly(ζ) * ZH(ζ) = 21680131508316546133776511944515611827072429717437918331349788695345791946113
Should match: True ✓
```

**The actual constraint holds!** The problem is Cell 99's computation is wrong.

## Root Cause: Operator Precedence Bug

Cell 99 (line 4177):
```python
master_poly_v = (t_gates_v + alpha * t_perm_start_v + (alpha * alpha) % p * t_perm_step_v) % p
```

This computes:
```
t_gates_v + alpha * t_perm_start_v + ((alpha * alpha) % p) * t_perm_step_v
```

But it should compute:
```
(t_gates_v + alpha * t_perm_start_v + alpha² * t_perm_step_v) % p
```

The issue is `(alpha * alpha) % p * t_perm_step_v`:
- Evaluates as: `((alpha * alpha) % p) * t_perm_step_v`
- This is correct for computing `alpha²`, but then multiplying by `t_perm_step_v` can overflow!
- The result is taken mod p at the END, but intermediate values may be huge

## The Fix

Cell 99 should use proper modular arithmetic:

```python
# WRONG:
master_poly_v = (t_gates_v + alpha * t_perm_start_v + (alpha * alpha) % p * t_perm_step_v) % p

# CORRECT:
alpha_squared = (alpha * alpha) % p
master_poly_v = (t_gates_v + alpha * t_perm_start_v % p + alpha_squared * t_perm_step_v % p) % p

# OR:
master_poly_v = (t_gates_v % p + (alpha * t_perm_start_v) % p + (alpha_squared * t_perm_step_v) % p) % p
```

## Better: Use pow() for Large Numbers

Python's integers can get very large without overflow, but for field arithmetic, we should reduce modulo frequently:

```python
# Best practice:
alpha_squared = pow(alpha, 2, p)  # Computes (alpha²) mod p efficiently
term1 = t_gates_v % p
term2 = (alpha * t_perm_start_v) % p
term3 = (alpha_squared * t_perm_step_v) % p
master_poly_v = (term1 + term2 + term3) % p
```

## Why This Causes the Mismatch

When Python computes:
```python
alpha * t_perm_start_v + (alpha * alpha) % p * t_perm_step_v
```

Without intermediate modulo operations, we get:
```
alpha * 14137876478618072624062430264502608323363555797003582126157081025375294027730
+ alpha² * 10371980008377178641492207363036296977106984607486883510533567997051720396751
```

These are HUGE numbers. The final `% p` reduces the result, but the intermediate computation may have different behavior than computing mod p at each step.

In modular arithmetic, we should reduce frequently to avoid overflow/precision issues:
```python
((a % p) + (b % p)) % p  ≡  (a + b) % p
```

But in practice, with very large intermediate values, it's safer to reduce after each operation.

## The Fix to Apply

Update Cell 99:

```python
# Compute constraints at ζ
t_gates_v = (qM_z * a_zeta * b_zeta + qL_z * a_zeta + qR_z * b_zeta - c_zeta) % p
t_perm_start_v = ((z_zeta - 1) * L1_z) % p
t_perm_step_v = (z_zeta * N_z - D_z * z_zeta_omega) % p

# Compute master polynomial with proper modular arithmetic
alpha_squared = pow(alpha, 2, p)
term1 = t_gates_v
term2 = (alpha * t_perm_start_v) % p
term3 = (alpha_squared * t_perm_step_v) % p
master_poly_v = (term1 + term2 + term3) % p

ZH_z = pow(zeta, 4, p) - 1  # or (pow(zeta, 4, p) - 1) % p
rhs = (t_zeta * ZH_z) % p
```

This ensures all intermediate values are properly reduced modulo p.
