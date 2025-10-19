#!/usr/bin/env python3
"""
Check if the blinding issue is causing the quotient constraint failure
Run this from a notebook cell after running cells 91-98
"""

print("=" * 70)
print("CHECKING BLINDING ISSUE")
print("=" * 70)

print("\nCell 96 uses:")
print("  z_zeta = z_poly(zeta)")
print("  t_zeta = quotient_poly(zeta)")
print()
print("But it SHOULD use:")
print("  z_zeta = z_poly_blind(zeta)")
print("  t_zeta = quotient_poly_blind(zeta)")
print()

# Check if blinded versions exist
print("Checking if blinded polynomials are defined:")
try:
    print(f"  ✓ z_poly_blind exists: {type(z_poly_blind)}")
except NameError:
    print(f"  ✗ z_poly_blind not defined")

try:
    print(f"  ✓ quotient_poly_blind exists: {type(quotient_poly_blind)}")
except NameError:
    print(f"  ✗ quotient_poly_blind not defined")

print()

# Check the actual values
print("Current values in global scope:")
print(f"  z_zeta = {z_zeta}")
print(f"  t_zeta = {t_zeta}")
print()

# Compute what they should be
try:
    z_zeta_blind = z_poly_blind(zeta)
    t_zeta_blind = quotient_poly_blind(zeta)

    print("What they should be (using blinded polynomials):")
    print(f"  z_poly_blind(ζ) = {z_zeta_blind}")
    print(f"  quotient_poly_blind(ζ) = {t_zeta_blind}")
    print()

    print("Do they match?")
    print(f"  z_zeta matches z_poly_blind(ζ): {z_zeta == z_zeta_blind}")
    print(f"  t_zeta matches quotient_poly_blind(ζ): {t_zeta == t_zeta_blind}")
    print()

    if z_zeta != z_zeta_blind or t_zeta != t_zeta_blind:
        print("❌ FOUND THE ISSUE!")
        print()
        print("Cell 96 uses unblinded polynomials, but it should use blinded ones!")
        print()
        print("The prover computes constraints using BLINDED polynomials:")
        print("  - a_blind, b_blind, c_blind")
        print("  - z_poly_blind")
        print("  - quotient_poly_blind")
        print()
        print("But cell 96 evaluates at ζ using UNBLINDED z_poly and quotient_poly!")
        print()
        print("This causes a mismatch in the quotient constraint check.")
        print()

        # Show the difference
        print("Differences:")
        print(f"  z difference: {(z_zeta_blind - z_zeta) % p}")
        print(f"  t difference: {(t_zeta_blind - t_zeta) % p}")
        print()

        # Check if it's ZH(zeta) related
        try:
            ZH_zeta = ZH(zeta)
            print(f"  ZH(ζ) = {ZH_zeta}")
            print()
            print("The difference should be a multiple of ZH(ζ) due to blinding.")
        except:
            pass

    else:
        print("✓ Values match - blinding is not the issue")

except NameError as e:
    print(f"Cannot check blinded versions: {e}")
    print()
    print("This might be the issue - blinded polynomials not in scope")

print()
print("=" * 70)
print("ADDITIONAL CHECK: z_zeta_omega")
print("=" * 70)

print("\nCell 96 also uses:")
print("  z_zeta_omega = z_poly(zeta_omega)")
print()

try:
    zeta_omega = (zeta * ω) % p
    z_zeta_omega_blind = z_poly_blind(zeta_omega)

    print(f"Current z_zeta_omega: {z_zeta_omega}")
    print(f"Should be z_poly_blind(ζ·ω): {z_zeta_omega_blind}")
    print(f"Match: {z_zeta_omega == z_zeta_omega_blind}")

    if z_zeta_omega != z_zeta_omega_blind:
        print()
        print("❌ z_zeta_omega also uses unblinded polynomial!")
        print(f"Difference: {(z_zeta_omega_blind - z_zeta_omega) % p}")
except NameError as e:
    print(f"Cannot check: {e}")

print()
print("=" * 70)
