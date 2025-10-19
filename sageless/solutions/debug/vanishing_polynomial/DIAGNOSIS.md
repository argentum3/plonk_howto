# Vanishing Polynomial ZH_z Modular Arithmetic Bug

## Issue

User reports Cell 103 still failing with quotient constraint check.

The line:
```python
ZH_z = zeta_v**n - 1
```

is missing modular reduction.

## Analysis

In finite field arithmetic, ALL operations must reduce modulo p.

Current code at line 4645:
```python
ZH_z = zeta_v**n - 1
```

This computes a very large integer without reducing modulo p.

Then line 4648 compares:
```python
if master_poly_v == t_zeta * ZH_z:
```

Since `master_poly_v` and `t_zeta` are already reduced mod p, but `ZH_z` is not,
and the multiplication `t_zeta * ZH_z` is also not reduced, this comparison will fail.

## Fix

Line 4645 should be:
```python
ZH_z = (pow(zeta_v, n, p) - 1) % p
```

Or equivalently:
```python
ZH_z = (zeta_v**n - 1) % p
```

Using `pow(base, exp, p)` is more efficient for large exponents.

## Root Cause

Same as previous modular arithmetic bugs - missing `% p` reduction causes:
1. Large intermediate values that overflow Python's int comparison
2. Incorrect comparisons even though mathematical identity is correct

## Impact

This bug causes the final quotient constraint check to fail even when all
polynomial values are computed correctly.
