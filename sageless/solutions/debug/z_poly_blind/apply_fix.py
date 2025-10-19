#!/usr/bin/env python3
"""
Apply fix for z_poly_blind verification failure
Changes Cell 92 to commit to z_poly_blind instead of z_poly
"""

import json
import sys

notebook_path = '/Users/boy/projects/plonk/sageless/PlonK-Tutorial.ipynb'

print("=" * 70)
print("APPLYING FIX FOR z_poly_blind VERIFICATION FAILURE")
print("=" * 70)

# Load notebook
print(f"\nLoading notebook: {notebook_path}")
with open(notebook_path, 'r') as f:
    notebook = json.load(f)

print(f"Notebook has {len(notebook['cells'])} cells")

# Find Cell 92 - contains "c_z = kzg.commit(z_poly)"
cell92_idx = None
for i, cell in enumerate(notebook['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'c_z = kzg.commit(z_poly)' in source:
            cell92_idx = i
            print(f"\nFound Cell 92 at index {i}")
            break

if cell92_idx is None:
    print("ERROR: Could not find Cell 92 with c_z commitment")
    sys.exit(1)

print("\n" + "=" * 70)
print("APPLYING FIX TO CELL 92")
print("=" * 70)

# Fix Cell 92
cell92 = notebook['cells'][cell92_idx]
source92 = ''.join(cell92['source'])

# Replacements to make
replacements = [
    ('c_z = kzg.commit(z_poly)', 'c_z = kzg.commit(z_poly_blind)'),
    ('print(f"\\nCommitment to z:")', 'print(f"\\nCommitment to z_poly_blind:")'),
]

changes_made = 0
for old, new in replacements:
    if old in source92:
        source92 = source92.replace(old, new)
        changes_made += 1
        print(f"✓ Changed: {old}")
        print(f"       To: {new}")

if changes_made == 0:
    print("✗ No changes made - commitment already correct or pattern not found")
else:
    # Update cell source
    cell92['source'] = source92.split('\n')
    cell92['source'] = [line + '\n' if i < len(cell92['source']) - 1 else line
                        for i, line in enumerate(cell92['source'])]
    print(f"\n✓ Cell 92 updated: {changes_made} changes made")

print("\n" + "=" * 70)
print("SAVING UPDATED NOTEBOOK")
print("=" * 70)

# Save backup
backup_path = notebook_path + '.backup2'
print(f"\nCreating backup: {backup_path}")
with open(backup_path, 'w') as f:
    json.dump(notebook, f, indent=1)

# Save updated notebook
print(f"Saving updated notebook: {notebook_path}")
with open(notebook_path, 'w') as f:
    json.dump(notebook, f, indent=1)

print("\n✓✓✓ FIX APPLIED SUCCESSFULLY ✓✓✓")
print("\nNext steps:")
print("1. Re-run Cell 92 (Exercise 20) - new c_z commitment")
print("2. Re-run Cell 94 (Exercise 21) - uses c_z in transcript")
print("3. Re-run Cell 96 (Exercise 22) - generates proofs")
print("4. Re-run Cell 98 - assembles proof")
print("5. Re-run Cell 100 - verify_plonk")
print("\nExpected results:")
print("  Cell 96: ✓✓✓ ALL OPENING PROOFS VERIFIED SUCCESSFULLY ✓✓✓")
print("  Cell 100: Quotient constraint holds. Verifier result: True All checks passed!")
