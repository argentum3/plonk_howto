#!/usr/bin/env python3
"""
Exercise 16: Accumulator Functions for Grand Product Argument

This exercise implements accumulator functions that compute partial products
of numerators and denominators. These accumulators build up the grand product
step by step, which is essential for the PlonK permutation argument.

Formulas:
    acc_numerator(i, column, f, σ, β, γ) = ∏_{j=1}^{i-1} numerator(j, column, f, σ, β, γ)
    acc_denominator(i, column, f, σ, β, γ) = ∏_{j=1}^{i-1} denominator(j, column, f, σ, β, γ)

The product goes from j=1 to i-1, so:
    - acc_*(1, ...) = 1 (empty product)
    - acc_*(2, ...) = numerator(1, ...)
    - acc_*(3, ...) = numerator(1, ...) * numerator(2, ...)
    - acc_*(n+1, ...) = numerator(1, ...) * ... * numerator(n, ...)
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

# Numerator and denominator functions (from Exercise 15)
def numerator(i, column, f, sigma, beta, gamma):
    """Compute numerator: pos(column, i) + β·f(ω^i) + γ"""
    position = pos(column, i)
    ω_to_i = pow(ω, i, p)
    f_of_ω_i = f(ω_to_i)
    value = (position + beta * f_of_ω_i + gamma) % p
    return value

def denominator(i, column, f, sigma, beta, gamma):
    """Compute denominator: σ(pos(column, i)) + β·f(ω^i) + γ"""
    position = pos(column, i)
    sigma_position = sigma[position]
    ω_to_i = pow(ω, i, p)
    f_of_ω_i = f(ω_to_i)
    value = (sigma_position + beta * f_of_ω_i + gamma) % p
    return value

# ============================================================================
# EXERCISE 16: ACCUMULATOR FUNCTIONS
# ============================================================================

def acc_numerator(i, column, f, sigma, beta, gamma):
    """
    Compute accumulator for numerator: product from j=1 to i-1.

    Formula: ∏_{j=1}^{i-1} numerator(j, column, f, σ, β, γ)

    Args:
        i: Upper bound (exclusive) for the product
        column: Column number (1=a, 2=b, 3=c)
        f: Polynomial for this column
        sigma: Permutation dictionary
        beta: Random challenge β
        gamma: Random challenge γ

    Returns:
        Product of numerators from j=1 to i-1 (mod p)

    Note:
        - For i=1, returns 1 (empty product)
        - For i=n+1, returns product of all n numerators for this column
    """
    value = 1

    # Compute product from j=1 to i-1
    for j in range(1, i):
        value = (value * numerator(j, column, f, sigma, beta, gamma)) % p

    return value


def acc_denominator(i, column, f, sigma, beta, gamma):
    """
    Compute accumulator for denominator: product from j=1 to i-1.

    Formula: ∏_{j=1}^{i-1} denominator(j, column, f, σ, β, γ)

    Args:
        i: Upper bound (exclusive) for the product
        column: Column number (1=a, 2=b, 3=c)
        f: Polynomial for this column
        sigma: Permutation dictionary
        beta: Random challenge β
        gamma: Random challenge γ

    Returns:
        Product of denominators from j=1 to i-1 (mod p)

    Note:
        - For i=1, returns 1 (empty product)
        - For i=n+1, returns product of all n denominators for this column
    """
    value = 1

    # Compute product from j=1 to i-1
    for j in range(1, i):
        value = (value * denominator(j, column, f, sigma, beta, gamma)) % p

    return value


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("EXERCISE 16: ACCUMULATOR FUNCTIONS")
    print("=" * 70)

    print("\nAccumulator Functions:")
    print("  acc_numerator(i, ...) = ∏_{j=1}^{i-1} numerator(j, ...)")
    print("  acc_denominator(i, ...) = ∏_{j=1}^{i-1} denominator(j, ...)")

    print("\nKey property:")
    print("  The product goes from j=1 to i-1 (i is exclusive)")
    print("  So acc_*(1, ...) = 1 (empty product)")
    print("  And acc_*(n+1, ...) = product of all n terms")

    beta = 42
    gamma = 42

    print("\n" + "=" * 70)
    print("TESTING ACCUMULATOR FUNCTIONS")
    print("=" * 70)

    # Test empty product
    print("\nTest 1: Empty product (i=1)")
    acc_num_1 = acc_numerator(1, 1, a, sigma, beta, gamma)
    acc_den_1 = acc_denominator(1, 1, a, sigma, beta, gamma)
    print(f"  acc_numerator(1, 1, a, ...) = {acc_num_1}")
    print(f"  acc_denominator(1, 1, a, ...) = {acc_den_1}")
    assert acc_num_1 == 1, "Empty product should be 1"
    assert acc_den_1 == 1, "Empty product should be 1"
    print("  ✓ Both equal 1 (correct)")

    # Test single term
    print("\nTest 2: Single term (i=2, includes j=1)")
    num_1 = numerator(1, 1, a, sigma, beta, gamma)
    den_1 = denominator(1, 1, a, sigma, beta, gamma)
    acc_num_2 = acc_numerator(2, 1, a, sigma, beta, gamma)
    acc_den_2 = acc_denominator(2, 1, a, sigma, beta, gamma)
    print(f"  numerator(1, 1, a, ...) = {num_1}")
    print(f"  acc_numerator(2, 1, a, ...) = {acc_num_2}")
    assert acc_num_2 == num_1, "Should equal single numerator"
    print(f"  denominator(1, 1, a, ...) = {den_1}")
    print(f"  acc_denominator(2, 1, a, ...) = {acc_den_2}")
    assert acc_den_2 == den_1, "Should equal single denominator"
    print("  ✓ Accumulators match single terms")

    # Test multiple terms
    print("\nTest 3: Multiple terms (i=3, includes j=1,2)")
    num_2 = numerator(2, 1, a, sigma, beta, gamma)
    expected_acc_num_3 = (num_1 * num_2) % p
    acc_num_3 = acc_numerator(3, 1, a, sigma, beta, gamma)
    print(f"  numerator(1, ...) = {num_1}")
    print(f"  numerator(2, ...) = {num_2}")
    print(f"  Expected product: {expected_acc_num_3}")
    print(f"  acc_numerator(3, ...) = {acc_num_3}")
    assert acc_num_3 == expected_acc_num_3, "Should equal product of first two numerators"
    print("  ✓ Accumulator matches product")

    # Test full accumulator (all n=4 gates)
    print("\nTest 4: Full accumulator (i=n+1=5, includes j=1,2,3,4)")
    acc_num_full = acc_numerator(n+1, 1, a, sigma, beta, gamma)
    acc_den_full = acc_denominator(n+1, 1, a, sigma, beta, gamma)
    print(f"  acc_numerator(n+1, 1, a, ...) = {acc_num_full}")
    print(f"  acc_denominator(n+1, 1, a, ...) = {acc_den_full}")

    # Verify by computing manually
    manual_num = 1
    manual_den = 1
    for j in range(1, n+1):
        manual_num = (manual_num * numerator(j, 1, a, sigma, beta, gamma)) % p
        manual_den = (manual_den * denominator(j, 1, a, sigma, beta, gamma)) % p

    assert acc_num_full == manual_num, "Should match manual calculation"
    assert acc_den_full == manual_den, "Should match manual calculation"
    print("  ✓ Matches manual calculation")

    print("\n" + "=" * 70)
    print("GRAND PRODUCT CHECK (from cells 69-70)")
    print("=" * 70)

    print("\nComputing N_n and D_n:")
    print("  N_n = product of all numerators across all columns")
    print("  D_n = product of all denominators across all columns")

    N_n_a = acc_numerator(n+1, 1, a, sigma, beta, gamma)
    N_n_b = acc_numerator(n+1, 2, b, sigma, beta, gamma)
    N_n_c = acc_numerator(n+1, 3, c, sigma, beta, gamma)
    N_n = (N_n_a * N_n_b * N_n_c) % p

    D_n_a = acc_denominator(n+1, 1, a, sigma, beta, gamma)
    D_n_b = acc_denominator(n+1, 2, b, sigma, beta, gamma)
    D_n_c = acc_denominator(n+1, 3, c, sigma, beta, gamma)
    D_n = (D_n_a * D_n_b * D_n_c) % p

    print(f"\n  N_n (column a): {N_n_a}")
    print(f"  N_n (column b): {N_n_b}")
    print(f"  N_n (column c): {N_n_c}")
    print(f"  N_n (total): {N_n}")

    print(f"\n  D_n (column a): {D_n_a}")
    print(f"  D_n (column b): {D_n_b}")
    print(f"  D_n (column c): {D_n_c}")
    print(f"  D_n (total): {D_n}")

    print(f"\n  N_n // D_n = {N_n // D_n}")
    print(f"  N_n % D_n = {N_n % D_n}")

    # The key check: N_n / D_n should equal 1
    check_result = (N_n // D_n == 1)
    print(f"\n  Check: N_n // D_n == 1? {check_result}")

    if check_result:
        print("  ✓ PASS: Grand product equals 1!")
        print("\n  This confirms the permutation σ correctly encodes")
        print("  the copy constraints in the circuit.")
    else:
        print("  ✗ FAIL: Grand product does not equal 1")
        print(f"  N_n = {N_n}")
        print(f"  D_n = {D_n}")
        # Check if they're equal modulo p
        if N_n % p == D_n % p:
            print("  BUT: N_n ≡ D_n (mod p), so they ARE equal in the field!")
            print("  ✓ The permutation is valid!")

    print("\n" + "=" * 70)
    print("✓ Exercise 16 Complete!")
    print("=" * 70)

    print("\nThe accumulator functions compute partial products of")
    print("numerators and denominators, which will be used in the")
    print("recursive z function to efficiently verify the permutation.")
