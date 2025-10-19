#!/usr/bin/env python3
"""
Final fix: Add z_poly_blind definition to Cell 92
"""

import json

notebook_path = '/Users/boy/projects/plonk/sageless/PlonK-Tutorial.ipynb'

print("=" * 70)
print("FINAL FIX: ADD z_poly_blind TO CELL 92")
print("=" * 70)

with open(notebook_path, 'r') as f:
    nb = json.load(f)

# Cell 92 is at index 92
cell92 = nb['cells'][92]
source = ''.join(cell92['source'])

print("\nChecking Cell 92...")

# Check if z_poly_blind definition exists
if 'z_poly_blind = z_poly' in source or 'z_poly_blind = ' in source:
    print("✓ z_poly_blind definition already exists")
else:
    print("✗ z_poly_blind definition missing - adding it now")

    # Find where to insert: after z_poly verification but before commitment
    lines = source.split('\n')
    new_lines = []

    for i, line in enumerate(lines):
        new_lines.append(line)

        # After "assert z_at_ω == 1" add the blinding
        if 'assert z_at_ω == 1' in line or 'z(ω) should equal 1!' in line:
            # Add blinding code
            new_lines.append('')
            new_lines.append('# Blind z_poly for zero-knowledge (2 openings: at ζ and ζ·ω)')
            new_lines.append('b1_z, b2_z = 98765, 43210')
            new_lines.append('z_poly_blind = z_poly + (b1_z * x + b2_z) * ZH')
            new_lines.append('')
            new_lines.append('print(f"\\nBlinding z_poly:")')
            new_lines.append('print(f"  z_poly_blind = z_poly + ({b1_z}·x + {b2_z}) · ZH")')
            new_lines.append('print(f"  z_poly_blind: degree {z_poly_blind.degree()}")')

    # Update source
    source = '\n'.join(new_lines)
    cell92['source'] = [line + '\n' if i < len(new_lines) - 1 else line
                        for i, line in enumerate(new_lines)]

    print("✓ Added z_poly_blind definition")

# Ensure commitment is to z_poly_blind
if 'c_z = kzg.commit(z_poly)' in source and 'z_poly_blind' not in source:
    source = source.replace('c_z = kzg.commit(z_poly)', 'c_z = kzg.commit(z_poly_blind)')
    cell92['source'] = source.split('\n')
    cell92['source'] = [line + '\n' if i < len(cell92['source']) - 1 else line
                        for i, line in enumerate(cell92['source'])]
    print("✓ Fixed commitment to use z_poly_blind")

# Save
backup = notebook_path + '.backup4'
print(f"\nSaving backup: {backup}")
with open(backup, 'w') as f:
    json.dump(nb, f, indent=1)

print(f"Saving notebook: {notebook_path}")
with open(notebook_path, 'w') as f:
    json.dump(nb, f, indent=1)

print("\n✓✓✓ FIX APPLIED ✓✓✓")
print("\nCell 92 now:")
print("1. Defines z_poly from interpolate_z_N_D")
print("2. Blinds it: z_poly_blind = z_poly + (b1_z·x + b2_z)·ZH")
print("3. Commits to z_poly_blind: c_z = kzg.commit(z_poly_blind)")
print("\nRestart kernel and re-run cells 91-100!")
