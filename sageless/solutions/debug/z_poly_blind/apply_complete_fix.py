#!/usr/bin/env python3
"""
Apply complete fix for z_poly_blind issue
1. Add z_poly_blind definition in Cell 92
2. Ensure c_z commits to z_poly_blind
"""

import json
import sys

notebook_path = '/Users/boy/projects/plonk/sageless/PlonK-Tutorial.ipynb'

print("=" * 70)
print("APPLYING COMPLETE FIX FOR z_poly_blind")
print("=" * 70)

# Load notebook
print(f"\nLoading notebook: {notebook_path}")
with open(notebook_path, 'r') as f:
    notebook = json.load(f)

print(f"Notebook has {len(notebook['cells'])} cells")

# Find Cell 92 - Exercise 20 with z_poly, N_poly, D_poly = interpolate_z_N_D
cell92_idx = None
for i, cell in enumerate(notebook['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'z_poly, N_poly, D_poly = interpolate_z_N_D(a_blind, b_blind, c_blind, beta, gamma, Ω)' in source:
            cell92_idx = i
            print(f"\nFound Cell 92 (Exercise 20) at index {i}")
            break

if cell92_idx is None:
    print("ERROR: Could not find Cell 92 with interpolate_z_N_D")
    sys.exit(1)

print("\n" + "=" * 70)
print("CHECKING IF z_poly_blind IS DEFINED IN CELL 92")
print("=" * 70)

cell92 = notebook['cells'][cell92_idx]
source92 = ''.join(cell92['source'])

if 'z_poly_blind = ' in source92:
    print("✓ z_poly_blind is already defined in Cell 92")
    needs_blinding = False
else:
    print("✗ z_poly_blind is NOT defined in Cell 92 - needs to be added")
    needs_blinding = True

print("\n" + "=" * 70)
print("APPLYING FIX TO CELL 92")
print("=" * 70)

if needs_blinding:
    print("\nAdding z_poly_blind definition...")

    # Find the line after interpolate_z_N_D
    lines = source92.split('\n')
    new_lines = []

    for i, line in enumerate(lines):
        new_lines.append(line)

        # After the interpolate_z_N_D line, add blinding
        if 'z_poly, N_poly, D_poly = interpolate_z_N_D(a_blind, b_blind, c_blind, beta, gamma, Ω)' in line:
            # Check if next lines already have z_poly_blind
            has_blinding_next = False
            if i + 1 < len(lines) and 'z_poly_blind' in lines[i + 1]:
                has_blinding_next = True

            if not has_blinding_next:
                print(f"  Found interpolate_z_N_D at line {i}")
                print(f"  Adding z_poly_blind definition after it")

                # Add blank line if needed
                if i + 1 < len(lines) and lines[i + 1].strip():
                    new_lines.append('')

                # Add blinding code
                new_lines.append('# Blind z_poly for zero-knowledge (at most 2 openings)')
                new_lines.append('b1_z, b2_z = 98765, 43210')
                new_lines.append('z_poly_blind = z_poly + (b1_z * x + b2_z) * ZH')
                new_lines.append('')
                new_lines.append('print(f"\\nBlinding z_poly:")')
                new_lines.append('print(f"  z_poly_blind = z_poly + ({b1_z}·x + {b2_z}) · ZH")')
                new_lines.append('print(f"  z_poly_blind: degree {z_poly_blind.degree()}")')

    source92 = '\n'.join(new_lines)
    print("✓ Added z_poly_blind definition")

# Ensure c_z commits to z_poly_blind (not z_poly)
if 'c_z = kzg.commit(z_poly)' in source92 and 'c_z = kzg.commit(z_poly_blind)' not in source92:
    print("\nFixing c_z commitment...")
    source92 = source92.replace('c_z = kzg.commit(z_poly)', 'c_z = kzg.commit(z_poly_blind)')
    source92 = source92.replace('print(f"\\nCommitment to z:")', 'print(f"\\nCommitment to z_poly_blind:")')
    print("✓ Changed c_z to commit to z_poly_blind")
elif 'c_z = kzg.commit(z_poly_blind)' in source92:
    print("✓ c_z already commits to z_poly_blind")

# Update cell source
cell92['source'] = source92.split('\n')
cell92['source'] = [line + '\n' if i < len(cell92['source']) - 1 else line
                    for i, line in enumerate(cell92['source'])]

print("\n" + "=" * 70)
print("SAVING UPDATED NOTEBOOK")
print("=" * 70)

# Save backup
backup_path = notebook_path + '.backup3'
print(f"\nCreating backup: {backup_path}")
with open(backup_path, 'w') as f:
    json.dump(notebook, f, indent=1)

# Save updated notebook
print(f"Saving updated notebook: {notebook_path}")
with open(notebook_path, 'w') as f:
    json.dump(notebook, f, indent=1)

print("\n✓✓✓ COMPLETE FIX APPLIED SUCCESSFULLY ✓✓✓")
print("\nChanges made to Cell 92:")
print("1. Added z_poly_blind definition with blinding factors")
print("2. Ensured c_z commits to z_poly_blind")
print("\nNext steps:")
print("1. Restart kernel (to clear old z_poly_blind from tutorial)")
print("2. Run cells 91-100 in order")
print("3. Verify all proofs pass in Cell 96")
print("4. Verify quotient constraint passes in Cell 100")
