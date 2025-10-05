#!/usr/bin/env python3
"""
Exercise 8: KZG Polynomial Commitment Function

Implement the commitment function that takes:
- S1: Trusted setup vector [P, τ·P, τ²·P, ..., τˡ·P]
- p: A polynomial with coefficients [a₀, a₁, a₂, ...]

Returns:
- c: A commitment point on the curve (elliptic curve point)

The commitment is computed as:
  c = Σᵢ aᵢ · S1[i] = a₀·P + a₁·(τ·P) + a₂·(τ²·P) + ... = p(τ)·P

This allows committing to a polynomial without revealing it!
"""

import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import kzg
from py_ecc.bn128 import multiply, add, Z1

# Import polynomial library and S1 from exercise 7
from lib.polynomials import p, a, b, c as poly_c

print("="*70)
print("EXERCISE 8: KZG POLYNOMIAL COMMITMENT")
print("="*70)

# First, we need to compute S1 from Exercise 7
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

# Define the commitment function
def commitment(S1, p):
    """
    Compute KZG commitment to polynomial p using trusted setup S1

    Args:
        S1: List of curve points [P, τ·P, τ²·P, ..., τˡ·P]
        p: Polynomial object with coefficients

    Returns:
        c: Commitment point on the elliptic curve (represents p(τ)·P)
    """
    # Get polynomial coefficients
    coeffs = p.coeffs

    # Start with point at infinity (identity element)
    c = Z1  # Point at infinity in G1

    # Compute commitment: c = Σᵢ aᵢ · S1[i]
    for i, coeff in enumerate(coeffs):
        if i >= len(S1):
            raise ValueError(f"Polynomial degree {len(coeffs)-1} exceeds setup max degree {len(S1)-1}")

        # Multiply S1[i] by coefficient aᵢ
        term = multiply(S1[i], coeff % kzg.n)

        # Add to running sum
        c = add(c, term)

    return c

# Test the commitment function on polynomial a(x) from Fibonacci example
print("\nStep 2: Testing commitment on polynomial a(x)...")
print(f"Polynomial a(x) coefficients: {a.coeffs}")
print(f"Polynomial a(x) degree: {len(a.coeffs) - 1}")

# Compute commitment
c_commitment = commitment(S1, a)

print(f"\n✓ Computed commitment c")

# Format the output nicely
def format_point_projective(point, indent="  "):
    """Format point in projective coordinates with line breaks"""
    if len(point) == 2:
        x, y = point
        return f"(\n{indent}{x} :\n{indent}{y} :\n{indent}1\n)"
    return str(point)

print("\n" + "="*70)
print("COMMITMENT RESULT")
print("="*70)

print("\nCommitment c (affine coordinates):")
print(f"  c = {c_commitment}")

print("\nCommitment c (projective coordinates - notebook format):")
print(f"  c = {format_point_projective(c_commitment)}")

# Verify against expected value
expected_x = 19772988533509128204934208855583299243034568734268587639600165428945857082832
expected_y = 21198549198844316278609987090510616007059968516882705878791833422348082226388
expected_c = (expected_x, expected_y)

print("\n" + "="*70)
print("VERIFICATION")
print("="*70)

print(f"\nExpected commitment:")
print(f"  x = {expected_x}")
print(f"  y = {expected_y}")

print(f"\nComputed commitment:")
print(f"  x = {c_commitment[0]}")
print(f"  y = {c_commitment[1]}")

match = c_commitment == expected_c
print(f"\n✓ Match: {match}")

if match:
    print("\n🎉 Commitment computed correctly!")
else:
    print("\n⚠️  Commitment does not match expected value")
    print("   This might be due to different polynomial or setup parameters")

# Explain what this means
print("\n" + "="*70)
print("WHAT DOES THIS MEAN?")
print("="*70)
print("""
The commitment c is a single elliptic curve point that represents the
polynomial a(x) evaluated at the secret point τ, then multiplied by P:

    c = a(τ) · P

Key properties:
1. BINDING: Can't change a(x) after committing (c locks you in)
2. HIDING: c reveals nothing about a(x) (can't reverse to get polynomial)
3. SUCCINCT: c is just one curve point (~48 bytes), regardless of degree
4. HOMOMORPHIC: Can compute on commitments algebraically

This commitment can be sent to a verifier BEFORE receiving any challenge,
preventing adaptive attacks where the prover changes their polynomial
based on the challenge.
""")

print("="*70)
print("✓ Exercise 8 Complete!")
print("="*70)
print("\nThe commitment function is ready for use in the full KZG protocol!")
print("Next: Create proofs that evaluations are correct (Exercise 9+)")
