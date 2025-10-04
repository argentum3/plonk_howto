#!/usr/bin/env python3
"""
Exercise 4 Solution: Vanishing Polynomials and Quotient Polynomials

Compute vanishing polynomials Z(x) and Z'(x), and quotient polynomials Q(x), Q1(x), Q2(x)
for the constraint polynomials using polynomial division.
"""

import sys
import os
# Add parent directory to path to access lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib.polynomials import Polynomial, PolynomialVar, p, interpolate, I, LI, RI, O, a, b, c, qL, qR, qM

print("=" * 70)
print("EXERCISE 4: Vanishing Polynomials and Polynomial Division")
print("=" * 70)

# Create x variable
x = PolynomialVar(p)

# From previous exercises - FULL gate constraint formula with selectors
t = qM*a*b + qL*a + qR*b - c  # Complete gate constraint polynomial
f1 = a(x+1) - b(x)  # Wiring constraint 1
f2 = b(x+1) - c(x)  # Wiring constraint 2

print("\nGate constraint formula: t = qM*a*b + qL*a + qR*b - c")
print(f"  Degree of t: {t.degree()}")

print("\n1. Computing Z(x) - vanishing polynomial for I = {1, 2, 3, 4}")
print("   Z(x) = (x-1)(x-2)(x-3)(x-4)")

# Method 1: Using the provided pattern
# R(1) means Polynomial([1])
Z = Polynomial([1], p)  # Start with constant polynomial 1
for i in I:
    Z = Z * (x - i)

print(f"   ✓ Z(x) computed")
print(f"   Degree of Z: {Z.degree()}")
print(f"   Z coefficients: {Z.coeffs}")

# Verify Z vanishes at all points in I
print("\n   Verification - Z(i) should be 0 for all i ∈ I:")
for i in I:
    val = Z(i)
    status = "✓" if val == 0 else "✗"
    print(f"   Z({i}) = {val} {status}")

print("\n2. Computing Q(x) - quotient of t(x) / Z(x)")
print("   NOTE: t(i) = 0 for i ∈ {1,2,3} but NOT for i=4")
print("   So Z won't perfectly divide t, but we compute the quotient anyway")

# Use quo_rem for polynomial division
Q, remainder = t.quo_rem(Z)

print(f"   ✓ Q(x) computed using polynomial division")
print(f"   Degree of Q: {Q.degree()}")
print(f"   Remainder: {remainder.coeffs}")

# Check if the division is exact
is_exact = all(c == 0 for c in remainder.coeffs)
print(f"   Is division exact? {is_exact}")

if not is_exact:
    print(f"   Note: Non-zero remainder expected since t(4) ≠ 0")

# Verify t(x) = Q(x) * Z(x) + remainder
verification = Q * Z + remainder
matches = all((t.coeffs[i] if i < len(t.coeffs) else 0) == (verification.coeffs[i] if i < len(verification.coeffs) else 0)
              for i in range(max(len(t.coeffs), len(verification.coeffs))))
print(f"\n   Verification - t(x) = Q(x)·Z(x) + remainder: {matches}")

print(f"\n   Q(x) coefficients (should match expected from cell 17):")
for i, coeff in enumerate(Q.coeffs):
    print(f"   x^{i}: {coeff}")

print("\n3. Computing Z1(x) - vanishing polynomial for I' = I\\{3,4} = {1, 2}")
print("   Z1(x) = (x-1)(x-2)")

# I' = I \ {3, 4} = {1, 2}
I_prime = [i for i in I if i not in {3, 4}]

Z1 = Polynomial([1], p)  # Start with constant polynomial 1
for i in I_prime:
    Z1 = Z1 * (x - i)

print(f"   ✓ Z1(x) computed")
print(f"   Degree of Z1: {Z1.degree()}")
print(f"   Z1 coefficients: {Z1.coeffs}")

# Verify Z1 vanishes at points in I'
print("\n   Verification - Z1(i) should be 0 for i ∈ {1, 2}:")
for i in I_prime:
    val = Z1(i)
    status = "✓" if val == 0 else "✗"
    print(f"   Z1({i}) = {val} {status}")

print("\n4. Computing Q1(x) - quotient of f1(x) / Z1(x)")
print("   f1(i) = 0 for i ∈ {1, 2}, so Z1 should divide f1")

Q1, remainder1 = f1.quo_rem(Z1)

print(f"   ✓ Q1(x) computed")
print(f"   Degree of Q1: {Q1.degree()}")
print(f"   Remainder degree: {remainder1.degree()}")
print(f"   Remainder coeffs: {remainder1.coeffs} (should be small/zero)")

# Verify f1(x) = Q1(x) * Z1(x)
verification1 = Q1 * Z1
print(f"   Verification - f1 == Q1*Z1: {all(f1.coeffs[i] == verification1.coeffs[i] for i in range(len(f1.coeffs)))}")

print("\n5. Computing Q2(x) - quotient of f2(x) / Z1(x)")
print("   f2(i) = 0 for i ∈ {1, 2}, so Z1 should divide f2")

Q2, remainder2 = f2.quo_rem(Z1)

print(f"   ✓ Q2(x) computed")
print(f"   Degree of Q2: {Q2.degree()}")
print(f"   Remainder degree: {remainder2.degree()}")
print(f"   Remainder coeffs: {remainder2.coeffs} (should be small/zero)")

# Verify f2(x) = Q2(x) * Z1(x)
verification2 = Q2 * Z1
print(f"   Verification - f2 == Q2*Z1: {all(f2.coeffs[i] == verification2.coeffs[i] for i in range(len(f2.coeffs)))}")

print("\n" + "=" * 70)
print("SUMMARY - Exercise 4 Results")
print("=" * 70)

print(f"\nZ(x) = ∏(x-i) for i ∈ {{1,2,3,4}}")
print(f"  Degree: {Z.degree()}")
print(f"  Z(x) = {' + '.join([f'{c}*x^{i}' if i > 0 else str(c) for i, c in enumerate(Z.coeffs)])}")

print(f"\nQ(x) from t(x) = Q(x)·Z(x)")
print(f"  Degree: {Q.degree()}")
print(f"  First 3 coeffs: {Q.coeffs[:3]}")

print(f"\nZ1(x) = (x-1)(x-2) for I'={{1,2}}")
print(f"  Degree: {Z1.degree()}")
print(f"  Z1(x) = {' + '.join([f'{c}*x^{i}' if i > 0 else str(c) for i, c in enumerate(Z1.coeffs)])}")

print(f"\nQ1(x) from f1(x) = Q1(x)·Z1(x)")
print(f"  Degree: {Q1.degree()}")
print(f"  Q1 coeffs: {Q1.coeffs}")

print(f"\nQ2(x) from f2(x) = Q2(x)·Z1(x)")
print(f"  Degree: {Q2.degree()}")
print(f"  Q2 coeffs: {Q2.coeffs}")

print("\n✓ Exercise 4 Complete!")

# Export results for use in notebook
print("\n" + "=" * 70)
print("CODE FOR CELL 16:")
print("=" * 70)
print("""
# Solution for Exercise 4

# Compute Z(x) = vanishing polynomial for I = {1,2,3,4}
Z = Polynomial([1], p)  # Start with constant polynomial 1
for i in I:
    Z = Z * (x - i)

# Compute Q(x) from t(x) = Q(x)·Z(x)
Q, _ = t.quo_rem(Z)

# Compute Z1(x) = vanishing polynomial for I' = I\\{3,4} = {1,2}
I_prime = [i for i in I if i not in {3, 4}]
Z1 = Polynomial([1], p)
for i in I_prime:
    Z1 = Z1 * (x - i)

# Compute Q1(x) from f1(x) = Q1(x)·Z1(x)
Q1, _ = f1.quo_rem(Z1)

# Compute Q2(x) from f2(x) = Q2(x)·Z1(x)
Q2, _ = f2.quo_rem(Z1)

# Verify
assert t == Q * Z  # Gate constraints
assert f1 == Q1 * Z1  # Wiring constraint 1
assert f2 == Q2 * Z1  # Wiring constraint 2
""")
