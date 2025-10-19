#!/usr/bin/env python3
"""
Fix Cell 94: Use z_poly_blind instead of z_poly in constraint polynomials

Cell 94 is using z_poly (unblinded) when it should use z_poly_blind!
This causes bigt to be computed incorrectly.
"""

import json

notebook_path = '/Users/boy/projects/plonk/sageless/PlonK-Tutorial.ipynb'

print("=" * 70)
print("FIXING CELL 94: USE z_poly_blind IN CONSTRAINTS")
print("=" * 70)

with open(notebook_path, 'r') as f:
    nb = json.load(f)

# Find Cell 94
cell94_idx = None
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'bigt = t_gates + alpha * t_perm_start' in source and 'quotient_poly, remainder = bigt.quo_rem(ZH)' in source:
            cell94_idx = i
            print(f"\nFound Cell 94 at index {i}")
            break

if cell94_idx is None:
    print("ERROR: Could not find Cell 94")
    exit(1)

cell94 = nb['cells'][cell94_idx]
source94 = ''.join(cell94['source'])

print("\nCurrent t_perm_start and t_perm_step:")
for line in source94.split('\n'):
    if 't_perm_start = ' in line or 't_perm_step = ' in line or 'z_shifted = ' in line:
        print(f"  {line.strip()}")

# Make the replacements
replacements = [
    ('t_perm_start = (z_poly - 1) * L1', 't_perm_start = (z_poly_blind - 1) * L1'),
    ('z_shifted = z_poly(x * ω)', 'z_shifted = z_poly_blind(x * ω)'),
    ('t_perm_step = z_poly * N_poly - D_poly * z_shifted', 't_perm_step = z_poly_blind * N_poly - D_poly * z_shifted'),
]

changes = 0
for old, new in replacements:
    if old in source94:
        source94 = source94.replace(old, new)
        changes += 1
        print(f"\n✓ Changed: {old}")
        print(f"      To: {new}")

if changes == 0:
    print("\n⚠ No changes made - patterns not found")
    print("\nTrying alternative patterns...")

    # Alternative: look for the lines and replace them
    lines = source94.split('\n')
    new_lines = []
    for line in lines:
        if line.strip() == 't_perm_start = (z_poly - 1) * L1':
            new_lines.append(line.replace('z_poly', 'z_poly_blind'))
            changes += 1
        elif line.strip() == 'z_shifted = z_poly(x * ω)' or 'z_shifted = z_poly(x * ω)' in line:
            new_lines.append(line.replace('z_poly(', 'z_poly_blind('))
            changes += 1
        elif 't_perm_step = z_poly * N_poly' in line:
            new_lines.append(line.replace('z_poly *', 'z_poly_blind *'))
            changes += 1
        else:
            new_lines.append(line)

    if changes > 0:
        source94 = '\n'.join(new_lines)
        print(f"✓ Made {changes} changes with alternative method")

cell94['source'] = source94.split('\n')
cell94['source'] = [line + '\n' if i < len(cell94['source']) - 1 else line
                    for i, line in enumerate(cell94['source'])]

print("\n" + "=" * 70)
print("SAVING NOTEBOOK")
print("=" * 70)

backup = notebook_path + '.backup_cell94_z_poly_fix'
print(f"\nCreating backup: {backup}")
with open(backup, 'w') as f:
    json.dump(nb, f, indent=1)

print(f"Saving updated notebook: {notebook_path}")
with open(notebook_path, 'w') as f:
    json.dump(nb, f, indent=1)

print("\n✓✓✓ FIX APPLIED ✓✓✓")
print(f"\nMade {changes} changes to use z_poly_blind in Cell 94")
print("\nNext steps:")
print("  1. Reload notebook in Jupyter")
print("  2. Restart kernel")
print("  3. Run cells 91-100")
print("  4. Cell 99: master_poly should match bigt(ζ)")
print("  5. Cell 100: All checks should pass")
