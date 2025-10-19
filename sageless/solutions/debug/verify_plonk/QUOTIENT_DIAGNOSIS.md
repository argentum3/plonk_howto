# Quotient Constraint Failure Diagnosis

## Summary

The quotient constraint check mathematically **passes** when all values are computed correctly. However, there's an architectural issue with how `verify_plonk` accesses N_poly and D_poly.

## Debug Results

Running `debug_quotient_constraint.py` shows:

```
✓✓✓ QUOTIENT CONSTRAINT CHECK PASSES ✓✓✓
```

All mathematical checks pass:
- Gate constraint at ζ: ✓
- Permutation start constraint at ζ: ✓
- Permutation step constraint at ζ: ✓
- Master polynomial equation: `master_poly(ζ) == t_zeta * ZH(ζ)` ✓

## The Real Issue: N_poly and D_poly Access

### What verify_plonk Does

In cell 100, verify_plonk calls:
```python
N_z = N_poly(zeta_v)
D_z = D_poly(zeta_v)
```

This assumes N_poly and D_poly are available in the global scope.

### Where N_poly and D_poly Come From

These are defined in cell 92 (Exercise 20):
```python
z_poly, N_poly, D_poly = interpolate_z_N_D(a_blind, b_blind, c_blind, beta, gamma, Ω)
```

**Critical problem**: N_poly and D_poly are computed from the witness polynomials (a_blind, b_blind, c_blind), which the verifier should NOT have access to in a real zero-knowledge proof system.

### Why This Matters

In the actual PlonK protocol, the verifier must be able to compute N(ζ) and D(ζ) without knowing the witness polynomials. Instead, the verifier should use:

1. **Public selector polynomials**: S_σ1, S_σ2, S_σ3 (permutation selectors)
2. **Witness evaluations from the proof**: a_zeta, b_zeta, c_zeta
3. **Challenge values**: β, γ

### Correct Verifier Computation

The verifier should compute:

```python
# N(ζ) - numerator of permutation argument
N_z = (a_zeta + beta*zeta_v + gamma) * \
      (b_zeta + beta*k1*zeta_v + gamma) * \
      (c_zeta + beta*k2*zeta_v + gamma)

# D(ζ) - denominator of permutation argument
D_z = (a_zeta + beta*S_sigma1(zeta_v) + gamma) * \
      (b_zeta + beta*S_sigma2(zeta_v) + gamma) * \
      (c_zeta + beta*S_sigma3(zeta_v) + gamma)
```

Where:
- k1, k2 are public coset generators
- S_sigma1, S_sigma2, S_sigma3 are public permutation selector polynomials
- a_zeta, b_zeta, c_zeta are provided in the proof

## Current Tutorial Architecture

The tutorial takes a shortcut for educational purposes:

1. **Prover side** (cells 91-96): Computes N_poly and D_poly from witness polynomials
2. **Verifier side** (cell 100): Reuses the prover's N_poly and D_poly from global scope

This works for the tutorial but isn't how a real implementation would work.

## Why The Check Might Be Failing

If you're seeing "Quotient constraint check failed!", the likely causes are:

### Possibility 1: N_poly/D_poly Not in Scope
If cells 91-92 haven't been run in the current kernel session, N_poly and D_poly won't be defined, causing an error.

**Solution**: Make sure cell 92 (Exercise 20) has been executed before running cell 100.

### Possibility 2: Kernel State Mismatch
If the notebook cells were run out of order, N_poly and D_poly might be from an earlier proof attempt with different challenges.

**Solution**: Run cells 91-96 in sequence, then run cell 98, then run cell 100.

### Possibility 3: Modular Arithmetic Issues
Python integer arithmetic can exceed the field modulus during intermediate computations.

**Solution**: The debug script shows this isn't the issue - all values match correctly.

## Verification

To verify the quotient constraint is mathematically correct, the debug script shows:

```
LHS (master_poly(ζ)) = 3885249990729996212842747704758551423564885776737667845155142691670933249891
RHS (t_zeta * ZH(ζ)) = 3885249990729996212842747704758551423564885776737667845155142691670933249891
Equal: True
```

## Recommendations

### For Tutorial Use
The current approach is fine for learning - just ensure cells are run in order.

### For Production Implementation
The verifier should:
1. NOT rely on N_poly and D_poly from prover
2. Compute N(ζ) and D(ζ) using the formula above with public parameters
3. Require S_sigma1, S_sigma2, S_sigma3 polynomials as part of the public setup

## Testing

Run the debug script to verify mathematical correctness:
```bash
./run.sh sageless/solutions/debug/verify_plonk/debug_quotient_constraint.py
```

This confirms the quotient constraint equation holds correctly when all values are properly computed.
