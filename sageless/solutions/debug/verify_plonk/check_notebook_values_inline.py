#!/usr/bin/env python3
"""
Inline checker for quotient constraint - run this from a notebook cell
This assumes you've already run cells 91-98 in the notebook
"""

print("=" * 70)
print("CHECKING QUOTIENT CONSTRAINT IN NOTEBOOK")
print("=" * 70)

# Get verifier's computation
zeta_v = zeta
alpha_v = alpha
beta_v = beta
gamma_v = gamma

print(f"\nChallenges:")
print(f"  beta  = {beta_v}")
print(f"  gamma = {gamma_v}")
print(f"  alpha = {alpha_v}")
print(f"  zeta  = {zeta_v}")

# Evaluate selectors at zeta
qL_z = qL(zeta_v)
qR_z = qR(zeta_v)
qM_z = qM(zeta_v)

print(f"\nSelector evaluations at ζ:")
print(f"  qL(ζ) = {qL_z}")
print(f"  qR(ζ) = {qR_z}")
print(f"  qM(ζ) = {qM_z}")

# Get N and D evaluations
print(f"\nChecking if N_poly and D_poly are defined:")
try:
    N_z = N_poly(zeta_v)
    D_z = D_poly(zeta_v)
    print(f"  ✓ N_poly and D_poly are accessible")
    print(f"  N(ζ) = {N_z}")
    print(f"  D(ζ) = {D_z}")
except NameError as e:
    print(f"  ✗ ERROR: {e}")
    print(f"  → Run cell 92 first to define N_poly and D_poly")

# Get evaluations from proof
print(f"\nEvaluations from proof:")
print(f"  a_zeta = {a_zeta}")
print(f"  b_zeta = {b_zeta}")
print(f"  c_zeta = {c_zeta}")
print(f"  z_zeta = {z_zeta}")
print(f"  t_zeta = {t_zeta}")
print(f"  z_zeta_omega = {z_zeta_omega}")

# Compute L1 at zeta
zeta_omega_v = (zeta_v * ω) % p
L1_z = L1(zeta_v)

print(f"\nL1(ζ) = {L1_z}")
print(f"ζ·ω = {zeta_omega_v}")

# Compute constraints
print(f"\n" + "=" * 70)
print("CONSTRAINT COMPUTATIONS")
print("=" * 70)

# Gate constraint
t_gates_v = (qM_z * a_zeta * b_zeta + qL_z * a_zeta + qR_z * b_zeta - c_zeta) % p
print(f"\n1. Gate constraint at ζ:")
print(f"   t_gates(ζ) = {t_gates_v}")

# Verify against direct polynomial evaluation
try:
    t_gates_direct = t_gates(zeta_v)
    print(f"   t_gates(ζ) direct = {t_gates_direct}")
    print(f"   Match: {t_gates_v == t_gates_direct}")
except NameError:
    print(f"   (t_gates polynomial not in scope)")

# Permutation start
t_perm_start_v = ((z_zeta - 1) * L1_z) % p
print(f"\n2. Permutation start at ζ:")
print(f"   t_perm_start(ζ) = {t_perm_start_v}")

try:
    t_perm_start_direct = t_perm_start(zeta_v)
    print(f"   t_perm_start(ζ) direct = {t_perm_start_direct}")
    print(f"   Match: {t_perm_start_v == t_perm_start_direct}")
except NameError:
    print(f"   (t_perm_start polynomial not in scope)")

# Permutation step
try:
    t_perm_step_v = (z_zeta * N_z - D_z * z_zeta_omega) % p
    print(f"\n3. Permutation step at ζ:")
    print(f"   t_perm_step(ζ) = {t_perm_step_v}")

    try:
        t_perm_step_direct = t_perm_step(zeta_v)
        print(f"   t_perm_step(ζ) direct = {t_perm_step_direct}")
        print(f"   Match: {t_perm_step_v == t_perm_step_direct}")
    except NameError:
        print(f"   (t_perm_step polynomial not in scope)")

except NameError as e:
    print(f"\n3. ✗ ERROR computing permutation step: {e}")
    t_perm_step_v = 0

# Master polynomial
master_poly_v = (t_gates_v + alpha_v * t_perm_start_v + (alpha_v * alpha_v) % p * t_perm_step_v) % p
print(f"\n4. Master polynomial at ζ:")
print(f"   master_poly(ζ) = {master_poly_v}")

try:
    bigt_direct = bigt(zeta_v)
    print(f"   bigt(ζ) direct = {bigt_direct}")
    print(f"   Match: {master_poly_v == bigt_direct}")
except NameError:
    print(f"   (bigt polynomial not in scope)")

# Vanishing polynomial
ZH_z = (pow(zeta_v, 4, p) - 1) % p
print(f"\n5. Vanishing polynomial at ζ:")
print(f"   ZH(ζ) = {ZH_z}")

try:
    ZH_direct = ZH(zeta_v)
    print(f"   ZH(ζ) direct = {ZH_direct}")
    print(f"   Match: {ZH_z == ZH_direct}")
except:
    print(f"   (ZH polynomial not in scope)")

# RHS
rhs = (t_zeta * ZH_z) % p
print(f"\n6. Right-hand side:")
print(f"   t(ζ) · ZH(ζ) = {rhs}")

# THE CHECK
print(f"\n" + "=" * 70)
print("THE CRITICAL CHECK")
print("=" * 70)

print(f"\nDoes master_poly(ζ) == t(ζ) · ZH(ζ)?")
print(f"  LHS: {master_poly_v}")
print(f"  RHS: {rhs}")

if master_poly_v == rhs:
    print(f"  ✓✓✓ PASS ✓✓✓")
else:
    print(f"  ✗✗✗ FAIL ✗✗✗")
    diff = (master_poly_v - rhs) % p
    print(f"\n  Difference (mod p): {diff}")
    if diff < p // 2:
        print(f"  Difference (signed): +{diff}")
    else:
        print(f"  Difference (signed): -{p - diff}")

    # Additional debugging
    print(f"\n" + "=" * 70)
    print("ADDITIONAL DEBUGGING")
    print("=" * 70)

    # Check each component contribution
    print(f"\nComponent contributions to LHS:")
    print(f"  t_gates(ζ)            = {t_gates_v}")
    print(f"  α · t_perm_start(ζ)   = {(alpha_v * t_perm_start_v) % p}")
    print(f"  α² · t_perm_step(ζ)   = {((alpha_v * alpha_v) % p * t_perm_step_v) % p}")
    print(f"  Sum (LHS)             = {master_poly_v}")

    print(f"\nRHS components:")
    print(f"  t(ζ)                  = {t_zeta}")
    print(f"  ZH(ζ)                 = {ZH_z}")
    print(f"  Product (RHS)         = {rhs}")

    # Check if quotient_poly is correct
    try:
        quotient_direct = quotient_poly(zeta_v)
        quotient_blind_direct = quotient_poly_blind(zeta_v)
        print(f"\nQuotient polynomial checks:")
        print(f"  quotient_poly(ζ)        = {quotient_direct}")
        print(f"  quotient_poly_blind(ζ)  = {quotient_blind_direct}")
        print(f"  t_zeta from proof       = {t_zeta}")
        print(f"  quotient_blind matches t_zeta: {quotient_blind_direct == t_zeta}")

        # Check if bigt/ZH == quotient
        print(f"\nDirect polynomial division check:")
        bigt_at_zeta = bigt(zeta_v)
        ZH_at_zeta = ZH(zeta_v)
        print(f"  bigt(ζ) = {bigt_at_zeta}")
        print(f"  ZH(ζ) = {ZH_at_zeta}")
        if ZH_at_zeta == 0:
            print(f"  ⚠️  WARNING: ZH(ζ) = 0, so ζ is a root of ZH!")
            print(f"     This means the check should use polynomial division, not evaluation")
        else:
            ratio = (bigt_at_zeta * pow(ZH_at_zeta, -1, p)) % p
            print(f"  bigt(ζ) / ZH(ζ) = {ratio}")
            print(f"  Matches quotient_poly(ζ): {ratio == quotient_direct}")
    except Exception as e:
        print(f"  Error checking quotient: {e}")

print(f"\n" + "=" * 70)
