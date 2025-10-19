#!/usr/bin/env python3
"""
Comprehensive diagnostic for verify_plonk
This script will be inserted into the notebook to debug the exact issue.
"""

diagnostic_code = """
print("=" * 80)
print("COMPREHENSIVE verify_plonk DIAGNOSTIC")
print("=" * 80)

# 1. Check what's in proof_dictionary
print("\\n1. PROOF DICTIONARY STRUCTURE")
print("-" * 80)
print("Keys in proof_dictionary:", list(proof_dictionary.keys()))
print("\\nKeys in commitments:", list(proof_dictionary['commitments'].keys()))
print("Keys in challenges:", list(proof_dictionary['challenges'].keys()))
print("Keys in evaluations:", list(proof_dictionary['evaluations'].keys()))
print("Keys in proofs:", list(proof_dictionary['proofs'].keys()))

# 2. Extract values the way verify_plonk SHOULD
print("\\n2. VALUES FROM PROOF DICTIONARY")
print("-" * 80)
a_zeta_from_proof = proof_dictionary['evaluations']['a_zeta']
b_zeta_from_proof = proof_dictionary['evaluations']['b_zeta']
c_zeta_from_proof = proof_dictionary['evaluations']['c_zeta']
z_zeta_from_proof = proof_dictionary['evaluations']['z_zeta']
z_zeta_omega_from_proof = proof_dictionary['evaluations']['z_zeta_omega']
t_zeta_from_proof = proof_dictionary['evaluations']['t_zeta']

print(f"a_zeta (from proof): {a_zeta_from_proof}")
print(f"b_zeta (from proof): {b_zeta_from_proof}")
print(f"c_zeta (from proof): {c_zeta_from_proof}")
print(f"z_zeta (from proof): {z_zeta_from_proof}")
print(f"z_zeta_omega (from proof): {z_zeta_omega_from_proof}")
print(f"t_zeta (from proof): {t_zeta_from_proof}")

# 3. Check global notebook variables
print("\\n3. GLOBAL NOTEBOOK VARIABLES")
print("-" * 80)
print(f"a_zeta (global): {a_zeta}")
print(f"b_zeta (global): {b_zeta}")
print(f"c_zeta (global): {c_zeta}")
print(f"z_zeta (global): {z_zeta}")
print(f"z_zeta_omega (global): {z_zeta_omega}")
print(f"t_zeta (global): {t_zeta}")

# 4. Compare them
print("\\n4. COMPARISON: Are they the same?")
print("-" * 80)
print(f"a_zeta matches: {a_zeta_from_proof == a_zeta}")
print(f"b_zeta matches: {b_zeta_from_proof == b_zeta}")
print(f"c_zeta matches: {c_zeta_from_proof == c_zeta}")
print(f"z_zeta matches: {z_zeta_from_proof == z_zeta}")
print(f"z_zeta_omega matches: {z_zeta_omega_from_proof == z_zeta_omega}")
print(f"t_zeta matches: {t_zeta_from_proof == t_zeta}")

# 5. Recompute constraints using PROOF VALUES
print("\\n5. CONSTRAINT COMPUTATION WITH PROOF VALUES")
print("-" * 80)

# Get challenges
alpha_v = proof_dictionary['challenges']['alpha']
zeta_v = proof_dictionary['challenges']['zeta']

# Compute selector polynomials at zeta_v
qL_z = qL(zeta_v)
qR_z = qR(zeta_v)
qM_z = qM(zeta_v)
N_z = N_poly(zeta_v)
D_z = D_poly(zeta_v)
L1_z = L1(zeta_v)

# Gate constraints
t_gates_v_proof = (qM_z*a_zeta_from_proof*b_zeta_from_proof + qL_z*a_zeta_from_proof+qR_z*b_zeta_from_proof-c_zeta_from_proof) % p
t_gates_v_global = (qM_z*a_zeta*b_zeta + qL_z*a_zeta+qR_z*b_zeta-c_zeta) % p

print(f"t_gates_v (using proof values): {t_gates_v_proof}")
print(f"t_gates_v (using global values): {t_gates_v_global}")
print(f"Match: {t_gates_v_proof == t_gates_v_global}")

# Permutation constraints
t_perm_start_v_proof = (z_zeta_from_proof - 1) * L1_z
t_perm_start_v_global = (z_zeta - 1) * L1_z

print(f"\\nt_perm_start_v (using proof values): {t_perm_start_v_proof}")
print(f"t_perm_start_v (using global values): {t_perm_start_v_global}")
print(f"Match: {t_perm_start_v_proof == t_perm_start_v_global}")

t_perm_step_v_proof = (z_zeta_from_proof * N_z - D_z * z_zeta_omega_from_proof) % p
t_perm_step_v_global = (z_zeta * N_z - D_z * z_zeta_omega) % p

print(f"\\nt_perm_step_v (using proof values): {t_perm_step_v_proof}")
print(f"t_perm_step_v (using global values): {t_perm_step_v_global}")
print(f"Match: {t_perm_step_v_proof == t_perm_step_v_global}")

# 6. Master polynomial computation
print("\\n6. MASTER POLYNOMIAL COMPUTATION")
print("-" * 80)

# Using proof values
alpha_v_squared = pow(alpha_v, 2, p)
term1_proof = t_gates_v_proof
term2_proof = (alpha_v * t_perm_start_v_proof) % p
term3_proof = (alpha_v_squared * t_perm_step_v_proof) % p
master_poly_v_proof = (term1_proof + term2_proof + term3_proof) % p

# Using global values
term1_global = t_gates_v_global
term2_global = (alpha_v * t_perm_start_v_global) % p
term3_global = (alpha_v_squared * t_perm_step_v_global) % p
master_poly_v_global = (term1_global + term2_global + term3_global) % p

print(f"master_poly_v (using proof values): {master_poly_v_proof}")
print(f"master_poly_v (using global values): {master_poly_v_global}")
print(f"Match: {master_poly_v_proof == master_poly_v_global}")

# 7. Vanishing polynomial
print("\\n7. VANISHING POLYNOMIAL")
print("-" * 80)
ZH_z = (pow(zeta_v, n, p) - 1) % p
print(f"ZH_z = {ZH_z}")

# 8. Right-hand side of quotient constraint
print("\\n8. QUOTIENT CONSTRAINT RHS")
print("-" * 80)
rhs_proof = (t_zeta_from_proof * ZH_z) % p
rhs_global = (t_zeta * ZH_z) % p

print(f"t_zeta * ZH_z (using proof value): {rhs_proof}")
print(f"t_zeta * ZH_z (using global value): {rhs_global}")
print(f"Match: {rhs_proof == rhs_global}")

# 9. THE CRITICAL CHECK
print("\\n9. QUOTIENT CONSTRAINT CHECK")
print("-" * 80)
print(f"master_poly_v (LHS, proof):  {master_poly_v_proof}")
print(f"t_zeta * ZH_z (RHS, proof):  {rhs_proof}")
print(f"MATCH (using proof values):  {master_poly_v_proof == rhs_proof}")
print()
print(f"master_poly_v (LHS, global): {master_poly_v_global}")
print(f"t_zeta * ZH_z (RHS, global): {rhs_global}")
print(f"MATCH (using global values): {master_poly_v_global == rhs_global}")

# 10. If they don't match, show the difference
print("\\n10. DEBUGGING DIFFERENCES")
print("-" * 80)
if master_poly_v_proof != rhs_proof:
    diff = (master_poly_v_proof - rhs_proof) % p
    print(f"Difference (proof): {diff}")
    print(f"Difference is zero: {diff == 0}")

if master_poly_v_global != rhs_global:
    diff = (master_poly_v_global - rhs_global) % p
    print(f"Difference (global): {diff}")
    print(f"Difference is zero: {diff == 0}")

# 11. Check if t_perm_start_v needs modulo
print("\\n11. CHECK MODULAR ARITHMETIC IN CONSTRAINTS")
print("-" * 80)
t_perm_start_v_no_mod = (z_zeta_from_proof - 1) * L1_z
t_perm_start_v_with_mod = ((z_zeta_from_proof - 1) * L1_z) % p
print(f"t_perm_start_v (no mod): {t_perm_start_v_no_mod}")
print(f"t_perm_start_v (with mod): {t_perm_start_v_with_mod}")
print(f"Same: {t_perm_start_v_no_mod == t_perm_start_v_with_mod}")
print(f"Both < p: {t_perm_start_v_no_mod < p and t_perm_start_v_with_mod < p}")

print("\\n" + "=" * 80)
print("END DIAGNOSTIC")
print("=" * 80)
"""

print(diagnostic_code)
