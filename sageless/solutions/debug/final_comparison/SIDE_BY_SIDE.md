# Side-by-Side Comparison: verify_plonk

This document shows old vs new code side-by-side for easy comparison.

---

## Section 1: Function Signature and Setup

### Lines 1-50 (UNCHANGED)

Both versions identical through Fiat-Shamir transcript reconstruction and challenge generation.

---

## Section 2: Pairing Checks List

### OLD (Line 51)
```python
checks = [
    # inputs and output openings
    ('c_a',          'proof_value_a',         'value_a', ω),
    ('c_b',          'proof_value_b',         'value_b',ω),
    ('c_c',          'proof_output',         'output',ω^4),     # ❌ BUG: ^ is XOR!
    # witness openings
    ('c_a',          'proof_a',         'a_zeta', zeta_v),
    ('c_b',          'proof_b',         'b_zeta',zeta_v),
    ('c_c',          'proof_c',         'c_zeta',zeta_v),
    # z and t openings
    ('c_z',          'proof_z',         'z_zeta',zeta_v),
    ('c_t',          'proof_t',         't_zeta',zeta_v),
    # z(ζ·ω) for perm check
    ('c_z',          'proof_z_omega',   'z_zeta_omega',zeta_v* ω ),
]
```

### NEW (Line 51)
```python
checks = [
    # inputs and output openings
    ('c_a',          'proof_value_a',         'value_a', ω),
    ('c_b',          'proof_value_b',         'value_b',ω),
    ('c_c',          'proof_output',          'output', pow(ω, 4, p)),  # ✓ FIXED: Proper exponentiation
    # witness openings
    ('c_a',          'proof_a',         'a_zeta', zeta_v),
    ('c_b',          'proof_b',         'b_zeta',zeta_v),
    ('c_c',          'proof_c',         'c_zeta',zeta_v),
    # z and t openings
    ('c_z',          'proof_z',         'z_zeta',zeta_v),
    ('c_t',          'proof_t',         't_zeta',zeta_v),
    # z(ζ·ω) for perm check
    ('c_z',          'proof_z_omega',   'z_zeta_omega',zeta_v* ω ),
]
```

**Change**: `ω^4` → `pow(ω, 4, p)`

---

## Section 3: Variable Extraction

### OLD (After Line 68)
```python
    for (c_key, π_key, b_key, challenge_point) in checks:
        C = proof_dictionary['commitments'][c_key]
        π = proof_dictionary['proofs'][π_key]
        b = proof_dictionary['evaluations'][b_key]

        if not verification(C, π, challenge_point, b):
            return False, f"Pairing check failed for {c_key}"
                                                                    # ❌ BUG: Variables not extracted!
    qL_z = qL(zeta_v)                                              # Uses global a_zeta, b_zeta, etc.
    qR_z = qR(zeta_v)
    qM_z = qM(zeta_v)
    N_z = N_poly(zeta_v)
    D_z = D_poly(zeta_v)
```

### NEW (After Line 68)
```python
    for (c_key, π_key, b_key, challenge_point) in checks:
        C = proof_dictionary['commitments'][c_key]
        π = proof_dictionary['proofs'][π_key]
        b = proof_dictionary['evaluations'][b_key]

        if not verification(C, π, challenge_point, b):
            return False, f"Pairing check failed for {c_key}"

    # ✓ ADDED: Extract evaluated values from proof dictionary
    a_zeta = proof_dictionary['evaluations']['a_zeta']
    b_zeta = proof_dictionary['evaluations']['b_zeta']
    c_zeta = proof_dictionary['evaluations']['c_zeta']
    z_zeta = proof_dictionary['evaluations']['z_zeta']
    z_zeta_omega = proof_dictionary['evaluations']['z_zeta_omega']
    t_zeta = proof_dictionary['evaluations']['t_zeta']

    qL_z = qL(zeta_v)
    qR_z = qR(zeta_v)
    qM_z = qM(zeta_v)
    N_z = N_poly(zeta_v)
    D_z = D_poly(zeta_v)
```

**Change**: Added 6 lines to extract variables from proof_dictionary

---

## Section 4: Gate Constraints

### OLD (Line 78)
```python
# Check 1: Gate constraints

t_gates_v = qM_z*a_zeta*b_zeta + qL_z*a_zeta+qR_z*b_zeta-c_zeta  # ❌ BUG: No % p
```

### NEW (Line 78)
```python
# Check 1: Gate constraints

t_gates_v = (qM_z*a_zeta*b_zeta + qL_z*a_zeta+qR_z*b_zeta-c_zeta) % p  # ✓ FIXED: Added % p
```

**Change**: Added `% p` for modular reduction

---

## Section 5: Permutation Constraints

### OLD (Lines 81-83)
```python
# Check 2: Permutation constraints
L1_z = L1(zeta_v)
t_perm_start_v = (z_zeta - 1) * L1_z                      # ❌ CRITICAL BUG: Creates 150+ digit number!
t_perm_step_v = z_zeta * N_z - D_z * z_zeta_omega         # ❌ BUG: No % p
```

### NEW (Lines 81-83)
```python
# Check 2: Permutation constraints
L1_z = L1(zeta_v)
t_perm_start_v = ((z_zeta - 1) * L1_z) % p                # ✓ FIXED: Reduces to field element
t_perm_step_v = (z_zeta * N_z - D_z * z_zeta_omega) % p   # ✓ FIXED: Added % p
```

**Changes**: Added `% p` to both permutation constraint computations

---

## Section 6: Master Polynomial Computation

### OLD (Lines 85-88)
```python
# Check 3: Quotient constraint
# Reconstruct the value of the master polynomial at zeta
master_poly_v = t_gates_v + alpha_v * t_perm_start_v + alpha_v**2 * t_perm_step_v
                                                                    # ❌ BUGS:
                                                                    # - alpha_v**2 not modular
                                                                    # - No intermediate reductions
                                                                    # - Hard to debug
```

### NEW (Lines 85-91)
```python
# Check 3: Quotient constraint
# Reconstruct the value of the master polynomial at zeta
# Compute master polynomial with proper modular arithmetic
alpha_v_squared = pow(alpha_v, 2, p)                      # ✓ Efficient modular square
term1 = t_gates_v                                          # ✓ Already reduced
term2 = (alpha_v * t_perm_start_v) % p                    # ✓ Reduce after multiplication
term3 = (alpha_v_squared * t_perm_step_v) % p             # ✓ Reduce after multiplication
master_poly_v = (term1 + term2 + term3) % p               # ✓ Reduce final sum
```

**Changes**:
- Broke single line into step-by-step computation
- Each step has proper modular reduction
- Used `pow(alpha_v, 2, p)` for efficiency

---

## Section 7: Vanishing Polynomial

### OLD (Line 91)
```python
# Reconstruct the value of the vanishing polynomial at zeta
ZH_z = zeta_v**n - 1        # ❌ BUGS:
                            # - Computes huge integer power first
                            # - No modular reduction
                            # - Inefficient
```

### NEW (Line 94)
```python
# Reconstruct the value of the vanishing polynomial at zeta
ZH_z = (pow(zeta_v, n, p) - 1) % p    # ✓ FIXED:
                                       # - Modular exponentiation (efficient)
                                       # - Proper reduction
                                       # - Always produces field element
```

**Changes**:
- `zeta_v**n` → `pow(zeta_v, n, p)` (modular exponentiation)
- Added `% p` to entire expression

---

## Section 8: Final Quotient Constraint Check

### OLD (Lines 94-98)
```python
# The final check: Does the master polynomial identity hold?
if master_poly_v == t_zeta * ZH_z:              # ❌ BUG: RHS not reduced!
    print("Quotient constraint holds.")         # Can fail even when mathematically correct
else:
    return False, "Quotient constraint check failed!"
```

### NEW (Lines 97-101)
```python
# The final check: Does the master polynomial identity hold?
if master_poly_v == (t_zeta * ZH_z) % p:        # ✓ FIXED: Both sides in canonical form
    print("Quotient constraint holds.")          # Now compares correctly
else:
    return False, "Quotient constraint check failed!"
```

**Change**: Added `% p` to right-hand side for canonical comparison

---

## Section 9: Return Statement (UNCHANGED)

### Both Versions
```python
return True, "All checks passed!"
```

No changes to the success return.

---

## Visual Summary of All Changes

```
Line 51:  ω^4                                  →  pow(ω, 4, p)
Line 69:  [missing]                            →  a_zeta = proof_dictionary['evaluations']['a_zeta']
Line 70:  [missing]                            →  b_zeta = proof_dictionary['evaluations']['b_zeta']
Line 71:  [missing]                            →  c_zeta = proof_dictionary['evaluations']['c_zeta']
Line 72:  [missing]                            →  z_zeta = proof_dictionary['evaluations']['z_zeta']
Line 73:  [missing]                            →  z_zeta_omega = proof_dictionary['evaluations']['z_zeta_omega']
Line 74:  [missing]                            →  t_zeta = proof_dictionary['evaluations']['t_zeta']
Line 78:  ... - c_zeta                         →  ... - c_zeta) % p
Line 82:  ... * L1_z                           →  ... * L1_z) % p
Line 83:  ... * z_zeta_omega                   →  ... * z_zeta_omega) % p
Line 85:  master_poly_v = t_gates_v + ...     →  alpha_v_squared = pow(alpha_v, 2, p)
Line 86:  [was part of line 85]               →  term1 = t_gates_v
Line 87:  [was part of line 85]               →  term2 = (alpha_v * t_perm_start_v) % p
Line 88:  [was part of line 85]               →  term3 = (alpha_v_squared * t_perm_step_v) % p
Line 89:  [was part of line 85]               →  master_poly_v = (term1 + term2 + term3) % p
Line 91:  ZH_z = zeta_v**n - 1                →  ZH_z = (pow(zeta_v, n, p) - 1) % p
Line 94:  ... == t_zeta * ZH_z:               →  ... == (t_zeta * ZH_z) % p:
```

**Total Changes**: 8 distinct fixes across 15+ lines

---

## Bug Severity Classification

| Bug | Severity | Impact |
|-----|----------|--------|
| `ω^4` (XOR instead of exponentiation) | 🔴 **CRITICAL** | Wrong pairing check point |
| Missing variable extraction | 🔴 **CRITICAL** | Function not self-contained |
| `t_perm_start_v` no `% p` | 🔴 **CRITICAL** | 150+ digit intermediate value |
| `master_poly_v` no proper reduction | 🔴 **CRITICAL** | Comparison can fail |
| `ZH_z` no modular exponentiation | 🔴 **CRITICAL** | Inefficient and incorrect |
| Final comparison RHS no `% p` | 🔴 **CRITICAL** | Non-canonical comparison |
| `t_gates_v` no `% p` | 🟡 **MAJOR** | Numerical correctness |
| `t_perm_step_v` no `% p` | 🟡 **MAJOR** | Numerical correctness |

**All 8 bugs were critical or major** - the function could not work correctly without these fixes!

---

## Key Takeaway

Every single change follows one simple principle:

> **In finite field arithmetic (mod p), ALWAYS reduce intermediate results.**

This is the difference between correct cryptographic code and broken cryptographic code.
