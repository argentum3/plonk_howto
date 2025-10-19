#!/usr/bin/env python3
"""
Backup notebook and remove diagnostic Cell 102 (CHECKING BLINDING ISSUE)
"""

import json
import shutil
from datetime import datetime

notebook_path = '/Users/boy/projects/plonk/sageless/PlonK-Tutorial.ipynb'

print("=" * 70)
print("CLEANING UP NOTEBOOK - REMOVE DIAGNOSTIC CELL")
print("=" * 70)

# Create timestamped backup
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_path = f'{notebook_path}.backup_before_cleanup_{timestamp}'

print(f"\n1. Creating backup: {backup_path}")
shutil.copy2(notebook_path, backup_path)
print("   ✓ Backup created")

# Load notebook
with open(notebook_path, 'r') as f:
    nb = json.load(f)

print(f"\n2. Current notebook has {len(nb['cells'])} cells")

# Find Cell 102 with "CHECKING BLINDING ISSUE"
cell_to_remove = None
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'CHECKING BLINDING ISSUE' in source:
            cell_to_remove = i
            print(f"\n3. Found diagnostic cell at index {i}")
            print(f"   First few lines:")
            lines = source.split('\n')[:5]
            for line in lines:
                print(f"     {line}")
            break

if cell_to_remove is None:
    print("\n3. Diagnostic cell not found - may have already been removed")
    print("   Nothing to do.")
else:
    # Remove the cell
    print(f"\n4. Removing cell at index {cell_to_remove}")
    del nb['cells'][cell_to_remove]
    print(f"   ✓ Cell removed")
    print(f"   Notebook now has {len(nb['cells'])} cells")

    # Save updated notebook
    print(f"\n5. Saving updated notebook")
    with open(notebook_path, 'w') as f:
        json.dump(nb, f, indent=1)
    print("   ✓ Saved")

    print("\n" + "=" * 70)
    print("CLEANUP COMPLETE")
    print("=" * 70)
    print(f"\nRemoved diagnostic cell")
    print(f"Backup saved to: {backup_path}")
    print(f"\nNotebook now has {len(nb['cells'])} cells")
    print("\nYou can reload the notebook in Jupyter to see the changes.")

print("\n" + "=" * 70)
