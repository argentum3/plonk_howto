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
