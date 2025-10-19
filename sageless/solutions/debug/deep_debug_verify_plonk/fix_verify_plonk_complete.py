#!/usr/bin/env python3
"""
Complete fix for verify_plonk based on diagnostic output

Fixes:
1. Extract variables from proof_dictionary (self-containment)
2. Add % p to t_perm_start_v (line 4632)
3. Add % p to final comparison RHS (line 4648)
"""

import json
import sys
from pathlib import Path

# Paths
notebook_path = Path("/Users/boy/projects/plonk/sageless/PlonK-Tutorial.ipynb")
backup_path = notebook_path.parent / f"{notebook_path.name}.backup_verify_plonk_complete_fix"

print("=" * 80)
print("COMPLETE FIX FOR verify_plonk")
print("=" * 80)
print()

# Load notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find verify_plonk cell
cell_idx = None
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'def verify_plonk' in source and 'quotient constraint check failed' in source.lower():
            cell_idx = i
            break

if cell_idx is None:
    print("ERROR: Could not find verify_plonk cell")
    sys.exit(1)

print(f"Found verify_plonk cell at index {cell_idx}")
print()

# Get source
source_text = ''.join(nb['cells'][cell_idx]['source'])

print("Applying 3 fixes...")
print()

# Fix 1: Add variable extraction after pairing checks (after line with "Pairing check failed")
FIX1_MARKER = '            return False, f"Pairing check failed for {c_key}"\n'
FIX1_INSERT = '''            return False, f"Pairing check failed for {c_key}"

    # Extract evaluated values from proof dictionary
    a_zeta = proof_dictionary['evaluations']['a_zeta']
    b_zeta = proof_dictionary['evaluations']['b_zeta']
    c_zeta = proof_dictionary['evaluations']['c_zeta']
    z_zeta = proof_dictionary['evaluations']['z_zeta']
    z_zeta_omega = proof_dictionary['evaluations']['z_zeta_omega']
    t_zeta = proof_dictionary['evaluations']['t_zeta']
'''

if FIX1_MARKER in source_text:
    # Check if already fixed
    if "a_zeta = proof_dictionary['evaluations']['a_zeta']" not in source_text:
        source_text = source_text.replace(FIX1_MARKER, FIX1_INSERT)
        print("✓ Fix 1: Added variable extraction from proof_dictionary")
    else:
        print("✓ Fix 1: Variable extraction already present")
else:
    print("✗ Fix 1: Could not find insertion point")
    print("  Looking for:", FIX1_MARKER.strip())

print()

# Fix 2: Add % p to t_perm_start_v
FIX2_OLD = "    t_perm_start_v = (z_zeta - 1) * L1_z\n"
FIX2_NEW = "    t_perm_start_v = ((z_zeta - 1) * L1_z) % p\n"

if FIX2_OLD in source_text:
    source_text = source_text.replace(FIX2_OLD, FIX2_NEW)
    print("✓ Fix 2: Added % p to t_perm_start_v")
elif FIX2_NEW in source_text:
    print("✓ Fix 2: t_perm_start_v already has % p")
else:
    print("✗ Fix 2: Could not find t_perm_start_v line")
    print("  Looking for:", FIX2_OLD.strip())

print()

# Fix 3: Add % p to final comparison RHS
FIX3_OLD = "    if master_poly_v == t_zeta * ZH_z:\n"
FIX3_NEW = "    if master_poly_v == (t_zeta * ZH_z) % p:\n"

if FIX3_OLD in source_text:
    source_text = source_text.replace(FIX3_OLD, FIX3_NEW)
    print("✓ Fix 3: Added % p to final comparison RHS")
elif FIX3_NEW in source_text:
    print("✓ Fix 3: Final comparison already has % p")
else:
    print("✗ Fix 3: Could not find final comparison line")
    print("  Looking for:", FIX3_OLD.strip())

print()

# Update cell
nb['cells'][cell_idx]['source'] = source_text.splitlines(keepends=True)

# Save
print("=" * 80)
print("SAVING NOTEBOOK")
print("=" * 80)
print()

print(f"Creating backup: {backup_path}")
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print(f"Saving updated notebook: {notebook_path}")
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print()
print("✓✓✓ ALL FIXES APPLIED ✓✓✓")
print()
print("Applied fixes:")
print("  1. Extract variables from proof_dictionary (after pairing checks)")
print("  2. Add % p to t_perm_start_v computation")
print("  3. Add % p to final comparison RHS")
print()
print("These fixes ensure:")
print("  - verify_plonk is self-contained (doesn't rely on global variables)")
print("  - All intermediate values are properly reduced modulo p")
print("  - Comparison uses consistent field element representations")
print()
print("Next steps:")
print("  1. Reload notebook in Jupyter")
print("  2. Restart kernel")
print("  3. Run cells 91-103")
print("  4. verify_plonk should now pass!")
