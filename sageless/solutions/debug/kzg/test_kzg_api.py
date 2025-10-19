#!/usr/bin/env python3
"""
Test the new kzg.commit() and kzg.prove() API
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sageless'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sageless/solutions'))

# Import everything needed
import kzg
from lib.polynomials import Polynomial, p, a, b, c
from py_ecc.bn128 import multiply

print("="*70)
print("TESTING KZG API")
print("="*70)

# Set up trusted setup (same as Exercise 7)
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

print(f"\nTrusted setup:")
print(f"  τ = {τ}")
print(f"  l = {l}")
print(f"  |S1| = {len(S1)}")

# Initialize kzg
kzg.set_trusted_setup(S1, S2)
print("\n✓ kzg.set_trusted_setup(S1, S2) called")

# Test commit
print("\n" + "="*70)
print("TEST 1: kzg.commit()")
print("="*70)

c_a = kzg.commit(a)
print(f"\nc_a = kzg.commit(a)")
print(f"  x = {c_a[0]}")
print(f"  y = {c_a[1]}")
print("✓ Commitment created successfully")

# Test prove
print("\n" + "="*70)
print("TEST 2: kzg.prove()")
print("="*70)

γ = 151515
print(f"\nγ = {γ}")
print(f"a(γ) = {a(γ)}")

π = kzg.prove(a, γ)
print(f"\nπ = kzg.prove(a, γ)")
print(f"  x = {π[0]}")
print(f"  y = {π[1]}")
print("✓ Proof created successfully")

# Test verify
print("\n" + "="*70)
print("TEST 3: kzg.verify()")
print("="*70)

valid = kzg.verify(c_a, π, γ, a(γ))
print(f"\nkzg.verify(c_a, π, γ, a(γ)) = {valid}")

if valid:
    print("✓ Proof verified successfully")
else:
    print("✗ Proof verification failed")

# Test with wrong value
invalid = kzg.verify(c_a, π, γ, a(γ) + 1)
print(f"\nkzg.verify(c_a, π, γ, a(γ)+1) = {invalid}")

if not invalid:
    print("✓ Correctly rejected invalid proof")
else:
    print("✗ Should have rejected invalid proof")

print("\n" + "="*70)
if valid and not invalid:
    print("✓✓✓ ALL TESTS PASSED ✓✓✓")
else:
    print("✗✗✗ SOME TESTS FAILED ✗✗✗")
print("="*70)
