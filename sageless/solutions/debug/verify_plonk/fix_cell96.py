# ============================================================================
# FIX FOR CELL 96: Use blinded polynomials
# ============================================================================
#
# PART 1: EVALUATIONS
# Find these lines in Cell 96 and change them:
# ============================================================================

# OLD: z_zeta = z_poly(zeta)
# NEW:
z_zeta = z_poly_blind(zeta)
print(f"\nz_zeta = z_poly_blind(ζ) = {z_zeta}")

# OLD: t_zeta = quotient_poly(zeta)
# NEW:
t_zeta = quotient_poly_blind(zeta)
print(f"t_zeta = quotient_poly_blind(ζ) = {t_zeta}")

# Evaluate z_poly_blind at ζ·ω
zeta_omega = (zeta * ω) % p
print(f"\nζ·ω = {zeta_omega}")

# OLD: z_zeta_omega = z_poly(zeta_omega)
# NEW:
z_zeta_omega = z_poly_blind(zeta_omega)
print(f"z_zeta_omega = z_poly_blind(ζ·ω) = {z_zeta_omega}")

# ============================================================================
# PART 2: OPENING PROOFS
# Find the proof generation section and change these lines:
# ============================================================================

print("\nGenerating KZG opening proofs...")

proof_a = kzg.prove(a_blind, zeta)
print(f"  ✓ proof_a = prove(a_blind, ζ)")

proof_b = kzg.prove(b_blind, zeta)
print(f"  ✓ proof_b = prove(b_blind, ζ)")

proof_c = kzg.prove(c_blind, zeta)
print(f"  ✓ proof_c = prove(c_blind, ζ)")

# OLD: proof_z = kzg.prove(z_poly, zeta)
# NEW:
proof_z = kzg.prove(z_poly_blind, zeta)
print(f"  ✓ proof_z = prove(z_poly_blind, ζ)")

# OLD: proof_t = kzg.prove(quotient_poly, zeta)
# NEW:
proof_t = kzg.prove(quotient_poly_blind, zeta)
print(f"  ✓ proof_t = prove(quotient_poly_blind, ζ)")

# OLD: proof_z_omega = kzg.prove(z_poly, zeta_omega)
# NEW:
proof_z_omega = kzg.prove(z_poly_blind, zeta_omega)
print(f"  ✓ proof_z_omega = prove(z_poly_blind, ζ·ω)")

# ============================================================================
# PART 3: VERIFICATION (optional - for testing)
# Update the verification print statements if you have them:
# ============================================================================

print("\n" + "="*70)
print("VERIFICATION OF OPENING PROOFS")
print("="*70)

verify_a = kzg.verify(c_a, proof_a, zeta, a_zeta)
print(f"\n  Verify a_blind(ζ) = {a_zeta}: {verify_a}")

verify_b = kzg.verify(c_b, proof_b, zeta, b_zeta)
print(f"  Verify b_blind(ζ) = {b_zeta}: {verify_b}")

verify_c = kzg.verify(c_c, proof_c, zeta, c_zeta)
print(f"  Verify c_blind(ζ) = {c_zeta}: {verify_c}")

verify_z = kzg.verify(c_z, proof_z, zeta, z_zeta)
print(f"  Verify z_poly_blind(ζ) = {z_zeta}: {verify_z}")

verify_t = kzg.verify(c_t, proof_t, zeta, t_zeta)
print(f"  Verify quotient_poly_blind(ζ) = {t_zeta}: {verify_t}")

verify_z_omega = kzg.verify(c_z, proof_z_omega, zeta_omega, z_zeta_omega)
print(f"  Verify z_poly_blind(ζ·ω) = {z_zeta_omega}: {verify_z_omega}")

if all([verify_a, verify_b, verify_c, verify_z, verify_t, verify_z_omega]):
    print("\n✓✓✓ ALL OPENING PROOFS VERIFIED SUCCESSFULLY ✓✓✓")
else:
    print("\n✗✗✗ SOME PROOFS FAILED ✗✗✗")
