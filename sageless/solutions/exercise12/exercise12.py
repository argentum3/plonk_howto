#!/usr/bin/env python3
"""
Exercise 12: Polynomial Interpolation over Multiplicative Domain

Interpolate the value vectors (LI, RI, O) and selector vectors (SL, SR, SM)
over the multiplicative domain Ω instead of the additive indices I.

Previously:
  - Domain I = {1, 2, 3, 4} (additive indices)
  - Polynomials: a = interpolate(I, LI.values())

Now:
  - Domain Ω = {ω, ω^2, ω^3, ω^4=1} (multiplicative roots of unity)
  - Polynomials: a = interpolate(Ω, LI.values())

The same interpolate() function works for both domains!

Key difference:
  - Previously: a(1) = LI[1], a(2) = LI[2], etc.
  - Now: a(ω) = LI[1], a(ω^2) = LI[2], etc.

The polynomials will be different, but they encode the same witness values
at the corresponding domain points.
"""

import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib.polynomials import p, interpolate

print("="*70)
print("EXERCISE 12: INTERPOLATION OVER MULTIPLICATIVE DOMAIN")
print("="*70)

# Step 1: Find generator ω from Exercise 11
print("\nStep 1: Computing generator ω and domain Ω...")

n = pow(2, 2)  # n = 4
r = (p - 1) // 4

# Find smallest h such that ω = h^r has order 4
def has_order_4(omega, modulus):
    if pow(omega, 4, modulus) != 1:
        return False
    for i in [1, 2, 3]:
        if pow(omega, i, modulus) == 1:
            return False
    return True

h = 1
ω = None
while h < p:
    candidate = pow(h, r, p)
    if has_order_4(candidate, p):
        ω = candidate
        break
    h += 1

print(f"  Generator: ω = {ω}")
print(f"  (found using h = {h})")

# Construct domain Ω = {ω, ω^2, ω^3, ω^4=1}
Ω = [pow(ω, i, p) for i in range(1, n + 1)]
print(f"\n  Domain Ω = {{ω, ω^2, ω^3, ω^4}}")
for i, elem in enumerate(Ω, 1):
    print(f"    ω^{i} = {elem}")

# Step 2: Define value vectors (witness values)
print(f"\n" + "="*70)
print("STEP 2: VALUE VECTORS (Witness)")
print("="*70)

# These represent the circuit execution:
# Gate 1: 0 + 1 = 1 (addition)
# Gate 2: 1 + 1 = 2 (addition)
# Gate 3: 1 + 2 = 3 (addition)
# Gate 4: 3 * 3 = 9 (multiplication)

LI = {1: 0, 2: 1, 3: 1, 4: 3}  # Left inputs
RI = {1: 1, 2: 1, 3: 2, 4: 3}  # Right inputs
O  = {1: 1, 2: 2, 3: 3, 4: 9}  # Outputs

print(f"\nValue vectors (indexed by gate number i):")
print(f"  LI (left inputs):   {LI}")
print(f"  RI (right inputs):  {RI}")
print(f"  O  (outputs):       {O}")

# Step 3: Interpolate witness polynomials over Ω
print(f"\n" + "="*70)
print("STEP 3: INTERPOLATE WITNESS POLYNOMIALS OVER Ω")
print("="*70)

print(f"\nInterpolating:")
print(f"  a(x): left input polynomial")
print(f"  b(x): right input polynomial")
print(f"  c(x): output polynomial")

print(f"\nMapping:")
print(f"  Gate i=1 → domain point ω^1")
print(f"  Gate i=2 → domain point ω^2")
print(f"  Gate i=3 → domain point ω^3")
print(f"  Gate i=4 → domain point ω^4")

a = interpolate(Ω, list(LI.values()))  # a(ω^i) = LI[i]
b = interpolate(Ω, list(RI.values()))  # b(ω^i) = RI[i]
c = interpolate(Ω, list(O.values()))   # c(ω^i) = O[i]

print(f"\n✓ Interpolated a(x) with degree {a.degree()}")
print(f"✓ Interpolated b(x) with degree {b.degree()}")
print(f"✓ Interpolated c(x) with degree {c.degree()}")

# Step 4: Define selector vectors
print(f"\n" + "="*70)
print("STEP 4: SELECTOR VECTORS")
print("="*70)

# Selectors indicate gate types:
# SL, SR: 1 for addition gates, 0 for multiplication
# SM: 0 for addition gates, 1 for multiplication

SL = {1: 1, 2: 1, 3: 1, 4: 0}  # Selector for left input in addition
SR = {1: 1, 2: 1, 3: 1, 4: 0}  # Selector for right input in addition
SM = {1: 0, 2: 0, 3: 0, 4: 1}  # Selector for multiplication

print(f"\nSelector vectors (gate types):")
print(f"  SL (left addition):  {SL}")
print(f"  SR (right addition): {SR}")
print(f"  SM (multiplication): {SM}")

print(f"\nGate types:")
for i in range(1, 5):
    gate_type = "addition" if SL[i] == 1 else "multiplication"
    print(f"  Gate {i}: {gate_type}")

# Step 5: Interpolate selector polynomials over Ω
print(f"\n" + "="*70)
print("STEP 5: INTERPOLATE SELECTOR POLYNOMIALS OVER Ω")
print("="*70)

qL = interpolate(Ω, list(SL.values()))  # qL(ω^i) = SL[i]
qR = interpolate(Ω, list(SR.values()))  # qR(ω^i) = SR[i]
qM = interpolate(Ω, list(SM.values()))  # qM(ω^i) = SM[i]

print(f"\n✓ Interpolated qL(x) with degree {qL.degree()}")
print(f"✓ Interpolated qR(x) with degree {qR.degree()}")
print(f"✓ Interpolated qM(x) with degree {qM.degree()}")

# Step 6: Verify interpolations
print(f"\n" + "="*70)
print("VERIFICATION: Check polynomial evaluations at domain points")
print("="*70)

print(f"\nWitness polynomials (a, b, c):")
print(f"  i  | Domain Point | a(ω^i) = LI[i] | b(ω^i) = RI[i] | c(ω^i) = O[i]")
print(f"  " + "-"*75)

all_correct = True
for i in range(1, 5):
    omega_i = Ω[i-1]
    a_val = a(omega_i)
    b_val = b(omega_i)
    c_val = c(omega_i)

    match_a = "✓" if a_val == LI[i] else "✗"
    match_b = "✓" if b_val == RI[i] else "✗"
    match_c = "✓" if c_val == O[i] else "✗"

    print(f"  {i}  | ω^{i:8}  | {a_val:4d} = {LI[i]:4d} {match_a} | {b_val:4d} = {RI[i]:4d} {match_b} | {c_val:4d} = {O[i]:4d} {match_c}")

    if a_val != LI[i] or b_val != RI[i] or c_val != O[i]:
        all_correct = False

print(f"\nSelector polynomials (qL, qR, qM):")
print(f"  i  | qL(ω^i) = SL[i] | qR(ω^i) = SR[i] | qM(ω^i) = SM[i]")
print(f"  " + "-"*60)

for i in range(1, 5):
    omega_i = Ω[i-1]
    qL_val = qL(omega_i)
    qR_val = qR(omega_i)
    qM_val = qM(omega_i)

    match_qL = "✓" if qL_val == SL[i] else "✗"
    match_qR = "✓" if qR_val == SR[i] else "✗"
    match_qM = "✓" if qM_val == SM[i] else "✗"

    print(f"  {i}  | {qL_val:4d} = {SL[i]:4d} {match_qL}   | {qR_val:4d} = {SR[i]:4d} {match_qR}   | {qM_val:4d} = {SM[i]:4d} {match_qM}")

    if qL_val != SL[i] or qR_val != SR[i] or qM_val != SM[i]:
        all_correct = False

if all_correct:
    print(f"\n✓ All polynomial evaluations match expected values!")
else:
    print(f"\n⚠️  Some evaluations don't match!")

# Step 7: Compare with additive domain interpolation
print(f"\n" + "="*70)
print("COMPARISON: Multiplicative Ω vs Additive I")
print("="*70)

# Interpolate over additive domain for comparison
I = [1, 2, 3, 4]
a_additive = interpolate(I, list(LI.values()))

print(f"\nPolynomial a(x) coefficients:")
print(f"\n  Over multiplicative domain Ω:")
print(f"    Coefficients: {a.coeffs}")
print(f"    Degree: {a.degree()}")

print(f"\n  Over additive domain I:")
print(f"    Coefficients: {a_additive.coeffs}")
print(f"    Degree: {a_additive.degree()}")

print(f"\n  → Different polynomials, but same witness values at domain points!")

# Step 8: Validate exact coefficients for multiplicative domain
print(f"\n" + "="*70)
print("COEFFICIENT VALIDATION")
print("="*70)

# Expected coefficients for a(x) over Ω (from the tutorial)
expected_a_coeffs = [
    16416182153879456416684804308942956316411273300312025757773653139931856371714,  # constant term
    5472060717959818804459621193740257811501762607132022234940276763289347427726,   # x term
    5472060717959818805561601436314318772137091100104008585924551046643952123905,   # x^2 term
    16416182153879456417786784551517017277046601793284012108757927423286461067892   # x^3 term
]

print(f"\nValidating a(x) coefficients over multiplicative domain Ω:")
print(f"\na(x) = {expected_a_coeffs[3]} * x^3")
print(f"     + {expected_a_coeffs[2]} * x^2")
print(f"     + {expected_a_coeffs[1]} * x")
print(f"     + {expected_a_coeffs[0]}")

# Check each coefficient
print(f"\nCoefficient comparison:")
coeffs_match = True
for i, (expected, actual) in enumerate(zip(expected_a_coeffs, a.coeffs)):
    match = "✓" if expected == actual else "✗"
    if expected != actual:
        coeffs_match = False
    print(f"  x^{i}: {match}")
    if expected != actual:
        print(f"    Expected: {expected}")
        print(f"    Got:      {actual}")

if coeffs_match:
    print(f"\n✓ All coefficients match expected values!")
else:
    print(f"\n⚠️  Coefficient mismatch!")

# Validate polynomial representation
print(f"\n" + "="*70)
print("POLYNOMIAL a(x) OVER Ω - FULL REPRESENTATION")
print("="*70)

print(f"\na(x) = {a.coeffs[3]} * x^3")
print(f"     + {a.coeffs[2]} * x^2")
print(f"     + {a.coeffs[1]} * x")
print(f"     + {a.coeffs[0]}")

print(f"\nLatex format:")
print(f"a(x) = {a.coeffs[3]} x^3")
print(f"     + {a.coeffs[2]} x^2")
print(f"     + {a.coeffs[1]} x")
print(f"     + {a.coeffs[0]}")

# Summary
print(f"\n" + "="*70)
print("SUMMARY")
print("="*70)

print(f"""
Successfully interpolated all polynomials over multiplicative domain Ω!

Witness polynomials (encoding circuit execution):
  a(x): Left input values    - degree {a.degree()}
  b(x): Right input values   - degree {b.degree()}
  c(x): Output values        - degree {c.degree()}

Selector polynomials (encoding gate types):
  qL(x): Left addition sel.  - degree {qL.degree()}
  qR(x): Right addition sel. - degree {qR.degree()}
  qM(x): Multiplication sel. - degree {qM.degree()}

Domain mapping:
  Gate 1 → ω^1 = {Ω[0]}
  Gate 2 → ω^2 = {Ω[1]}
  Gate 3 → ω^3 = {Ω[2]}
  Gate 4 → ω^4 = {Ω[3]} (= 1)

Key advantage:
  Using multiplicative domain Ω enables constant-time vanishing polynomial
  Z(x) = x^4 - 1 instead of (x-1)(x-2)(x-3)(x-4)

Next steps:
  - Use these polynomials for constraint checking over Ω
  - Leverage Z(x) = x^n - 1 for efficient quotient computations
  - Build towards PlonK's permutation argument
""")

print("="*70)
print("✓ Exercise 12 Complete!")
print("="*70)
