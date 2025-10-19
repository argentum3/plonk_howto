#!/usr/bin/env python3
"""
Fix verify_plonk function: Add proper modular arithmetic
"""

import json

notebook_path = '/Users/boy/projects/plonk/sageless/PlonK-Tutorial.ipynb'

print("=" * 70)
print("FIXING verify_plonk: MODULAR ARITHMETIC")
print("=" * 70)

with open(notebook_path, 'r') as f:
    nb = json.load(f)

# Find Cell with verify_plonk function
cell_idx = None
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'def verify_plonk(proof_dictionary):' in source:
            cell_idx = i
            print(f"\nFound verify_plonk cell at index {i}")
            break

if cell_idx is None:
    print("ERROR: Could not find verify_plonk cell")
    exit(1)

cell = nb['cells'][cell_idx]
source = ''.join(cell['source'])

print("\nCurrent problematic lines:")
for line in source.split('\n'):
    if 't_gates_v =' in line and 'qM_z' in line:
        print(f"  {line.strip()}")
    elif 't_perm_step_v =' in line and 'z_zeta' in line:
        print(f"  {line.strip()}")
    elif 'master_poly_v = t_gates_v + alpha_v' in line:
        print(f"  {line.strip()}")

# Apply fixes
replacements = [
    # Fix t_gates_v
    (
        '    t_gates_v = qM_z*a_zeta*b_zeta + qL_z*a_zeta+qR_z*b_zeta-c_zeta',
        '    t_gates_v = (qM_z*a_zeta*b_zeta + qL_z*a_zeta+qR_z*b_zeta-c_zeta) % p'
    ),
    # Fix t_perm_step_v
    (
        '    t_perm_step_v = z_zeta * N_z - D_z * z_zeta_omega',
        '    t_perm_step_v = (z_zeta * N_z - D_z * z_zeta_omega) % p'
    ),
    # Fix master_poly_v - use multi-line approach for clarity
    (
        '    master_poly_v = t_gates_v + alpha_v * t_perm_start_v + alpha_v**2 * t_perm_step_v',
        '''    # Compute master polynomial with proper modular arithmetic
    alpha_v_squared = pow(alpha_v, 2, p)
    term1 = t_gates_v
    term2 = (alpha_v * t_perm_start_v) % p
    term3 = (alpha_v_squared * t_perm_step_v) % p
    master_poly_v = (term1 + term2 + term3) % p'''
    ),
]

changes = 0
for old, new in replacements:
    if old in source:
        source = source.replace(old, new)
        changes += 1
        print(f"\n✓ Fixed: {old.strip()}")

if changes != len(replacements):
    print(f"\n⚠ Only {changes}/{len(replacements)} changes applied")
    print("Some patterns may not have matched exactly")

cell['source'] = source.split('\n')
cell['source'] = [line + '\n' if i < len(cell['source']) - 1 else line
                  for i, line in enumerate(cell['source'])]

print("\n" + "=" * 70)
print("SAVING NOTEBOOK")
print("=" * 70)

backup = notebook_path + '.backup_verify_plonk_modulo_fix'
print(f"\nCreating backup: {backup}")
with open(backup, 'w') as f:
    json.dump(nb, f, indent=1)

print(f"Saving updated notebook: {notebook_path}")
with open(notebook_path, 'w') as f:
    json.dump(nb, f, indent=1)

print("\n✓✓✓ FIX APPLIED ✓✓✓")
print(f"\nMade {changes} modular arithmetic fixes to verify_plonk")
print("\nFixed lines:")
print("  1. t_gates_v - added % p")
print("  2. t_perm_step_v - added % p")
print("  3. master_poly_v - proper step-by-step modular arithmetic")
print("\nNext steps:")
print("  1. Reload notebook in Jupyter")
print("  2. Restart kernel")
print("  3. Run cells 91-103")
print("  4. verify_plonk should now pass!")
