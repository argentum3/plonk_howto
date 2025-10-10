#!/usr/bin/env python3
"""
Exercise 11: Finding a Generator of a Multiplicative Subgroup

Find a generator ω of a domain of order 4 (a multiplicative subgroup).

Algorithm:
1. Compute r = (p-1)/4
2. Find smallest h ∈ F_p such that ω = h^r has multiplicative order 4
3. Verify: ω^4 = 1 and ω^i ≠ 1 for i ∈ {1, 2, 3}

Why this works:
- The multiplicative group F_p* has order p-1
- By Lagrange's theorem, h^(p-1) = 1 for all h ≠ 0
- If we want ω of order 4, we need ω^4 = 1
- Setting r = (p-1)/4, we get (h^r)^4 = h^(p-1) = 1
- Not all h work: we need the ORDER to be exactly 4, not a divisor of 4

The domain Ω = {ω, ω^2, ω^3, ω^4=1} are the 4th roots of unity.
"""

import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib.polynomials import p

print("="*70)
print("EXERCISE 11: FINDING A GENERATOR OF ORDER 4")
print("="*70)

# The field modulus (BN254 curve order)
print(f"\nField modulus p = {p}")
print(f"Size of multiplicative group F_p*: p-1 = {p-1}")

# We want a domain of order n = 4
n = pow(2, 2)  # n = 4
print(f"\nTarget domain order: n = {n}")

# Step 1: Compute r = (p-1)/4
r = (p - 1) // 4
print(f"\nStep 1: Compute r = (p-1)/4")
print(f"  r = {r}")

# Verify that 4 divides (p-1)
if (p - 1) % 4 != 0:
    print(f"\n⚠️  WARNING: 4 does not divide (p-1)!")
    print(f"  Cannot find 4th roots of unity in F_p")
else:
    print(f"  ✓ Verified: 4 divides (p-1)")

# Step 2: Find smallest h such that ω = h^r has order 4
print(f"\nStep 2: Find smallest h such that ω = h^r has multiplicative order 4")
print(f"  Requirements:")
print(f"    - ω^4 = 1 (ω is a 4th root of unity)")
print(f"    - ω^i ≠ 1 for i ∈ {{1, 2, 3}} (order is EXACTLY 4)")

def has_order_4(omega, modulus):
    """Check if omega has multiplicative order exactly 4"""
    # Check ω^4 = 1
    if pow(omega, 4, modulus) != 1:
        return False

    # Check ω^1 ≠ 1, ω^2 ≠ 1, ω^3 ≠ 1
    for i in [1, 2, 3]:
        if pow(omega, i, modulus) == 1:
            return False

    return True

h = 1
ω = None

print(f"\n  Searching for h...")
while h < p:
    # Compute ω = h^r mod p
    candidate = pow(h, r, p)

    if has_order_4(candidate, p):
        ω = candidate
        print(f"  ✓ Found h = {h}")
        print(f"    ω = h^r mod p = {ω}")
        break

    h += 1

    # Safety check (shouldn't need more than a few tries)
    if h > 100:
        print(f"  ⚠️  Searched h = 1 to 100, no generator found!")
        break

if ω is None:
    print(f"\n⚠️  ERROR: Could not find generator ω")
    sys.exit(1)

# Step 3: Verify ω has order 4
print(f"\n" + "="*70)
print("VERIFICATION")
print("="*70)

print(f"\nGenerator ω = {ω}")
print(f"Found using h = {h}")

print(f"\nChecking powers of ω:")
powers = []
for i in range(1, 5):
    power_i = pow(ω, i, p)
    powers.append(power_i)
    is_one = "= 1 ✓" if power_i == 1 else "≠ 1"
    print(f"  ω^{i} mod p = {power_i:70d}  {is_one}")

# Verify order is exactly 4
order_check = (
    pow(ω, 4, p) == 1 and
    pow(ω, 1, p) != 1 and
    pow(ω, 2, p) != 1 and
    pow(ω, 3, p) != 1
)

print(f"\n" + "="*70)
if order_check:
    print("✓ SUCCESS! ω has multiplicative order 4")
else:
    print("⚠️  FAILED! ω does not have order 4")
print("="*70)

# Step 4: Construct the domain Ω
print(f"\n" + "="*70)
print("MULTIPLICATIVE DOMAIN Ω")
print("="*70)

Ω = []
for i in range(1, n + 1):
    element = pow(ω, i, p)
    Ω.append(element)

print(f"\nΩ = {{ω, ω^2, ω^3, ω^4}} = {{ω, ω^2, ω^3, 1}}")
print(f"\nDomain elements:")
for i, element in enumerate(Ω, start=1):
    print(f"  ω^{i} = {element}")

# Verify last element is 1
if Ω[-1] == 1:
    print(f"\n✓ Verified: ω^{n} = 1")
else:
    print(f"\n⚠️  Warning: ω^{n} = {Ω[-1]} ≠ 1")

# Step 5: Verify vanishing polynomial
print(f"\n" + "="*70)
print("VANISHING POLYNOMIAL")
print("="*70)

print(f"\nFor a multiplicative domain of order {n}:")
print(f"  The vanishing polynomial is simply: Z(x) = x^{n} - 1")
print(f"\nThis is much simpler than multiplying (x - ω^i) for each element!")

print(f"\nVerifying Z(ω^i) = 0 for all i:")
for i in range(1, n + 1):
    omega_i = pow(ω, i, p)
    Z_omega_i = (pow(omega_i, n, p) - 1) % p
    is_zero = "= 0 ✓" if Z_omega_i == 0 else "≠ 0 ⚠️"
    print(f"  Z(ω^{i}) = (ω^{i})^{n} - 1 = {Z_omega_i:10d}  {is_zero}")

# Summary
print(f"\n" + "="*70)
print("SUMMARY")
print("="*70)

print(f"""
Found generator ω = {ω}

Domain Ω = {{{', '.join(str(x) for x in Ω)}}}

Key properties:
  ✓ ω^4 = 1 (ω is a 4th root of unity)
  ✓ ω^i ≠ 1 for i ∈ {{1, 2, 3}} (order is exactly 4)
  ✓ Ω has {n} elements
  ✓ Vanishing polynomial: Z(x) = x^4 - 1 (constant time!)

Why multiplicative domains are better:
  1. Vanishing polynomial Z(x) = x^n - 1 (constant time computation)
  2. No need to multiply (x - i) for each domain element
  3. More efficient FFT/NTT operations
  4. Better structure for PlonK and other ZK-SNARKs

This domain will replace the additive indices I = {{1, 2, 3, 4}}
in the next exercises!
""")

print("="*70)
print("✓ Exercise 11 Complete!")
print("="*70)
