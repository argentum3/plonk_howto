#!/usr/bin/env python3
"""
Exercise 20: Generating Challenges and Permutation Polynomials

This exercise continues building the Fiat-Shamir transcript by:
1. Generating challenge β from the transcript
2. Generating challenge γ from the transcript
3. Computing z, N, D polynomials using β and γ
4. Committing to z polynomial and adding to transcript

The challenges β and γ are used in the permutation argument to
ensure copy constraints are satisfied across the circuit.
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
print("EXERCISE 20: CHALLENGES AND PERMUTATION POLYNOMIALS")
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
qL_vals = [0, 0, 0, 1]
qR_vals = [0, 0, 0, 1]
qM_vals = [1, 1, 1, 0]
qL = interpolate(Ω, qL_vals)
qR = interpolate(Ω, qR_vals)
qM = interpolate(Ω, qM_vals)

# Vanishing polynomial
x = PolynomialVar(p)
ZH = x
for _ in range(n - 1):
    ZH = ZH * x
ZH = ZH - 1

# ============================================================================
# BLINDING (from Exercise 18)
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
# PERMUTATION SETUP (from Exercise 14)
# ============================================================================

def pos(column, index):
    """Convert (column, index) to position in flattened array"""
    return ((column-1)*n + index)

# Permutation encoding wiring constraints
sigma = {}
sigma[pos(1,1)] = pos(1,1)  # a[1] = 0 (constant)
sigma[pos(1,2)] = pos(2,1)  # a[2] ↔ b[1]
sigma[pos(2,1)] = pos(1,2)
sigma[pos(1,3)] = pos(2,2)  # a[3] → b[2] → c[1] → a[3]
sigma[pos(2,2)] = pos(3,1)
sigma[pos(3,1)] = pos(1,3)
sigma[pos(3,2)] = pos(2,3)  # c[2] ↔ b[3]
sigma[pos(2,3)] = pos(3,2)
sigma[pos(3,3)] = pos(1,4)  # c[3] → a[4] → b[4] → c[3]
sigma[pos(1,4)] = pos(2,4)
sigma[pos(2,4)] = pos(3,3)
sigma[pos(3,4)] = pos(3,4)  # c[4] = 9 (output)

# ============================================================================
# PERMUTATION FUNCTIONS (from Exercises 15-17)
# ============================================================================

def numerator(i, column, f, sigma, beta, gamma):
    """Compute numerator for grand product argument: pos(column, i) + β·f(ω^i) + γ"""
    position = pos(column, i)
    ω_to_i = pow(ω, i, p)
    f_of_ω_i = f(ω_to_i)
    value = (position + beta * f_of_ω_i + gamma) % p
    return value

def denominator(i, column, f, sigma, beta, gamma):
    """Compute denominator for grand product argument: σ(pos(column, i)) + β·f(ω^i) + γ"""
    position = pos(column, i)
    sigma_position = sigma[position]
    ω_to_i = pow(ω, i, p)
    f_of_ω_i = f(ω_to_i)
    value = (sigma_position + beta * f_of_ω_i + gamma) % p
    return value

def interpolate_z_N_D(a, b, c, beta, gamma, Ω):
    """
    Compute and interpolate the z, N, and D polynomials for permutation argument.

    The z polynomial satisfies:
        z(ω) = 1 (base case)
        z(ω^(i+1)) = z(ω^i) · [N(ω^i) / D(ω^i)]
    """
    n = len(Ω)
    z_values = []
    N_values = []
    D_values = []

    z_current = 1

    for i in range(1, n + 1):
        z_values.append(z_current)

        # Compute numerator and denominator for all three columns
        num_a = numerator(i, 1, a, sigma, beta, gamma)
        num_b = numerator(i, 2, b, sigma, beta, gamma)
        num_c = numerator(i, 3, c, sigma, beta, gamma)

        den_a = denominator(i, 1, a, sigma, beta, gamma)
        den_b = denominator(i, 2, b, sigma, beta, gamma)
        den_c = denominator(i, 3, c, sigma, beta, gamma)

        # N(ω^i) = product of all numerators
        N_i = (num_a * num_b * num_c) % p
        N_values.append(N_i)

        # D(ω^i) = product of all denominators
        D_i = (den_a * den_b * den_c) % p
        D_values.append(D_i)

        # Update z for next iteration
        D_i_inv = pow(D_i, p - 2, p)
        z_current = (z_current * N_i * D_i_inv) % p

    # Interpolate polynomials
    z_poly = interpolate(Ω, z_values)
    N_poly = interpolate(Ω, N_values)
    D_poly = interpolate(Ω, D_values)

    return z_poly, N_poly, D_poly

# ============================================================================
# TRUSTED SETUP (from Exercise 7)
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
    """Add a value to the transcript"""
    return transcript + delim + str(v)

def generate_challenge(transcript):
    """Generate a challenge by hashing the transcript"""
    transcript_bytes = transcript.encode('utf-8')
    sha256_hash = hashlib.sha256(transcript_bytes).hexdigest()
    hash_int = int(sha256_hash, 16)
    return hash_int % p

# ============================================================================
# BUILD INITIAL TRANSCRIPT (from Exercise 19)
# ============================================================================

print("\n" + "="*70)
print("STEP 1: INITIAL TRANSCRIPT (Exercise 19)")
print("="*70)

transcript = ""

# Evaluate and push public values
value_a = a(ω)
value_b = b(ω)
value_c = c(pow(ω, 4, p))

transcript = push(value_a, transcript)
transcript = push(value_b, transcript)
transcript = push(value_c, transcript)

print(f"\nPublic values: a(ω)={value_a}, b(ω)={value_b}, c(ω^4)={value_c}")

# Commit to blinded polynomials
c_a = kzg.commit(a_blind)
c_b = kzg.commit(b_blind)
c_c = kzg.commit(c_blind)

transcript = push(c_a, transcript)
transcript = push(c_b, transcript)
transcript = push(c_c, transcript)

print(f"Transcript length after step 1: {len(transcript)} characters")

# ============================================================================
# EXERCISE 20 SOLUTION
# ============================================================================

print("\n" + "="*70)
print("STEP 2: CHALLENGES AND PERMUTATION (Exercise 20)")
print("="*70)

# Generate challenge β from transcript
beta = generate_challenge(transcript)
print(f"\nGenerated β from transcript:")
print(f"  β = {beta}")

# Push β to transcript
transcript = push(beta, transcript)
print(f"  Pushed β to transcript")

# Generate challenge γ from updated transcript
gamma = generate_challenge(transcript)
print(f"\nGenerated γ from transcript:")
print(f"  γ = {gamma}")

# Push γ to transcript
transcript = push(gamma, transcript)
print(f"  Pushed γ to transcript")

print(f"\nTranscript length after challenges: {len(transcript)} characters")

# Interpolate z, N, D polynomials using β and γ
print(f"\nComputing permutation polynomials with β={beta}, γ={gamma}...")
z_poly, N_poly, D_poly = interpolate_z_N_D(a_blind, b_blind, c_blind, beta, gamma, Ω)

print(f"  z_poly: degree {z_poly.degree()}")
print(f"  N_poly: degree {N_poly.degree()}")
print(f"  D_poly: degree {D_poly.degree()}")

# Verify z(ω) = 1
z_at_ω = z_poly(ω)
print(f"\nVerification: z(ω) = {z_at_ω} (should be 1)")
assert z_at_ω == 1, "z(ω) should equal 1!"

# Commit to z polynomial
c_z = kzg.commit(z_poly)
print(f"\nCommitment to z:")
print(f"  c_z = {c_z}")

# Push z commitment to transcript
transcript = push(c_z, transcript)
print(f"  Pushed c_z to transcript")

print(f"\nFinal transcript length: {len(transcript)} characters")

# ============================================================================
# VERIFICATION
# ============================================================================

print("\n" + "="*70)
print("VERIFICATION")
print("="*70)

# Check L1*(z-1) divisible by ZH
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

check1 = ZH.divides(L1*(z_poly-1))
print(f"\nZH divides L1*(z-1): {check1}")

# Check recursive constraint
check2 = ZH.divides(z_poly*N_poly - D_poly*z_poly(x*ω))
print(f"ZH divides z*N - D*z(x*ω): {check2}")

if check1 and check2:
    print("\n✓✓✓ ALL VERIFICATION CHECKS PASSED ✓✓✓")
else:
    print("\n✗✗✗ VERIFICATION FAILED ✗✗✗")

# ============================================================================
# SOLUTION FOR NOTEBOOK CELL 92
# ============================================================================

print("\n" + "="*70)
print("SOLUTION FOR NOTEBOOK CELL 92")
print("="*70)
print("""
beta = generate_challenge(transcript)
transcript = push(beta, transcript)
gamma = generate_challenge(transcript)
transcript = push(gamma, transcript)
z_poly, N_poly, D_poly = interpolate_z_N_D(a_blind, b_blind, c_blind, beta, gamma, Ω)
c_z = kzg.commit(z_poly)
transcript = push(c_z, transcript)
""")

print("="*70)
print("✓ Exercise 20 Complete!")
print("="*70)
