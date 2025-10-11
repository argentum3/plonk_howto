#!/usr/bin/env python3
"""
Exercise 14: Computing Permutation for Copy Constraints

Compute a permutation σ that encodes the wiring (copy constraints) between
the three columns a, b, c of the circuit.

The permutation maps positions 1..12 to 1..12, where:
  - Column a: positions 1-4 (gates 1-4)
  - Column b: positions 5-8 (gates 1-4)
  - Column c: positions 9-12 (gates 1-4)

Position function:
  pos(column, index) = (column-1)*n + index
  where n=4 (number of gates), column ∈ {1,2,3}, index ∈ {1,2,3,4}

Wiring (from circuit values):
  Gate 1: 0 + 1 = 1
  Gate 2: 1 + 1 = 2
  Gate 3: 1 + 2 = 3
  Gate 4: 3 * 3 = 9

Equivalence classes (values that must be equal):
  {a[1]} = {0}                    - standalone (constant 0)
  {a[2], a[3], b[1]} = {1}        - value 1 appears 3 times
  {b[2], b[3], c[2]} = {1}        - value 1 appears 3 times (wait, this is wrong)

Let me trace more carefully:
  a[1]=0, b[1]=1, c[1]=1  →  position 1 (a[1]) is alone
  a[2]=1, b[2]=1, c[2]=2  →  a[2] and b[2] are equal (both 1)
  a[3]=1, b[3]=2, c[3]=3  →  a[3]=1, b[3]=2, c[3]=3
  a[4]=3, b[4]=3, c[4]=9  →  a[4] and b[4] are equal (both 3)

Actually, looking at the circuit flow:
  - c[1]=1 is reused as a[2] and b[2]
  - c[2]=2 is reused as b[3]
  - c[3]=3 is reused as a[4] and b[4]

So the cycles are:
  {pos(1,1)} = {1} - constant 0, self-cycle
  {pos(1,2), pos(2,1)} - already given
  {pos(3,1), pos(2,2), pos(1,3)} - cycle for value 1
  {pos(3,2), pos(2,3)} - cycle for value 2
  {pos(3,3), pos(1,4), pos(2,4)} - cycle for value 3
  {pos(3,4)} = {12} - output 9, self-cycle
"""

import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

print("="*70)
print("EXERCISE 14: COMPUTING PERMUTATION FOR COPY CONSTRAINTS")
print("="*70)

# Circuit parameters
n = 4  # Number of gates

# Position function
def pos(column, index):
    """
    Map (column, index) to global position in range [1, 12]

    column: 1 (a), 2 (b), or 3 (c)
    index: 1-4 (gate number)
    """
    return (column - 1) * n + index

print(f"\nCircuit structure:")
print(f"  n = {n} gates")
print(f"  3 columns: a (left), b (right), c (output)")
print(f"  Total positions: 3n = {3*n}")

# Display position mapping
print(f"\n" + "="*70)
print("POSITION MAPPING")
print("="*70)

print(f"\nGlobal position = pos(column, index) = (column-1)*n + index")
print(f"\n  Column a (left input):   positions {pos(1,1)}-{pos(1,4)}")
print(f"  Column b (right input):  positions {pos(2,1)}-{pos(2,4)}")
print(f"  Column c (output):       positions {pos(3,1)}-{pos(3,4)}")

print(f"\nDetailed mapping:")
for i in range(1, n+1):
    print(f"  Gate {i}: a[{i}]=pos(1,{i})={pos(1,i):2d}, b[{i}]=pos(2,{i})={pos(2,i):2d}, c[{i}]=pos(3,{i})={pos(3,i):2d}")

# Circuit values
print(f"\n" + "="*70)
print("CIRCUIT VALUES")
print("="*70)

LI = {1: 0, 2: 1, 3: 1, 4: 3}  # a column values
RI = {1: 1, 2: 1, 3: 2, 4: 3}  # b column values
O  = {1: 1, 2: 2, 3: 3, 4: 9}  # c column values

print(f"\n  Gate | a[i] | b[i] | c[i] | Constraint")
print(f"  " + "-"*45)
for i in range(1, n+1):
    constraint = "addition" if i in [1,2,3] else "multiplication"
    op = "+" if i in [1,2,3] else "*"
    result = LI[i] + RI[i] if i in [1,2,3] else LI[i] * RI[i]
    print(f"  {i}    |  {LI[i]}   |  {RI[i]}   |  {O[i]:2d}  | {LI[i]} {op} {RI[i]} = {result}")

# Trace wiring (which values are reused where)
print(f"\n" + "="*70)
print("WIRING ANALYSIS (Copy Constraints)")
print("="*70)

print(f"\nTracing value flow through the circuit:")
print(f"  - Output c[i] from gate i can be reused as input a[j] or b[j] in later gates")
print(f"\n  Gate 1: c[1] = 1  →  reused as a[2]=1 and b[2]=1")
print(f"  Gate 2: c[2] = 2  →  reused as b[3]=2")
print(f"  Gate 3: c[3] = 3  →  reused as a[4]=3 and b[4]=3")
print(f"  Gate 4: c[4] = 9  →  final output (not reused)")

# Build permutation σ
print(f"\n" + "="*70)
print("BUILDING PERMUTATION σ")
print("="*70)

sigma = {}

# First input a[1] = 0 (constant, self-cycle)
print(f"\n1. Position {pos(1,1)} (a[1]=0): constant input, self-cycle")
sigma[pos(1,1)] = pos(1,1)

# Cycle: a[2] → b[1] → a[2] (value 1)
# This is already given in the exercise
print(f"\n2. Cycle for initial 1: a[2]=1, b[1]=1")
print(f"   {pos(1,2)} → {pos(2,1)} → {pos(1,2)}")
sigma[pos(1,2)] = pos(2,1)
sigma[pos(2,1)] = pos(1,2)

# Cycle: a[3] → b[2] → c[1] → a[3] (value 1 from gate 1 output)
print(f"\n3. Cycle for value 1 (from c[1]): a[3]=1, b[2]=1, c[1]=1")
print(f"   {pos(1,3)} → {pos(2,2)} → {pos(3,1)} → {pos(1,3)}")
sigma[pos(1,3)] = pos(2,2)
sigma[pos(2,2)] = pos(3,1)
sigma[pos(3,1)] = pos(1,3)

# Cycle: c[2] → b[3] → c[2] (value 2 from gate 2 output)
print(f"\n4. Cycle for value 2 (from c[2]): c[2]=2, b[3]=2")
print(f"   {pos(3,2)} → {pos(2,3)} → {pos(3,2)}")
sigma[pos(3,2)] = pos(2,3)
sigma[pos(2,3)] = pos(3,2)

# Cycle: c[3] → a[4] → b[4] → c[3] (value 3 from gate 3 output)
print(f"\n5. Cycle for value 3 (from c[3]): c[3]=3, a[4]=3, b[4]=3")
print(f"   {pos(3,3)} → {pos(1,4)} → {pos(2,4)} → {pos(3,3)}")
sigma[pos(3,3)] = pos(1,4)
sigma[pos(1,4)] = pos(2,4)
sigma[pos(2,4)] = pos(3,3)

# Final output c[4] = 9 (self-cycle)
print(f"\n6. Position {pos(3,4)} (c[4]=9): final output, self-cycle")
sigma[pos(3,4)] = pos(3,4)

# Verification
print(f"\n" + "="*70)
print("VERIFICATION")
print("="*70)

print(f"\nPermutation σ (as dictionary):")
for k in sorted(sigma.keys()):
    print(f"  σ[{k:2d}] = {sigma[k]:2d}")

# Check 1: Length
check1 = len(sigma) == 12
print(f"\nCheck 1: Length should be 12: {check1}")
if not check1:
    print(f"  Got: {len(sigma)}")

# Check 2: No repeated elements in domain
check2 = len(set(sigma.keys())) == 12
print(f"Check 2: No repeated keys: {check2}")

# Check 3: Domain and image are both {1..12}
check3 = (set(sigma.keys()) == set(range(1, 13)) == set(sigma.values()))
print(f"Check 3: Domain and image are {{1..12}}: {check3}")
if not check3:
    print(f"  Keys: {sorted(sigma.keys())}")
    print(f"  Values: {sorted(sigma.values())}")

# Check 4: Specific cycle (3, 6, 9) - value 1 from c[1]
check4 = (sigma[3] == 6 and sigma[6] == 9 and sigma[9] == 3)
print(f"Check 4: Cycle (3, 6, 9) exists: {check4}")
if not check4:
    print(f"  σ[3] = {sigma.get(3)} (expected 6)")
    print(f"  σ[6] = {sigma.get(6)} (expected 9)")
    print(f"  σ[9] = {sigma.get(9)} (expected 3)")

all_checks = check1 and check2 and check3 and check4

if all_checks:
    print(f"\n✓ All checks passed!")
else:
    print(f"\n⚠️ Some checks failed!")

# Display cycles
print(f"\n" + "="*70)
print("PERMUTATION CYCLES")
print("="*70)

# Find all cycles
visited = set()
cycles = []

for start in sorted(sigma.keys()):
    if start in visited:
        continue

    cycle = []
    current = start
    while current not in visited:
        visited.add(current)
        cycle.append(current)
        current = sigma[current]

    cycles.append(cycle)

print(f"\nPermutation σ as cycles:")
for i, cycle in enumerate(cycles, 1):
    if len(cycle) == 1:
        print(f"  Cycle {i}: ({cycle[0]}) - self-cycle")
    else:
        cycle_str = " → ".join(str(x) for x in cycle)
        print(f"  Cycle {i}: {cycle_str} → {cycle[0]}")

# Summary
print(f"\n" + "="*70)
print("SUMMARY")
print("="*70)

print(f"""
Permutation σ encodes copy constraints (wiring) in the circuit:

Total positions: 12
  - Column a (left):  {list(range(1, 5))}
  - Column b (right): {list(range(5, 9))}
  - Column c (out):   {list(range(9, 13))}

Permutation has {len(cycles)} cycles:
  - 2 self-cycles (constants/final output)
  - {len([c for c in cycles if len(c) > 1])} non-trivial cycles (wiring)

This permutation σ will be used in PlonK's permutation argument
to enforce that wired values are equal without revealing them!

Key insight:
  If positions i and j are in the same cycle, they must have equal values.
  The permutation σ encodes this equivalence relation.
""")

print("="*70)
print("✓ Exercise 14 Complete!")
print("="*70)
