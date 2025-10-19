#!/usr/bin/env python3
"""
Verify that Cell 92 now has z_poly_blind definition
"""

import json

notebook_path = '/Users/boy/projects/plonk/sageless/PlonK-Tutorial.ipynb'

print("=" * 70)
print("VERIFYING z_poly_blind FIX IN CELL 92")
print("=" * 70)

with open(notebook_path, 'r') as f:
    nb = json.load(f)

cell92 = nb['cells'][92]
source = ''.join(cell92['source'])

print("\nChecking Cell 92 (Exercise 20)...")
print()

# Check 1: z_poly definition
has_z_poly = 'z_poly, N_poly, D_poly = interpolate_z_N_D' in source
print(f"1. Defines z_poly from interpolate_z_N_D: {'✓' if has_z_poly else '✗'}")

# Check 2: z_poly_blind definition
has_blind_def = 'z_poly_blind = z_poly' in source or 'z_poly_blind =' in source
print(f"2. Defines z_poly_blind: {'✓' if has_blind_def else '✗'}")

# Check 3: Uses blinding factors
has_blinding = 'b1_z' in source and 'b2_z' in source
print(f"3. Uses blinding factors (b1_z, b2_z): {'✓' if has_blinding else '✗'}")

# Check 4: Commits to z_poly_blind
commits_to_blind = 'c_z = kzg.commit(z_poly_blind)' in source
commits_to_unblind = 'c_z = kzg.commit(z_poly)' in source and not commits_to_blind
print(f"4. Commits to z_poly_blind: {'✓' if commits_to_blind else '✗'}")

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print()

all_checks = has_z_poly and has_blind_def and has_blinding and commits_to_blind

if all_checks:
    print("✓✓✓ ALL CHECKS PASSED ✓✓✓")
    print()
    print("Cell 92 (Exercise 20) is now complete:")
    print("  1. Computes z_poly from witnesses")
    print("  2. Blinds it to create z_poly_blind")
    print("  3. Commits to z_poly_blind")
    print()
    print("Next steps:")
    print("  1. Restart kernel")
    print("  2. Run cells 91-100")
    print("  3. All verifications should pass!")
else:
    print("✗✗✗ SOME CHECKS FAILED ✗✗✗")
    print()
    if not has_z_poly:
        print("  - Missing z_poly definition")
    if not has_blind_def:
        print("  - Missing z_poly_blind definition")
    if not has_blinding:
        print("  - Missing blinding factors")
    if not commits_to_blind:
        print("  - Commits to wrong polynomial (should be z_poly_blind)")
    print()
    print("Run fix_cell92_final.py to apply the fix")

print()
print("=" * 70)

# Show relevant lines
if has_blind_def:
    print("z_poly_blind definition in Cell 92:")
    print()
    for line in source.split('\n'):
        if 'z_poly_blind' in line or 'b1_z' in line or 'b2_z' in line:
            print(f"  {line}")
    print()
    print("=" * 70)
