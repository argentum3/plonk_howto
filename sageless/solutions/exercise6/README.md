# Exercise 6: Bilinearity of Pairings

## Problem

Verify that the pairing function `e` is bilinear by checking:

```
e([s]·P, Q) = e(P, [s]·Q) = e(P, Q)^s
```

where:
- `s` is a randomly sampled integer
- `P` is the generator of G1 (BN254 curve)
- `Q` is the generator of G2 (BN254 curve)
- `e` is the pairing function mapping G1 × G2 → GT

## Bilinearity Property

A pairing is **bilinear** if it satisfies:
- **Left linearity**: `e(aP, Q) = e(P, Q)^a` for all `a` and points `P, Q`
- **Right linearity**: `e(P, bQ) = e(P, Q)^b` for all `b` and points `P, Q`

This exercise verifies both properties hold simultaneously.

## Solution

Run the solution:

```bash
cd sageless/solutions/exercise6
source ../../../.venv/bin/activate  # Activate venv for py_ecc
python exercise6.py
```

The solution:
1. Randomly samples an integer `s` from the curve order
2. Computes `[s]·P` (scalar multiplication in G1)
3. Computes `[s]·Q` (scalar multiplication in G2)
4. Verifies `e([s]·P, Q) = e(P, [s]·Q)` (bilinearity)
5. Verifies `e([s]·P, Q) = e(P, Q)^s` (exponentiation property)

## Expected Output

```
✓ All bilinearity checks passed!

This confirms that the pairing function e satisfies:
    e([s]·P, Q) = e(P, [s]·Q) = e(P, Q)^s
```

## Files

- `exercise6.py` - Complete solution with bilinearity verification
- `README.md` - This file

## Dependencies

- `py_ecc` - For BN254 curve operations and pairing function
- `kzg.py` - For curve parameters (P, Q, p, n)
