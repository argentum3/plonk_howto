#!/usr/bin/env python3
"""
Exercise 9: KZG Proof Generation

Implement the proof function that creates a proof π for polynomial evaluation.

Given:
- f(x): A polynomial
- γ: A challenge point
- f(γ): The claimed evaluation

The prover creates a quotient polynomial:
    Qc(x) = (f(x) - f(γ)) / (x - γ)

Then computes the proof:
    π = Qc(τ)·P = Σᵢ bᵢ·S1[i]

where bᵢ are the coefficients of Qc(x).

This proof allows the verifier to check that f(γ) is correct without
knowing the polynomial f(x) or the secret τ!
"""

import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import kzg
from py_ecc.bn128 import multiply, add, Z1

# Import polynomial library
from lib.polynomials import p, a, b, c as poly_c, PolynomialVar, Polynomial

# Create polynomial variable x
x = PolynomialVar(p)

print("="*70)
print("EXERCISE 9: KZG PROOF GENERATION")
print("="*70)

# Step 1: Compute trusted setup S1 from Exercise 7
print("\nStep 1: Computing trusted setup S1...")
τ = 424242
l = 10

P = kzg.P
S1 = []
τ_power = 1
for i in range(l + 1):
    point = multiply(P, τ_power)
    S1.append(point)
    τ_power = (τ_power * τ) % kzg.n

print(f"✓ Computed S1 with {len(S1)} points")

# Step 2: Define the proof function
def proof(S1, Qc):
    """
    Generate KZG proof for polynomial evaluation

    Args:
        S1: Trusted setup vector [P, τ·P, τ²·P, ..., τˡ·P]
        Qc: Quotient polynomial (f(x) - f(γ)) / (x - γ)

    Returns:
        π: Proof point on elliptic curve = Qc(τ)·P
    """
    from py_ecc.bn128 import multiply, add, Z1
    # Get polynomial coefficients
    coeffs = Qc.coeffs
    print("Qc coefficients:", coeffs)

    # Start with point at infinity (identity element)
    π = Z1

    # Compute proof: π = Σᵢ bᵢ · S1[i] = Qc(τ)·P
    for i, coeff in enumerate(coeffs):
        if i >= len(S1):
            raise ValueError(f"Polynomial degree {len(coeffs)-1} exceeds setup max degree {len(S1)-1}")

        # Multiply S1[i] by coefficient bᵢ
        term = multiply(S1[i], coeff % kzg.n)

        # Add to running sum
        π = add(π, term)

    return π

# Step 3: Test on polynomial a(x) with challenge γ = 151515
print("\nStep 2: Testing proof generation on polynomial a(x)...")

γ = 151515
print(f"Challenge: γ = {γ}")

# Evaluate polynomial at challenge point
b_eval = a(γ)
print(f"Evaluation: a(γ) = {b_eval}")

# Compute quotient polynomial Qc(x) = (a(x) - a(γ)) / (x - γ)
print("\nComputing quotient polynomial Qc(x) = (a(x) - a(γ)) / (x - γ)...")

# Create polynomial for the constant a(γ)
b_poly = Polynomial([b_eval], p)

# Compute numerator: a(x) - a(γ)
numerator = a - b_poly

# Compute denominator: (x - γ)
denominator = x - γ

# Perform polynomial division
Qc, remainder = numerator.quo_rem(denominator)

print(f"✓ Quotient polynomial Qc(x) computed")
print(f"  Degree of Qc: {len(Qc.coeffs) - 1}")
print(f"  Remainder: {remainder.coeffs} (should be [0])")

if remainder.coeffs != [0]:
    print("⚠️  Warning: Non-zero remainder! This means (a(x) - a(γ)) is not divisible by (x - γ)")
    print("   This should not happen if γ is a root of a(x) - a(γ)")

# Generate the proof
print("\nStep 3: Generating proof π...")
π = proof(S1, Qc)
print(f"✓ Proof generated")

# Format output nicely
def format_point_projective(point, indent="  "):
    """Format point in projective coordinates with line breaks"""
    if len(point) == 2:
        x, y = point
        return f"(\n{indent}{x} :\n{indent}{y} :\n{indent}1\n)"
    return str(point)

print("\n" + "="*70)
print("PROOF RESULT")
print("="*70)

print("\nProof π (affine coordinates):")
print(f"  π = {π}")

print("\nProof π (projective coordinates - notebook format):")
print(f"  π = {format_point_projective(π)}")

print(f"\nEvaluation:")
print(f"  a(γ) = {b_eval}")

# Verify against expected values
expected_π_x = 18427764633036746853571353448280965399000717707037995558464363091930831203059
expected_π_y = 15823869948268955546174436172082876809321127559750802916163692992123652869945
expected_π = (expected_π_x, expected_π_y)
expected_b = 1739069066686765

print("\n" + "="*70)
print("VERIFICATION")
print("="*70)

print(f"\nExpected proof π:")
print(f"  x = {expected_π_x}")
print(f"  y = {expected_π_y}")

print(f"\nComputed proof π:")
print(f"  x = {π[0]}")
print(f"  y = {π[1]}")

π_match = π == expected_π
print(f"\n✓ Proof match: {π_match}")

print(f"\nExpected evaluation: a(γ) = {expected_b}")
print(f"Computed evaluation: a(γ) = {b_eval}")

b_match = b_eval == expected_b
print(f"✓ Evaluation match: {b_match}")

if π_match and b_match:
    print("\n🎉 Proof and evaluation computed correctly!")
else:
    print("\n⚠️  Values do not match expected results")
    if not π_match:
        print("   Proof mismatch")
    if not b_match:
        print("   Evaluation mismatch")

# Explain what this means
print("\n" + "="*70)
print("WHAT DOES THIS PROOF DO?")
print("="*70)
print(f"""
The proof π allows the verifier to check that a(γ) = {b_eval} is correct
WITHOUT knowing the polynomial a(x) or the secret τ!

How it works:
1. Prover claims: a({γ}) = {b_eval}
2. If true, then (a(x) - {b_eval}) must be divisible by (x - {γ})
3. So we can write: a(x) - {b_eval} = Qc(x) · (x - {γ})
4. The proof is: π = Qc(τ)·P

The verifier will later check using pairings that:
    e(π, τ·Q - γ·Q) = e(a(τ)·P - {b_eval}·P, Q)

This is equivalent to checking:
    Qc(τ)·(τ - γ) = a(τ) - {b_eval}

If this holds, the evaluation must be correct!

Key insight: The verifier checks polynomial equality at the secret
point τ, but neither party knows τ (it was destroyed in setup).
The pairing allows this check without revealing τ.
""")

print("="*70)
print("✓ Exercise 9 Complete!")
print("="*70)
print("\nThe proof function is ready!")
print("Next: Implement verification using pairings (Exercise 10)")
