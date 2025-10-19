#!/usr/bin/env python3
"""
Fix ZH_z modular arithmetic in verify_plonk (Cell 103)

Changes line 4645 from:
    ZH_z = zeta_v**n - 1

To:
    ZH_z = (pow(zeta_v, n, p) - 1) % p
"""

import json
import sys
from pathlib import Path

# Paths
notebook_path = Path("/Users/boy/projects/plonk/sageless/PlonK-Tutorial.ipynb")
backup_path = notebook_path.parent / f"{notebook_path.name}.backup_ZH_z_fix"

print("=" * 70)
print("FIXING ZH_z: MODULAR ARITHMETIC")
print("=" * 70)
print()

# Load notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find verify_plonk cell (should be 103)
cell_idx = None
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'def verify_plonk' in source and 'ZH_z = zeta_v**n - 1' in source:
            cell_idx = i
            break

if cell_idx is None:
    print("ERROR: Could not find verify_plonk cell with ZH_z line")
    sys.exit(1)

print(f"Found verify_plonk cell at index {cell_idx}")
print()

# Get current source
source_lines = nb['cells'][cell_idx]['source']
source_text = ''.join(source_lines)

# Show current problematic line
print("Current problematic line:")
for line in source_lines:
    if 'ZH_z = zeta_v**n - 1' in line:
        print(f"  {line.rstrip()}")
print()

# Fix: Replace the line
OLD_LINE = "    ZH_z = zeta_v**n - 1\n"
NEW_LINE = "    ZH_z = (pow(zeta_v, n, p) - 1) % p\n"

if OLD_LINE in source_text:
    source_text = source_text.replace(OLD_LINE, NEW_LINE)
    print(f"✓ Fixed: ZH_z = zeta_v**n - 1")
    print(f"  Changed to: ZH_z = (pow(zeta_v, n, p) - 1) % p")
    print()
else:
    print("ERROR: Could not find exact line to replace")
    print("Expected:")
    print(f"  '{OLD_LINE}'")
    sys.exit(1)

# Update cell
nb['cells'][cell_idx]['source'] = source_text.splitlines(keepends=True)

# Save
print("=" * 70)
print("SAVING NOTEBOOK")
print("=" * 70)
print()

print(f"Creating backup: {backup_path}")
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print(f"Saving updated notebook: {notebook_path}")
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print()
print("✓✓✓ FIX APPLIED ✓✓✓")
print()
print("Fixed ZH_z modular arithmetic in verify_plonk")
print()
print("Changed line 4645:")
print(f"  FROM: ZH_z = zeta_v**n - 1")
print(f"  TO:   ZH_z = (pow(zeta_v, n, p) - 1) % p")
print()
print("Next steps:")
print("  1. Reload notebook in Jupyter")
print("  2. Restart kernel")
print("  3. Run cells 91-103")
print("  4. verify_plonk should now pass!")
