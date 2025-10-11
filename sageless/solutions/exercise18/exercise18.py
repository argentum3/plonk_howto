#!/usr/bin/env python3
"""
Exercise 18: Blinding Polynomials for Zero-Knowledge

This exercise implements polynomial blinding to achieve zero-knowledge properties.
By adding random multiples of the vanishing polynomial ZH, we hide the witness
values while preserving the polynomial constraints.

Blinding formula:
    f_blind(x) = f(x) + p(x) · ZH(x)

where p(x) is a random polynomial of appropriate degree.

Key property: f_blind(ω^i) = f(ω^i) for all ω^i in Ω (since ZH(ω^i) = 0)
"""

import sys
import os
import random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib.polynomials import p, Polynomial, PolynomialVar, interpolate

def random_polynomial(degree, modulus):
    """Generate a random polynomial of given degree"""
    coeffs = [random.randint(0, modulus - 1) for _ in range(degree + 1)]
    return Polynomial(coeffs, modulus)

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

# Interpolate z, N, D function (from Exercise 17)
def interpolate_z_N_D(a, b, c, beta, gamma, Ω):
    """Compute and interpolate the z, N, and D polynomials"""
    n = len(Ω)
    z_values = []
    N_values = []
    D_values = []
    z_current = 1

    for i in range(1, n + 1):
        z_values.append(z_current)

        num_a = numerator(i, 1, a, sigma, beta, gamma)
        num_b = numerator(i, 2, b, sigma, beta, gamma)
        num_c = numerator(i, 3, c, sigma, beta, gamma)

        den_a = denominator(i, 1, a, sigma, beta, gamma)
        den_b = denominator(i, 2, b, sigma, beta, gamma)
        den_c = denominator(i, 3, c, sigma, beta, gamma)

        N_i = (num_a * num_b * num_c) % p
        N_values.append(N_i)

        D_i = (den_a * den_b * den_c) % p
        D_values.append(D_i)

        D_i_inv = pow(D_i, p - 2, p)
        z_current = (z_current * N_i * D_i_inv) % p

    z = interpolate(Ω, z_values)
    N = interpolate(Ω, N_values)
    D = interpolate(Ω, D_values)

    return z, N, D

# Compute ZH (vanishing polynomial)
x = PolynomialVar(p)
ZH = x
for _ in range(n - 1):
    ZH = ZH * x
ZH = ZH - 1  # ZH = x^4 - 1

# ============================================================================
# EXERCISE 18: BLINDING POLYNOMIALS
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("EXERCISE 18: BLINDING POLYNOMIALS FOR ZERO-KNOWLEDGE")
    print("=" * 70)

    print("\nBlinding formula:")
    print("  f_blind(x) = f(x) + p(x) · ZH(x)")
    print("\nwhere:")
    print("  - p(x) is a random polynomial")
    print("  - ZH(x) = x^n - 1 (vanishing polynomial)")

    print("\nKey property:")
    print("  f_blind(ω^i) = f(ω^i) for all ω^i ∈ Ω")
    print("  (because ZH(ω^i) = 0)")

    # Number of openings (k=2 means at most 2 openings)
    k = 2

    print(f"\nAssuming at most k={k} openings")
    print(f"Random blinding polynomial degree: k-1 = {k-1}")

    # Challenges
    beta = 42
    gamma = 42

    print("\n" + "=" * 70)
    print("BLINDING WITNESS POLYNOMIALS")
    print("=" * 70)

    # Blind a (already shown in cell 81 as example)
    print("\n1. Blinding a(x):")
    p_poly_a = random_polynomial(degree=k-1, modulus=p)
    print(f"   p_a(x) = {p_poly_a}")
    a_blind = a + p_poly_a * ZH
    print(f"   deg(a) = {a.degree()}, deg(a_blind) = {a_blind.degree()}")

    # Blind b
    print("\n2. Blinding b(x):")
    p_poly_b = random_polynomial(degree=k-1, modulus=p)
    print(f"   p_b(x) = {p_poly_b}")
    b_blind = b + p_poly_b * ZH
    print(f"   deg(b) = {b.degree()}, deg(b_blind) = {b_blind.degree()}")

    # Blind c
    print("\n3. Blinding c(x):")
    p_poly_c = random_polynomial(degree=k-1, modulus=p)
    print(f"   p_c(x) = {p_poly_c}")
    c_blind = c + p_poly_c * ZH
    print(f"   deg(c) = {c.degree()}, deg(c_blind) = {c_blind.degree()}")

    # Verify blinded polynomials equal original at domain points
    print("\n" + "=" * 70)
    print("VERIFYING BLINDING PRESERVES VALUES AT DOMAIN POINTS")
    print("=" * 70)

    all_match = True
    for i in range(1, n + 1):
        ω_i = pow(ω, i, p)
        if a(ω_i) != a_blind(ω_i):
            print(f"✗ Mismatch at ω^{i}: a({ω_i}) ≠ a_blind({ω_i})")
            all_match = False
        if b(ω_i) != b_blind(ω_i):
            print(f"✗ Mismatch at ω^{i}: b({ω_i}) ≠ b_blind({ω_i})")
            all_match = False
        if c(ω_i) != c_blind(ω_i):
            print(f"✗ Mismatch at ω^{i}: c({ω_i}) ≠ c_blind({ω_i})")
            all_match = False

    if all_match:
        print("✓ All blinded polynomials match originals at domain points Ω")
    else:
        print("✗ Some blinded polynomials don't match!")

    print("\n" + "=" * 70)
    print("INTERPOLATING z, N, D POLYNOMIALS")
    print("=" * 70)

    print(f"\nUsing challenges: β={beta}, γ={gamma}")

    # Interpolate using BLINDED polynomials
    z_poly, N_poly, D_poly = interpolate_z_N_D(a_blind, b_blind, c_blind, beta, gamma, Ω)

    print(f"\nInterpolated polynomials:")
    print(f"  deg(z_poly) = {z_poly.degree()}")
    print(f"  deg(N_poly) = {N_poly.degree()}")
    print(f"  deg(D_poly) = {D_poly.degree()}")

    print("\n" + "=" * 70)
    print("BLINDING z POLYNOMIAL")
    print("=" * 70)

    print(f"\nBlinding z_poly (assuming at most k={k} openings):")
    p_poly_z = random_polynomial(degree=k-1, modulus=p)
    print(f"   p_z(x) = {p_poly_z}")
    z_poly_blind = z_poly + p_poly_z * ZH
    print(f"   deg(z_poly) = {z_poly.degree()}, deg(z_poly_blind) = {z_poly_blind.degree()}")

    # Verify z values still match at domain points
    print("\nVerifying z_poly_blind matches z_poly at domain points:")
    z_match = True
    for i in range(1, n + 1):
        ω_i = pow(ω, i, p)
        if z_poly(ω_i) != z_poly_blind(ω_i):
            print(f"✗ Mismatch at ω^{i}")
            z_match = False

    if z_match:
        print("✓ z_poly_blind matches z_poly at all domain points")

    print("\n" + "=" * 70)
    print("VALIDATION CHECK (from cell 85)")
    print("=" * 70)

    print("\nChecking: ZH divides z_poly_blind*N_poly - D_poly*z_poly_blind(x*ω)")

    # This should still pass because blinding doesn't affect values at domain points
    constraint = z_poly_blind * N_poly - D_poly * z_poly_blind(x * ω)
    divisible = ZH.divides(constraint)

    print(f"  Result: {divisible}")

    if divisible:
        print("  ✓ PASS: Recursive constraint still satisfied with blinded polynomials!")
    else:
        print("  ✗ FAIL: Something went wrong with blinding")

    assert divisible == True, "Validation check failed!"

    print("\n" + "=" * 70)
    print("✓ Exercise 18 Complete!")
    print("=" * 70)

    print("\nBlinded polynomials successfully created:")
    print("  - a_blind, b_blind, c_blind (witness polynomials)")
    print("  - z_poly_blind (accumulator polynomial)")
    print("  - N_poly, D_poly (numerator/denominator, not blinded)")
    print("\nThese blinded polynomials:")
    print("  ✓ Hide witness values from malicious verifiers")
    print("  ✓ Preserve correctness (same values at domain points)")
    print("  ✓ Maintain all polynomial constraints")
    print("  ✓ Enable zero-knowledge proofs!")

    # Print the solutions for the notebook
    print("\n" + "=" * 70)
    print("SOLUTIONS FOR NOTEBOOK (cell 83):")
    print("=" * 70)
    print(f"""
beta = gamma = 42

b_blind = b + random_polynomial(degree={k-1}, modulus=p) * ZH
c_blind = c + random_polynomial(degree={k-1}, modulus=p) * ZH
z_poly, N_poly, D_poly = interpolate_z_N_D(a_blind, b_blind, c_blind, beta, gamma, Ω)
z_poly_blind = z_poly + random_polynomial(degree={k-1}, modulus=p) * ZH
""")
