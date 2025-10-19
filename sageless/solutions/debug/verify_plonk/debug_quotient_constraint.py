#!/usr/bin/env python3
"""
Debug script to investigate why the quotient constraint check fails in verify_plonk.

The verify_plonk function checks:
    master_poly_v == t_zeta * ZH_z

Where:
- master_poly_v = t_gates_v + alpha_v * t_perm_start_v + alpha_v**2 * t_perm_step_v
- t_zeta = quotient_poly(zeta)
- ZH_z = zeta^n - 1

This should satisfy: bigt(zeta) = quotient_poly(zeta) * ZH(zeta)

This script will:
1. Reconstruct all components step by step
2. Compute master_poly_v the way the verifier does
3. Compare with t_zeta * ZH_z
4. Identify the mismatch
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from lib.polynomials import p, Polynomial, PolynomialVar, interpolate
import kzg
from py_ecc.bn128 import multiply
import hashlib

print("="*70)
print("DEBUG: QUOTIENT CONSTRAINT CHECK FAILURE")
print("="*70)

# ============================================================================
# SETUP
# ============================================================================

n = 4
r = (p - 1) // 4
h = 5
ω = pow(h, r, p)
Ω = [pow(ω, i, p) for i in range(1, n+1)]

# Circuit values
LI = {1:0, 2:1, 3:1, 4:3}
RI = {1:1, 2:1, 3:2, 4:3}
O  = {1:1, 2:2, 3:3, 4:9}

a = interpolate(Ω, list(LI.values()))
b = interpolate(Ω, list(RI.values()))
c = interpolate(Ω, list(O.values()))

# Selector polynomials
SL = {1: 1, 2: 1, 3: 1, 4: 0}
SR = {1: 1, 2: 1, 3: 1, 4: 0}
SM = {1: 0, 2: 0, 3: 0, 4: 1}
qL = interpolate(Ω, list(SL.values()))
qR = interpolate(Ω, list(SR.values()))
qM = interpolate(Ω, list(SM.values()))

# Polynomial variable
x = PolynomialVar(p)

# Vanishing polynomial
ZH = x
for _ in range(n - 1):
    ZH = ZH * x
ZH = ZH - 1

# Blinding
def random_polynomial(degree, modulus):
    import random
    coeffs = [random.randint(0, modulus - 1) for _ in range(degree + 1)]
    return Polynomial(coeffs, modulus)

import random
random.seed(42)
k = 2

a_blind = a + random_polynomial(degree=k-1, modulus=p) * ZH
b_blind = b + random_polynomial(degree=k-1, modulus=p) * ZH
c_blind = c + random_polynomial(degree=k-1, modulus=p) * ZH

# Permutation setup
def pos(column, index):
    return ((column-1)*n + index)

sigma = {}
sigma[pos(1,1)] = pos(1,1)
sigma[pos(1,2)] = pos(2,1)
sigma[pos(2,1)] = pos(1,2)
sigma[pos(1,3)] = pos(2,2)
sigma[pos(2,2)] = pos(3,1)
sigma[pos(3,1)] = pos(1,3)
sigma[pos(3,2)] = pos(2,3)
sigma[pos(2,3)] = pos(3,2)
sigma[pos(3,3)] = pos(1,4)
sigma[pos(1,4)] = pos(2,4)
sigma[pos(2,4)] = pos(3,3)
sigma[pos(3,4)] = pos(3,4)

def numerator(i, column, f, sigma, beta, gamma):
    position = pos(column, i)
    ω_to_i = pow(ω, i, p)
    f_of_ω_i = f(ω_to_i)
    value = (position + beta * f_of_ω_i + gamma) % p
    return value

def denominator(i, column, f, sigma, beta, gamma):
    position = pos(column, i)
    sigma_position = sigma[position]
    ω_to_i = pow(ω, i, p)
    f_of_ω_i = f(ω_to_i)
    value = (sigma_position + beta * f_of_ω_i + gamma) % p
    return value

def interpolate_z_N_D(a, b, c, beta, gamma, Ω):
    n = len(Ω)
    z_values = []
    N_values = []
    D_values = []
    z_current = 1

    for i in range(1, n + 1):
        z_values.append(z_current)

        num_a = numerator(i, 1, a, sigma, beta, gamma)
        num_b = numerator(i, 2, b, sigma, beta, gamma)
        num_c = numerator(i, 3, c, sigma, beta, gamma)

        den_a = denominator(i, 1, a, sigma, beta, gamma)
        den_b = denominator(i, 2, b, sigma, beta, gamma)
        den_c = denominator(i, 3, c, sigma, beta, gamma)

        N_i = (num_a * num_b * num_c) % p
        N_values.append(N_i)

        D_i = (den_a * den_b * den_c) % p
        D_values.append(D_i)

        D_i_inv = pow(D_i, p - 2, p)
        z_current = (z_current * N_i * D_i_inv) % p

    z_poly = interpolate(Ω, z_values)
    N_poly = interpolate(Ω, N_values)
    D_poly = interpolate(Ω, D_values)

    return z_poly, N_poly, D_poly

# Trusted setup
τ = 424242
l = 10
P = kzg.P

S1 = []
τ_power = 1
for i in range(l + 1):
    point = multiply(P, τ_power % kzg.n)
    S1.append(point)
    τ_power = (τ_power * τ) % kzg.n

S2 = multiply(kzg.Q, τ % kzg.n)
kzg.set_trusted_setup(S1, S2)

# Transcript functions
def push(v, transcript, delim="|"):
    return transcript + delim + str(v)

def generate_challenge(transcript):
    transcript_bytes = transcript.encode('utf-8')
    sha256_hash = hashlib.sha256(transcript_bytes).hexdigest()
    hash_int = int(sha256_hash, 16)
    return hash_int % p

# ============================================================================
# BUILD PROOF (Exercises 19-22)
# ============================================================================

print("\n" + "="*70)
print("BUILDING PROOF")
print("="*70)

transcript = ""

# Exercise 19
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

# Exercise 20
beta = generate_challenge(transcript)
transcript = push(beta, transcript)

gamma = generate_challenge(transcript)
transcript = push(gamma, transcript)

z_poly, N_poly, D_poly = interpolate_z_N_D(a_blind, b_blind, c_blind, beta, gamma, Ω)

c_z = kzg.commit(z_poly)
transcript = push(c_z, transcript)

# Exercise 21
alpha = generate_challenge(transcript)
transcript = push(alpha, transcript)

# Compute L1
L1_factors = []
for m in range(2, n + 1):
    ω_m = pow(ω, m, p)
    numerator_poly = x - ω_m
    denominator_scalar = (ω - ω_m) % p
    denominator_inv = pow(denominator_scalar, p - 2, p)
    factor = numerator_poly * denominator_inv
    L1_factors.append(factor)

L1 = Polynomial([1], p)
for factor in L1_factors:
    L1 = L1 * factor

# Constraints
t_gates = qM * a_blind * b_blind + qL * a_blind + qR * b_blind - c_blind
t_perm_start = (z_poly - 1) * L1
z_shifted = z_poly(x * ω)
t_perm_step = z_poly * N_poly - D_poly * z_shifted

# Master polynomial
bigt = t_gates + alpha * t_perm_start + (alpha * alpha) * t_perm_step

# Quotient
quotient_poly, remainder = bigt.quo_rem(ZH)

c_t = kzg.commit(quotient_poly)
transcript = push(c_t, transcript)

# Exercise 22
zeta = generate_challenge(transcript)
transcript = push(zeta, transcript)

a_zeta = a_blind(zeta)
b_zeta = b_blind(zeta)
c_zeta = c_blind(zeta)
z_zeta = z_poly(zeta)
t_zeta = quotient_poly(zeta)

zeta_omega = (zeta * ω) % p
z_zeta_omega = z_poly(zeta_omega)

print(f"Challenges:")
print(f"  beta = {beta}")
print(f"  gamma = {gamma}")
print(f"  alpha = {alpha}")
print(f"  zeta = {zeta}")

# ============================================================================
# VERIFIER'S COMPUTATION
# ============================================================================

print("\n" + "="*70)
print("VERIFIER'S COMPUTATION")
print("="*70)

# Evaluate selector polynomials at zeta
qL_z = qL(zeta)
qR_z = qR(zeta)
qM_z = qM(zeta)

print(f"\nSelector evaluations at zeta:")
print(f"  qL(zeta) = {qL_z}")
print(f"  qR(zeta) = {qR_z}")
print(f"  qM(zeta) = {qM_z}")

# Evaluate N and D at zeta
# NOTE: The verifier needs to compute N_poly and D_poly!
# Let me check what verify_plonk uses...

print(f"\n" + "="*70)
print("CRITICAL: How does verifier get N_poly and D_poly?")
print("="*70)

# The verifier doesn't have N_poly and D_poly as polynomials!
# They need to compute N(zeta) and D(zeta) from the evaluations

# N(x) at each domain point is the product of numerators
# D(x) at each domain point is the product of denominators

# But at arbitrary zeta (not a domain point), we need the polynomial

# Let's check if the verifier is supposed to have N_poly and D_poly
# Looking at the verify_plonk code, it uses:
#   N_z = N_poly(zeta_v)
#   D_z = D_poly(zeta_v)

# This means the verifier needs access to N_poly and D_poly!
# But these are computed from the witness polynomials...

print(f"\nThe issue: verify_plonk calls N_poly(zeta) and D_poly(zeta)")
print(f"But N_poly and D_poly are computed from a_blind, b_blind, c_blind")
print(f"which the verifier doesn't know!")

print(f"\nLet's check what N_poly and D_poly actually are...")

# Compute N at zeta using the verifier's approach
# The verifier can compute N(zeta) from a_zeta, b_zeta, c_zeta, beta, gamma

print(f"\n" + "="*70)
print("COMPUTING N(zeta) AND D(zeta) - VERIFIER'S METHOD")
print("="*70)

# At evaluation point zeta, the verifier computes:
# N(zeta) and D(zeta) using the permutation structure

# Actually, the verifier needs to know the structure of N and D
# N is the product of (pos + beta*f + gamma) for all columns
# D is the product of (sigma(pos) + beta*f + gamma) for all columns

# But this is evaluated at domain points, not at zeta!
# So we need to interpolate and then evaluate at zeta

# Let me check: does the prover send N_poly and D_poly evaluations?
# Looking at proof_dictionary in cell 98... NO!

print(f"\nProof dictionary does NOT include N(zeta) or D(zeta)!")
print(f"\nBut verify_plonk tries to call N_poly(zeta) and D_poly(zeta)")
print(f"\nThis means N_poly and D_poly must be in scope from earlier cells!")

# Let me check what N_poly should evaluate to at zeta
N_z_actual = N_poly(zeta)
D_z_actual = D_poly(zeta)

print(f"\nActual values from N_poly and D_poly:")
print(f"  N_poly(zeta) = {N_z_actual}")
print(f"  D_poly(zeta) = {D_z_actual}")

# ============================================================================
# VERIFIER'S CONSTRAINT CHECKS
# ============================================================================

print(f"\n" + "="*70)
print("VERIFIER'S CONSTRAINT CHECKS")
print("="*70)

# Gate constraint
t_gates_v = (qM_z * a_zeta * b_zeta + qL_z * a_zeta + qR_z * b_zeta - c_zeta) % p
print(f"\n1. Gate constraint at zeta:")
print(f"   t_gates(zeta) = qM(z)*a(z)*b(z) + qL(z)*a(z) + qR(z)*b(z) - c(z)")
print(f"   t_gates(zeta) = {qM_z}*{a_zeta}*{b_zeta} + {qL_z}*{a_zeta} + {qR_z}*{b_zeta} - {c_zeta}")
print(f"   t_gates(zeta) = {t_gates_v}")

# Check by evaluating the polynomial directly
t_gates_direct = t_gates(zeta)
print(f"   Direct evaluation: t_gates(zeta) = {t_gates_direct}")
print(f"   Match: {t_gates_v == t_gates_direct}")

# Permutation start constraint
L1_z = L1(zeta)
t_perm_start_v = ((z_zeta - 1) * L1_z) % p
print(f"\n2. Permutation start constraint at zeta:")
print(f"   t_perm_start(zeta) = (z(zeta) - 1) * L1(zeta)")
print(f"   t_perm_start(zeta) = ({z_zeta} - 1) * {L1_z}")
print(f"   t_perm_start(zeta) = {t_perm_start_v}")

# Direct evaluation
t_perm_start_direct = t_perm_start(zeta)
print(f"   Direct evaluation: t_perm_start(zeta) = {t_perm_start_direct}")
print(f"   Match: {t_perm_start_v == t_perm_start_direct}")

# Permutation step constraint
t_perm_step_v = (z_zeta * N_z_actual - D_z_actual * z_zeta_omega) % p
print(f"\n3. Permutation step constraint at zeta:")
print(f"   t_perm_step(zeta) = z(zeta) * N(zeta) - D(zeta) * z(zeta*omega)")
print(f"   t_perm_step(zeta) = {z_zeta} * {N_z_actual} - {D_z_actual} * {z_zeta_omega}")
print(f"   t_perm_step(zeta) = {t_perm_step_v}")

# Direct evaluation
t_perm_step_direct = t_perm_step(zeta)
print(f"   Direct evaluation: t_perm_step(zeta) = {t_perm_step_direct}")
print(f"   Match: {t_perm_step_v == t_perm_step_direct}")

# ============================================================================
# MASTER POLYNOMIAL CHECK
# ============================================================================

print(f"\n" + "="*70)
print("MASTER POLYNOMIAL CHECK")
print("="*70)

# Compute master polynomial value at zeta (verifier's way)
alpha_squared = (alpha * alpha) % p
master_poly_v = (t_gates_v + alpha * t_perm_start_v + alpha_squared * t_perm_step_v) % p

print(f"\nMaster polynomial at zeta (verifier computes):")
print(f"  master_poly(zeta) = t_gates(zeta) + alpha*t_perm_start(zeta) + alpha^2*t_perm_step(zeta)")
print(f"  master_poly(zeta) = {t_gates_v} + {alpha}*{t_perm_start_v} + {alpha_squared}*{t_perm_step_v}")
print(f"  master_poly(zeta) = {master_poly_v}")

# Direct evaluation of bigt
bigt_direct = bigt(zeta)
print(f"\nDirect evaluation:")
print(f"  bigt(zeta) = {bigt_direct}")
print(f"  Match: {master_poly_v == bigt_direct}")

# Vanishing polynomial at zeta
ZH_z = (pow(zeta, n, p) - 1) % p
print(f"\nVanishing polynomial at zeta:")
print(f"  ZH(zeta) = zeta^{n} - 1 = {ZH_z}")

# Direct evaluation
ZH_direct = ZH(zeta)
print(f"  Direct: ZH(zeta) = {ZH_direct}")
print(f"  Match: {ZH_z == ZH_direct}")

# Right-hand side: t_zeta * ZH_z
rhs = (t_zeta * ZH_z) % p
print(f"\nRight-hand side:")
print(f"  t_zeta * ZH(zeta) = {t_zeta} * {ZH_z}")
print(f"  t_zeta * ZH(zeta) = {rhs}")

# ============================================================================
# THE CHECK
# ============================================================================

print(f"\n" + "="*70)
print("THE FINAL CHECK")
print("="*70)

print(f"\nDoes master_poly(zeta) == t_zeta * ZH(zeta)?")
print(f"  LHS (master_poly(zeta)) = {master_poly_v}")
print(f"  RHS (t_zeta * ZH(zeta)) = {rhs}")
print(f"  Equal: {master_poly_v == rhs}")

if master_poly_v != rhs:
    diff = (master_poly_v - rhs) % p
    print(f"\n  Difference: {diff}")
    print(f"  Difference (as signed): {diff if diff < p//2 else diff - p}")

# ============================================================================
# DIAGNOSIS
# ============================================================================

print(f"\n" + "="*70)
print("DIAGNOSIS")
print("="*70)

# Check if the issue is with modular arithmetic
print(f"\nChecking if modular arithmetic is the issue...")

# Recompute without intermediate modulo
t_gates_v_no_mod = qM_z * a_zeta * b_zeta + qL_z * a_zeta + qR_z * b_zeta - c_zeta
t_perm_start_v_no_mod = (z_zeta - 1) * L1_z
t_perm_step_v_no_mod = z_zeta * N_z_actual - D_z_actual * z_zeta_omega

master_poly_v_no_mod = t_gates_v_no_mod + alpha * t_perm_start_v_no_mod + alpha**2 * t_perm_step_v_no_mod
master_poly_v_final = master_poly_v_no_mod % p

print(f"\nWithout intermediate modulo:")
print(f"  master_poly(zeta) % p = {master_poly_v_final}")
print(f"  Previous result: {master_poly_v}")
print(f"  Match: {master_poly_v_final == master_poly_v}")

# Check the equation component by component
print(f"\n" + "="*70)
print("COMPONENT-BY-COMPONENT VERIFICATION")
print("="*70)

# Expected relationship: bigt = quotient_poly * ZH
# At zeta: bigt(zeta) = quotient_poly(zeta) * ZH(zeta)

quotient_times_ZH = (quotient_poly(zeta) * ZH(zeta)) % p
bigt_at_zeta = bigt(zeta)

print(f"\nDirect polynomial evaluation:")
print(f"  quotient_poly(zeta) * ZH(zeta) = {quotient_times_ZH}")
print(f"  bigt(zeta) = {bigt_at_zeta}")
print(f"  Match: {quotient_times_ZH == bigt_at_zeta}")

print(f"\nUsing t_zeta from proof:")
print(f"  t_zeta * ZH(zeta) = {t_zeta * ZH_z % p}")
print(f"  quotient_poly(zeta) = {quotient_poly(zeta)}")
print(f"  Match: {t_zeta == quotient_poly(zeta)}")

# ============================================================================
# SUMMARY
# ============================================================================

print(f"\n" + "="*70)
print("SUMMARY")
print("="*70)

if master_poly_v == rhs:
    print(f"\n✓✓✓ QUOTIENT CONSTRAINT CHECK PASSES ✓✓✓")
else:
    print(f"\n✗✗✗ QUOTIENT CONSTRAINT CHECK FAILS ✗✗✗")
    print(f"\nThe verifier's computation of master_poly(zeta) does not equal t_zeta * ZH(zeta)")
    print(f"\nPossible issues:")
    print(f"  1. N_poly and D_poly are not available to the verifier")
    print(f"  2. Modular arithmetic mismatch")
    print(f"  3. Missing evaluations in the proof")

    print(f"\nKey observation:")
    print(f"  The verify_plonk function calls N_poly(zeta_v) and D_poly(zeta_v)")
    print(f"  But N_poly and D_poly are computed from witness polynomials")
    print(f"  The verifier should NOT have access to these!")
    print(f"  ")
    print(f"  The verifier needs N(zeta) and D(zeta) to be sent in the proof,")
    print(f"  OR needs to compute them from public information.")
