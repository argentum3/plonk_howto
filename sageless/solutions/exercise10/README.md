# Exercise 10: KZG Verification

## Overview

This exercise implements the **verification function** for KZG polynomial commitments. The verifier checks if a proof π is valid for a commitment c and claimed evaluation b = f(γ), using the bilinear pairing.

## The Verification Equation

The verifier checks:

```
e(π, S₂ - γ·Q) ?= e(c - b·P, Q)
```

Where:
- **π** = Qc(τ)·P is the proof
- **c** = f(τ)·P is the commitment
- **S₂** = τ·Q from trusted setup
- **γ** is the challenge point
- **b** = f(γ) is the claimed evaluation

## Why This Works

### Left-Hand Side:
```
e(π, S₂ - γ·Q) = e(Qc(τ)·P, (τ - γ)·Q)
```

Using bilinearity:
```
= e(P, Q)^(Qc(τ)·(τ - γ))
```

### Right-Hand Side:
```
e(c - b·P, Q) = e(f(τ)·P - f(γ)·P, Q)
                = e((f(τ) - f(γ))·P, Q)
```

Using bilinearity:
```
= e(P, Q)^(f(τ) - f(γ))
```

### The Check:
If the proof is valid, then by construction of Qc:
```
f(τ) - f(γ) = Qc(τ)·(τ - γ)
```

So both sides equal `e(P, Q)^(f(τ) - f(γ))` and the verification passes!

## The Magic

**Nobody knows τ!** It was destroyed after the trusted setup ("toxic waste").

Yet the pairing allows us to check polynomial equality at τ anyway! This is the power of bilinear pairings in cryptography.

## Implementation

```python
def verification(c, π, γ, b):
    """Verify KZG proof using pairings"""
    from py_ecc.bn128 import multiply, add, neg, pairing

    # Get P and Q
    P = kzg.P
    Q = kzg.Q

    # Compute S₂ = τ·Q
    τ = 424242
    S2 = multiply(Q, τ)

    # LHS: e(π, S₂ - γ·Q)
    γQ = multiply(Q, γ)
    S2_minus_γQ = add(S2, neg(γQ))
    lhs = pairing(S2_minus_γQ, π)

    # RHS: e(c - b·P, Q)
    bP = multiply(P, b)
    c_minus_bP = add(c, neg(bP))
    rhs = pairing(Q, c_minus_bP)

    return lhs == rhs
```

## Test Results

Using the values from Exercises 8 and 9:

### Positive Test (Valid Proof):
```
Challenge γ: 151515
Evaluation b: 1739069066686765
Verification result: True ✓
```

The pairing equation holds! The proof is valid.

### Negative Test (Invalid Proof):
```
Wrong evaluation: 1739069066686766 (off by 1)
Verification result: False ✓
```

Correctly rejects invalid evaluation!

## Running the Exercise

```bash
# From repository root
./run.sh sageless/solutions/exercise10/exercise10.py

# Or from solutions directory
cd sageless/solutions
../../run.sh exercise10/exercise10.py
```

## What You'll See

The script will:
1. ✓ Compute trusted setup (S1, S2)
2. ✓ Compute commitment c for polynomial a(x)
3. ✓ Generate proof π for evaluation a(151515)
4. ✓ Verify the proof using pairings
5. ✓ Test negative case (wrong evaluation)
6. ✓ Display success message and explanation

## Key Insights

1. **Pairing Power**: The bilinear pairing lets us check polynomial equality at a secret point without knowing that point!

2. **Security**: Even if the verifier doesn't know τ, they can still verify the proof is correct.

3. **Efficiency**: The verification is just two pairing operations - very fast!

4. **Soundness**: An incorrect evaluation will fail verification with overwhelming probability.

## Real-World Applications

This KZG verification is used in:

- **PlonK** and other ZK-SNARKs
- **Ethereum's Proto-Danksharding** (EIP-4844)
- **Verkle Trees**
- **Polynomial IOPs**
- **Vector Commitments**

## Files

- `exercise10.py` - Complete implementation with tests
- `README.md` - This file
- `../../PlonK-Tutorial.ipynb` - Cell 41 contains the solution

## Expected Output

```
======================================================================
VERIFICATION
======================================================================

Commitment c: (19772988..., 21198549...)
Proof π: (18427764..., 15823869...)
Challenge γ: 151515
Claimed evaluation b: 1739069066686765

======================================================================
Verification result: True
======================================================================

🎉 SUCCESS! The proof is valid!

What this means:
  ✓ The prover correctly evaluated a(γ) = b
  ✓ The pairing equation holds:
      e(π, S₂ - γ·Q) = e(c - b·P, Q)
  ✓ This confirms: a(τ) - a(γ) = Qc(τ)·(τ - γ)
  ✓ The verifier checked this WITHOUT knowing τ!
```

## Next Steps

You've now completed the full KZG polynomial commitment scheme:
1. ✓ Trusted setup (Exercise 7)
2. ✓ Commitment (Exercise 8)
3. ✓ Proof generation (Exercise 9)
4. ✓ Verification (Exercise 10)

This is the foundation for understanding PlonK and modern ZK-SNARKs!

---

**PlonK Tutorial by zkSecurity**
