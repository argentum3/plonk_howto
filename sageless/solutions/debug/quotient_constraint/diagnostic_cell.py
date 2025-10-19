# Diagnostic for Cell 99 failure
# Copy and paste this into a notebook cell to run

print("=" * 70)
print("DIAGNOSTIC: Cell 99 Failure Investigation")
print("=" * 70)

# Check 1: Which polynomials exist?
print("\n1. Checking polynomial definitions:")
print(f"   z_poly exists: {'z_poly' in dir()}")
print(f"   z_poly_blind exists: {'z_poly_blind' in dir()}")
print(f"   quotient_poly exists: {'quotient_poly' in dir()}")
print(f"   quotient_poly_blind exists: {'quotient_poly_blind' in dir()}")

# Check 2: Which polynomial is z_zeta from?
print("\n2. Checking z_zeta source:")
print(f"   z_zeta = {z_zeta}")

if 'z_poly_blind' in dir() and 'z_poly' in dir():
    z_from_blind = z_poly_blind(zeta)
    z_from_unblind = z_poly(zeta)
    print(f"   z_poly_blind(ζ) = {z_from_blind}")
    print(f"   z_poly(ζ)       = {z_from_unblind}")

    if z_zeta == z_from_blind:
        print(f"   ✓ z_zeta is from z_poly_blind (CORRECT)")
    elif z_zeta == z_from_unblind:
        print(f"   ✗ z_zeta is from z_poly (WRONG!)")
    else:
        print(f"   ? z_zeta doesn't match either")

# Check 3: Which polynomial is t_zeta from?
print("\n3. Checking t_zeta source:")
print(f"   t_zeta = {t_zeta}")

if 'quotient_poly' in dir():
    t_from_unblind = quotient_poly(zeta)
    print(f"   quotient_poly(ζ) = {t_from_unblind}")

    if t_zeta == t_from_unblind:
        print(f"   ✓ t_zeta is from quotient_poly (CORRECT)")
    else:
        print(f"   ✗ t_zeta doesn't match quotient_poly(ζ)")

if 'quotient_poly_blind' in dir():
    t_from_blind = quotient_poly_blind(zeta)
    print(f"   quotient_poly_blind(ζ) = {t_from_blind}")
    if t_zeta == t_from_blind:
        print(f"   ✗ t_zeta is from quotient_poly_blind (WRONG!)")

# Check 4: Commitment check
print("\n4. Checking commitments:")
if 'z_poly_blind' in dir() and 'z_poly' in dir():
    c_z_should_be = kzg.commit(z_poly_blind)
    c_z_wrong = kzg.commit(z_poly)
    print(f"   c_z = {c_z}")
    print(f"   commit(z_poly_blind) = {c_z_should_be}")
    print(f"   commit(z_poly)       = {c_z_wrong}")

    if c_z == c_z_should_be:
        print(f"   ✓ c_z is from z_poly_blind (CORRECT)")
    elif c_z == c_z_wrong:
        print(f"   ✗ c_z is from z_poly (WRONG!)")
        print(f"   → This means Cell 92 didn't commit to z_poly_blind!")

# Check 5: Recompute master polynomial directly
print("\n5. Recomputing constraints at ζ:")

# Get selector values
qL_z = qL(zeta)
qR_z = qR(zeta)
qM_z = qM(zeta)
L1_z = L1(zeta)
N_z = N_poly(zeta)
D_z = D_poly(zeta)
zeta_omega = (zeta * ω) % p

# Compute each component
t_gates_v = (qM_z * a_zeta * b_zeta + qL_z * a_zeta + qR_z * b_zeta - c_zeta) % p
t_perm_start_v = ((z_zeta - 1) * L1_z) % p
t_perm_step_v = (z_zeta * N_z - D_z * z_zeta_omega) % p

print(f"   t_gates(ζ)      = {t_gates_v}")
print(f"   t_perm_start(ζ) = {t_perm_start_v}")
print(f"   t_perm_step(ζ)  = {t_perm_step_v}")

# Master polynomial
master_poly_v = (t_gates_v + alpha * t_perm_start_v + (alpha * alpha) % p * t_perm_step_v) % p
print(f"\n   master_poly(ζ) = {master_poly_v}")

# Compare with direct polynomial evaluation
if 'bigt' in dir():
    bigt_at_zeta = bigt(zeta)
    print(f"   bigt(ζ) direct = {bigt_at_zeta}")
    print(f"   Match: {master_poly_v == bigt_at_zeta}")

    if master_poly_v != bigt_at_zeta:
        print(f"   ✗ MISMATCH! master_poly_v ≠ bigt(ζ)")
        print(f"   → The constraint polynomials don't match the master polynomial!")

# RHS check
ZH_z = (pow(zeta, 4, p) - 1) % p
rhs = (t_zeta * ZH_z) % p

print(f"\n6. Quotient constraint:")
print(f"   LHS (master_poly): {master_poly_v}")
print(f"   RHS (t_zeta*ZH):   {rhs}")
print(f"   Match: {master_poly_v == rhs}")

if master_poly_v != rhs:
    diff = (master_poly_v - rhs) % p
    print(f"   Difference: {diff}")

    # Check if bigt/ZH == quotient_poly
    if 'bigt' in dir() and 'quotient_poly' in dir():
        print(f"\n7. Checking polynomial division:")
        bigt_at_zeta = bigt(zeta)
        quotient_at_zeta = quotient_poly(zeta)
        expected_rhs = (quotient_at_zeta * ZH_z) % p

        print(f"   bigt(ζ) = {bigt_at_zeta}")
        print(f"   quotient_poly(ζ) * ZH(ζ) = {expected_rhs}")
        print(f"   Should match: {bigt_at_zeta == expected_rhs}")

print("\n" + "=" * 70)
