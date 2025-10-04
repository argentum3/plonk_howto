"""
Exercise 6: Bilinearity of Pairings

Check that the pairing function e is bilinear by verifying:
    e([s]·P, Q) = e(P, [s]·Q) = e(P, Q)^s

where s is a randomly sampled integer.
"""

import sys
import os

# Add sageless directory to path
sageless_dir = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, sageless_dir)

import random
import kzg
from py_ecc.bn128 import pairing, multiply

def e(P, Q):
    """
    Compute pairing using py_ecc library
    P: point in G1
    Q: point in G2
    Returns: pairing result in F_p^12
    """
    # py_ecc.bn128.pairing expects (G2, G1) order
    return pairing(Q, P)

# BN254 curve parameters
p = kzg.p  # Base field modulus
n = kzg.n  # Curve order
P = kzg.P  # G1 generator
Q = kzg.Q  # G2 generator

print("BN254 Curve Parameters:")
print(f"Base field modulus p = {p}")
print(f"Curve order n = {n}")
print(f"G1 generator P = {P}")
print(f"G2 generator Q = {Q}")
print()

# Sample random integer s
s = random.randint(1, n-1)
print(f"Randomly sampled s = {s}\n")

# Compute [s]·P (scalar multiplication in G1)
sP = multiply(P, s)
print(f"[s]·P = {sP}")

# Compute [s]·Q (scalar multiplication in G2)
sQ = multiply(Q, s)
print(f"[s]·Q = {sQ}")
print()

# Compute e([s]·P, Q)
left = e(sP, Q)
print("Computing e([s]·P, Q)...")

# Compute e(P, [s]·Q)
middle = e(P, sQ)
print("Computing e(P, [s]·Q)...")

# Compute e(P, Q)^s
ePQ = e(P, Q)
print("Computing e(P, Q)^s...")
# Note: The pairing result is in F_p^12 (FQ12 type in py_ecc)
# The FQP type supports __pow__ with just the exponent
right = pow(ePQ, s)

print("\n" + "="*70)
print("BILINEARITY VERIFICATION")
print("="*70)
print(f"\ne([s]·P, Q) == e(P, [s]·Q): {left == middle}")
print(f"e([s]·P, Q) == e(P, Q)^s:   {left == right}")

# Both should be True for bilinearity
assert left == middle, "First bilinearity property failed!"
assert left == right, "Second bilinearity property failed!"

print("\n✓ All bilinearity checks passed!")
print("\nThis confirms that the pairing function e satisfies:")
print("    e([s]·P, Q) = e(P, [s]·Q) = e(P, Q)^s")
