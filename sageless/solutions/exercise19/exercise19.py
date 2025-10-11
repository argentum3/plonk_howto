#!/usr/bin/env python3
"""
Exercise 19: Building Fiat-Shamir Transcript - Step 1

This exercise begins the non-interactive proof construction using the
Fiat-Shamir transform. We build a transcript by pushing public values
and commitments, and compute opening proofs for the inputs and output.

Step 1 involves:
1. Evaluating a(ω), b(ω) (inputs) and c(ω^4) (output)
2. Pushing these values to the transcript
3. Computing KZG commitments to blinded polynomials
4. Pushing commitments to the transcript
5. Computing opening proofs (not added to transcript)
"""

import sys
import os
import hashlib

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from lib.polynomials import p, Polynomial, PolynomialVar, interpolate
import kzg

# Setup from previous exercises
n = 4

# Generator ω of multiplicative domain
r = (p - 1) // 4
h = 5
ω = pow(h, r, p)
Ω = [pow(ω, i, p) for i in range(1, n+1)]

# Circuit values
LI = {1:0, 2:1, 3:1, 4:3}
RI = {1:1, 2:1, 3:2, 4:3}
O  = {1:1, 2:2, 3:3, 4:9}

# Interpolate original polynomials over Ω
a = interpolate(Ω, list(LI.values()))
b = interpolate(Ω, list(RI.values()))
c = interpolate(Ω, list(O.values()))

# Vanishing polynomial ZH = x^4 - 1
x = PolynomialVar(p)
ZH = x
for _ in range(n - 1):
    ZH = ZH * x
ZH = ZH - 1

# Helper functions
def random_polynomial(degree, modulus):
    """Generate a random polynomial of given degree"""
    import random
    coeffs = [random.randint(0, modulus - 1) for _ in range(degree + 1)]
    return Polynomial(coeffs, modulus)

def push(v, transcript, delim="|"):
    """Add a value to the transcript"""
    return transcript + delim + str(v)

# Blind polynomials (from Exercise 18)
k = 2
import random
random.seed(42)  # For reproducibility

p_poly_a = random_polynomial(degree=k-1, modulus=p)
a_blind = a + p_poly_a * ZH

p_poly_b = random_polynomial(degree=k-1, modulus=p)
b_blind = b + p_poly_b * ZH

p_poly_c = random_polynomial(degree=k-1, modulus=p)
c_blind = c + p_poly_c * ZH

# ============================================================================
# EXERCISE 19: BUILDING TRANSCRIPT - STEP 1
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("EXERCISE 19: FIAT-SHAMIR TRANSCRIPT - STEP 1")
    print("=" * 70)

    print("\nStep 1: Public inputs/outputs and commitments")
    print("  - Evaluate a(ω), b(ω) (inputs)")
    print("  - Evaluate c(ω^4) (output)")
    print("  - Push values to transcript")
    print("  - Compute commitments to blinded polynomials")
    print("  - Compute opening proofs")

    print("\n" + "=" * 70)
    print("EVALUATING WITNESS POLYNOMIALS")
    print("=" * 70)

    # Evaluate at ω (first point in domain)
    ω_1 = pow(ω, 1, p)
    value_a = a(ω_1)
    value_b = b(ω_1)

    print(f"\nInputs (at ω):")
    print(f"  a(ω) = {value_a} (expected 0)")
    print(f"  b(ω) = {value_b} (expected 1)")

    # Evaluate at ω^4 (fourth point in domain - the output)
    ω_4 = pow(ω, 4, p)
    value_c = c(ω_4)

    print(f"\nOutput (at ω^4):")
    print(f"  c(ω^4) = {value_c} (expected 9)")

    # Verify expected values
    assert value_a == 0, f"Expected a(ω) = 0, got {value_a}"
    assert value_b == 1, f"Expected b(ω) = 1, got {value_b}"
    assert value_c == 9, f"Expected c(ω^4) = 9, got {value_c}"
    print("\n✓ All values match expected circuit behavior")

    print("\n" + "=" * 70)
    print("BUILDING TRANSCRIPT")
    print("=" * 70)

    # Start with empty transcript
    transcript = ""
    print(f"\nInitial transcript: '{transcript}'")

    # Push public values in order
    transcript = push(value_a, transcript)
    print(f"After pushing a(ω)=0: ...{transcript[-30:]}")

    transcript = push(value_b, transcript)
    print(f"After pushing b(ω)=1: ...{transcript[-30:]}")

    transcript = push(value_c, transcript)
    print(f"After pushing c(ω^4)=9: ...{transcript[-30:]}")

    print("\n" + "=" * 70)
    print("COMPUTING KZG COMMITMENTS")
    print("=" * 70)

    # Compute trusted setup (from Exercise 7)
    from py_ecc.bn128 import multiply
    τ = 424242  # Toxic waste
    l = 10  # Degree bound
    P = kzg.P

    # Compute S1 = [P, τP, τ²P, ..., τˡP]
    S1 = []
    τ_power = 1
    for i in range(l + 1):
        point = multiply(P, τ_power % kzg.n)
        S1.append(point)
        τ_power = (τ_power * τ) % kzg.n

    # Commitment function (from Exercise 8)
    def commitment(S1, poly):
        from py_ecc.bn128 import multiply, add, Z1
        coeffs = poly.coeffs
        c = Z1
        for i, coeff in enumerate(coeffs):
            if i < len(S1):
                term = multiply(S1[i], coeff % kzg.n)
                c = add(c, term)
        return c

    # Proof function (from Exercise 9)
    def prove(S1, poly, γ):
        from lib.polynomials import Polynomial
        # Compute quotient Q(x) = (p(x) - p(γ)) / (x - γ)
        p_γ = poly(γ)
        numerator = poly - Polynomial([p_γ], p)
        divisor = Polynomial([(-γ) % p, 1], p)  # x - γ
        quotient, remainder = numerator.quo_rem(divisor)
        # π = commitment to quotient
        π = commitment(S1, quotient)
        return π

    # Verify function (from Exercise 10)
    def verify(commitment_C, proof_π, γ, v):
        from py_ecc.bn128 import pairing, G2, multiply, add, neg
        # Check e(C - vP, G2) = e(π, τG2 - γG2)
        # Compute C - vP
        vP = multiply(P, v % kzg.n)
        C_minus_vP = add(commitment_C, neg(vP))
        # Compute τG2 - γG2 = (τ - γ)G2
        τ_minus_γ = (τ - γ) % kzg.n
        τ_minus_γ_G2 = multiply(G2, τ_minus_γ)
        # Compute pairings
        lhs = pairing(G2, C_minus_vP)
        rhs = pairing(τ_minus_γ_G2, proof_π)
        return lhs == rhs

    # Commit to blinded polynomials
    print("\nCommitting to blinded witness polynomials:")

    c_a = commitment(S1, a_blind)
    print(f"  c_a = commitment(S1, a_blind)")
    print(f"    = {c_a}")

    c_b = commitment(S1, b_blind)
    print(f"  c_b = commitment(S1, b_blind)")
    print(f"    = {c_b}")

    c_c = commitment(S1, c_blind)
    print(f"  c_c = commitment(S1, c_blind)")
    print(f"    = {c_c}")

    # Push commitments to transcript
    print("\nPushing commitments to transcript:")
    transcript = push(c_a, transcript)
    print(f"  After c_a: ...{transcript[-40:]}")

    transcript = push(c_b, transcript)
    print(f"  After c_b: ...{transcript[-40:]}")

    transcript = push(c_c, transcript)
    print(f"  After c_c: ...{transcript[-40:]}")

    print("\n" + "=" * 70)
    print("COMPUTING OPENING PROOFS")
    print("=" * 70)

    print("\nComputing proofs for witness openings:")
    print("  (Proofs are NOT added to transcript)")

    # Proof for a at ω
    proof_value_a = prove(S1, a_blind, ω_1)
    print(f"\n  proof_value_a = prove(S1, a_blind, ω)")
    print(f"    Point: ω = {ω_1}")
    print(f"    Value: a_blind(ω) = {a_blind(ω_1)}")
    print(f"    Proof: {proof_value_a}")

    # Proof for b at ω
    proof_value_b = prove(S1, b_blind, ω_1)
    print(f"\n  proof_value_b = prove(S1, b_blind, ω)")
    print(f"    Point: ω = {ω_1}")
    print(f"    Value: b_blind(ω) = {b_blind(ω_1)}")
    print(f"    Proof: {proof_value_b}")

    # Proof for c at ω^4
    proof_output = prove(S1, c_blind, ω_4)
    print(f"\n  proof_output = prove(S1, c_blind, ω^4)")
    print(f"    Point: ω^4 = {ω_4}")
    print(f"    Value: c_blind(ω^4) = {c_blind(ω_4)}")
    print(f"    Proof: {proof_output}")

    print("\n" + "=" * 70)
    print("VERIFYING PROOFS")
    print("=" * 70)

    # Verify the proofs work correctly
    print("\nVerifying opening proofs:")

    verify_a = verify(c_a, proof_value_a, ω_1, value_a)
    print(f"  Verify a(ω) = 0: {verify_a}")
    assert verify_a, "Proof for a failed!"

    verify_b = verify(c_b, proof_value_b, ω_1, value_b)
    print(f"  Verify b(ω) = 1: {verify_b}")
    assert verify_b, "Proof for b failed!"

    verify_c = verify(c_c, proof_output, ω_4, value_c)
    print(f"  Verify c(ω^4) = 9: {verify_c}")
    assert verify_c, "Proof for c failed!"

    print("\n✓ All opening proofs verified successfully!")

    print("\n" + "=" * 70)
    print("✓ Exercise 19 Complete!")
    print("=" * 70)

    print("\nTranscript state after Step 1:")
    print(f"  Length: {len(transcript)} characters")
    print(f"  Contains: inputs (a(ω), b(ω)), output (c(ω^4)), commitments (c_a, c_b, c_c)")

    print("\nProofs computed (not in transcript):")
    print(f"  proof_value_a: Opening proof for a(ω) = 0")
    print(f"  proof_value_b: Opening proof for b(ω) = 1")
    print(f"  proof_output: Opening proof for c(ω^4) = 9")

    print("\nNext step (Exercise 20):")
    print("  - Generate β and γ challenges from transcript")
    print("  - Interpolate z, N, D polynomials")
    print("  - Commit to z polynomial")

    # Print solutions for notebook
    print("\n" + "=" * 70)
    print("SOLUTIONS FOR NOTEBOOK (cell 89):")
    print("=" * 70)
    print(f"""
transcript = ""
# Evaluate witness polynomials at input/output points
value_a = a(ω)  # Should be 0
value_b = b(ω)  # Should be 1
value_c = c(pow(ω, 4, p))  # Should be 9

# Push values to transcript
transcript = push(value_a, transcript)
transcript = push(value_b, transcript)
transcript = push(value_c, transcript)

# Compute commitments to blinded polynomials
c_a = kzg.commit(a_blind)
c_b = kzg.commit(b_blind)
c_c = kzg.commit(c_blind)

# Push commitments to transcript
transcript = push(c_a, transcript)
transcript = push(c_b, transcript)
transcript = push(c_c, transcript)

# Compute opening proofs (NOT added to transcript)
proof_value_a = kzg.prove(a_blind, ω)
proof_value_b = kzg.prove(b_blind, ω)
proof_output = kzg.prove(c_blind, pow(ω, 4, p))
""")
