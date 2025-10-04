#!/usr/bin/env python3
"""
Exercise 5 Solution: Schwartz-Zippel Probabilistic Equality Checks

Instead of checking polynomial equality by comparing all coefficients or doing
expensive polynomial multiplication, we use the Schwartz-Zippel lemma to check
equality at random points with negligible probability of error.

For polynomials f(x) and g(x) of degree ≤ d over field F_p:
- If f(x) ≠ g(x), then Pr[f(γ) = g(γ)] ≤ d/p ≈ 9/(2^254) ≈ 10^-75
- If f(x) = g(x), then f(γ) = g(γ) always

This makes verification O(d) instead of O(d^2) - much more succinct!
"""

import sys
import os
import io

# Add parent directory to path to access lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Suppress lib output
old_stdout = sys.stdout
sys.stdout = io.StringIO()
from lib.polynomials import *
sys.stdout = old_stdout

print("=" * 70)
print("EXERCISE 5: Schwartz-Zippel Probabilistic Equality Checks")
print("=" * 70)

# Create x variable
x = PolynomialVar(p)

# Reconstruct all polynomials from previous exercises
t = qM*a*b + qL*a + qR*b - c  # Gate constraint polynomial
f1 = a(x+1) - b(x)            # Wiring constraint 1
f2 = b(x+1) - c(x)            # Wiring constraint 2

# Compute vanishing polynomials and quotients (from Exercise 4)
Z = Polynomial([1], p)
for i in I:
    Z = Z * (x - i)
Q, _ = t.quo_rem(Z)

I_prime = [i for i in I if i not in {3, 4}]
Z1 = Polynomial([1], p)
for i in I_prime:
    Z1 = Z1 * (x - i)
Q1, _ = f1.quo_rem(Z1)
Q2, _ = f2.quo_rem(Z1)

print("\nPolynomial Setup Complete:")
print(f"  t degree: {t.degree()}, Q degree: {Q.degree()}, Z degree: {Z.degree()}")
print(f"  f1 degree: {f1.degree()}, Q1 degree: {Q1.degree()}")
print(f"  f2 degree: {f2.degree()}, Q2 degree: {Q2.degree()}")
print(f"  Z1 degree: {Z1.degree()}")

print("\n" + "=" * 70)
print("SCHWARTZ-ZIPPEL CHECKS")
print("=" * 70)

# Random challenge values
γ1 = 42
γ2 = 74102
γ3 = 987654321987654321

print(f"\nRandom challenge values:")
print(f"  γ1 = {γ1}")
print(f"  γ2 = {γ2}")
print(f"  γ3 = {γ3}")

print("\n" + "-" * 70)
print("CHECK 1: Gate Constraints")
print("-" * 70)
print(f"Checking: t(γ1) = Q(γ1) · Z(γ1)")
print(f"where γ1 = {γ1}")

# Evaluate at γ1
t_γ1 = t(γ1)
Q_γ1 = Q(γ1)
Z_γ1 = Z(γ1)
product_γ1 = (Q_γ1 * Z_γ1) % p

print(f"\n  t(γ1) = {t_γ1}")
print(f"  Q(γ1) = {Q_γ1}")
print(f"  Z(γ1) = {Z_γ1}")
print(f"  Q(γ1) · Z(γ1) = {product_γ1}")

check1_passes = (t_γ1 == product_γ1)
print(f"\n  ✓ Check passes: {check1_passes}")

# Verify against expected value
expected_γ1 = 21888242871839275222246405745257275088548364400416034343698204183303103172977
if t_γ1 == expected_γ1:
    print(f"  ✓ Matches expected value from exercise")
else:
    print(f"  ✗ Expected: {expected_γ1}")
    print(f"    Got:      {t_γ1}")

print("\n" + "-" * 70)
print("CHECK 2: Wiring Constraint 1")
print("-" * 70)
print(f"Checking: f1(γ2) = Q1(γ2) · Z1(γ2)")
print(f"where γ2 = {γ2}")

# Evaluate at γ2
f1_γ2 = f1(γ2)
Q1_γ2 = Q1(γ2)
Z1_γ2 = Z1(γ2)
product_γ2 = (Q1_γ2 * Z1_γ2) % p

print(f"\n  f1(γ2) = {f1_γ2}")
print(f"  Q1(γ2) = {Q1_γ2}")
print(f"  Z1(γ2) = {Z1_γ2}")
print(f"  Q1(γ2) · Z1(γ2) = {product_γ2}")

check2_passes = (f1_γ2 == product_γ2)
print(f"\n  ✓ Check passes: {check2_passes}")

# Verify against expected value
expected_γ2 = 271248759392650
if f1_γ2 == expected_γ2:
    print(f"  ✓ Matches expected value from exercise")
else:
    print(f"  ✗ Expected: {expected_γ2}")
    print(f"    Got:      {f1_γ2}")

print("\n" + "-" * 70)
print("CHECK 3: Wiring Constraint 2")
print("-" * 70)
print(f"Checking: f2(γ3) = Q2(γ3) · Z1(γ3)")
print(f"where γ3 = {γ3}")

# Evaluate at γ3
f2_γ3 = f2(γ3)
Q2_γ3 = Q2(γ3)
Z1_γ3 = Z1(γ3)
product_γ3 = (Q2_γ3 * Z1_γ3) % p

print(f"\n  f2(γ3) = {f2_γ3}")
print(f"  Q2(γ3) = {Q2_γ3}")
print(f"  Z1(γ3) = {Z1_γ3}")
print(f"  Q2(γ3) · Z1(γ3) = {product_γ3}")

check3_passes = (f2_γ3 == product_γ3)
print(f"\n  ✓ Check passes: {check3_passes}")

# Verify against expected value
expected_γ3 = 21888242871839275222245442326925691337956137906799110242993653357780575606177
if f2_γ3 == expected_γ3:
    print(f"  ✓ Matches expected value from exercise")
else:
    print(f"  ✗ Expected: {expected_γ3}")
    print(f"    Got:      {f2_γ3}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

all_checks_pass = check1_passes and check2_passes and check3_passes

print(f"\nAll Schwartz-Zippel checks passed: {all_checks_pass}")

if all_checks_pass:
    print("\n✓ Gate constraints verified at γ1 = 42")
    print("✓ Wiring constraint 1 verified at γ2 = 74102")
    print("✓ Wiring constraint 2 verified at γ3 = 987654321987654321")

    print(f"\nProbability of false positive: ≤ d/p ≈ 9/(2^254) ≈ 10^-75")
    print("(Less likely than guessing someone's private key!)")

print("\n" + "=" * 70)
print("RESULTS FOR CELL 23")
print("=" * 70)

print(f"""
Expected results:
  t(γ1)  = Q(γ1)·Z(γ1)   = {expected_γ1}
  f1(γ2) = Q1(γ2)·Z1(γ2) = {expected_γ2}
  f2(γ3) = Q2(γ3)·Z1(γ3) = {expected_γ3}

Computed results:
  t(γ1)  = {t_γ1}
  f1(γ2) = {f1_γ2}
  f2(γ3) = {f2_γ3}

Match: {t_γ1 == expected_γ1 and f1_γ2 == expected_γ2 and f2_γ3 == expected_γ3}
""")

print("=" * 70)
print("CODE FOR CELL 23:")
print("=" * 70)
print("""
γ1 = 42
γ2 = 74102
γ3 = 987654321987654321

# Check 1: Gate constraints
t_γ1 = t(γ1)
Q_γ1 = Q(γ1)
Z_γ1 = Z(γ1)
assert t_γ1 == (Q_γ1 * Z_γ1) % p
print(f"t(γ1) = Q(γ1)·Z(γ1) = {t_γ1}")

# Check 2: Wiring constraint 1
f1_γ2 = f1(γ2)
Q1_γ2 = Q1(γ2)
Z1_γ2 = Z1(γ2)
assert f1_γ2 == (Q1_γ2 * Z1_γ2) % p
print(f"f1(γ2) = Q1(γ2)·Z1(γ2) = {f1_γ2}")

# Check 3: Wiring constraint 2
f2_γ3 = f2(γ3)
Q2_γ3 = Q2(γ3)
Z1_γ3 = Z1(γ3)
assert f2_γ3 == (Q2_γ3 * Z1_γ3) % p
print(f"f2(γ3) = Q2(γ3)·Z1(γ3) = {f2_γ3}")

print("✓ All Schwartz-Zippel checks passed!")
""")

print("\n✓ Exercise 5 Complete!")
