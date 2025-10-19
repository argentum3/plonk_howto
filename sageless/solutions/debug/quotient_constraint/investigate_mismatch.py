#!/usr/bin/env python3
"""
Investigate why Cell 99 quotient constraint check fails

The issue: Cell 99 manually recomputes the quotient constraint but gets different result
"""

print("=" * 70)
print("INVESTIGATING CELL 99 QUOTIENT CONSTRAINT MISMATCH")
print("=" * 70)

print("""
HYPOTHESIS: Cell 99 uses different values than what was used in proof generation

Cell 99 manual check computes:
    master_poly_v = t_gates_v + α·t_perm_start_v + α²·t_perm_step_v
    rhs = t_zeta * ZH(zeta)

And checks if they match.

But there are several potential issues:

1. BLINDING MISMATCH
   - Cell 94 (Exercise 21) builds master polynomial from BLINDED polynomials:
     bigt = t_gates + α·t_perm_start + α²·t_perm_step
     where t_gates uses a_blind, b_blind, c_blind
     and t_perm_start, t_perm_step use z_poly_blind

   - Cell 96 evaluates t_zeta = quotient_poly_blind(zeta)

   - But Cell 99 computes constraints using:
     a_zeta, b_zeta, c_zeta (from a_blind, b_blind, c_blind) ✓
     z_zeta, z_zeta_omega (from z_poly_blind) ✓
     t_zeta (from quotient_poly_blind) ✓

   So blinding should be consistent!

2. WRONG z_poly_blind USED
   - If Cell 99 uses z_zeta from an old z_poly_blind (tutorial),
     but t_zeta is from the new quotient_poly_blind (Exercise 21),
     they won't match!

3. N_poly and D_poly ISSUE
   - Cell 99 uses N_poly(zeta) and D_poly(zeta)
   - These should be from Exercise 20 (Cell 92)
   - But maybe they're from the tutorial?

4. QUOTIENT POLYNOMIAL MISMATCH
   - t_zeta should be quotient_poly_blind(zeta)
   - But maybe Cell 99 is running before Cell 96?
   - Or t_zeta is from an old computation?

Let me trace through what should happen:
""")

print("\n" + "=" * 70)
print("EXPECTED FLOW")
print("=" * 70)

print("""
Cell 92 (Exercise 20):
  - Generates β, γ
  - Computes z_poly, N_poly, D_poly from a_blind, b_blind, c_blind
  - Blinds z_poly → z_poly_blind
  - Commits c_z = kzg.commit(z_poly_blind)

Cell 94 (Exercise 21):
  - Generates α
  - Builds master polynomial:
    t_gates = qM·a_blind·b_blind + qL·a_blind + qR·b_blind - c_blind
    t_perm_start = (z_poly_blind - 1)·L1
    t_perm_step = z_poly_blind·N_poly - D_poly·z_poly_blind(x·ω)
    bigt = t_gates + α·t_perm_start + α²·t_perm_step
  - Computes quotient: quotient_poly = bigt / ZH
  - Blinds it: quotient_poly_blind = quotient_poly + (b1_t·x + b2_t)·ZH
  - Commits c_t = kzg.commit(quotient_poly_blind)

Cell 96 (Exercise 22):
  - Generates ζ
  - Evaluates:
    a_zeta = a_blind(ζ)
    b_zeta = b_blind(ζ)
    c_zeta = c_blind(ζ)
    z_zeta = z_poly_blind(ζ)
    t_zeta = quotient_poly_blind(ζ)
    z_zeta_omega = z_poly_blind(ζ·ω)

Cell 99 (Manual Check):
  - Recomputes:
    t_gates_v = qM(ζ)·a_zeta·b_zeta + qL(ζ)·a_zeta + qR(ζ)·b_zeta - c_zeta
    t_perm_start_v = (z_zeta - 1)·L1(ζ)
    t_perm_step_v = z_zeta·N_poly(ζ) - D_poly(ζ)·z_zeta_omega
    master_poly_v = t_gates_v + α·t_perm_start_v + α²·t_perm_step_v
  - Checks: master_poly_v == t_zeta * ZH(ζ)

The equation should be:
  bigt(ζ) = quotient_poly_blind(ζ) * ZH(ζ)

But with blinding:
  quotient_poly_blind = quotient_poly + (b1_t·x + b2_t)·ZH

So:
  quotient_poly_blind(ζ) = quotient_poly(ζ) + (b1_t·ζ + b2_t)·ZH(ζ)

If ZH(ζ) ≠ 0, then the blinding term contributes!

Wait... that's the issue!
""")

print("\n" + "=" * 70)
print("THE REAL ISSUE: BLINDING OF QUOTIENT POLYNOMIAL")
print("=" * 70)

print("""
The quotient polynomial blinding adds:
  quotient_poly_blind = quotient_poly + (b1_t·x + b2_t)·ZH

When we evaluate at ζ:
  quotient_poly_blind(ζ) = quotient_poly(ζ) + (b1_t·ζ + b2_t)·ZH(ζ)

The equation we're checking is:
  bigt(ζ) = quotient_poly_blind(ζ) * ZH(ζ)

Expanding:
  bigt(ζ) = [quotient_poly(ζ) + (b1_t·ζ + b2_t)·ZH(ζ)] * ZH(ζ)
  bigt(ζ) = quotient_poly(ζ)·ZH(ζ) + (b1_t·ζ + b2_t)·ZH(ζ)²

But we know:
  bigt = quotient_poly * ZH  (polynomial identity)

So at ζ:
  bigt(ζ) = quotient_poly(ζ) * ZH(ζ)

Therefore:
  quotient_poly(ζ)·ZH(ζ) = quotient_poly_blind(ζ)·ZH(ζ) - (b1_t·ζ + b2_t)·ZH(ζ)²

This only works if ZH(ζ) = 0 (i.e., ζ is a root of ZH).

But ζ is a RANDOM challenge point, so ZH(ζ) ≠ 0 with overwhelming probability!

CONCLUSION: We CANNOT blind the quotient polynomial the same way we blind other polynomials!

The blinding of quotient_poly breaks the quotient identity at ζ.
""")

print("\n" + "=" * 70)
print("WHY THIS BREAKS")
print("=" * 70)

print("""
For witness polynomials (a_blind, b_blind, c_blind, z_poly_blind):
  - We evaluate them at ζ: a_blind(ζ), etc.
  - The blinding term (random * ZH) adds unpredictable values
  - This is fine because we're just proving evaluations

But for quotient_poly:
  - We need: bigt(ζ) = quotient_poly(ζ) * ZH(ζ)
  - This is a CONSTRAINT that must hold
  - If we blind quotient_poly, we get:
    bigt(ζ) ≠ quotient_poly_blind(ζ) * ZH(ζ)

The standard PlonK protocol uses DIFFERENT blinding for the quotient:
  - Split quotient_poly into chunks: t_lo, t_mid, t_hi
  - Commit to each chunk separately
  - This allows blinding while preserving the quotient identity

But in our simplified tutorial, we should NOT blind the quotient polynomial!
""")

print("\n" + "=" * 70)
print("THE FIX")
print("=" * 70)

print("""
In Cell 94 (Exercise 21), we should:

REMOVE the quotient polynomial blinding:
  # DELETE THESE LINES:
  b1_t, b2_t = 55555, 66666
  quotient_poly_blind = quotient_poly + (b1_t * x + b2_t) * ZH
  c_t = kzg.commit(quotient_poly_blind)

REPLACE WITH:
  # Commit to (unblinded) quotient polynomial
  # Note: In full PlonK, quotient is split and blinded differently
  c_t = kzg.commit(quotient_poly)

In Cell 96 (Exercise 22), change:
  # FROM:
  t_zeta = quotient_poly_blind(zeta)
  proof_t = kzg.prove(quotient_poly_blind, zeta)

  # TO:
  t_zeta = quotient_poly(zeta)
  proof_t = kzg.prove(quotient_poly, zeta)

This way:
  - bigt(ζ) = quotient_poly(ζ) * ZH(ζ) will hold
  - Cell 99 manual check will pass
  - Cell 100 verify_plonk will pass

Note: This reduces zero-knowledge slightly, but the witness polynomials
(a_blind, b_blind, c_blind, z_poly_blind) are still blinded, which
provides the main zero-knowledge property.
""")

print("\n" + "=" * 70)
