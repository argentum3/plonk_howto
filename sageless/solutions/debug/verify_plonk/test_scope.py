#!/usr/bin/env python3
"""
Test if N_poly and D_poly are accessible to verify_plonk
"""

print("=" * 70)
print("TESTING N_poly AND D_poly SCOPE")
print("=" * 70)

# This script simulates what happens when verify_plonk runs
# in the notebook environment

print("\nScenario 1: N_poly and D_poly NOT defined")
print("-" * 70)
try:
    N_z = N_poly(12345)  # This will fail if not defined
    print(f"✓ N_poly is accessible: N_poly(12345) = {N_z}")
except NameError as e:
    print(f"✗ NameError: {e}")
    print("  → This means N_poly is not in scope!")

try:
    D_z = D_poly(12345)  # This will fail if not defined
    print(f"✓ D_poly is accessible: D_poly(12345) = {D_z}")
except NameError as e:
    print(f"✗ NameError: {e}")
    print("  → This means D_poly is not in scope!")

print("\n" + "=" * 70)
print("DIAGNOSIS")
print("=" * 70)
print("""
If you see NameError above, it means verify_plonk is trying to access
N_poly and D_poly but they're not defined in the current scope.

This happens if:
1. Cell 92 (Exercise 20) wasn't run before cell 100
2. The kernel was restarted and cells weren't re-run
3. Cells were run out of order

SOLUTION:
Run these cells in order:
  - Cell 91-92 (Exercise 20) - defines N_poly, D_poly
  - Cell 93-94 (Exercise 21) - builds master polynomial
  - Cell 95-96 (Exercise 22) - generates opening proofs
  - Cell 98 - assembles proof dictionary
  - Cell 100 - verify_plonk (uses N_poly, D_poly from cell 92)
""")
