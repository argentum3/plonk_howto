"""
Test script to verify Cell 14 works with the fixed Polynomial class
This simulates running cells 10-14 in sequence
"""

import sys
sys.path.append('..')

print("Importing from exercise3.py (which has the fix)...")
from exercise3 import Polynomial, PolynomialVar, p, interpolate, I, LI, RI, O, a, b, c

print("✓ Imports successful")

# Create x variable (from the notebook)
x = PolynomialVar(p)
print(f"✓ Created x: {type(x)}")

# Cell 12 - Compute t polynomial
print("\n=== Testing Cell 12 ===")
t = a + b - c
print(f"✓ t = a + b - c created, degree: {t.degree()}")

# Cell 13 - Check t(i) for addition gates
print("\n=== Testing Cell 13 ===")
for i in I:
    if i != 4:
        assert t(i) == 0
        print(f"✓ t({i}) = 0")

# Cell 14 - The problematic cell
print("\n=== Testing Cell 14 (THE FIX) ===")
print("Computing f1 = a(x+1) - b(x)...")

try:
    # This is the line that was failing
    f1 = a(x+1) - b(x)
    print(f"✓ f1 created successfully!")
    print(f"  Type: {type(f1)}")
    print(f"  Degree: {f1.degree()}")

    # Test the constraint
    print("\nTesting constraint f1(i) = 0 for i ∈ I\\{3,4}:")
    for i in I:
        if (i != 3) and (i != 4):
            result = f1(i)
            assert result == 0
            print(f"  ✓ f1({i}) = {result}")

    print("\n✓✓✓ Cell 14 constraint 1 PASSED! ✓✓✓")

except Exception as e:
    print(f"\n✗✗✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Continue with f2
print("\n=== Testing Cell 14 constraint 2 ===")
print("Computing f2 = b(x+1) - c(x)...")

try:
    f2 = b(x+1) - c(x)
    print(f"✓ f2 created successfully!")
    print(f"  Type: {type(f2)}")
    print(f"  Degree: {f2.degree()}")

    # Test the constraint
    print("\nTesting constraint f2(i) = 0 for i ∈ I\\{3,4}:")
    for i in I:
        if (i != 3) and (i != 4):
            result = f2(i)
            assert result == 0
            print(f"  ✓ f2({i}) = {result}")

    print("\n✓✓✓ Cell 14 constraint 2 PASSED! ✓✓✓")

except Exception as e:
    print(f"\n✗✗✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*60)
print("ALL TESTS PASSED! Cell 14 works correctly.")
print("="*60)
print("\nIF THE NOTEBOOK STILL FAILS:")
print("1. Go to Kernel → Restart Kernel")
print("2. Run all cells from the beginning (Shift+Enter on each cell)")
print("3. The old Polynomial class was cached in memory")
