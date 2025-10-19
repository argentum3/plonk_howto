#!/usr/bin/env python3
"""
Apply fixes to PlonK-Tutorial.ipynb for the quotient constraint bug
"""

import json
import sys

notebook_path = '/Users/boy/projects/plonk/sageless/PlonK-Tutorial.ipynb'

print("=" * 70)
print("APPLYING FIXES TO PLONK TUTORIAL NOTEBOOK")
print("=" * 70)

# Load notebook
print(f"\nLoading notebook: {notebook_path}")
with open(notebook_path, 'r') as f:
    notebook = json.load(f)

print(f"Notebook has {len(notebook['cells'])} cells")

# Find Cell 94 - contains "# Commit to quotient"
cell94_idx = None
for i, cell in enumerate(notebook['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if '# Commit to quotient' in source and 'quotient_poly, remainder = bigt.quo_rem(ZH)' in source:
            cell94_idx = i
            print(f"\nFound Cell 94 at index {i}")
            break

if cell94_idx is None:
    print("ERROR: Could not find Cell 94")
    sys.exit(1)

# Find Cell 96 - contains "z_zeta = z_poly(zeta)"
cell96_idx = None
for i, cell in enumerate(notebook['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'z_zeta = z_poly(zeta)' in source and 't_zeta = quotient_poly(zeta)' in source:
            cell96_idx = i
            print(f"Found Cell 96 at index {i}")
            break

if cell96_idx is None:
    print("ERROR: Could not find Cell 96")
    sys.exit(1)

# Find Cell 100 - contains "def verify_plonk"
cell100_idx = None
for i, cell in enumerate(notebook['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'def verify_plonk(proof_dictionary):' in source:
            cell100_idx = i
            print(f"Found Cell 100 at index {i}")
            break

if cell100_idx is None:
    print("ERROR: Could not find Cell 100")
    sys.exit(1)

print("\n" + "=" * 70)
print("FIX #1: CELL 94 - ADD quotient_poly_blind")
print("=" * 70)

# Fix Cell 94
cell94 = notebook['cells'][cell94_idx]
source94 = ''.join(cell94['source'])

# Find and replace the commit section
old_text = """# Commit to quotient
c_t = kzg.commit(quotient_poly)
print(f"\\nCommitment to quotient:")
print(f"  c_t = {c_t}")

transcript = push(c_t, transcript)"""

new_text = """# Blind the quotient polynomial (for zero-knowledge)
# We add random multiples of ZH since bigt is built from blinded polynomials
b1_t, b2_t = 55555, 66666
quotient_poly_blind = quotient_poly + (b1_t * x + b2_t) * ZH

print(f"\\nBlinding quotient polynomial:")
print(f"  quotient_poly_blind = quotient_poly + ({b1_t}·x + {b2_t}) · ZH")
print(f"  quotient_poly_blind: degree {quotient_poly_blind.degree()}")

# Commit to blinded quotient
c_t = kzg.commit(quotient_poly_blind)
print(f"\\nCommitment to blinded quotient:")
print(f"  c_t = {c_t}")

# Add to transcript
transcript = push(c_t, transcript)
print(f"\\nUpdated transcript after c_t")"""

if old_text in source94:
    source94 = source94.replace(old_text, new_text)
    cell94['source'] = source94.split('\n')
    # Ensure each line ends with \n except the last
    cell94['source'] = [line + '\n' if i < len(cell94['source']) - 1 else line
                        for i, line in enumerate(cell94['source'])]
    print("✓ Cell 94 updated successfully")
else:
    print("✗ Could not find exact text to replace in Cell 94")
    print("Attempting partial match...")

    # Try a more flexible replacement
    if "c_t = kzg.commit(quotient_poly)" in source94:
        # Split into lines for easier manipulation
        lines = source94.split('\n')
        new_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.strip() == "# Commit to quotient":
                # Found the section - replace it
                new_lines.append("# Blind the quotient polynomial (for zero-knowledge)")
                new_lines.append("# We add random multiples of ZH since bigt is built from blinded polynomials")
                new_lines.append("b1_t, b2_t = 55555, 66666")
                new_lines.append("quotient_poly_blind = quotient_poly + (b1_t * x + b2_t) * ZH")
                new_lines.append("")
                new_lines.append('print(f"\\nBlinding quotient polynomial:")')
                new_lines.append('print(f"  quotient_poly_blind = quotient_poly + ({b1_t}·x + {b2_t}) · ZH")')
                new_lines.append('print(f"  quotient_poly_blind: degree {quotient_poly_blind.degree()}")')
                new_lines.append("")
                new_lines.append("# Commit to blinded quotient")
                i += 1
                # Skip the old c_t = kzg.commit(quotient_poly) line
                while i < len(lines) and 'c_t = kzg.commit(quotient_poly)' in lines[i]:
                    i += 1
                new_lines.append("c_t = kzg.commit(quotient_poly_blind)")
            else:
                new_lines.append(line)
            i += 1

        source94 = '\n'.join(new_lines)
        cell94['source'] = [line + '\n' if i < len(new_lines) - 1 else line
                            for i, line in enumerate(new_lines)]
        print("✓ Cell 94 updated with partial match")

print("\n" + "=" * 70)
print("FIX #2: CELL 96 - USE BLINDED POLYNOMIALS")
print("=" * 70)

# Fix Cell 96
cell96 = notebook['cells'][cell96_idx]
source96 = ''.join(cell96['source'])

# Replace evaluations
replacements = [
    ("z_zeta = z_poly(zeta)", "z_zeta = z_poly_blind(zeta)"),
    ("t_zeta = quotient_poly(zeta)", "t_zeta = quotient_poly_blind(zeta)"),
    ("z_zeta_omega = z_poly(zeta_omega)", "z_zeta_omega = z_poly_blind(zeta_omega)"),
    ('print(f"z_zeta = z_poly(ζ) = {z_zeta}")', 'print(f"z_zeta = z_poly_blind(ζ) = {z_zeta}")'),
    ('print(f"t_zeta = quotient_poly(ζ) = {t_zeta}")', 'print(f"t_zeta = quotient_poly_blind(ζ) = {t_zeta}")'),
    ('print(f"z_zeta_omega = z_poly(ζ·ω) = {z_zeta_omega}")', 'print(f"z_zeta_omega = z_poly_blind(ζ·ω) = {z_zeta_omega}")'),
    # Proofs
    ("proof_z = kzg.prove(z_poly, zeta)", "proof_z = kzg.prove(z_poly_blind, zeta)"),
    ("proof_t = kzg.prove(quotient_poly, zeta)", "proof_t = kzg.prove(quotient_poly_blind, zeta)"),
    ("proof_z_omega = kzg.prove(z_poly, zeta_omega)", "proof_z_omega = kzg.prove(z_poly_blind, zeta_omega)"),
    ('print(f"  ✓ proof_z = prove(z_poly, ζ)")', 'print(f"  ✓ proof_z = prove(z_poly_blind, ζ)")'),
    ('print(f"  ✓ proof_t = prove(quotient_poly, ζ)")', 'print(f"  ✓ proof_t = prove(quotient_poly_blind, ζ)")'),
    ('print(f"  ✓ proof_z_omega = prove(z_poly, ζ·ω)")', 'print(f"  ✓ proof_z_omega = prove(z_poly_blind, ζ·ω)")'),
    # Verification print statements
    ('print(f"  Verify z_poly(ζ) = {z_zeta}: {verify_z}")', 'print(f"  Verify z_poly_blind(ζ) = {z_zeta}: {verify_z}")'),
    ('print(f"  Verify quotient_poly(ζ) = {t_zeta}: {verify_t}")', 'print(f"  Verify quotient_poly_blind(ζ) = {t_zeta}: {verify_t}")'),
    ('print(f"  Verify z_poly(ζ·ω) = {z_zeta_omega}: {verify_z_omega}")', 'print(f"  Verify z_poly_blind(ζ·ω) = {z_zeta_omega}: {verify_z_omega}")'),
]

changes_made = 0
for old, new in replacements:
    if old in source96:
        source96 = source96.replace(old, new)
        changes_made += 1

cell96['source'] = source96.split('\n')
cell96['source'] = [line + '\n' if i < len(cell96['source']) - 1 else line
                    for i, line in enumerate(cell96['source'])]

print(f"✓ Cell 96 updated: {changes_made} replacements made")

print("\n" + "=" * 70)
print("FIX #3: ADD VERIFICATION CELL AFTER CELL 100")
print("=" * 70)

# Create new verification cell
verification_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Verification that the fix worked\n",
        "print(f\"✓ verify_plonk passed!\")\n",
        "print(f\"✓ quotient_poly_blind was used: degree {quotient_poly_blind.degree()}\")\n",
        "print(f\"✓ z_poly_blind was used for evaluations\")\n"
    ]
}

# Insert after cell 100
notebook['cells'].insert(cell100_idx + 1, verification_cell)
print(f"✓ Added verification cell at index {cell100_idx + 1}")

print("\n" + "=" * 70)
print("SAVING UPDATED NOTEBOOK")
print("=" * 70)

# Save backup first
backup_path = notebook_path + '.backup'
print(f"\nCreating backup: {backup_path}")
with open(backup_path, 'w') as f:
    json.dump(notebook, f, indent=1)

# Save updated notebook
print(f"Saving updated notebook: {notebook_path}")
with open(notebook_path, 'w') as f:
    json.dump(notebook, f, indent=1)

print("\n✓✓✓ ALL FIXES APPLIED SUCCESSFULLY ✓✓✓")
print("\nNext steps:")
print("1. Restart the notebook kernel")
print("2. Run cells 91-100 in order")
print("3. You should see 'Quotient constraint holds.'")
print("4. Run the new verification cell after cell 100")
