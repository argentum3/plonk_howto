#!/usr/bin/env python3
"""
Deep investigation: Why does Cell 99 fail even with correct code?

The output shows:
  LHS (master_poly): 15881336282346686748609892963327418060523628370946765287006697761502273751856
  RHS (t_zeta*ZH):   21680131508316546133776511944515611827072429717437918331349788695345791946113
  Match: False

This means the values don't match. Let's trace why.
"""

print("=" * 70)
print("DEEP INVESTIGATION: WHY CELL 99 FAILS")
print("=" * 70)

print("""
From the output, we know:
  - New code is running (no quotient_poly_blind)
  - t_zeta comes from quotient_poly(zeta)
  - But LHS ≠ RHS

Let's trace what could cause this mismatch.
""")

print("\n" + "=" * 70)
print("HYPOTHESIS 1: t_zeta is from wrong quotient_poly")
print("=" * 70)

print("""
Cell 94 builds:
  bigt = t_gates + α·t_perm_start + α²·t_perm_step
  quotient_poly = bigt / ZH

Cell 96 evaluates:
  t_zeta = quotient_poly(zeta)

Cell 99 checks:
  master_poly_v = t_gates_v + α·t_perm_start_v + α²·t_perm_step_v
  rhs = t_zeta * ZH(zeta)

For this to work:
  bigt(zeta) MUST equal master_poly_v

Let's check each component of bigt vs master_poly_v:
""")

print("\n" + "=" * 70)
print("HYPOTHESIS 2: Blinded vs Unblinded Polynomials")
print("=" * 70)

print("""
Cell 94 builds bigt using:
  t_gates = qM·a_blind·b_blind + qL·a_blind + qR·b_blind - c_blind
  t_perm_start = (z_poly_blind - 1)·L1
  t_perm_step = z_poly_blind·N_poly - D_poly·z_poly_blind(x·ω)

Cell 99 builds master_poly_v using:
  t_gates_v = qM(ζ)·a_zeta·b_zeta + qL(ζ)·a_zeta + qR(ζ)·b_zeta - c_zeta
  t_perm_start_v = (z_zeta - 1)·L1(ζ)
  t_perm_step_v = z_zeta·N_poly(ζ) - D_poly(ζ)·z_zeta_omega

These SHOULD be the same because:
  - a_zeta = a_blind(ζ)
  - b_zeta = b_blind(ζ)
  - c_zeta = c_blind(ζ)
  - z_zeta = z_poly_blind(ζ)
  - z_zeta_omega = z_poly_blind(ζ·ω)

So evaluating the polynomial at ζ should equal computing with the values at ζ.

UNLESS... the values used in Cell 99 don't match what was used in Cell 94!
""")

print("\n" + "=" * 70)
print("HYPOTHESIS 3: Old Values in Cell 99")
print("=" * 70)

print("""
Cell 99 uses these variables:
  - a_zeta, b_zeta, c_zeta (from Cell 96)
  - z_zeta, z_zeta_omega (from Cell 96)
  - t_zeta (from Cell 96)
  - N_poly, D_poly (from Cell 92)
  - qL, qR, qM (from earlier)
  - L1 (from earlier)
  - alpha, beta, gamma, zeta (challenges)

If ANY of these are from an old run, the check will fail!

Most likely culprits:
  1. z_zeta might be from old z_poly (not z_poly_blind)
  2. t_zeta might be from old quotient_poly_blind
  3. N_poly, D_poly might be from tutorial, not Exercise 20

Let me check which is most likely...
""")

print("\n" + "=" * 70)
print("MOST LIKELY ISSUE: z_zeta from WRONG polynomial")
print("=" * 70)

print("""
Wait! I just realized the issue!

In Cell 96, we have TWO changes:
  1. z_zeta = z_poly_blind(zeta)  ✓ (we fixed this)
  2. t_zeta = quotient_poly(zeta)  ✓ (we just fixed this)

But when we FIRST fixed Cell 96, we changed z_zeta to use z_poly_blind.

Now, if Cell 92 is using the OLD code that commits to z_poly (not z_poly_blind),
then the commitment c_z is wrong, which affects the transcript, which affects
ALL subsequent challenges (alpha, zeta), which makes everything wrong!

Let me check: Does Cell 92 define z_poly_blind AND commit to it?
""")

print("\n" + "=" * 70)
print("CRITICAL CHECK: Cell 92 z_poly_blind")
print("=" * 70)

print("""
Cell 92 should have:

1. Compute z_poly from interpolate_z_N_D
2. Blind it: z_poly_blind = z_poly + (b1_z·x + b2_z)·ZH
3. Commit to z_poly_blind: c_z = kzg.commit(z_poly_blind)

If Cell 92 is missing step 2 or step 3, then:
  - c_z is wrong
  - transcript is wrong after c_z
  - alpha, zeta are wrong
  - Everything downstream is wrong!

This would explain why LHS ≠ RHS even with correct formulas.
""")

print("\n" + "=" * 70)
print("ACTION ITEMS")
print("=" * 70)

print("""
To diagnose this, run in a notebook cell:

```python
print("Cell 92 check:")
print(f"  z_poly defined: {hasattr(z_poly, 'degree')}")
try:
    print(f"  z_poly_blind defined: {hasattr(z_poly_blind, 'degree')}")
    print(f"  z_poly degree: {z_poly.degree()}")
    print(f"  z_poly_blind degree: {z_poly_blind.degree()}")

    # Check if they're different
    test_point = 12345
    z_val = z_poly(test_point)
    z_blind_val = z_poly_blind(test_point)
    print(f"  z_poly({test_point}) = {z_val}")
    print(f"  z_poly_blind({test_point}) = {z_blind_val}")
    print(f"  Different: {z_val != z_blind_val}")

    # Check commitment
    import kzg as kzg_module
    c_z_from_z = kzg.commit(z_poly)
    c_z_from_z_blind = kzg.commit(z_poly_blind)
    print(f"  c_z matches commit(z_poly): {c_z == c_z_from_z}")
    print(f"  c_z matches commit(z_poly_blind): {c_z == c_z_from_z_blind}")

except NameError as e:
    print(f"  ERROR: {e}")

print("\\nCell 96 check:")
print(f"  z_zeta = {z_zeta}")
try:
    z_from_blind = z_poly_blind(zeta)
    z_from_unblind = z_poly(zeta)
    print(f"  z_poly_blind(zeta) = {z_from_blind}")
    print(f"  z_poly(zeta) = {z_from_unblind}")
    print(f"  z_zeta matches z_poly_blind(zeta): {z_zeta == z_from_blind}")
    print(f"  z_zeta matches z_poly(zeta): {z_zeta == z_from_unblind}")
except NameError as e:
    print(f"  ERROR: {e}")
```

This will tell us EXACTLY which polynomial is being used.
""")

print("\n" + "=" * 70)
