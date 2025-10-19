#!/usr/bin/env python3
"""
Diagnose z_poly_blind verification failure

The issue: c_z is committed to z_poly (unblinded) but proofs are for z_poly_blind
"""

print("=" * 70)
print("DIAGNOSING z_poly_blind VERIFICATION FAILURE")
print("=" * 70)

print("""
HYPOTHESIS: c_z commitment mismatch

Cell 92 (Exercise 20) does:
    c_z = kzg.commit(z_poly)           # Commits to UNBLINDED

Cell 96 (Exercise 22) does:
    z_zeta = z_poly_blind(zeta)        # Evaluates BLINDED
    proof_z = kzg.prove(z_poly_blind, zeta)  # Proves BLINDED

Then verification:
    kzg.verify(c_z, proof_z, zeta, z_zeta)

This checks if:
    c_z == commitment to polynomial P where P(zeta) = z_zeta

But:
    c_z = commit(z_poly)               # Commitment to unblinded
    proof_z = prove(z_poly_blind, ...)  # Proof for blinded
    z_zeta = z_poly_blind(zeta)        # Evaluation of blinded

MISMATCH: c_z is for z_poly, but proof and evaluation are for z_poly_blind!

This will ALWAYS fail because:
    commit(z_poly) ≠ commit(z_poly_blind)
""")

print("\n" + "=" * 70)
print("THE PROBLEM")
print("=" * 70)

print("""
In Cell 92 (Exercise 20), we have:

    z_poly, N_poly, D_poly = interpolate_z_N_D(a_blind, b_blind, c_blind, beta, gamma, Ω)

    # Blind z_poly
    z_poly_blind = z_poly + random_polynomial(degree=k-1, modulus=p) * ZH

    # ❌ WRONG: Commit to unblinded z_poly
    c_z = kzg.commit(z_poly)

Should be:

    # ✓ CORRECT: Commit to blinded z_poly_blind
    c_z = kzg.commit(z_poly_blind)
""")

print("\n" + "=" * 70)
print("WHY THIS HAPPENS")
print("=" * 70)

print("""
The KZG verification checks:

    e(C - [b]₁, [1]₂) = e(π, [s - z]₂)

Where:
    C = commitment to polynomial P
    b = P(z) = claimed evaluation
    π = opening proof
    z = evaluation point

For this to pass:
    C must be commitment to the SAME polynomial that π proves

In our case:
    c_z = commit(z_poly)                    # Commitment to P₁
    proof_z = prove(z_poly_blind, zeta)     # Proof for P₂ where P₂ ≠ P₁
    z_zeta = z_poly_blind(zeta)             # Evaluation of P₂

The verifier checks if c_z commits to a polynomial that equals z_zeta at zeta.
But c_z commits to z_poly, not z_poly_blind, so it fails!
""")

print("\n" + "=" * 70)
print("THE FIX")
print("=" * 70)

print("""
In Cell 92 (Exercise 20), change:

    c_z = kzg.commit(z_poly)

To:

    c_z = kzg.commit(z_poly_blind)

This ensures the commitment matches the polynomial used for proofs and evaluations.
""")

print("\n" + "=" * 70)
print("VERIFICATION")
print("=" * 70)

print("""
After the fix, the verification should work:

    commit(z_poly_blind) → c_z
    prove(z_poly_blind, zeta) → proof_z
    z_poly_blind(zeta) → z_zeta

    verify(c_z, proof_z, zeta, z_zeta) → ✓ True

Because now all three (commitment, proof, evaluation) use the same polynomial!
""")

print("\n" + "=" * 70)
print("IMPACT ON OTHER CELLS")
print("=" * 70)

print("""
This change affects:
1. Cell 92 - commits to z_poly_blind instead of z_poly
2. Cell 96 - verification now passes (no change needed)
3. Cell 98 - proof dictionary unchanged (no change needed)
4. Cell 100 - verify_plonk unchanged (no change needed)

The verify_plonk function verifies c_z against z_zeta and z_zeta_omega.
These values come from z_poly_blind, so c_z must also be from z_poly_blind.
""")

print("\n" + "=" * 70)
