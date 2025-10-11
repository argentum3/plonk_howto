#!/usr/bin/env python3
"""
Exercise 15: Numerator and Denominator Functions for Permutation Argument

This exercise implements the numerator and denominator functions used in PlonK's
grand product argument for verifying copy constraints.

Formulas:
    numerator(i, column, f, σ, β, γ) = pos(column, i) + β·f(ω^i) + γ
    denominator(i, column, f, σ, β, γ) = σ(pos(column, i)) + β·f(ω^i) + γ

where:
    - pos(column, i) = (column-1)*n + i  (position in the flattened circuit)
    - f is the polynomial for the column (a, b, or c)
    - ω is the generator of the multiplicative domain
    - σ is the permutation encoding copy constraints
    - β, γ are random challenges
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib.polynomials import p, Polynomial, interpolate

# Setup from previous exercises
n = 4

# Generator ω of multiplicative domain (from Exercise 11)
r = (p - 1) // 4
h = 5
ω = pow(h, r, p)
Ω = [pow(ω, i, p) for i in range(1, n+1)]

# Circuit values
LI = {1:0, 2:1, 3:1, 4:3}
RI = {1:1, 2:1, 3:2, 4:3}
O  = {1:1, 2:2, 3:3, 4:9}

# Interpolate polynomials over Ω (from Exercise 12)
a = interpolate(Ω, list(LI.values()))
b = interpolate(Ω, list(RI.values()))
c = interpolate(Ω, list(O.values()))

# Position function
def pos(column, index):
    """Map (column, index) to global position in [1..12]"""
    return (column - 1) * n + index

# Permutation σ (from Exercise 14)
sigma = {}
sigma[pos(1,1)] = pos(1,1)
sigma[pos(1,2)] = pos(2,1)
sigma[pos(2,1)] = pos(1,2)
sigma[pos(1,3)] = pos(2,2)
sigma[pos(2,2)] = pos(3,1)
sigma[pos(3,1)] = pos(1,3)
sigma[pos(3,2)] = pos(2,3)
sigma[pos(2,3)] = pos(3,2)
sigma[pos(3,3)] = pos(1,4)
sigma[pos(1,4)] = pos(2,4)
sigma[pos(2,4)] = pos(3,3)
sigma[pos(3,4)] = pos(3,4)

# ============================================================================
# EXERCISE 15: NUMERATOR AND DENOMINATOR FUNCTIONS
# ============================================================================

def numerator(i, column, f, sigma, beta, gamma):
    """
    Compute numerator for grand product argument.

    Formula: pos(column, i) + β·f(ω^i) + γ

    Args:
        i: Gate index (1 to n)
        column: Column number (1=a, 2=b, 3=c)
        f: Polynomial for this column
        sigma: Permutation dictionary
        beta: Random challenge β
        gamma: Random challenge γ

    Returns:
        Numerator value (mod p)
    """
    # Compute position in the flattened circuit
    position = pos(column, i)

    # Evaluate f at ω^i
    ω_to_i = pow(ω, i, p)
    f_of_ω_i = f(ω_to_i)

    # Formula: pos(column, i) + β·f(ω^i) + γ
    value = (position + beta * f_of_ω_i + gamma) % p

    return value


def denominator(i, column, f, sigma, beta, gamma):
    """
    Compute denominator for grand product argument.

    Formula: σ(pos(column, i)) + β·f(ω^i) + γ

    Args:
        i: Gate index (1 to n)
        column: Column number (1=a, 2=b, 3=c)
        f: Polynomial for this column
        sigma: Permutation dictionary
        beta: Random challenge β
        gamma: Random challenge γ

    Returns:
        Denominator value (mod p)
    """
    # Compute position in the flattened circuit
    position = pos(column, i)

    # Look up σ(position) - where this position maps to in the permutation
    sigma_position = sigma[position]

    # Evaluate f at ω^i
    ω_to_i = pow(ω, i, p)
    f_of_ω_i = f(ω_to_i)

    # Formula: σ(pos(column, i)) + β·f(ω^i) + γ
    value = (sigma_position + beta * f_of_ω_i + gamma) % p

    return value


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("EXERCISE 15: NUMERATOR AND DENOMINATOR FUNCTIONS")
    print("=" * 70)

    print("\nGrand Product Argument Setup:")
    print(f"  n = {n} gates")
    print(f"  ω = {ω}")
    print(f"  Domain Ω = {{ω¹, ω², ω³, ω⁴}}")

    print("\n" + "=" * 70)
    print("FORMULAS")
    print("=" * 70)

    print("\nNumerator:")
    print("  numerator(i, column, f, σ, β, γ) = pos(column, i) + β·f(ω^i) + γ")

    print("\nDenominator:")
    print("  denominator(i, column, f, σ, β, γ) = σ(pos(column, i)) + β·f(ω^i) + γ")

    print("\nKey insight:")
    print("  If the permutation is correct, the grand product should equal 1:")
    print("  GP = ∏ numerator(i, column, f, σ, β, γ) / denominator(i, column, f, σ, β, γ)")

    # Test with challenges β=42, γ=42
    beta = 42
    gamma = 42

    print("\n" + "=" * 70)
    print("TESTING WITH β=42, γ=42")
    print("=" * 70)

    # Test case 1: numerator(3, 1, a, σ, 42, 42)
    print("\nTest 1: numerator(3, 1, a, σ, 42, 42)")
    print(f"  i=3, column=1")
    print(f"  Position: pos(1, 3) = {pos(1, 3)}")
    print(f"  f(ω³): a(ω³) = {a(pow(ω, 3, p))}")
    result = numerator(3, 1, a, sigma, beta, gamma)
    print(f"  Result: {result}")
    print(f"  Expected: 87")
    assert result == 87, f"Expected 87, got {result}"
    print("  ✓ PASS")

    # Test case 2: denominator(3, 1, a, σ, 42, 42)
    print("\nTest 2: denominator(3, 1, a, σ, 42, 42)")
    print(f"  i=3, column=1")
    print(f"  Position: pos(1, 3) = {pos(1, 3)}")
    print(f"  σ(pos(1, 3)) = σ(3) = {sigma[pos(1, 3)]}")
    print(f"  f(ω³): a(ω³) = {a(pow(ω, 3, p))}")
    result = denominator(3, 1, a, sigma, beta, gamma)
    print(f"  Result: {result}")
    print(f"  Expected: 90")
    assert result == 90, f"Expected 90, got {result}"
    print("  ✓ PASS")

    # Test case 3: numerator(6, 2, b, σ, 42, 42)
    print("\nTest 3: numerator(6, 2, b, σ, 42, 42)")
    print(f"  i=6, column=2 (Note: i > n is OK, ω^6 = ω^2 since ω has order 4)")
    print(f"  Position: pos(2, 6) = {pos(2, 6)}")
    print(f"  f(ω⁶) = f(ω²): b(ω²) = {b(pow(ω, 6, p))}")
    result = numerator(6, 2, b, sigma, beta, gamma)
    print(f"  Result: {result}")
    print(f"  Expected: 94")
    assert result == 94, f"Expected 94, got {result}"
    print("  ✓ PASS")

    # Test case 4: denominator(6, 2, b, σ, 42, 42)
    print("\nTest 4: denominator(6, 2, b, σ, 42, 42)")
    print(f"  i=6, column=2")
    print(f"  Position: pos(2, 6) = {pos(2, 6)}")
    print(f"  σ(pos(2, 6)) = σ(10) = {sigma[pos(2, 6)]}")
    print(f"  f(ω⁶) = f(ω²): b(ω²) = {b(pow(ω, 6, p))}")
    result = denominator(6, 2, b, sigma, beta, gamma)
    print(f"  Result: {result}")
    print(f"  Expected: 91")
    assert result == 91, f"Expected 91, got {result}"
    print("  ✓ PASS")

    print("\n" + "=" * 70)
    print("VERIFYING CYCLE (3, 6, 9)")
    print("=" * 70)

    print("\nPositions in cycle (3, 6, 9) all have value 1:")
    print(f"  Position 3 = a[3] = {a(pow(ω, 3, p))}")
    print(f"  Position 6 = b[2] = {b(pow(ω, 2, p))}")
    print(f"  Position 9 = c[1] = {c(pow(ω, 1, p))}")

    print("\nComputing products for this cycle:")

    # Position 3 (column 1, i=3)
    num3 = numerator(3, 1, a, sigma, beta, gamma)
    den3 = denominator(3, 1, a, sigma, beta, gamma)
    print(f"  Position 3: num={num3}, den={den3}, ratio={num3}/{den3}")

    # Position 6 (column 2, i=2)
    num6 = numerator(2, 2, b, sigma, beta, gamma)
    den6 = denominator(2, 2, b, sigma, beta, gamma)
    print(f"  Position 6: num={num6}, den={den6}, ratio={num6}/{den6}")

    # Position 9 (column 3, i=1)
    num9 = numerator(1, 3, c, sigma, beta, gamma)
    den9 = denominator(1, 3, c, sigma, beta, gamma)
    print(f"  Position 9: num={num9}, den={den9}, ratio={num9}/{den9}")

    # Verify cycle product
    cycle_numerator_product = (num3 * num6 * num9) % p
    cycle_denominator_product = (den3 * den6 * den9) % p

    print(f"\n  Product of numerators: {cycle_numerator_product}")
    print(f"  Product of denominators: {cycle_denominator_product}")

    # For a valid permutation, these should be related through the cycle structure
    print("\n  Note: The numerator and denominator products differ because they")
    print("  evaluate at σ(position) vs position, but the overall grand product")
    print("  across all positions will equal 1 if the permutation is valid!")

    print("\n" + "=" * 70)
    print("✓ Exercise 15 Complete!")
    print("=" * 70)

    print("\nThe numerator and denominator functions are ready to be used in")
    print("Exercise 16 to compute the accumulator functions for the grand")
    print("product argument.")
