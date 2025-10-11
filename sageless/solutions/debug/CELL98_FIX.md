# Cell 98 Fix: Undefined Variable 'output'

## Problem

Cell 98 was trying to create a proof dictionary with all artifacts to send to the verifier, but it referenced an undefined variable `output`:

```python
'evaluations': {
    'value_a': value_a,
    'value_b': value_b,
    'output': output,  # ← Error: name 'output' is not defined
    'a_zeta': a_zeta,
    ...
}
```

This caused:
```
NameError: name 'output' is not defined
```

## Root Cause

The variable is actually called `value_c` (the output value c(ω^4) = 9 from Exercise 19), not `output`.

## Solution

Changed the reference from `output` to `value_c`:

```python
'evaluations': {
    'value_a': value_a,
    'value_b': value_b,
    'output': value_c,  # ✓ Fixed: now references correct variable
    'a_zeta': a_zeta,
    ...
}
```

## What Cell 98 Does

Cell 98 collects all proof artifacts into a dictionary that would be sent to the verifier:

### Commitments (5)
- c_a, c_b, c_c: Witness polynomial commitments
- c_z: Permutation accumulator commitment
- c_t: Quotient polynomial commitment

### Challenges (4)
- beta, gamma: Permutation challenges (Exercise 20)
- alpha: Constraint combination challenge (Exercise 21)
- zeta: Evaluation challenge (Exercise 22)

### Evaluations (9)
- value_a, value_b, value_c: Public inputs/outputs (Exercise 19)
- a_zeta, b_zeta, c_zeta: Witness evaluations at ζ (Exercise 22)
- z_zeta: Permutation accumulator at ζ (Exercise 22)
- t_zeta: Quotient evaluation at ζ (Exercise 22)
- z_zeta_omega: Permutation accumulator at ζ·ω (Exercise 22)

### Opening Proofs (9)
- proof_value_a, proof_value_b, proof_output: Proofs for public values (Exercise 19)
- proof_a, proof_b, proof_c: Proofs for witness evaluations (Exercise 22)
- proof_z: Proof for z at ζ (Exercise 22)
- proof_t: Proof for quotient at ζ (Exercise 22)
- proof_z_omega: Proof for z at ζ·ω (Exercise 22)

## Note on Variable Naming

Throughout the exercises, we've used consistent naming:
- `value_a = a(ω)` - input value
- `value_b = b(ω)` - input value
- `value_c = c(ω^4)` - output value

The key `'output'` in the dictionary makes sense semantically (it's the circuit output), but it should map to the variable `value_c`, not a non-existent variable called `output`.

## Verification

After the fix, cell 98 should run without errors and create the complete proof dictionary ready for the verifier.
