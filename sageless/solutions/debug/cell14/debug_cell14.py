#!/usr/bin/env python3
"""
Debug and fix for Cell 14: Polynomial Composition Issue

The problem: a(x+1) needs polynomial composition, not evaluation
When x is a PolynomialVar, x+1 is a Polynomial, and a(x+1) should return
the composed polynomial a(x+1), not try to evaluate a at polynomial x+1.
"""

import sys
import os

# Add parent directory to path to access lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import from lib
from lib.polynomials import Polynomial, PolynomialVar, p, interpolate, I, LI, RI, O, a, b, c

print("=" * 70)
print("DEBUGGING CELL 14: Polynomial Composition")
print("=" * 70)

# Create x variable
x = PolynomialVar(p)

print("\n1. Understanding the issue:")
print(f"   x is a PolynomialVar: {x}")
print(f"   x.poly = {x.poly.coeffs}")

x_plus_1 = x + 1
print(f"\n   x+1 is a Polynomial: {type(x_plus_1)}")
print(f"   (x+1).coeffs = {x_plus_1.coeffs}")

print("\n2. What we need:")
print("   a(x+1) should give us polynomial composition a ∘ (x+1)")
print("   This means substituting (x+1) for x in polynomial a(x)")
print("   If a(x) = a0 + a1*x + a2*x^2 + a3*x^3")
print("   Then a(x+1) = a0 + a1*(x+1) + a2*(x+1)^2 + a3*(x+1)^3")

print("\n3. The fix:")
print("   We need to modify Polynomial.__call__ to handle Polynomial arguments")
print("   OR use a separate composition method")

# Let's implement the fix by adding a compose method
def compose(poly, substitution):
    """
    Polynomial composition: compute poly(substitution)
    If poly = a0 + a1*x + a2*x^2 + ...
    And substitution is a polynomial p(x)
    Returns: a0 + a1*p(x) + a2*p(x)^2 + ...
    """
    result = Polynomial([0], poly.modulus)
    power_of_sub = Polynomial([1], poly.modulus)  # Start with p(x)^0 = 1

    for coeff in poly.coeffs:
        # Add coeff * substitution^i to result
        result = result + (power_of_sub * coeff)
        # Update power: multiply by substitution
        power_of_sub = power_of_sub * substitution

    return result

print("\n4. Testing the composition:")
print(f"   a(x) coeffs: {a.coeffs}")

# Compose a with (x+1)
a_composed = compose(a, x_plus_1)
print(f"\n   a(x+1) using composition:")
print(f"   Degree: {a_composed.degree()}")
print(f"   First 3 coeffs: {a_composed.coeffs[:3]}")

# Verify by evaluating at specific points
print("\n5. Verification:")
print("   For polynomial composition to be correct:")
print("   a(x+1) evaluated at i should equal a(i+1)")
print()
print("   i  | a(i+1) | a_composed(i) | Match?")
print("   " + "-" * 45)
for i in I:
    if i < 4:  # Can evaluate i+1
        expected = a(i + 1)
        actual = a_composed(i)
        match = "✓" if expected == actual else "✗"
        print(f"   {i}  | {expected:6d} | {actual:6d}        | {match}")

print("\n6. Now let's compute f1 = a(x+1) - b(x):")
b_poly = b  # b(x) as a polynomial
f1 = compose(a, x_plus_1) - b_poly
print(f"   f1 degree: {f1.degree()}")
print(f"   f1 coeffs: {f1.coeffs}")

print("\n7. Check constraint: f1(i) should be 0 for i ∈ I\\{3,4}")
print("   i  | f1(i) | Expected")
print("   " + "-" * 30)
for i in I:
    if i not in {3, 4}:
        val = f1(i)
        status = "✓ PASS" if val == 0 else "✗ FAIL"
        print(f"   {i}  | {val:5d} | 0        {status}")

print("\n" + "=" * 70)
print("SOLUTION: Add polynomial composition support to Polynomial class")
print("=" * 70)
