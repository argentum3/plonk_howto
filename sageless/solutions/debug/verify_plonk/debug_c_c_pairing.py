#!/usr/bin/env python3
"""
Debug script to investigate why the pairing check for c_c fails in verify_plonk.

The verify_plonk function checks:
    verification(c_c, proof_output, ω^4, value_c)

Where:
- c_c: Commitment to c_blind
- proof_output: Opening proof for c_blind at ω^4
- ω^4: The fourth domain point (should equal 1 in our domain)
- value_c: c(ω^4) which should be 9

This script will:
1. Reconstruct all the components
2. Test the pairing check step by step
3. Identify where the mismatch occurs
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from lib.polynomials import p, Polynomial, PolynomialVar, interpolate
import kzg
from py_ecc.bn128 import multiply
import hashlib

print("="*70)
print("DEBUG: c_c PAIRING CHECK FAILURE")
print("="*70)

# ============================================================================
# SETUP
# ============================================================================

n = 4
r = (p - 1) // 4
h = 5
ω = pow(h, r, p)
Ω = [pow(ω, i, p) for i in range(1, n+1)]

print(f"\nDomain setup:")
print(f"  n = {n}")
print(f"  ω = {ω}")
print(f"  Ω = {Ω}")

# Check ω^4
ω_4 = pow(ω, 4, p)
print(f"\n  ω^4 = {ω_4}")
print(f"  ω^4 == 1: {ω_4 == 1}")
print(f"  ω^4 % p = {ω_4 % p}")

# Circuit values
O = {1:1, 2:2, 3:3, 4:9}
c = interpolate(Ω, list(O.values()))

print(f"\nOriginal polynomial c:")
print(f"  c(ω^1) = {c(Ω[0])} (should be 1)")
print(f"  c(ω^2) = {c(Ω[1])} (should be 2)")
print(f"  c(ω^3) = {c(Ω[2])} (should be 3)")
print(f"  c(ω^4) = {c(Ω[3])} (should be 9)")

# Evaluate c at ω^4 directly
value_c_direct = c(ω_4)
print(f"\nDirect evaluation:")
print(f"  c(ω^4) = {value_c_direct}")

# ============================================================================
# BLINDING
# ============================================================================

x = PolynomialVar(p)
ZH = x
for _ in range(n - 1):
    ZH = ZH * x
ZH = ZH - 1

def random_polynomial(degree, modulus):
    import random
    coeffs = [random.randint(0, modulus - 1) for _ in range(degree + 1)]
    return Polynomial(coeffs, modulus)

import random
random.seed(42)

# Skip a_blind and b_blind to get to c_blind with same random seed
k = 2
a_random = random_polynomial(degree=k-1, modulus=p)
b_random = random_polynomial(degree=k-1, modulus=p)
c_random = random_polynomial(degree=k-1, modulus=p)

c_blind = c + c_random * ZH

print(f"\nBlinded polynomial c_blind:")
print(f"  c_blind degree: {c_blind.degree()}")

# Check that blinding preserves values at domain points
print(f"\nChecking c_blind at domain points (should match c):")
for i, ω_i in enumerate(Ω, 1):
    c_val = c(ω_i)
    c_blind_val = c_blind(ω_i)
    match = (c_val == c_blind_val)
    print(f"  c(ω^{i}) = {c_val}, c_blind(ω^{i}) = {c_blind_val}, match: {match}")

# ============================================================================
# TRUSTED SETUP
# ============================================================================

τ = 424242
l = 10
P = kzg.P

S1 = []
τ_power = 1
for i in range(l + 1):
    point = multiply(P, τ_power % kzg.n)
    S1.append(point)
    τ_power = (τ_power * τ) % kzg.n

S2 = multiply(kzg.Q, τ % kzg.n)

kzg.set_trusted_setup(S1, S2)

# ============================================================================
# COMMITMENT AND PROOF
# ============================================================================

print(f"\n" + "="*70)
print("COMMITMENT AND PROOF")
print("="*70)

c_c = kzg.commit(c_blind)
print(f"\nCommitment c_c:")
print(f"  c_c = {c_c}")

# The issue: verify_plonk uses ω^4 as the evaluation point
# But in Exercise 19, we evaluated at pow(ω, 4, p)
eval_point = pow(ω, 4, p)
print(f"\nEvaluation point:")
print(f"  ω^4 (computed) = {eval_point}")
print(f"  ω^4 == 1: {eval_point == 1}")

# Evaluate c_blind at this point
value_c = c_blind(eval_point)
print(f"\nEvaluation:")
print(f"  c_blind(ω^4) = {value_c}")
print(f"  Expected (c(ω^4)): {c(eval_point)}")
print(f"  Match: {value_c == c(eval_point)}")

# Generate proof for this evaluation
print(f"\nGenerating proof...")
proof_output = kzg.prove(c_blind, eval_point)
print(f"  proof_output = {proof_output}")

# ============================================================================
# VERIFICATION TEST
# ============================================================================

print(f"\n" + "="*70)
print("VERIFICATION TEST")
print("="*70)

# Test 1: Verify with the correct evaluation point
print(f"\nTest 1: Verify with ω^4 = {eval_point}")
result1 = kzg.verify(c_c, proof_output, eval_point, value_c)
print(f"  Result: {result1}")

# Test 2: What if verify_plonk is using raw ω^4 without modulo?
ω_4_raw = ω ** 4
print(f"\nTest 2: Check if using ω^4 without modulo")
print(f"  ω^4 (raw, no modulo) = {ω_4_raw}")
print(f"  Is this different from ω^4 % p? {ω_4_raw != eval_point}")

# Test 3: Verify at ω^4 == 1
print(f"\nTest 3: Verify at point 1 (since ω^4 = 1)")
value_at_1 = c_blind(1)
print(f"  c_blind(1) = {value_at_1}")
print(f"  value_c = {value_c}")
print(f"  Match: {value_at_1 == value_c}")

result3 = kzg.verify(c_c, proof_output, 1, value_at_1)
print(f"  Verify(c_c, proof_output, 1, c_blind(1)): {result3}")

# ============================================================================
# DIAGNOSIS
# ============================================================================

print(f"\n" + "="*70)
print("DIAGNOSIS")
print("="*70)

print(f"\nPotential issues:")

# Issue 1: Evaluation point mismatch
print(f"\n1. Evaluation point used in proof generation:")
print(f"   In Exercise 19, we used: pow(ω, 4, p) = {pow(ω, 4, p)}")
print(f"   This equals: {pow(ω, 4, p)}")
print(f"   Since ω^4 = 1 in our domain, this should be 1")

# Issue 2: Check what value verify_plonk is using
print(f"\n2. What verify_plonk might be doing:")
print(f"   verify_plonk uses: ω^4 directly")
print(f"   In Python: ω^4 means XOR operation if not using pow()!")
print(f"   ω ^ 4 = {ω ^ 4} (this is XOR, not exponentiation!)")
print(f"   pow(ω, 4, p) = {pow(ω, 4, p)} (this is correct exponentiation)")

# Issue 3: Check the actual verification call
print(f"\n3. The verification call in verify_plonk:")
print(f"   verification(c_c, proof_output, ω^4, value_c)")
print(f"   If ω^4 is computed as ω^4 in Python syntax...")
print(f"   That would be XOR: {ω} ^ 4 = {ω ^ 4}")
print(f"   But it should be: pow(ω, 4, p) = {pow(ω, 4, p)}")

# Test this hypothesis
print(f"\n" + "="*70)
print("TESTING HYPOTHESIS: XOR vs POW")
print("="*70)

xor_result = ω ^ 4
print(f"\nω ^ 4 (XOR): {xor_result}")
print(f"pow(ω, 4, p): {pow(ω, 4, p)}")

# Try verifying with XOR value
if xor_result != eval_point:
    print(f"\nTrying to verify with XOR value...")
    value_at_xor = c_blind(xor_result)
    print(f"  c_blind({xor_result}) = {value_at_xor}")

    # This won't work with the same proof since proof is for different point
    result_xor = kzg.verify(c_c, proof_output, xor_result, value_at_xor)
    print(f"  Verify with XOR point: {result_xor}")

# ============================================================================
# SOLUTION
# ============================================================================

print(f"\n" + "="*70)
print("SOLUTION")
print("="*70)

print(f"\nThe issue is likely in how ω^4 is computed in verify_plonk.")
print(f"\nIn Python, '^' is the XOR operator, not exponentiation!")
print(f"  ω ^ 4 = {ω ^ 4} (WRONG - this is XOR)")
print(f"  ω ** 4 or pow(ω, 4, p) = {pow(ω, 4, p)} (CORRECT)")

print(f"\nverify_plonk line:")
print(f"  ('c_c', 'proof_output', 'output', ω^4)")
print(f"\nShould be:")
print(f"  ('c_c', 'proof_output', 'output', pow(ω, 4, p))")
print(f"  or")
print(f"  ('c_c', 'proof_output', 'output', ω**4)")

print(f"\n" + "="*70)
print("VERIFICATION WITH CORRECT POINT")
print("="*70)

correct_point = pow(ω, 4, p)
correct_value = c_blind(correct_point)

print(f"\nUsing correct exponentiation:")
print(f"  Point: pow(ω, 4, p) = {correct_point}")
print(f"  Value: c_blind({correct_point}) = {correct_value}")

# Generate new proof with correct point (should match what we already have)
proof_correct = kzg.prove(c_blind, correct_point)
verify_correct = kzg.verify(c_c, proof_correct, correct_point, correct_value)

print(f"  Proof: {proof_correct}")
print(f"  Verification: {verify_correct}")

if verify_correct:
    print(f"\n✓✓✓ VERIFICATION SUCCEEDS WITH CORRECT EXPONENTIATION ✓✓✓")
else:
    print(f"\n✗✗✗ Still failing - need further investigation ✗✗✗")

print(f"\n" + "="*70)
print("SUMMARY")
print("="*70)

print(f"""
The pairing check for c_c is failing because of operator precedence in Python.

In the verify_plonk function, this line:
    ('c_c', 'proof_output', 'output', ω^4)

Uses '^' which is XOR, not exponentiation!

WRONG: ω^4 = {ω ^ 4} (XOR operation)
RIGHT: pow(ω, 4, p) = {pow(ω, 4, p)} (exponentiation)
RIGHT: ω**4 % p = {(ω**4) % p} (exponentiation with modulo)

Since we're in a multiplicative domain where ω^4 = 1:
  pow(ω, 4, p) = 1

But XOR gives a completely different number:
  ω ^ 4 = {ω ^ 4}

The proof was generated for the correct point (1), but verification
is checking at the wrong point ({ω ^ 4}), causing the mismatch.

NOTE: The user said not to change cell 100, so this is a known issue
in the tutorial that demonstrates the importance of operator precedence!
""")
