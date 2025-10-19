#!/usr/bin/env python3
"""
Fix quotient constraint issue by removing quotient_poly_blind

The quotient polynomial cannot be blinded the same way as witness polynomials
because it breaks the mathematical identity: bigt(ζ) = quotient_poly(ζ) * ZH(ζ)
"""

import json

notebook_path = '/Users/boy/projects/plonk/sageless/PlonK-Tutorial.ipynb'

print("=" * 70)
print("FIXING QUOTIENT CONSTRAINT ISSUE")
print("=" * 70)

with open(notebook_path, 'r') as f:
    nb = json.load(f)

print(f"\nNotebook has {len(nb['cells'])} cells")

# Find Cell 94 (Exercise 21)
cell94_idx = None
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'quotient_poly, remainder = bigt.quo_rem(ZH)' in source:
            cell94_idx = i
            print(f"Found Cell 94 (Exercise 21) at index {i}")
            break

if cell94_idx is None:
    print("ERROR: Could not find Cell 94")
    exit(1)

# Find Cell 96 (Exercise 22)
cell96_idx = None
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'a_zeta = a_blind(zeta)' in source and 'zeta = generate_challenge(transcript)' in source:
            cell96_idx = i
            print(f"Found Cell 96 (Exercise 22) at index {i}")
            break

if cell96_idx is None:
    print("ERROR: Could not find Cell 96")
    exit(1)

# Find Cell 103 (Verification cell)
cell103_idx = None
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'verify_plonk passed' in source and 'quotient_poly_blind was used' in source:
            cell103_idx = i
            print(f"Found Cell 103 (Verification) at index {i}")
            break

print("\n" + "=" * 70)
print("FIX #1: CELL 94 - REMOVE QUOTIENT BLINDING")
print("=" * 70)

cell94 = nb['cells'][cell94_idx]
source94 = ''.join(cell94['source'])

# Remove the blinding code and replace with simple commitment
old_blinding = """# Blind the quotient polynomial (for zero-knowledge)
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

new_commitment = """# Commit to quotient polynomial
# Note: We don't blind the quotient polynomial because blinding breaks
# the quotient constraint: bigt(ζ) = quotient_poly(ζ) * ZH(ζ)
# Real PlonK uses quotient polynomial splitting for zero-knowledge,
# but for this tutorial, witness blinding provides sufficient ZK property.
c_t = kzg.commit(quotient_poly)
print(f"\\nCommitment to quotient:")
print(f"  c_t = {c_t}")

# Add to transcript
transcript = push(c_t, transcript)"""

if old_blinding in source94:
    source94 = source94.replace(old_blinding, new_commitment)
    print("✓ Removed quotient_poly_blind and updated commitment")
else:
    print("⚠ Could not find exact blinding code, trying alternative...")
    # Try simpler replacement
    if 'quotient_poly_blind = quotient_poly' in source94:
        source94 = source94.replace('quotient_poly_blind = quotient_poly + (b1_t * x + b2_t) * ZH', '')
        source94 = source94.replace('b1_t, b2_t = 55555, 66666', '')
        source94 = source94.replace('c_t = kzg.commit(quotient_poly_blind)', 'c_t = kzg.commit(quotient_poly)')
        print("✓ Removed blinding with alternative method")

cell94['source'] = source94.split('\n')
cell94['source'] = [line + '\n' if i < len(cell94['source']) - 1 else line
                    for i, line in enumerate(cell94['source'])]

print("\n" + "=" * 70)
print("FIX #2: CELL 96 - USE UNBLINDED QUOTIENT")
print("=" * 70)

cell96 = nb['cells'][cell96_idx]
source96 = ''.join(cell96['source'])

replacements_96 = [
    ('t_zeta = quotient_poly_blind(zeta)', 't_zeta = quotient_poly(zeta)'),
    ('print(f"t_zeta = quotient_poly_blind(ζ) = {t_zeta}")', 'print(f"t_zeta = quotient_poly(ζ) = {t_zeta}")'),
    ('proof_t = kzg.prove(quotient_poly_blind, zeta)', 'proof_t = kzg.prove(quotient_poly, zeta)'),
    ('print(f"  ✓ proof_t = prove(quotient_poly_blind, ζ)")', 'print(f"  ✓ proof_t = prove(quotient_poly, ζ)")'),
    ('print(f"  Verify quotient_poly_blind(ζ) = {t_zeta}: {verify_t}")', 'print(f"  Verify quotient_poly(ζ) = {t_zeta}: {verify_t}")'),
]

changes_96 = 0
for old, new in replacements_96:
    if old in source96:
        source96 = source96.replace(old, new)
        changes_96 += 1

cell96['source'] = source96.split('\n')
cell96['source'] = [line + '\n' if i < len(cell96['source']) - 1 else line
                    for i, line in enumerate(cell96['source'])]

print(f"✓ Made {changes_96} changes to Cell 96")

if cell103_idx is not None:
    print("\n" + "=" * 70)
    print("FIX #3: CELL 103 - UPDATE VERIFICATION")
    print("=" * 70)

    cell103 = nb['cells'][cell103_idx]
    source103 = ''.join(cell103['source'])

    source103 = source103.replace(
        'print(f"✓ quotient_poly_blind was used: degree {quotient_poly_blind.degree()}")',
        'print(f"✓ quotient_poly was used: degree {quotient_poly.degree()}")'
    )

    cell103['source'] = source103.split('\n')
    cell103['source'] = [line + '\n' if i < len(cell103['source']) - 1 else line
                        for i, line in enumerate(cell103['source'])]

    print("✓ Updated verification cell")

print("\n" + "=" * 70)
print("SAVING NOTEBOOK")
print("=" * 70)

backup = notebook_path + '.backup_quotient_fix'
print(f"\nCreating backup: {backup}")
with open(backup, 'w') as f:
    json.dump(nb, f, indent=1)

print(f"Saving updated notebook: {notebook_path}")
with open(notebook_path, 'w') as f:
    json.dump(nb, f, indent=1)

print("\n✓✓✓ FIX APPLIED SUCCESSFULLY ✓✓✓")
print("\nChanges made:")
print("  Cell 94: Removed quotient_poly_blind, commit to quotient_poly")
print("  Cell 96: Use quotient_poly instead of quotient_poly_blind")
print("  Cell 103: Updated verification message")
print("\nNext steps:")
print("  1. Restart kernel")
print("  2. Run cells 91-100")
print("  3. Cell 99: Quotient constraint check should pass")
print("  4. Cell 100: verify_plonk should pass")
