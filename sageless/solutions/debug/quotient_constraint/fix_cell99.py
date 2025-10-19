#!/usr/bin/env python3
"""
Fix Cell 99: Proper modular arithmetic for master polynomial computation
"""

import json

notebook_path = '/Users/boy/projects/plonk/sageless/PlonK-Tutorial.ipynb'

print("=" * 70)
print("FIXING CELL 99: MODULAR ARITHMETIC")
print("=" * 70)

with open(notebook_path, 'r') as f:
    nb = json.load(f)

# Find Cell 99
cell99_idx = None
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'master_poly_v = (t_gates_v + alpha * t_perm_start_v' in source and 'Quotient constraint check' in source:
            cell99_idx = i
            print(f"\nFound Cell 99 at index {i}")
            break

if cell99_idx is None:
    print("ERROR: Could not find Cell 99")
    exit(1)

cell99 = nb['cells'][cell99_idx]
source99 = ''.join(cell99['source'])

print("\nCurrent master_poly_v computation:")
for line in source99.split('\n'):
    if 'master_poly_v' in line:
        print(f"  {line.strip()}")

# Fix the computation
old_line = "master_poly_v = (t_gates_v + alpha * t_perm_start_v + (alpha * alpha) % p * t_perm_step_v) % p"
new_lines = """# Compute master polynomial with proper modular arithmetic
alpha_squared = pow(alpha, 2, p)
term1 = t_gates_v
term2 = (alpha * t_perm_start_v) % p
term3 = (alpha_squared * t_perm_step_v) % p
master_poly_v = (term1 + term2 + term3) % p"""

if old_line in source99:
    source99 = source99.replace(old_line, new_lines)
    print("\n✓ Fixed master_poly_v computation")
else:
    print("\n⚠ Could not find exact line, trying pattern match...")
    # Try to find and replace the pattern
    lines = source99.split('\n')
    new_source_lines = []
    for i, line in enumerate(lines):
        if 'master_poly_v = ' in line and 'alpha * alpha' in line:
            # Replace this line with the new computation
            new_source_lines.append('# Compute master polynomial with proper modular arithmetic')
            new_source_lines.append('alpha_squared = pow(alpha, 2, p)')
            new_source_lines.append('term1 = t_gates_v')
            new_source_lines.append('term2 = (alpha * t_perm_start_v) % p')
            new_source_lines.append('term3 = (alpha_squared * t_perm_step_v) % p')
            new_source_lines.append('master_poly_v = (term1 + term2 + term3) % p')
            print(f"✓ Replaced line {i}")
        else:
            new_source_lines.append(line)
    source99 = '\n'.join(new_source_lines)

cell99['source'] = source99.split('\n')
cell99['source'] = [line + '\n' if i < len(cell99['source']) - 1 else line
                    for i, line in enumerate(cell99['source'])]

print("\n" + "=" * 70)
print("SAVING NOTEBOOK")
print("=" * 70)

backup = notebook_path + '.backup_cell99_fix'
print(f"\nCreating backup: {backup}")
with open(backup, 'w') as f:
    json.dump(nb, f, indent=1)

print(f"Saving updated notebook: {notebook_path}")
with open(notebook_path, 'w') as f:
    json.dump(nb, f, indent=1)

print("\n✓✓✓ FIX APPLIED ✓✓✓")
print("\nNext steps:")
print("  1. Reload notebook in Jupyter")
print("  2. Restart kernel")
print("  3. Run cells 91-100")
print("  4. Cell 99 should now show: Match: True")
