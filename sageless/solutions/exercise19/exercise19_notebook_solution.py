#!/usr/bin/env python3
"""
Exercise 19: Notebook solution using kzg.commit() and kzg.prove()

This solution demonstrates the simplified API that matches what's expected
in the notebook cell 90.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from lib.polynomials import p, Polynomial, PolynomialVar, interpolate
import kzg
from py_ecc.bn128 import multiply

print("="*70)
print("EXERCISE 19: FIAT-SHAMIR TRANSCRIPT - STEP 1 (Notebook Version)")
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

# Initialize kzg with trusted setup
kzg.set_trusted_setup(S1, S2)

print("\n✓ Trusted setup initialized")

# ============================================================================
# EXERCISE 19 SOLUTION
# ============================================================================

def push(v, transcript, delim="|"):
    """Add a value to the transcript"""
    return transcript + delim + str(v)

print("\n" + "="*70)
print("EXERCISE 19 SOLUTION")
print("="*70)

# Start with empty transcript
transcript = ""

# Evaluate witness polynomials at input/output points
value_a = a(ω)  # Should be 0
value_b = b(ω)  # Should be 1
value_c = c(pow(ω, 4, p))  # Should be 9

print(f"\nPublic values:")
print(f"  a(ω) = {value_a} (input 1)")
print(f"  b(ω) = {value_b} (input 2)")
print(f"  c(ω^4) = {value_c} (output)")

# Push values to transcript
transcript = push(value_a, transcript)
transcript = push(value_b, transcript)
transcript = push(value_c, transcript)

print(f"\nTranscript after pushing values:")
print(f"  '{transcript}'")

# Compute commitments to blinded polynomials
c_a = kzg.commit(a_blind)
c_b = kzg.commit(b_blind)
c_c = kzg.commit(c_blind)

print(f"\nCommitments:")
print(f"  c_a = {c_a}")
print(f"  c_b = {c_b}")
print(f"  c_c = {c_c}")

# Push commitments to transcript
transcript = push(c_a, transcript)
transcript = push(c_b, transcript)
transcript = push(c_c, transcript)

print(f"\nTranscript after pushing commitments:")
print(f"  Length: {len(transcript)} characters")

# Compute opening proofs (NOT added to transcript)
proof_value_a = kzg.prove(a_blind, ω)
proof_value_b = kzg.prove(b_blind, ω)
proof_output = kzg.prove(c_blind, pow(ω, 4, p))

print(f"\nOpening proofs (not in transcript):")
print(f"  proof_value_a = {proof_value_a}")
print(f"  proof_value_b = {proof_value_b}")
print(f"  proof_output = {proof_output}")

# ============================================================================
# VERIFICATION
# ============================================================================

print("\n" + "="*70)
print("VERIFICATION")
print("="*70)

verify_a = kzg.verify(c_a, proof_value_a, ω, value_a)
verify_b = kzg.verify(c_b, proof_value_b, ω, value_b)
verify_c = kzg.verify(c_c, proof_output, pow(ω, 4, p), value_c)

print(f"\nProof verifications:")
print(f"  verify(c_a, proof_value_a, ω, {value_a}) = {verify_a}")
print(f"  verify(c_b, proof_value_b, ω, {value_b}) = {verify_b}")
print(f"  verify(c_c, proof_output, ω^4, {value_c}) = {verify_c}")

if verify_a and verify_b and verify_c:
    print("\n✓✓✓ ALL PROOFS VERIFIED SUCCESSFULLY ✓✓✓")
else:
    print("\n✗✗✗ PROOF VERIFICATION FAILED ✗✗✗")

# ============================================================================
# SOLUTION FOR NOTEBOOK CELL 90
# ============================================================================

print("\n" + "="*70)
print("SOLUTION FOR NOTEBOOK CELL 90")
print("="*70)
print("""
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
""")

print("="*70)
print("✓ Exercise 19 Complete!")
print("="*70)
