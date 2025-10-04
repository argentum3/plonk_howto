#!/usr/bin/env python3
"""
Fibonacci Squared Constraint System
Based on PlonK Tutorial constraints for computing F_4^2
"""

# Define the index set I (assuming it's {1, 2, 3, 4} based on the constraints)
I = {1, 2, 3, 4}

# Witness values derived from constraints:
# Constraint 3 provides wiring between rows
# Row 1: 0 + 1 = 1
# Row 2: 1 + 1 = 2 (LI[2]=RI[1]=1, RI[2]=O[1]=1)
# Row 3: 1 + 2 = 3 (LI[3]=RI[2]=1, RI[3]=O[2]=2)
# Row 4: 3 * 3 = 9 (LI[4]=RI[4]=O[3]=3)
LI = {1: 0, 2: 1, 3: 1, 4: 3}  # Left input
RI = {1: 1, 2: 1, 3: 2, 4: 3}  # Right input
O = {1: 1, 2: 2, 3: 3, 4: 9}   # Output

# Constraint 1: LI(1) = 0, RI(1) = 1
assert LI[1] == 0 and RI[1] == 1

# Constraint 2: ∀i ∈ I \ {4} : LI(i) + RI(i) = O(i)
for i in I:
    if i != 4:
        print(f"Checking Constraint 2 for i={i}: {LI[i]} + {RI[i]} = {O[i]}")
        assert LI[i] + RI[i] == O[i]

# Constraint 3: ∀i ∈ I \ {3,4} : (LI(i+1) = RI(i)) ∧ (RI(i+1) = O(i))
for i in I:
    if i not in {3, 4}:
        assert LI[i + 1] == RI[i]
        assert RI[i + 1] == O[i]

# Constraint 4: LI(4) = RI(4) = O(3)
assert LI[4] == RI[4] == O[3]

# Constraint 5: LI(4) * RI(4) = O(4)
# This computes O(4) = F_4^2
assert LI[4] * RI[4] == O[4]

print("All constraints satisfied!")
print(f"Result: O(4) = F_4^2 = {O[4]}")
