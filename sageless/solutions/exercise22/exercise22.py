#!/usr/bin/env python3
"""
Exercise 22: Evaluation Challenge and Opening Proofs

This exercise generates the evaluation challenge ζ (zeta) and computes:
1. Polynomial evaluations at ζ for: a_blind, b_blind, c_blind, z_poly, quotient_poly
2. Polynomial evaluation at ζ·ω for: z_poly
3. KZG opening proofs for all evaluations

These evaluations and proofs allow the verifier to check the polynomial constraints
without knowing the full polynomials themselves.
"""

import sys
import os
import hashlib

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from lib.polynomials import p, Polynomial, PolynomialVar, interpolate
import kzg
from py_ecc.bn128 import multiply

print("="*70)
print("EXERCISE 22: EVALUATION CHALLENGE AND OPENING PROOFS")
print("="*70)

# ============================================================================
# SETUP (from previous exercises)
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

# Interpolate original polynomials
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

# Vanishing polynomial ZH = x^4 - 1
ZH = x
for _ in range(n - 1):
    ZH = ZH * x
ZH = ZH - 1

# ============================================================================
# BLINDING
# ============================================================================

def random_polynomial(degree, modulus):
    import random
    coeffs = [random.randint(0, modulus - 1) for _ in range(degree + 1)]
    return Polynomial(coeffs, modulus)

k = 2
import random
random.seed(42)

a_blind = a + random_polynomial(degree=k-1, modulus=p) * ZH
b_blind = b + random_polynomial(degree=k-1, modulus=p) * ZH
c_blind = c + random_polynomial(degree=k-1, modulus=p) * ZH

# ============================================================================
# PERMUTATION SETUP
# ============================================================================

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

# ============================================================================
# TRUSTED SETUP
# ============================================================================

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

# Initialize kzg
kzg.set_trusted_setup(S1, S2)

print("\n✓ Trusted setup initialized")

# ============================================================================
# TRANSCRIPT FUNCTIONS
# ============================================================================

def push(v, transcript, delim="|"):
    return transcript + delim + str(v)

def generate_challenge(transcript):
    transcript_bytes = transcript.encode('utf-8')
    sha256_hash = hashlib.sha256(transcript_bytes).hexdigest()
    hash_int = int(sha256_hash, 16)
    return hash_int % p

# ============================================================================
# BUILD TRANSCRIPT (from Exercises 19-21)
# ============================================================================

print("\n" + "="*70)
print("BUILDING TRANSCRIPT (Exercises 19-21)")
print("="*70)

transcript = ""

# Exercise 19: Public values and witness commitments
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

print(f"After Exercise 19: {len(transcript)} characters")

# Exercise 20: Challenges and permutation
beta = generate_challenge(transcript)
transcript = push(beta, transcript)

gamma = generate_challenge(transcript)
transcript = push(gamma, transcript)

z_poly, N_poly, D_poly = interpolate_z_N_D(a_blind, b_blind, c_blind, beta, gamma, Ω)

c_z = kzg.commit(z_poly)
transcript = push(c_z, transcript)

print(f"After Exercise 20: {len(transcript)} characters")

# Exercise 21: Master polynomial and quotient
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

print(f"After Exercise 21: {len(transcript)} characters")

# ============================================================================
# EXERCISE 22 SOLUTION
# ============================================================================

print("\n" + "="*70)
print("STEP 4: EVALUATION CHALLENGE AND PROOFS (Exercise 22)")
print("="*70)

# Generate evaluation challenge ζ (zeta)
zeta = generate_challenge(transcript)
print(f"\nGenerated ζ (zeta) from transcript:")
print(f"  ζ = {zeta}")

# Push ζ to transcript
transcript = push(zeta, transcript)
print(f"  Pushed ζ to transcript")

print(f"\nTranscript length after ζ: {len(transcript)} characters")

# Compute evaluations at ζ
print(f"\n" + "="*70)
print("COMPUTING POLYNOMIAL EVALUATIONS AT ζ")
print("="*70)

a_zeta = a_blind(zeta)
print(f"\na_zeta = a_blind(ζ) = {a_zeta}")

b_zeta = b_blind(zeta)
print(f"b_zeta = b_blind(ζ) = {b_zeta}")

c_zeta = c_blind(zeta)
print(f"c_zeta = c_blind(ζ) = {c_zeta}")

z_zeta = z_poly(zeta)
print(f"z_zeta = z_poly(ζ) = {z_zeta}")

t_zeta = quotient_poly(zeta)
print(f"t_zeta = quotient_poly(ζ) = {t_zeta}")

# Compute evaluation at ζ·ω
zeta_omega = (zeta * ω) % p
print(f"\nζ·ω = {zeta_omega}")

z_zeta_omega = z_poly(zeta_omega)
print(f"z_zeta_omega = z_poly(ζ·ω) = {z_zeta_omega}")

# Compute KZG opening proofs
print(f"\n" + "="*70)
print("COMPUTING KZG OPENING PROOFS")
print("="*70)

print(f"\nComputing opening proofs...")

proof_a = kzg.prove(a_blind, zeta)
print(f"  proof_a = prove(a_blind, ζ)")
print(f"    Proof point: {proof_a}")

proof_b = kzg.prove(b_blind, zeta)
print(f"\n  proof_b = prove(b_blind, ζ)")
print(f"    Proof point: {proof_b}")

proof_c = kzg.prove(c_blind, zeta)
print(f"\n  proof_c = prove(c_blind, ζ)")
print(f"    Proof point: {proof_c}")

proof_z = kzg.prove(z_poly, zeta)
print(f"\n  proof_z = prove(z_poly, ζ)")
print(f"    Proof point: {proof_z}")

proof_t = kzg.prove(quotient_poly, zeta)
print(f"\n  proof_t = prove(quotient_poly, ζ)")
print(f"    Proof point: {proof_t}")

proof_z_omega = kzg.prove(z_poly, zeta_omega)
print(f"\n  proof_z_omega = prove(z_poly, ζ·ω)")
print(f"    Proof point: {proof_z_omega}")

# ============================================================================
# VERIFICATION
# ============================================================================

print("\n" + "="*70)
print("VERIFICATION")
print("="*70)

print(f"\nVerifying opening proofs...")

verify_a = kzg.verify(c_a, proof_a, zeta, a_zeta)
print(f"  Verify a_blind(ζ) = {a_zeta}: {verify_a}")

verify_b = kzg.verify(c_b, proof_b, zeta, b_zeta)
print(f"  Verify b_blind(ζ) = {b_zeta}: {verify_b}")

verify_c = kzg.verify(c_c, proof_c, zeta, c_zeta)
print(f"  Verify c_blind(ζ) = {c_zeta}: {verify_c}")

verify_z = kzg.verify(c_z, proof_z, zeta, z_zeta)
print(f"  Verify z_poly(ζ) = {z_zeta}: {verify_z}")

verify_t = kzg.verify(c_t, proof_t, zeta, t_zeta)
print(f"  Verify quotient_poly(ζ) = {t_zeta}: {verify_t}")

verify_z_omega = kzg.verify(c_z, proof_z_omega, zeta_omega, z_zeta_omega)
print(f"  Verify z_poly(ζ·ω) = {z_zeta_omega}: {verify_z_omega}")

all_verified = verify_a and verify_b and verify_c and verify_z and verify_t and verify_z_omega

if all_verified:
    print("\n✓✓✓ ALL OPENING PROOFS VERIFIED SUCCESSFULLY ✓✓✓")
else:
    print("\n✗✗✗ SOME PROOFS FAILED VERIFICATION ✗✗✗")

# ============================================================================
# PROOF ARTIFACTS SUMMARY
# ============================================================================

print("\n" + "="*70)
print("PROOF ARTIFACTS FOR VERIFIER")
print("="*70)

print(f"\nCommitments (sent to verifier):")
print(f"  c_a (witness a commitment)")
print(f"  c_b (witness b commitment)")
print(f"  c_c (witness c commitment)")
print(f"  c_z (permutation accumulator commitment)")
print(f"  c_t (quotient polynomial commitment)")

print(f"\nEvaluations (sent to verifier):")
print(f"  a_zeta = {a_zeta}")
print(f"  b_zeta = {b_zeta}")
print(f"  c_zeta = {c_zeta}")
print(f"  z_zeta = {z_zeta}")
print(f"  t_zeta = {t_zeta}")
print(f"  z_zeta_omega = {z_zeta_omega}")

print(f"\nOpening proofs (sent to verifier):")
print(f"  proof_a (for a_blind at ζ)")
print(f"  proof_b (for b_blind at ζ)")
print(f"  proof_c (for c_blind at ζ)")
print(f"  proof_z (for z_poly at ζ)")
print(f"  proof_t (for quotient_poly at ζ)")
print(f"  proof_z_omega (for z_poly at ζ·ω)")

print(f"\nPublic inputs (known to verifier):")
print(f"  a(ω) = {value_a}")
print(f"  b(ω) = {value_b}")
print(f"  c(ω^4) = {value_c}")

# ============================================================================
# SOLUTION FOR NOTEBOOK CELL 96
# ============================================================================

print("\n" + "="*70)
print("SOLUTION FOR NOTEBOOK CELL 96")
print("="*70)
print("""
zeta = generate_challenge(transcript)
transcript = push(zeta, transcript)

# Evaluate polynomials at ζ
a_zeta = a_blind(zeta)
b_zeta = b_blind(zeta)
c_zeta = c_blind(zeta)
z_zeta = z_poly(zeta)
t_zeta = quotient_poly(zeta)

# Evaluate z_poly at ζ·ω
zeta_omega = (zeta * ω) % p
z_zeta_omega = z_poly(zeta_omega)

# Compute KZG opening proofs
proof_a = kzg.prove(a_blind, zeta)
proof_b = kzg.prove(b_blind, zeta)
proof_c = kzg.prove(c_blind, zeta)
proof_z = kzg.prove(z_poly, zeta)
proof_t = kzg.prove(quotient_poly, zeta)
proof_z_omega = kzg.prove(z_poly, zeta_omega)
""")

print("="*70)
print("✓ Exercise 22 Complete!")
print("="*70)
