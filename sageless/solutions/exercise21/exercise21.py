#!/usr/bin/env python3
"""
Exercise 21: Master Polynomial Construction

This exercise builds the "master polynomial" that combines both gate constraints
and permutation constraints into a single polynomial. This is more efficient than
checking each constraint separately.

The master polynomial is:
    bigt = t_gates + α·t_perm_start + α²·t_perm_step

Where:
- t_gates: gate constraint polynomial
- t_perm_start: boundary constraint (z(ω) = 1)
- t_perm_step: recursive permutation constraint
- α: random challenge combining the constraints

The quotient polynomial is then:
    quotient_poly = bigt / ZH

This quotient is what the verifier will check to ensure all constraints are satisfied.
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
print("EXERCISE 21: MASTER POLYNOMIAL CONSTRUCTION")
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

# Selector polynomials (from Exercise 12/13)
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
    """Compute numerator for grand product argument"""
    position = pos(column, i)
    ω_to_i = pow(ω, i, p)
    f_of_ω_i = f(ω_to_i)
    value = (position + beta * f_of_ω_i + gamma) % p
    return value

def denominator(i, column, f, sigma, beta, gamma):
    """Compute denominator for grand product argument"""
    position = pos(column, i)
    sigma_position = sigma[position]
    ω_to_i = pow(ω, i, p)
    f_of_ω_i = f(ω_to_i)
    value = (sigma_position + beta * f_of_ω_i + gamma) % p
    return value

def interpolate_z_N_D(a, b, c, beta, gamma, Ω):
    """Compute and interpolate z, N, D polynomials for permutation argument"""
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
    """Add a value to the transcript"""
    return transcript + delim + str(v)

def generate_challenge(transcript):
    """Generate a challenge by hashing the transcript"""
    transcript_bytes = transcript.encode('utf-8')
    sha256_hash = hashlib.sha256(transcript_bytes).hexdigest()
    hash_int = int(sha256_hash, 16)
    return hash_int % p

# ============================================================================
# BUILD TRANSCRIPT (from Exercises 19-20)
# ============================================================================

print("\n" + "="*70)
print("BUILDING TRANSCRIPT (Exercises 19-20)")
print("="*70)

transcript = ""

# Step 1: Public values and witness commitments (Exercise 19)
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

# Step 2: Challenges and permutation (Exercise 20)
beta = generate_challenge(transcript)
transcript = push(beta, transcript)

gamma = generate_challenge(transcript)
transcript = push(gamma, transcript)

z_poly, N_poly, D_poly = interpolate_z_N_D(a_blind, b_blind, c_blind, beta, gamma, Ω)

c_z = kzg.commit(z_poly)
transcript = push(c_z, transcript)

print(f"After Exercise 20: {len(transcript)} characters")

# ============================================================================
# EXERCISE 21 SOLUTION
# ============================================================================

print("\n" + "="*70)
print("STEP 3: MASTER POLYNOMIAL (Exercise 21)")
print("="*70)

# Generate challenge α from transcript
alpha = generate_challenge(transcript)
print(f"\nGenerated α from transcript:")
print(f"  α = {alpha}")

# Push α to transcript
transcript = push(alpha, transcript)
print(f"  Pushed α to transcript")

# Compute L1 (Lagrange basis polynomial for first point)
print(f"\nComputing L1 polynomial...")
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

print(f"  L1: degree {L1.degree()}")

# Compute gate constraint polynomial
print(f"\nComputing t_gates...")
t_gates = qM * a_blind * b_blind + qL * a_blind + qR * b_blind - c_blind
print(f"  t_gates: degree {t_gates.degree()}")

# Compute permutation start constraint (boundary condition)
print(f"\nComputing t_perm_start...")
t_perm_start = (z_poly - 1) * L1
print(f"  t_perm_start = (z_poly - 1) * L1")
print(f"  t_perm_start: degree {t_perm_start.degree()}")

# Compute shifted z polynomial: z(x*ω)
print(f"\nComputing z_shifted = z_poly(x*ω)...")
z_shifted = z_poly(x * ω)
print(f"  z_shifted: degree {z_shifted.degree()}")

# Compute permutation step constraint (recursive relation)
print(f"\nComputing t_perm_step...")
t_perm_step = z_poly * N_poly - D_poly * z_shifted
print(f"  t_perm_step = z_poly * N_poly - D_poly * z_shifted")
print(f"  t_perm_step: degree {t_perm_step.degree()}")

# Compute master polynomial: bigt = t_gates + α·t_perm_start + α²·t_perm_step
print(f"\nComputing master polynomial bigt...")
print(f"  bigt = t_gates + α·t_perm_start + α²·t_perm_step")

alpha_squared = (alpha * alpha) % p
bigt = t_gates + (alpha * t_perm_start) + (alpha_squared * t_perm_step)
print(f"  bigt: degree {bigt.degree()}")

# Compute quotient polynomial: bigt / ZH
print(f"\nComputing quotient polynomial...")
quotient_poly, remainder = bigt.quo_rem(ZH)

print(f"  quotient_poly = bigt / ZH")
print(f"  quotient_poly: degree {quotient_poly.degree()}")
print(f"  remainder: degree {remainder.degree()} (should be -1 for zero polynomial)")

# Verify division is exact
if remainder.degree() == -1 or all(c == 0 for c in remainder.coeffs):
    print(f"  ✓ ZH divides bigt exactly (remainder is zero)")
else:
    print(f"  ✗ WARNING: ZH does not divide bigt exactly!")
    print(f"     Remainder coeffs: {remainder.coeffs[:5]}...")

# Commit to quotient polynomial
c_t = kzg.commit(quotient_poly)
print(f"\nCommitment to quotient polynomial:")
print(f"  c_t = {c_t}")

# Push quotient commitment to transcript
transcript = push(c_t, transcript)
print(f"  Pushed c_t to transcript")

print(f"\nFinal transcript length: {len(transcript)} characters")

# ============================================================================
# VERIFICATION
# ============================================================================

print("\n" + "="*70)
print("VERIFICATION")
print("="*70)

# Verify that ZH divides each constraint polynomial
print(f"\nVerifying individual constraint polynomials:")

check_gates = ZH.divides(t_gates)
print(f"  ZH divides t_gates: {check_gates}")

check_perm_start = ZH.divides(t_perm_start)
print(f"  ZH divides t_perm_start: {check_perm_start}")

check_perm_step = ZH.divides(t_perm_step)
print(f"  ZH divides t_perm_step: {check_perm_step}")

# Verify master polynomial
check_bigt = ZH.divides(bigt)
print(f"\nZH divides bigt (master polynomial): {check_bigt}")

if check_gates and check_perm_start and check_perm_step and check_bigt:
    print("\n✓✓✓ ALL VERIFICATION CHECKS PASSED ✓✓✓")
else:
    print("\n⚠️  Some verification checks failed")
    if not check_gates:
        print("   - Gate constraints not satisfied")
    if not check_perm_start:
        print("   - Permutation boundary constraint not satisfied")
    if not check_perm_step:
        print("   - Permutation recursive constraint not satisfied")

# ============================================================================
# SOLUTION FOR NOTEBOOK CELL 94
# ============================================================================

print("\n" + "="*70)
print("SOLUTION FOR NOTEBOOK CELL 94")
print("="*70)
print("""
alpha = generate_challenge(transcript)
transcript = push(alpha, transcript)

# Compute L1 polynomial
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

# Gate constraint
t_gates = qM * a_blind * b_blind + qL * a_blind + qR * b_blind - c_blind

# Permutation constraints
t_perm_start = (z_poly - 1) * L1
z_shifted = z_poly(x * ω)
t_perm_step = z_poly * N_poly - D_poly * z_shifted

# Master polynomial
bigt = t_gates + alpha * t_perm_start + (alpha * alpha) * t_perm_step

# Quotient polynomial
quotient_poly, remainder = bigt.quo_rem(ZH)

# Commit and push to transcript
c_t = kzg.commit(quotient_poly)
transcript = push(c_t, transcript)
""")

print("="*70)
print("✓ Exercise 21 Complete!")
print("="*70)
