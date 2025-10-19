#!/usr/bin/env python3
"""
Diagnose the modulo arithmetic issue in verify_plonk

This script shows that verify_plonk doesn't use modulo operations,
which causes integer overflow beyond the field modulus p.
"""

print("=" * 70)
print("MODULO ARITHMETIC ISSUE DIAGNOSIS")
print("=" * 70)

print("""
HYPOTHESIS: verify_plonk fails because it doesn't use modulo arithmetic.

When multiplying large field elements, Python computes exact integer results
that can exceed the field modulus p. Without reducing modulo p, the equality
check will fail even though the values are equal in the field.

Let's demonstrate:
""")

# Example values from your notebook
p = 21888242871839275222246405745257275088548364400416034343698204186575808495617

# Simulate the issue
a = 18134454765911837919602477646588583518393278065010999960132769168537205261026
b = 13080992023246893530046576653157357293254313242929606374643603950805496266437
c = 8180790965712712367468445525840492642423220416249014994439271888929825593837

print(f"Example field elements:")
print(f"  a = {a}")
print(f"  b = {b}")
print(f"  c = {c}")
print(f"  p = {p}")
print()

# Method 1: Without modulo (what verify_plonk does)
result_no_mod = a * b + c
print(f"Method 1 (no modulo, like verify_plonk):")
print(f"  a * b + c = {result_no_mod}")
print(f"  Exceeds p? {result_no_mod >= p}")
print()

# Method 2: With modulo (what your manual check does)
result_with_mod = (a * b + c) % p
print(f"Method 2 (with modulo, like your manual check):")
print(f"  (a * b + c) % p = {result_with_mod}")
print(f"  Exceeds p? {result_with_mod >= p}")
print()

# The comparison
print(f"Are they equal?")
print(f"  {result_no_mod} == {result_with_mod}: {result_no_mod == result_with_mod}")
print(f"  But in the field, they represent the same value!")
print()

print("=" * 70)
print("IMPLICATION FOR verify_plonk")
print("=" * 70)

print("""
In verify_plonk, the code does:

    t_gates_v = qM_z*a_zeta*b_zeta + qL_z*a_zeta+qR_z*b_zeta-c_zeta
    master_poly_v = t_gates_v + alpha_v * t_perm_start_v + alpha_v**2 * t_perm_step_v
    ZH_z = zeta_v**n - 1

    if master_poly_v == t_zeta * ZH_z:
        ...

WITHOUT modulo operations, the values can exceed p, causing the comparison
to fail even though the values are equivalent in the field.

Your manual check does:

    t_gates_v = (...) % p
    master_poly_v = (...) % p
    ZH_z = (...) % p
    rhs = (t_zeta * ZH_z) % p

    if master_poly_v == rhs:
        ...

WITH modulo operations, the values are always reduced to [0, p), making
the comparison work correctly.
""")

print("=" * 70)
print("SOLUTION")
print("=" * 70)

print("""
The verify_plonk function needs to use modulo arithmetic everywhere.

However, you mentioned:
> "do not update the code in notebook for verify_plonk"

So the issue is likely that verify_plonk was DESIGNED to work without
explicit modulo operations, assuming Python's Polynomial class handles
modular arithmetic automatically.

Let me check if there's another issue...
""")

print("\n" + "=" * 70)
print("ALTERNATIVE HYPOTHESIS")
print("=" * 70)

print("""
Wait - you said your manual check PASSED:

    LHS (master_poly): 7290117150429173153347370958101709021798985414883489296976998059348729052942
    RHS (t_zeta*ZH):   7290117150429173153347370958101709021798985414883489296976998059348729052942
    Match: True

This means the VALUES are correct. So why does verify_plonk fail?

Possible reasons:
1. verify_plonk extracts values from proof_dictionary incorrectly
2. verify_plonk uses different variable names (a_zeta vs proof values)
3. verify_plonk's comparison uses wrong variables

Let's check what verify_plonk actually uses...
""")

print("\n" + "=" * 70)
print("CHECKING verify_plonk VARIABLES")
print("=" * 70)

print("""
verify_plonk gets values from proof_dictionary:

    a_zeta = proof_dictionary['evaluations']['a_zeta']
    b_zeta = proof_dictionary['evaluations']['b_zeta']
    c_zeta = proof_dictionary['evaluations']['c_zeta']
    z_zeta = proof_dictionary['evaluations']['z_zeta']
    t_zeta = proof_dictionary['evaluations']['t_zeta']
    z_zeta_omega = proof_dictionary['evaluations']['z_zeta_omega']

But wait - I don't see where verify_plonk extracts these!

Let me search for where verify_plonk gets a_zeta from proof_dictionary...
""")

print("\nLooking at verify_plonk code, I notice it uses:")
print("  - qL_z = qL(zeta_v)")
print("  - qR_z = qR(zeta_v)")
print("  - qM_z = qM(zeta_v)")
print("  - N_z = N_poly(zeta_v)")
print("  - D_z = D_poly(zeta_v)")
print()
print("But where does it get a_zeta, b_zeta, c_zeta, z_zeta, t_zeta?")
print()
print("It must be assuming they're in the global scope from cell 96!")
print()

print("=" * 70)
print("FINAL HYPOTHESIS")
print("=" * 70)

print("""
verify_plonk is accessing variables from the GLOBAL SCOPE instead of
extracting them from proof_dictionary!

This means:
1. It uses the global variables: a_zeta, b_zeta, c_zeta, z_zeta, t_zeta
2. These should be defined in cell 96 (Exercise 22)
3. If they're not defined, verify_plonk will fail with NameError
4. If they're defined but wrong, verify_plonk will fail the check

The proof_dictionary is only used for:
- Commitments (for pairing checks)
- Challenges (for transcript verification)
- Proofs (for pairing checks)

But NOT for the evaluations in the quotient constraint check!

TO VERIFY: Add a print statement in verify_plonk to see what values
it's actually using for the quotient constraint check.
""")

print("\n" + "=" * 70)
