#!/usr/bin/env python3
"""
Check what's currently in the notebook's memory
Run this from a notebook cell with: %run sageless/solutions/debug/quotient_constraint/check_current_state.py
"""

print("=" * 70)
print("CHECKING CURRENT NOTEBOOK STATE")
print("=" * 70)

print("\n1. Checking if quotient_poly_blind exists:")
try:
    degree = quotient_poly_blind.degree()
    print(f"   ✗ quotient_poly_blind EXISTS with degree {degree}")
    print(f"   → This is the problem! You have the OLD version in memory")
    has_blind = True
except NameError:
    print(f"   ✓ quotient_poly_blind does not exist (good!)")
    has_blind = False

print("\n2. Checking if quotient_poly exists:")
try:
    degree = quotient_poly.degree()
    print(f"   ✓ quotient_poly EXISTS with degree {degree}")
    has_unblind = True
except NameError:
    print(f"   ✗ quotient_poly does not exist")
    has_unblind = False

print("\n3. Checking t_zeta value:")
try:
    print(f"   t_zeta = {t_zeta}")

    if has_blind and has_unblind:
        t_from_blind = quotient_poly_blind(zeta)
        t_from_unblind = quotient_poly(zeta)
        print(f"   quotient_poly_blind(ζ) = {t_from_blind}")
        print(f"   quotient_poly(ζ)       = {t_from_unblind}")

        if t_zeta == t_from_blind:
            print(f"   ✗ t_zeta matches quotient_poly_blind (OLD)")
        elif t_zeta == t_from_unblind:
            print(f"   ✓ t_zeta matches quotient_poly (NEW)")
        else:
            print(f"   ? t_zeta doesn't match either")
except NameError as e:
    print(f"   ✗ Error: {e}")

print("\n4. Checking c_t commitment:")
try:
    print(f"   c_t = {c_t}")

    if has_blind and has_unblind:
        import kzg as kzg_module
        c_from_blind = kzg.commit(quotient_poly_blind)
        c_from_unblind = kzg.commit(quotient_poly)

        if c_t == c_from_blind:
            print(f"   ✗ c_t matches commit(quotient_poly_blind) (OLD)")
        elif c_t == c_from_unblind:
            print(f"   ✓ c_t matches commit(quotient_poly) (NEW)")
        else:
            print(f"   ? c_t doesn't match either")
except NameError as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 70)
print("DIAGNOSIS")
print("=" * 70)

if has_blind:
    print("""
✗ PROBLEM: quotient_poly_blind still exists in memory!

This means you're running the OLD code from before the fix.

SOLUTION:
1. Close and halt the notebook
2. Reopen PlonK-Tutorial.ipynb
3. Restart kernel
4. Run cells 91-100 in order

The notebook FILE was updated, but Jupyter still has the old code in memory.
You need to reload the notebook to see the changes.
""")
else:
    print("""
✓ GOOD: quotient_poly_blind does not exist

This means you're running the NEW code after the fix.

If Cell 99 still fails, there might be another issue.
Please share the exact error message from Cell 99.
""")

print("=" * 70)
