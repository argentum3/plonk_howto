#!/usr/bin/env python3
"""
Detailed debugging of quotient constraint failure
Comparing prover's computation vs verifier's computation step-by-step
"""

import sys
import os

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from lib.polynomials import p, Polynomial, PolynomialVar, interpolate
import kzg
from py_ecc.bn128 import multiply

# Initialize KZG
kzg_instance = kzg.setup()

# Get polynomial variable
x = PolynomialVar('x')

print("=" * 70)
print("DETAILED QUOTIENT CONSTRAINT DEBUG")
print("=" * 70)

# Load all the setup from previous exercises
print("\nLoading circuit setup...")

# Circuit definition (from early exercises)
Ω = {1: ω, 2: ω**2, 3: ω**3, 4: ω**4}

# Gate selectors (from Exercise 21)
SL = {1: 1, 2: 1, 3: 1, 4: 0}
SR = {1: 1, 2: 1, 3: 1, 4: 0}
SM = {1: 0, 2: 0, 3: 0, 4: 1}

qL = interpolate(Ω, list(SL.values()))
qR = interpolate(Ω, list(SR.values()))
qM = interpolate(Ω, list(SM.values()))

print(f"  Selector polynomials: qL, qR, qM defined")
print(f"    qL: {qL}")
print(f"    qR: {qR}")
print(f"    qM: {qM}")

# Witness values (x=3, y=4, output=144)
witness_a = {1: 3, 2: 7, 3: 11, 4: 3}
witness_b = {1: 4, 2: 4, 3: 4, 4: 4}
witness_c = {1: 7, 2: 11, 3: 15, 4: 12}

value_a = 3
value_b = 4
value_c = 144

print(f"\nWitness values:")
print(f"  a: {witness_a}")
print(f"  b: {witness_b}")
print(f"  c: {witness_c}")
print(f"  Public: value_a={value_a}, value_b={value_b}, value_c={value_c}")

# Reconstruct all polynomials
print("\n" + "=" * 70)
print("RECONSTRUCTING PROVER'S COMPUTATION")
print("=" * 70)

# Witness polynomials
a = interpolate(Ω, list(witness_a.values()))
b = interpolate(Ω, list(witness_b.values()))
c = interpolate(Ω, list(witness_c.values()))

# Blind witness polynomials
b1_a, b2_a = 12345, 67890
b1_b, b2_b = 11111, 22222
b1_c, b2_c = 33333, 44444

ZH = x^4 - 1
a_blind = a + b1_a * ZH
b_blind = b + b1_b * ZH
c_blind = c + b1_c * ZH

print(f"\nBlinded witness polynomials:")
print(f"  a_blind = a + {b1_a} * ZH")
print(f"  b_blind = b + {b1_b} * ZH")
print(f"  c_blind = c + {b1_c} * ZH")

# Commitments
c_a = kzg.commit(a_blind)
c_b = kzg.commit(b_blind)
c_c = kzg.commit(c_blind)

# Build transcript
transcript = ""
transcript = push(value_a, transcript)
transcript = push(value_b, transcript)
transcript = push(value_c, transcript)
transcript = push(c_a, transcript)
transcript = push(c_b, transcript)
transcript = push(c_c, transcript)

# Generate challenges β, γ
beta = generate_challenge(transcript)
transcript = push(beta, transcript)
gamma = generate_challenge(transcript)
transcript = push(gamma, transcript)

print(f"\nChallenges:")
print(f"  beta  = {beta}")
print(f"  gamma = {gamma}")

# Compute permutation polynomials
z_poly, N_poly, D_poly = interpolate_z_N_D(a_blind, b_blind, c_blind, beta, gamma, Ω)

# Blind z_poly
b1_z, b2_z = 98765, 43210
z_poly_blind = z_poly + b1_z * ZH

c_z = kzg.commit(z_poly_blind)
transcript = push(c_z, transcript)

# Generate challenge α
alpha = generate_challenge(transcript)
transcript = push(alpha, transcript)

print(f"  alpha = {alpha}")

# Build master polynomial (Exercise 21)
L1 = lagrange_poly(Ω, 1)

t_gates = qM * a_blind * b_blind + qL * a_blind + qR * b_blind - c_blind
t_perm_start = (z_poly_blind - 1) * L1
z_shifted = z_poly_blind(x * ω)
t_perm_step = z_poly_blind * N_poly - D_poly * z_shifted

bigt = t_gates + alpha * t_perm_start + (alpha * alpha) * t_perm_step

quotient_poly, remainder = bigt.quo_rem(ZH)

print(f"\nMaster polynomial components:")
print(f"  t_gates degree: {t_gates.degree()}")
print(f"  t_perm_start degree: {t_perm_start.degree()}")
print(f"  t_perm_step degree: {t_perm_step.degree()}")
print(f"  bigt degree: {bigt.degree()}")
print(f"  quotient_poly degree: {quotient_poly.degree()}")
print(f"  remainder: {remainder}")

if remainder != 0:
    print(f"  ⚠️  WARNING: ZH does not divide bigt! Remainder = {remainder}")
else:
    print(f"  ✓ ZH divides bigt cleanly")

# Blind quotient polynomial
b1_t, b2_t = 55555, 66666
quotient_poly_blind = quotient_poly + b1_t * ZH

c_t = kzg.commit(quotient_poly_blind)
transcript = push(c_t, transcript)

# Generate evaluation challenge ζ
zeta = generate_challenge(transcript)
transcript = push(zeta, transcript)

print(f"  zeta  = {zeta}")

# Evaluate at ζ
a_zeta = a_blind(zeta)
b_zeta = b_blind(zeta)
c_zeta = c_blind(zeta)
z_zeta = z_poly_blind(zeta)
t_zeta = quotient_poly_blind(zeta)

# Evaluate at ζ·ω
zeta_omega = (zeta * ω) % p
z_zeta_omega = z_poly_blind(zeta_omega)

print(f"\nEvaluations at ζ:")
print(f"  a_zeta = {a_zeta}")
print(f"  b_zeta = {b_zeta}")
print(f"  c_zeta = {c_zeta}")
print(f"  z_zeta = {z_zeta}")
print(f"  t_zeta = {t_zeta}")
print(f"\nEvaluations at ζ·ω:")
print(f"  z_zeta_omega = {z_zeta_omega}")

# Generate opening proofs
proof_a = kzg.prove(a_blind, zeta)
proof_b = kzg.prove(b_blind, zeta)
proof_c = kzg.prove(c_blind, zeta)
proof_z = kzg.prove(z_poly_blind, zeta)
proof_t = kzg.prove(quotient_poly_blind, zeta)
proof_z_omega = kzg.prove(z_poly_blind, zeta_omega)

# Also need proofs for public inputs/outputs
proof_value_a = kzg.prove(a_blind, ω)
proof_value_b = kzg.prove(b_blind, ω**2)
proof_output = kzg.prove(c_blind, pow(ω, 4, p))

print("\n✓ All opening proofs generated")

print("\n" + "=" * 70)
print("VERIFIER'S COMPUTATION (SIMULATED)")
print("=" * 70)

# Now simulate what the verifier does
zeta_v = zeta
alpha_v = alpha
beta_v = beta
gamma_v = gamma

print(f"\nVerifier uses:")
print(f"  zeta_v  = {zeta_v}")
print(f"  alpha_v = {alpha_v}")
print(f"  beta_v  = {beta_v}")
print(f"  gamma_v = {gamma_v}")

# Verifier evaluates selectors at ζ
qL_z = qL(zeta_v)
qR_z = qR(zeta_v)
qM_z = qM(zeta_v)

print(f"\nSelector evaluations at ζ:")
print(f"  qL(ζ) = {qL_z}")
print(f"  qR(ζ) = {qR_z}")
print(f"  qM(ζ) = {qM_z}")

# CRITICAL: How does verifier get N(ζ) and D(ζ)?
print(f"\nPermutation polynomial evaluations at ζ:")

# Method 1: Direct evaluation (assumes N_poly, D_poly in scope - CURRENT APPROACH)
N_z_direct = N_poly(zeta_v)
D_z_direct = D_poly(zeta_v)
print(f"  Method 1 (direct from N_poly, D_poly):")
print(f"    N(ζ) = {N_z_direct}")
print(f"    D(ζ) = {D_z_direct}")

# Method 2: What verifier SHOULD compute (from witness evaluations)
# This is the proper PlonK way
print(f"\n  Method 2 (computed from witness evaluations):")
print(f"    This would require S_sigma polynomials (not in tutorial)")

# Verifier computes L1 at ζ
zeta_omega_v = (zeta_v * ω) % p
L1_z = L1(zeta_v)

print(f"\nL1(ζ) = {L1_z}")

# Verifier computes constraint checks
print("\n" + "=" * 70)
print("CONSTRAINT CHECKS AT ζ")
print("=" * 70)

# Gate constraint
t_gates_v = (qM_z * a_zeta * b_zeta + qL_z * a_zeta + qR_z * b_zeta - c_zeta) % p
print(f"\n1. Gate constraint:")
print(f"   t_gates(ζ) = qM(ζ)·a(ζ)·b(ζ) + qL(ζ)·a(ζ) + qR(ζ)·b(ζ) - c(ζ)")
print(f"   t_gates(ζ) = {t_gates_v}")

# Permutation start constraint
t_perm_start_v = ((z_zeta - 1) * L1_z) % p
print(f"\n2. Permutation start constraint:")
print(f"   t_perm_start(ζ) = (z(ζ) - 1) · L1(ζ)")
print(f"   t_perm_start(ζ) = {t_perm_start_v}")

# Permutation step constraint
t_perm_step_v = (z_zeta * N_z_direct - D_z_direct * z_zeta_omega) % p
print(f"\n3. Permutation step constraint:")
print(f"   t_perm_step(ζ) = z(ζ) · N(ζ) - D(ζ) · z(ζ·ω)")
print(f"   t_perm_step(ζ) = {t_perm_step_v}")

# Master polynomial at ζ
master_poly_v = (t_gates_v + alpha_v * t_perm_start_v + (alpha_v * alpha_v) % p * t_perm_step_v) % p
print(f"\n4. Master polynomial at ζ:")
print(f"   master_poly(ζ) = t_gates(ζ) + α·t_perm_start(ζ) + α²·t_perm_step(ζ)")
print(f"   master_poly(ζ) = {master_poly_v}")

# Vanishing polynomial at ζ
ZH_z = (pow(zeta_v, 4, p) - 1) % p
print(f"\n5. Vanishing polynomial at ζ:")
print(f"   ZH(ζ) = ζ⁴ - 1 = {ZH_z}")

# Right-hand side
rhs = (t_zeta * ZH_z) % p
print(f"\n6. Right-hand side:")
print(f"   t(ζ) · ZH(ζ) = {rhs}")

print("\n" + "=" * 70)
print("THE CRITICAL CHECK")
print("=" * 70)

print(f"\nDoes master_poly(ζ) == t(ζ) · ZH(ζ)?")
print(f"  LHS: {master_poly_v}")
print(f"  RHS: {rhs}")
print(f"  Equal: {master_poly_v == rhs}")

if master_poly_v != rhs:
    print("\n❌ QUOTIENT CONSTRAINT FAILS!")
    diff = (master_poly_v - rhs) % p
    print(f"\nDifference: {diff}")
    print(f"Difference (signed): {diff if diff < p//2 else diff - p}")

    # Additional debugging
    print("\n" + "=" * 70)
    print("ADDITIONAL DEBUGGING")
    print("=" * 70)

    # Check if blinding is the issue
    print("\nChecking with unblinded polynomials:")

    # Unblinded evaluations
    a_zeta_unblind = a(zeta)
    b_zeta_unblind = b(zeta)
    c_zeta_unblind = c(zeta)
    z_zeta_unblind = z_poly(zeta)
    t_zeta_unblind = quotient_poly(zeta)
    z_zeta_omega_unblind = z_poly(zeta_omega)

    print(f"  a(ζ) unblinded: {a_zeta_unblind}")
    print(f"  a(ζ) blinded:   {a_zeta}")
    print(f"  Difference: {(a_zeta - a_zeta_unblind) % p}")

    # Check ZH at blinding differences
    ZH_zeta = ZH(zeta)
    print(f"\n  ZH(ζ) = {ZH_zeta}")
    expected_diff_a = (b1_a * ZH_zeta) % p
    actual_diff_a = (a_zeta - a_zeta_unblind) % p
    print(f"  Expected a difference (b1_a * ZH(ζ)): {expected_diff_a}")
    print(f"  Actual a difference: {actual_diff_a}")
    print(f"  Match: {expected_diff_a == actual_diff_a}")

    # Recompute with unblinded values
    print("\n  Recomputing constraints with unblinded polynomials:")

    t_gates_unblind = (qM_z * a_zeta_unblind * b_zeta_unblind + qL_z * a_zeta_unblind + qR_z * b_zeta_unblind - c_zeta_unblind) % p
    t_perm_start_unblind = ((z_zeta_unblind - 1) * L1_z) % p

    N_z_unblind = N_poly(zeta_v)  # N_poly doesn't change with blinding of a,b,c
    D_z_unblind = D_poly(zeta_v)  # D_poly doesn't change with blinding of a,b,c

    t_perm_step_unblind = (z_zeta_unblind * N_z_unblind - D_z_unblind * z_zeta_omega_unblind) % p

    master_poly_unblind = (t_gates_unblind + alpha_v * t_perm_start_unblind + (alpha_v * alpha_v) % p * t_perm_step_unblind) % p
    rhs_unblind = (t_zeta_unblind * ZH_z) % p

    print(f"    master_poly(ζ) unblinded: {master_poly_unblind}")
    print(f"    t(ζ)·ZH(ζ) unblinded:     {rhs_unblind}")
    print(f"    Equal: {master_poly_unblind == rhs_unblind}")

    # Check if the issue is with z_poly blinding
    print("\n  Checking z_poly blinding:")
    z_diff = (z_zeta - z_zeta_unblind) % p
    expected_z_diff = (b1_z * ZH_zeta) % p
    print(f"    Expected z difference (b1_z * ZH(ζ)): {expected_z_diff}")
    print(f"    Actual z difference: {z_diff}")
    print(f"    Match: {expected_z_diff == z_diff}")

    print("\n  Checking t_poly blinding:")
    t_diff = (t_zeta - t_zeta_unblind) % p
    expected_t_diff = (b1_t * ZH_zeta) % p
    print(f"    Expected t difference (b1_t * ZH(ζ)): {expected_t_diff}")
    print(f"    Actual t difference: {t_diff}")
    print(f"    Match: {expected_t_diff == t_diff}")

else:
    print("\n✓✓✓ QUOTIENT CONSTRAINT PASSES ✓✓✓")

print("\n" + "=" * 70)
print("COMPARING PROVER VS VERIFIER")
print("=" * 70)

# Direct polynomial evaluation
print(f"\nDirect polynomial evaluations:")
print(f"  t_gates(ζ) from polynomial:     {t_gates(zeta)}")
print(f"  t_gates(ζ) verifier computed:   {t_gates_v}")
print(f"  Match: {t_gates(zeta) == t_gates_v}")

print(f"\n  t_perm_start(ζ) from polynomial: {t_perm_start(zeta)}")
print(f"  t_perm_start(ζ) verifier:        {t_perm_start_v}")
print(f"  Match: {t_perm_start(zeta) == t_perm_start_v}")

print(f"\n  t_perm_step(ζ) from polynomial:  {t_perm_step(zeta)}")
print(f"  t_perm_step(ζ) verifier:         {t_perm_step_v}")
print(f"  Match: {t_perm_step(zeta) == t_perm_step_v}")

print(f"\n  bigt(ζ) from polynomial:         {bigt(zeta)}")
print(f"  master_poly(ζ) verifier:         {master_poly_v}")
print(f"  Match: {bigt(zeta) == master_poly_v}")

print(f"\n  quotient_poly(ζ):                {quotient_poly(zeta)}")
print(f"  quotient_poly_blind(ζ):          {quotient_poly_blind(zeta)}")
print(f"  t_zeta from proof:               {t_zeta}")
print(f"  Match (blind): {quotient_poly_blind(zeta) == t_zeta}")

print("\n" + "=" * 70)
print("END OF DETAILED DEBUG")
print("=" * 70)
