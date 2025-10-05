#!/usr/bin/env python3
"""
Exercise 7: KZG Trusted Setup

Compute the trusted setup parameters for KZG polynomial commitments:
- S1: Vector of powers of τ in G1: [P, τ·P, τ²·P, ..., τˡ·P]
- S2: τ·Q in G2

Where:
- τ (tau) = 424242 is the "toxic waste" (secret value)
- l = 10 is the maximum polynomial degree
- P is the generator of G1
- Q is the generator of G2
"""

import sys
import os

# Add sageless directory to path
sageless_dir = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, sageless_dir)

import kzg
from py_ecc.bn128 import multiply

# Trusted setup parameters
τ = 424242  # Toxic waste - must be destroyed after setup!
l = 10      # Maximum polynomial degree

print("="*70)
print("KZG TRUSTED SETUP - Exercise 7")
print("="*70)
print(f"\nParameters:")
print(f"  Toxic waste (τ) = {τ}")
print(f"  Max degree (l) = {l}")
print(f"  Curve: BN254/BN128")
print()

# Get generators
P = kzg.P  # G1 generator
Q = kzg.Q  # G2 generator

print(f"Generators:")
print(f"  P (G1 generator) = {P}")
print(f"  Q (G2 generator) = {Q}")
print()

# Compute S1: [P, τ·P, τ²·P, ..., τˡ·P]
# This is a list of l+1 points in G1
print("Computing S1 = [P, τ·P, τ²·P, ..., τˡ·P]...")
S1 = []

τ_power = 1  # Start with τ^0 = 1
for i in range(l + 1):
    # Compute [τ^i]·P = multiply(P, τ^i)
    point = multiply(P, τ_power)
    S1.append(point)

    # Next power: τ^(i+1) = τ^i * τ
    τ_power = (τ_power * τ) % kzg.n  # Reduce modulo curve order

print(f"✓ Computed S1 with {len(S1)} points")

# Compute S2: τ·Q
print("\nComputing S2 = τ·Q...")
S2 = multiply(Q, τ)
print(f"✓ Computed S2")

# Helper function to format long numbers with line breaks
def format_point_affine(point, indent="    "):
    """Format affine point (x, y) with line breaks for readability"""
    if len(point) == 2:
        x, y = point
        return f"(\n{indent}  {x},\n{indent}  {y}\n{indent})"
    return str(point)

def format_point_projective(point, indent="    "):
    """Format projective point (X : Y : Z) with line breaks for readability"""
    if len(point) == 2:
        x, y = point
        return f"(\n{indent}  {x} :\n{indent}  {y} :\n{indent}  1\n{indent})"
    elif len(point) == 3:
        # G2 points are tuples of tuples
        if isinstance(point[0], tuple):
            return (f"(\n{indent}  ({point[0][0]},\n{indent}   {point[0][1]}),\n"
                   f"{indent}  ({point[1][0]},\n{indent}   {point[1][1]})\n{indent})")
    return str(point)

def to_projective_str(point):
    """Convert affine (x, y) to projective (X : Y : Z) notation (compact)"""
    if len(point) == 2:
        x, y = point
        return f"({x} : {y} : 1)"
    return str(point)

# Display results
print("\n" + "="*70)
print("TRUSTED SETUP RESULTS")
print("="*70)

print("\nS1 (powers of τ in G1):")
print("\nAffine format (what py_ecc returns):")
for i, point in enumerate(S1):
    print(f"  S1[{i}] = τ^{i}·P = {format_point_affine(point, '  ')}")

print("\nProjective format (notebook notation):")
for i, point in enumerate(S1):
    print(f"  S1[{i}] = τ^{i}·P = {format_point_projective(point, '  ')}")

print(f"\nS2 (τ in G2):")
print(f"  S2 = τ·Q = {format_point_affine(S2, '  ')}")
print(f"  (G2 points are nested tuples representing extension field elements)")

# Verify the expected values from the notebook
print("\n" + "="*70)
print("COORDINATE SYSTEMS EXPLANATION")
print("="*70)
print("""
py_ecc returns points in AFFINE coordinates: (x, y)
The notebook shows points in PROJECTIVE coordinates: (X : Y : Z)

These represent the SAME mathematical point!

Conversion:
  Affine → Projective: (x, y) → (x : y : 1)
  Projective → Affine: (X : Y : Z) → (X/Z, Y/Z)

Example:
  Affine: (1, 2)
  Projective: (1 : 2 : 1)  [same point!]

Our solution uses affine (simpler, standard) but both are correct.
""")

print("="*70)
print("VERIFICATION")
print("="*70)

expected_S1_0 = (1, 2)
expected_S1_1 = (3388106087484702502772161951837520865682365219266094058038991331506090320735,
                 10310862820936104897688292475187545406556140958479334534497508049176340462168)
expected_S1_2 = (5786299459695789788261684662131390109566181344091061986154006773045920884529,
                 18198083969462810098554436542449595852850793038741994323649111219383738839374)

# Convert from projective to affine if needed
def to_affine(point):
    """Convert projective coordinates (x:y:z) to affine (x, y)"""
    if len(point) == 2:
        return point
    elif len(point) == 3:
        x, y, z = point
        if z == 0:
            return None  # Point at infinity
        z_inv = pow(z, -1, kzg.p)
        return ((x * z_inv) % kzg.p, (y * z_inv) % kzg.p)
    return point

print(f"\nChecking S1[0] (should be P):")
s1_0_affine = to_affine(S1[0])
print(f"  Expected (affine):     {expected_S1_0}")
print(f"  Expected (projective): (1 : 2 : 1)  [notebook format]")
print(f"  Got (affine):          {s1_0_affine}")
print(f"  Got (projective):      {to_projective_str(s1_0_affine)}")
print(f"  ✓ Match: {s1_0_affine == expected_S1_0}")

print(f"\nChecking S1[1] (should be τ·P):")
s1_1_affine = to_affine(S1[1])
print(f"  Expected (affine): {expected_S1_1}")
print(f"  Got (affine):      {s1_1_affine}")
print(f"  ✓ Match: {s1_1_affine == expected_S1_1}")

print(f"\nChecking S1[2] (should be τ²·P):")
s1_2_affine = to_affine(S1[2])
print(f"  Expected (affine): {expected_S1_2}")
print(f"  Got (affine):      {s1_2_affine}")
print(f"  ✓ Match: {s1_2_affine == expected_S1_2}")

print(f"\nNote: Affine (x, y) and Projective (x : y : 1) represent the same point!")

print("\n" + "="*70)
print("SECURITY NOTE")
print("="*70)
print("""
⚠️  TOXIC WASTE WARNING ⚠️

In a real KZG setup, the value τ (toxic waste) must be DESTROYED after
computing S1 and S2. If anyone knows τ, they can create fake proofs!

In practice, a "trusted setup ceremony" is used where multiple parties
contribute randomness. As long as ONE participant destroys their secret,
the setup is secure.

Famous ceremonies:
- Zcash Powers of Tau (2017)
- Ethereum KZG Ceremony (2022-2023)

For this exercise, τ=424242 is just for demonstration.
""")

print("✓ Exercise 7 Complete!\n")

# Export S1 and S2 for use in other exercises
print("Exporting S1 and S2 for Exercise 8...")
print("(These values can be imported by running this script and accessing S1, S2 variables)")
print("\nTo use in Exercise 8:")
print("  from exercise7 import S1, S2")
