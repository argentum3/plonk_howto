# Cell 14 Error Fix: Polynomial Composition

## The Error

```
TypeError: Can only divide by another polynomial
```

This error occurred when executing:
```python
f1 = a(x+1) - b(x)
```

## Root Cause

The error occurred because of a **type mismatch** in polynomial operations:

1. **`x` is a `PolynomialVar`** object (representing the variable x)
2. **`x+1` returns a `Polynomial`** object (the polynomial x+1 with coeffs [1, 1])
3. **`a(x+1)` tried to evaluate** polynomial `a` at a `Polynomial` argument
4. The original `Polynomial.__call__` method only handled **integer arguments**
5. When evaluating with a Polynomial, it tried to use `%` (modulo) operator
6. The `%` operator calls `quo_rem` which expects a Polynomial divisor, but got an integer
7. This caused the `TypeError`

## Why This Happened

The code `a(x+1)` is attempting **polynomial composition**, not evaluation at a numeric value:
- **Evaluation**: `a(5)` = compute the value of polynomial a at x=5 → returns an integer
- **Composition**: `a(x+1)` = substitute (x+1) for x in polynomial a(x) → returns a new polynomial

For example, if `a(x) = 2 + 3x + x²`, then:
- `a(5)` = 2 + 3(5) + 5² = 42 (integer)
- `a(x+1)` = 2 + 3(x+1) + (x+1)² = 6 + 5x + x² (polynomial)

The original `__call__` method only implemented evaluation, not composition.

## The Fix

Modified `Polynomial.__call__` to handle **both cases**:

```python
def __call__(self, x):
    """
    Evaluate polynomial at x
    If x is an integer: returns f(x) as an integer
    If x is a Polynomial: returns composition f(x) as a Polynomial
    """
    # Check if x is a Polynomial (composition)
    if isinstance(x, Polynomial):
        result = Polynomial([0], self.modulus)
        x_power = Polynomial([1], self.modulus)  # x^0 = 1
        for coeff in self.coeffs:
            result = result + (x_power * coeff)
            x_power = x_power * x
        return result
    else:
        # Integer evaluation
        result = 0
        x_power = 1
        for coeff in self.coeffs:
            result = (result + coeff * x_power) % self.modulus
            x_power = (x_power * x) % self.modulus
        return result
```

### How Composition Works

For a polynomial `f(x) = c₀ + c₁x + c₂x² + ... + cₙxⁿ` and substitution polynomial `g(x)`:

`f(g(x)) = c₀ + c₁·g(x) + c₂·g(x)² + ... + cₙ·g(x)ⁿ`

The algorithm:
1. Start with `result = 0` and `x_power = 1` (which is g(x)⁰)
2. For each coefficient cᵢ:
   - Add `cᵢ · x_power` to result
   - Multiply `x_power` by `g(x)` to get the next power
3. Return the composed polynomial

## Verification

After the fix, `f1 = a(x+1) - b(x)` works correctly:

```python
f1(1) = 0  ✓  (a(2) - b(1) = 1 - 1 = 0)
f1(2) = 0  ✓  (a(3) - b(2) = 1 - 1 = 0)
```

This satisfies the wiring constraint from the PLONK tutorial.

## Files Modified

1. **sageless/PlonK-Tutorial.ipynb** - Cell 10: Updated `Polynomial.__call__` method
2. **sageless/solutions/exercise3.py** - Updated `Polynomial.__call__` method

## Testing

Run the debug script to verify:
```bash
cd sageless/solutions
python3 debug_cell14.py
```

This demonstrates polynomial composition and validates the constraints work correctly.
