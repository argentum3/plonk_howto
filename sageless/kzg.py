#!/usr/bin/env python3
"""
KZG polynomial commitments using BN254 curve - SageMath-free version
Uses py_ecc library for elliptic curve operations and pairings
Install with: pip install py_ecc
"""

from py_ecc.bn128 import G1, G2, pairing, multiply, add, curve_order, field_modulus

# BN254/BN128 curve parameters
# Base field for BN254
p = field_modulus  # 21888242871839275222246405745257275088696311157297823662689037894645226208583
# Number of points on BN254
n = curve_order    # 21888242871839275222246405745257275088548364400416034343698204186575808495617

# G1 generator point (in affine coordinates)
# The py_ecc library provides G1 as (1, 2)
P = G1

# G2 generator point (in affine coordinates)
# The py_ecc library already provides the correct G2 generator for BN254
# which is embedded in F_p^2
Q = G2

def compute_pairing(point_g1, point_g2):
    """
    Compute pairing e(P, Q) for points P in G1 and Q in G2

    Args:
        point_g1: Point in G1 (tuple or py_ecc point)
        point_g2: Point in G2 (tuple or py_ecc point)

    Returns:
        Pairing result in F_p^12
    """
    return pairing(point_g2, point_g1)

# Global trusted setup - set this before using commit/prove/verify
_S1 = None
_S2 = None

def set_trusted_setup(S1, S2):
    """
    Set the global trusted setup parameters

    Args:
        S1: List of G1 points [P, τP, τ²P, ..., τˡP]
        S2: G2 point τQ
    """
    global _S1, _S2
    _S1 = S1
    _S2 = S2

def commit(poly):
    """
    Commit to a polynomial using KZG

    Args:
        poly: Polynomial object with coeffs attribute

    Returns:
        Commitment point on G1
    """
    if _S1 is None:
        raise ValueError("Trusted setup not initialized. Call kzg.set_trusted_setup(S1, S2) first.")

    from py_ecc.bn128 import multiply, add, Z1

    coeffs = poly.coeffs
    c = Z1  # Point at infinity

    for i, coeff in enumerate(coeffs):
        if i < len(_S1):
            term = multiply(_S1[i], coeff % n)
            c = add(c, term)

    return c

def prove(poly, γ):
    """
    Create an opening proof for polynomial at point γ

    Args:
        poly: Polynomial object
        γ: Point to evaluate at

    Returns:
        Proof point on G1
    """
    if _S1 is None:
        raise ValueError("Trusted setup not initialized. Call kzg.set_trusted_setup(S1, S2) first.")

    # Import Polynomial class
    from py_ecc.bn128 import multiply, add, Z1
    from lib.polynomials import Polynomial

    # Get the polynomial's modulus from the polynomial itself
    poly_p = poly.modulus

    # Evaluate poly at γ
    val = poly(γ)

    # Compute numerator: poly(x) - val
    numerator = poly - Polynomial([val], poly_p)

    # Compute divisor: x - γ
    divisor = Polynomial([(-γ) % poly_p, 1], poly_p)

    # Quotient
    quotient, remainder = numerator.quo_rem(divisor)

    # Commit to quotient
    coeffs = quotient.coeffs
    π = Z1

    for i, coeff in enumerate(coeffs):
        if i < len(_S1):
            term = multiply(_S1[i], coeff % n)
            π = add(π, term)

    return π

def verify(commitment_C, proof_π, γ, v):
    """
    Verify a KZG opening proof

    Args:
        commitment_C: Commitment to polynomial
        proof_π: Opening proof
        γ: Evaluation point
        v: Claimed value poly(γ)

    Returns:
        True if valid, False otherwise
    """
    if _S2 is None:
        raise ValueError("Trusted setup not initialized. Call kzg.set_trusted_setup(S1, S2) first.")

    from py_ecc.bn128 import multiply, add, neg, pairing

    # e(π, S₂ - γQ) ?= e(C - vP, Q)

    # Left side: e(π, S₂ - γQ)
    γQ = multiply(Q, γ % n)
    S2_minus_γQ = add(_S2, neg(γQ))
    lhs = pairing(S2_minus_γQ, proof_π)

    # Right side: e(C - vP, Q)
    vP = multiply(P, v % n)
    C_minus_vP = add(commitment_C, neg(vP))
    rhs = pairing(Q, C_minus_vP)

    return lhs == rhs
