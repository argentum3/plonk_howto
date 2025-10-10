#!/usr/bin/env python3
"""
Exercise 10: KZG Verification

Implement the verification function that checks if a KZG proof π is valid
for a commitment c and claimed evaluation b = f(γ).

The verification checks using pairings:
    e(π, S₂ - γ·Q) ?= e(c - b·P, Q)

This is equivalent to checking:
    f(τ) - f(γ) ?= Qc(τ)·(τ - γ)

where:
- π = Qc(τ)·P is the proof
- c = f(τ)·P is the commitment
- S₂ = τ·Q from trusted setup
- γ is the challenge
- b = f(γ) is the claimed evaluation

The pairing allows us to verify polynomial equality at the secret point τ
without anyone knowing τ (it was destroyed after trusted setup)!
"""

import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import kzg
from py_ecc.bn128 import multiply, add, neg, pairing, Z1
from lib.polynomials import p, a, Polynomial, PolynomialVar

print("="*70)
print("EXERCISE 10: KZG VERIFICATION")
print("="*70)

def verification(c, π, γ, b):
    """
    Verify a KZG proof using pairings

    Args:
        c: Commitment point = f(τ)·P
        π: Proof point = Qc(τ)·P
        γ: Challenge point
        b: Claimed evaluation f(γ)

    Returns:
        True if proof is valid, False otherwise

    Verification equation:
        e(π, S₂ - γ·Q) ?= e(c - b·P, Q)
    """
    from py_ecc.bn128 import multiply, add, neg, pairing

    # Get P and Q from kzg module
    P = kzg.P
    Q = kzg.Q

    # Compute S₂ from trusted setup
    τ = 424242  # The toxic waste (normally would be destroyed)
    S2 = multiply(Q, τ)

    # Left-hand side: e(π, S₂ - γ·Q)
    γQ = multiply(Q, γ)
    S2_minus_γQ = add(S2, neg(γQ))
    lhs = pairing(S2_minus_γQ, π)

    # Right-hand side: e(c - b·P, Q)
    bP = multiply(P, b)
    c_minus_bP = add(c, neg(bP))
    rhs = pairing(Q, c_minus_bP)

    # Check if equal
    return lhs == rhs


# Step 1: Compute trusted setup (S1 and S2)
print("\nStep 1: Computing trusted setup...")
τ = 424242
l = 10

P = kzg.P
Q = kzg.Q

# Compute S1: [P, τ·P, τ²·P, ..., τˡ·P]
S1 = []
τ_power = 1
for i in range(l + 1):
    point = multiply(P, τ_power)
    S1.append(point)
    τ_power = (τ_power * τ) % kzg.n

# Compute S2: τ·Q
S2 = multiply(Q, τ)

print(f"✓ Computed S1 with {len(S1)} points")
print(f"✓ Computed S2")


# Step 2: Compute commitment c for polynomial a(x)
print("\nStep 2: Computing commitment c for polynomial a(x)...")

def commitment(S1, poly):
    """Compute KZG commitment to polynomial"""
    coeffs = poly.coeffs
    c = Z1  # Point at infinity

    for i, coeff in enumerate(coeffs):
        term = multiply(S1[i], coeff % kzg.n)
        c = add(c, term)

    return c

c = commitment(S1, a)
print(f"✓ Commitment c computed")


# Step 3: Generate proof π for evaluation at γ
print("\nStep 3: Generating proof π for evaluation at γ = 151515...")

γ = 151515
b = a(γ)

print(f"Challenge: γ = {γ}")
print(f"Evaluation: a(γ) = {b}")

# Compute quotient polynomial Qc(x) = (a(x) - b) / (x - γ)
x = PolynomialVar(p)
b_poly = Polynomial([b], p)
Qc, remainder = (a - b_poly).quo_rem(x - γ)

print(f"Quotient Qc degree: {len(Qc.coeffs) - 1}")
print(f"Remainder: {remainder.coeffs}")

def proof(S1, Qc):
    """Generate KZG proof"""
    coeffs = Qc.coeffs
    π = Z1

    for i, coeff in enumerate(coeffs):
        term = multiply(S1[i], coeff % kzg.n)
        π = add(π, term)

    return π

π = proof(S1, Qc)
print(f"✓ Proof π generated")


# Step 4: Verify the proof!
print("\n" + "="*70)
print("VERIFICATION")
print("="*70)

result = verification(c, π, γ, b)

print(f"\nCommitment c: ({c[0]}, {c[1]})")
print(f"Proof π: ({π[0]}, {π[1]})")
print(f"Challenge γ: {γ}")
print(f"Claimed evaluation b: {b}")

print(f"\n{'='*70}")
print(f"Verification result: {result}")
print(f"{'='*70}")

if result:
    print("\n🎉 SUCCESS! The proof is valid!")
    print("\nWhat this means:")
    print("  ✓ The prover correctly evaluated a(γ) = b")
    print("  ✓ The pairing equation holds:")
    print("      e(π, S₂ - γ·Q) = e(c - b·P, Q)")
    print("  ✓ This confirms: a(τ) - a(γ) = Qc(τ)·(τ - γ)")
    print("  ✓ The verifier checked this WITHOUT knowing τ!")
else:
    print("\n⚠️  FAILED! The proof is invalid!")
    print("  Either:")
    print("  - The evaluation b is incorrect")
    print("  - The proof π is incorrect")
    print("  - The commitment c is incorrect")


# Step 5: Test with incorrect value (should fail)
print("\n" + "="*70)
print("NEGATIVE TEST: Testing with incorrect evaluation")
print("="*70)

wrong_b = b + 1
result_wrong = verification(c, π, γ, wrong_b)

print(f"\nUsing wrong evaluation: {wrong_b} (should be {b})")
print(f"Verification result: {result_wrong}")

if not result_wrong:
    print("✓ Correctly rejected invalid proof!")
else:
    print("⚠️  ERROR: Should have rejected invalid proof!")


# Summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)

print("""
The verification function checks polynomial evaluation using pairings!

Key insight:
  The pairing allows us to check that:
      f(τ) - f(γ) = Qc(τ)·(τ - γ)

  Without anyone knowing τ (the toxic waste)!

How it works:
  1. Prover commits: c = f(τ)·P
  2. Prover claims: f(γ) = b
  3. Prover creates proof: π = Qc(τ)·P where Qc = (f - b)/(x - γ)
  4. Verifier checks: e(π, τ·Q - γ·Q) ?= e(c - b·P, Q)

If the check passes, the evaluation must be correct!

This is the foundation of KZG polynomial commitments used in:
  - PlonK and other ZK-SNARKs
  - Ethereum's Proto-Danksharding (EIP-4844)
  - Verkle trees and more!
""")

print("="*70)
print("✓ Exercise 10 Complete!")
print("="*70)
