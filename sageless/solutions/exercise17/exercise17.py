#!/usr/bin/env python3
"""
Exercise 17: Interpolating z, N, and D Polynomials

This exercise implements the core of PlonK's permutation argument by computing
and interpolating three key polynomials:
- z: The recursive accumulator polynomial
- N: The numerator polynomial
- D: The denominator polynomial

The z polynomial satisfies the recursive relation:
    z(ω^(i+1)) = z(ω^i) · numerator(i) / denominator(i)

with boundary condition z(ω) = 1.

Key properties:
    - z(ω) = 1 (base case)
    - z(ω^(n+1)) = z(ω) = 1 (in multiplicative domain)
    - ZH divides L1*(z-1) (boundary constraint)
    - ZH divides z*N - D*z(x*ω) (recursive constraint)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib.polynomials import p, Polynomial, PolynomialVar, interpolate

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
# EXERCISE 17: INTERPOLATE Z, N, D POLYNOMIALS
# ============================================================================

def interpolate_z_N_D(a, b, c, beta, gamma, Ω):
    """
    Compute and interpolate the z, N, and D polynomials for permutation argument.

    The z polynomial satisfies:
        z(ω) = 1 (base case)
        z(ω^(i+1)) = z(ω^i) · [numerator(i, col) / denominator(i, col)]

    Args:
        a, b, c: Polynomials for the three columns
        beta, gamma: Random challenges
        Ω: Multiplicative domain [ω¹, ω², ω³, ω⁴]

    Returns:
        z: Interpolated z polynomial
        N: Interpolated numerator polynomial
        D: Interpolated denominator polynomial

    The numerator and denominator are computed by multiplying across all columns:
        N(ω^i) = numerator(i, 1, a) · numerator(i, 2, b) · numerator(i, 3, c)
        D(ω^i) = denominator(i, 1, a) · denominator(i, 2, b) · denominator(i, 3, c)
    """
    n = len(Ω)

    # Values for z at each point in Ω
    z_values = []

    # Values for N and D at each point in Ω
    N_values = []
    D_values = []

    # Initialize z(ω) = 1 (base case)
    z_current = 1

    # Compute z, N, D values at each ω^i for i = 1, 2, ..., n
    for i in range(1, n + 1):
        # Store current z value
        z_values.append(z_current)

        # Compute numerator and denominator for all three columns at index i
        num_a = numerator(i, 1, a, sigma, beta, gamma)
        num_b = numerator(i, 2, b, sigma, beta, gamma)
        num_c = numerator(i, 3, c, sigma, beta, gamma)

        den_a = denominator(i, 1, a, sigma, beta, gamma)
        den_b = denominator(i, 2, b, sigma, beta, gamma)
        den_c = denominator(i, 3, c, sigma, beta, gamma)

        # N(ω^i) = product of all numerators at this index
        N_i = (num_a * num_b * num_c) % p
        N_values.append(N_i)

        # D(ω^i) = product of all denominators at this index
        D_i = (den_a * den_b * den_c) % p
        D_values.append(D_i)

        # Update z for next iteration using recursive formula:
        # z(ω^(i+1)) = z(ω^i) · N(ω^i) / D(ω^i)
        # We need modular inverse of D_i
        D_i_inv = pow(D_i, p - 2, p)  # Fermat's little theorem: a^(-1) ≡ a^(p-2) (mod p)
        z_current = (z_current * N_i * D_i_inv) % p

    # Interpolate the three polynomials over Ω
    z = interpolate(Ω, z_values)
    N = interpolate(Ω, N_values)
    D = interpolate(Ω, D_values)

    return z, N, D


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("EXERCISE 17: INTERPOLATING Z, N, D POLYNOMIALS")
    print("=" * 70)

    print("\nRecursive formula for z:")
    print("  z(ω) = 1 (base case)")
    print("  z(ω^(i+1)) = z(ω^i) · numerator(i) / denominator(i)")

    print("\nNumerator and denominator polynomials:")
    print("  N(ω^i) = numerator(i,1,a) · numerator(i,2,b) · numerator(i,3,c)")
    print("  D(ω^i) = denominator(i,1,a) · denominator(i,2,b) · denominator(i,3,c)")

    beta = 42
    gamma = 42

    print("\n" + "=" * 70)
    print("COMPUTING Z, N, D POLYNOMIALS")
    print("=" * 70)

    z, N, D = interpolate_z_N_D(a, b, c, beta, gamma, Ω)

    print(f"\nPolynomial degrees:")
    print(f"  deg(z) = {z.degree()}")
    print(f"  deg(N) = {N.degree()}")
    print(f"  deg(D) = {D.degree()}")

    print(f"\nz polynomial coefficients: {z.coeffs}")
    print(f"N polynomial coefficients: {N.coeffs}")
    print(f"D polynomial coefficients: {D.coeffs}")

    # Verify z values at domain points
    print("\n" + "=" * 70)
    print("VERIFYING Z VALUES AT DOMAIN POINTS")
    print("=" * 70)

    print("\nz evaluated at Ω:")
    for i in range(1, n + 1):
        ω_i = pow(ω, i, p)
        z_at_ω_i = z(ω_i)
        print(f"  z(ω^{i}) = {z_at_ω_i}")

    # Check base case
    z_at_ω = z(pow(ω, 1, p))
    print(f"\n✓ Base case: z(ω) = {z_at_ω} (expected 1)")
    assert z_at_ω == 1, "Base case failed: z(ω) should equal 1"

    # Check that z(ω^(n+1)) = z(ω) in multiplicative domain
    ω_n_plus_1 = pow(ω, n + 1, p)
    z_at_ω_n_plus_1 = z(ω_n_plus_1)
    print(f"✓ Cyclic property: z(ω^{n+1}) = z(ω^{n}·ω) = z(ω) = {z_at_ω_n_plus_1}")
    assert z_at_ω_n_plus_1 == z_at_ω, "Cyclic property failed"

    # Validation checks from cells 73-78
    print("\n" + "=" * 70)
    print("VALIDATION CHECKS (from cells 73-78)")
    print("=" * 70)

    # Cell 73: Check that ZH divides L1*(z-1)
    print("\nCheck 1: ZH divides L1*(z-1)")
    print("  This verifies the boundary condition z(ω) = 1")

    x = PolynomialVar(p)

    # Compute L1 - Lagrange basis polynomial for first point
    # L1 = ∏_{m=2}^{n} (x - ω^m) / (ω - ω^m)
    def prod(generator):
        result = Polynomial([1], p)
        for item in generator:
            result = result * item
        return result

    # Build L1 by multiplying factors
    L1_factors = []
    for m in range(2, n + 1):
        ω_m = pow(ω, m, p)
        numerator_poly = x - ω_m  # Polynomial x - ω^m
        denominator_scalar = (ω - ω_m) % p  # Scalar ω - ω^m
        # Divide polynomial by scalar: multiply by modular inverse
        denominator_inv = pow(denominator_scalar, p - 2, p)
        factor = numerator_poly * denominator_inv
        L1_factors.append(factor)

    L1 = prod(L1_factors)
    if isinstance(L1, int):
        L1 = Polynomial([L1], p)

    # ZH = x^n - 1 (vanishing polynomial for Ω)
    # Use x**n to get polynomial x^n
    ZH = (x * x * x * x) - 1  # x^4 - 1 for n=4

    # Check if ZH divides L1*(z-1)
    z_minus_1 = z - Polynomial([1], p)
    L1_times_z_minus_1 = L1 * z_minus_1
    divisible_1 = ZH.divides(L1_times_z_minus_1)
    print(f"  ZH divides L1*(z-1): {divisible_1}")
    assert divisible_1, "Check 1 failed: ZH should divide L1*(z-1)"
    print("  ✓ PASS")

    # Cell 75: Check that ZH divides z*N - D*z(x*ω)
    print("\nCheck 2: ZH divides z*N - D*z(x*ω)")
    print("  This verifies the recursive constraint")

    # Compute z(x*ω)
    z_at_xω = z(x * ω)

    # Compute z*N - D*z(x*ω)
    constraint = z * N - D * z_at_xω
    divisible_2 = ZH.divides(constraint)
    print(f"  ZH divides z*N - D*z(x*ω): {divisible_2}")
    assert divisible_2, "Check 2 failed: ZH should divide z*N - D*z(x*ω)"
    print("  ✓ PASS")

    # Cell 77: Print the constraint polynomial
    print("\nConstraint polynomial z*N - D*z(x*ω):")
    print(f"  Degree: {constraint.degree()}")
    print(f"  First 3 coefficients: {constraint.coeffs[:3]}")
    print(f"  Last 3 coefficients: {constraint.coeffs[-3:]}")

    print("\n" + "=" * 70)
    print("✓ Exercise 17 Complete!")
    print("=" * 70)

    print("\nThe z polynomial successfully encodes the permutation argument:")
    print("  - Satisfies boundary condition z(ω) = 1")
    print("  - Satisfies recursive constraint at all points in Ω")
    print("  - Can be used to prove copy constraints without revealing wire values")
