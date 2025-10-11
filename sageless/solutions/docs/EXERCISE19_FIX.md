# Exercise 19 Fix: KZG API Update

## Problem

Cell 89 (now cell 90) in the notebook was using `kzg.commit()` and `kzg.prove()` functions that didn't exist in the kzg module, causing:

```
AttributeError: module 'kzg' has no attribute 'commit'
```

The notebook had defined lower-level functions `commitment(S1, poly)` and `proof(S1, Qc)` but cell 89 was expecting a simpler API.

## Solution

### 1. Added KZG Helper Functions

Updated [sageless/kzg.py](sageless/kzg.py) to include:

- `kzg.set_trusted_setup(S1, S2)` - Initialize the trusted setup globally
- `kzg.commit(poly)` - Commit to a polynomial using the stored S1
- `kzg.prove(poly, γ)` - Create an opening proof at point γ
- `kzg.verify(commitment, proof, γ, value)` - Verify an opening proof

These functions wrap the lower-level operations and provide a cleaner API that matches common usage patterns.

### 2. Added Initialization Cell

Inserted a new cell 88 in the notebook:

```python
# Initialize KZG with trusted setup
# This makes kzg.commit() and kzg.prove() available
kzg.set_trusted_setup(S1, S2)
```

This must be run after cell 31 (where S1 and S2 are computed) and before cell 90 (Exercise 19).

### 3. Updated Cell Numbers

Due to the inserted cell:
- Old cell 88 (Exercise 19 description) → Now cell 89
- Old cell 89 (Exercise 19 solution) → Now cell 90

### 4. Solution Files

Created two solution files:

1. **[sageless/solutions/exercise19/exercise19.py](sageless/solutions/exercise19/exercise19.py)**
   - Detailed version using manual `commitment(S1, poly)` and `prove(S1, poly, γ)` functions
   - Shows the full implementation details
   - Good for understanding how KZG works internally

2. **[sageless/solutions/exercise19/exercise19_notebook_solution.py](sageless/solutions/exercise19/exercise19_notebook_solution.py)**
   - Simplified version using `kzg.commit()` and `kzg.prove()` API
   - Matches the notebook cell 90 solution
   - Easier to use and understand

## Correct Solution for Cell 90

```python
transcript = ""
value_a = a(ω)
value_b = b(ω)
value_c = c(pow(ω, 4, p))
transcript = push(value_a, transcript)
transcript = push(value_b, transcript)
transcript = push(value_c, transcript)
c_a = kzg.commit(a_blind)
c_b = kzg.commit(b_blind)
c_c = kzg.commit(c_blind)
transcript = push(c_a, transcript)
transcript = push(c_b, transcript)
transcript = push(c_c, transcript)
proof_value_a = kzg.prove(a_blind, ω)
proof_value_b = kzg.prove(b_blind, ω)
proof_output = kzg.prove(c_blind, pow(ω, 4, p))
```

## Testing

```bash
# Test the new KZG API
./run.sh test_kzg_api.py

# Test Exercise 19 detailed solution
./run.sh sageless/solutions/exercise19/exercise19.py

# Test Exercise 19 notebook solution
./run.sh sageless/solutions/exercise19/exercise19_notebook_solution.py
```

All tests pass successfully! ✓

## Key Changes Summary

1. ✅ Added `kzg.commit()`, `kzg.prove()`, `kzg.verify()` functions to kzg.py
2. ✅ Added `kzg.set_trusted_setup()` to initialize the global setup
3. ✅ Inserted cell 88 to call `kzg.set_trusted_setup(S1, S2)`
4. ✅ Updated cell 90 template to use simplified API
5. ✅ Created two working solution files (detailed and simplified)
6. ✅ Updated README with both approaches
7. ✅ All solutions tested and verified

## Notes

- The simplified API (`kzg.commit`, `kzg.prove`) requires calling `kzg.set_trusted_setup(S1, S2)` first
- Both the detailed and simplified approaches are equivalent and produce the same results
- The simplified API is recommended for notebook usage as it's cleaner and matches common KZG library patterns
