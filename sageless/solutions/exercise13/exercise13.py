#!/usr/bin/env python3
"""
Exercise 13: Verifying Exact Division - Zero Remainder

Verify that the gate constraint polynomial t(x) is exactly divisible by the
vanishing polynomial Z(x) over the multiplicative domain Ω.

Given:
  t(x) = qM·a·b + qL·a + qR·b - c  (gate constraint polynomial)
  Z(x) = x^4 - 1                   (vanishing polynomial for Ω)

We need to verify:
  t(x) = Q(x) · Z(x)  with remainder R(x) = 0

This confirms that the constraints are satisfied at all domain points,
since Z(ω^i) = 0 for all ω^i ∈ Ω.

Why this works:
  - If t(ω^i) = 0 for all ω^i ∈ Ω, then Z(x) divides t(x)
  - The division is exact (R(x) = 0)
  - This is more efficient than checking t(ω^i) = 0 for each point
"""

import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib.polynomials import p, interpolate, PolynomialVar, Polynomial

print("="*70)
print("EXERCISE 13: VERIFYING EXACT DIVISION (ZERO REMAINDER)")
print("="*70)

# Step 1: Compute generator ω and domain Ω from Exercise 11
print("\nStep 1: Computing generator ω and domain Ω...")

n = pow(2, 2)  # n = 4
r = (p - 1) // 4

# Find smallest h such that ω = h^r has order 4
def has_order_4(omega, modulus):
    if pow(omega, 4, modulus) != 1:
        return False
    for i in [1, 2, 3]:
        if pow(omega, i, modulus) == 1:
            return False
    return True

h = 1
ω = None
while h < p:
    candidate = pow(h, r, p)
    if has_order_4(candidate, p):
        ω = candidate
        break
    h += 1

Ω = [pow(ω, i, p) for i in range(1, n + 1)]
print(f"  Generator ω found using h = {h}")
print(f"  Domain Ω = {{ω, ω^2, ω^3, ω^4}}")

# Step 2: Interpolate polynomials over Ω (from Exercise 12)
print(f"\nStep 2: Interpolating polynomials over Ω...")

# Value vectors
LI = {1: 0, 2: 1, 3: 1, 4: 3}
RI = {1: 1, 2: 1, 3: 2, 4: 3}
O  = {1: 1, 2: 2, 3: 3, 4: 9}

# Selector vectors
SL = {1: 1, 2: 1, 3: 1, 4: 0}
SR = {1: 1, 2: 1, 3: 1, 4: 0}
SM = {1: 0, 2: 0, 3: 0, 4: 1}

# Interpolate witness polynomials
a = interpolate(Ω, list(LI.values()))
b = interpolate(Ω, list(RI.values()))
c = interpolate(Ω, list(O.values()))

# Interpolate selector polynomials
qL = interpolate(Ω, list(SL.values()))
qR = interpolate(Ω, list(SR.values()))
qM = interpolate(Ω, list(SM.values()))

print(f"  ✓ Interpolated witness polynomials: a(x), b(x), c(x)")
print(f"  ✓ Interpolated selector polynomials: qL(x), qR(x), qM(x)")

# Step 3: Construct gate constraint polynomial t(x)
print(f"\n" + "="*70)
print("STEP 3: GATE CONSTRAINT POLYNOMIAL")
print("="*70)

print(f"\nThe gate constraint polynomial encodes all gate constraints:")
print(f"  t(x) = qM(x)·a(x)·b(x) + qL(x)·a(x) + qR(x)·b(x) - c(x)")

print(f"\nThis combines:")
print(f"  - Multiplication gates: qM(x)·a(x)·b(x)")
print(f"  - Addition gates: qL(x)·a(x) + qR(x)·b(x) - c(x)")

# Compute t(x)
t = qM * a * b + qL * a + qR * b - c

print(f"\n✓ Computed t(x)")
print(f"  Degree: {t.degree()}")

# Step 4: Define vanishing polynomial Z(x)
print(f"\n" + "="*70)
print("STEP 4: VANISHING POLYNOMIAL")
print("="*70)

print(f"\nFor multiplicative domain Ω of order {n}:")
print(f"  Z(x) = x^{n} - 1")

# Create Z(x) = x^4 - 1
x = PolynomialVar(p)
Z = (x * x * x * x) - 1  # x^4 - 1

print(f"\n✓ Defined Z(x) = x^4 - 1")
print(f"  Coefficients: {Z.coeffs}")
print(f"  Degree: {Z.degree()}")

# Step 5: Verify Z vanishes on Ω
print(f"\nVerifying Z(ω^i) = 0 for all ω^i ∈ Ω:")
all_zero = True
for i in range(1, n + 1):
    omega_i = Ω[i-1]
    Z_val = Z(omega_i)
    is_zero = "✓" if Z_val == 0 else "✗"
    print(f"  Z(ω^{i}) = {Z_val:10d}  {is_zero}")
    if Z_val != 0:
        all_zero = False

if all_zero:
    print(f"\n✓ Z(x) vanishes on all domain points!")
else:
    print(f"\n⚠️  Z(x) doesn't vanish on all points!")

# Step 6: Verify t vanishes on Ω
print(f"\n" + "="*70)
print("STEP 5: VERIFY t(x) VANISHES ON Ω")
print("="*70)

print(f"\nChecking t(ω^i) = 0 for all ω^i ∈ Ω:")
print(f"(This should be true if constraints are satisfied)")

t_vanishes = True
for i in range(1, n + 1):
    omega_i = Ω[i-1]
    t_val = t(omega_i)
    is_zero = "✓" if t_val == 0 else "✗"

    # Show the gate constraint at this point
    a_val = a(omega_i)
    b_val = b(omega_i)
    c_val = c(omega_i)
    qL_val = qL(omega_i)
    qR_val = qR(omega_i)
    qM_val = qM(omega_i)

    constraint = qM_val * a_val * b_val + qL_val * a_val + qR_val * b_val - c_val

    print(f"  Gate {i}: t(ω^{i}) = {t_val:10d}  {is_zero}")
    print(f"    → {qM_val}·{a_val}·{b_val} + {qL_val}·{a_val} + {qR_val}·{b_val} - {c_val} = {constraint}")

    if t_val != 0:
        t_vanishes = False

if t_vanishes:
    print(f"\n✓ t(x) vanishes on all domain points!")
    print(f"  This means the gate constraints are satisfied")
else:
    print(f"\n⚠️  t(x) doesn't vanish on all points!")
    print(f"  Constraints are NOT satisfied!")

# Step 7: Perform polynomial division t(x) / Z(x)
print(f"\n" + "="*70)
print("STEP 6: POLYNOMIAL DIVISION t(x) ÷ Z(x)")
print("="*70)

print(f"\nPerforming division: t(x) ÷ Z(x)")
print(f"  We expect: t(x) = Q(x) · Z(x) + R(x)")
print(f"  If constraints are satisfied: R(x) = 0")

# Compute quotient and remainder
Quo, Rem = t.quo_rem(Z)

print(f"\n✓ Division complete")
print(f"  Quotient Q(x) degree: {Quo.degree()}")
print(f"  Remainder R(x): {Rem.coeffs}")

# Step 8: Verify remainder is zero
print(f"\n" + "="*70)
print("VERIFICATION: IS REMAINDER ZERO?")
print("="*70)

is_zero_remainder = (Rem == 0)

print(f"\nRemainder R(x) = {Rem}")
print(f"\nIs remainder zero? {is_zero_remainder}")

if is_zero_remainder:
    print(f"\n✓ SUCCESS! The division is EXACT")
    print(f"\n  This proves:")
    print(f"    t(x) = Q(x) · Z(x)")
    print(f"\n  Since Z(x) divides t(x) exactly, and Z(ω^i) = 0 for all ω^i ∈ Ω,")
    print(f"  we have confirmed that t(ω^i) = 0 for all domain points.")
    print(f"\n  ✓ All gate constraints are satisfied!")
else:
    print(f"\n⚠️  FAILED! The division has a non-zero remainder")
    print(f"  Remainder: {Rem}")
    print(f"  This means constraints are NOT satisfied!")

# Step 9: Verify reconstruction
print(f"\n" + "="*70)
print("VERIFICATION: RECONSTRUCT t(x) FROM Q(x) AND Z(x)")
print("="*70)

# Reconstruct t(x) = Q(x) * Z(x)
t_reconstructed = Quo * Z

print(f"\nReconstruction:")
print(f"  t(x) = Q(x) · Z(x)")

# Check if they match
reconstruction_match = (t_reconstructed == t)

print(f"\nDo they match? {reconstruction_match}")

if reconstruction_match:
    print(f"✓ Reconstruction successful!")
    print(f"  t(x) = Q(x) · Z(x) exactly")
else:
    print(f"⚠️  Reconstruction failed!")

# Summary
print(f"\n" + "="*70)
print("SUMMARY")
print("="*70)

print(f"""
Gate constraint polynomial:
  t(x) = qM·a·b + qL·a + qR·b - c
  Degree: {t.degree()}

Vanishing polynomial:
  Z(x) = x^4 - 1
  Degree: {Z.degree()}

Division result:
  Quotient Q(x) degree: {Quo.degree()}
  Remainder R(x): {Rem}

Verification:
  ✓ Z(x) vanishes on Ω: {all_zero}
  ✓ t(x) vanishes on Ω: {t_vanishes}
  ✓ Remainder is zero: {is_zero_remainder}
  ✓ Reconstruction works: {reconstruction_match}

Conclusion:
  The division is EXACT with zero remainder!

  This proves that t(x) = Q(x) · Z(x), which confirms that
  all gate constraints are satisfied at every point in the domain Ω.

  This is a key step in the PlonK protocol:
  - Instead of checking t(ω^i) = 0 for each i
  - We check that Z(x) divides t(x) (one polynomial division)
  - Much more efficient for large circuits!
""")

print("="*70)
print("✓ Exercise 13 Complete!")
print("="*70)
