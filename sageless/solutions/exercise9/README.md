#!/usr/bin/env python3
# Exercise 9: KZG Proof Generation

## Problem

Implement the **proof function** that generates a KZG proof for polynomial evaluation:

```python
def proof(S1, Qc):
    # Generate proof π for quotient polynomial Qc
    return π
```

**Inputs:**
- `S1`: Trusted setup vector from Exercise 7
- `Qc`: Quotient polynomial `Qc(x) = (f(x) - f(γ)) / (x - γ)`

**Output:**
- `π`: A proof point on the elliptic curve

**Test case:**
- Polynomial: `a(x)` from Fibonacci example
- Challenge: `γ = 151515`
- Expected evaluation: `a(γ) = 1739069066686765`

## What is a KZG Proof?

A **proof** allows the prover to convince a verifier that a claimed polynomial evaluation is correct, without revealing the polynomial itself.

**The Protocol:**
1. **Prover** commits to polynomial `f(x)` → commitment `c`
2. **Verifier** sends challenge `γ`
3. **Prover** claims `f(γ) = y` and provides proof `π`
4. **Verifier** checks the proof using pairings

The proof works because of a key mathematical property:
> If `f(γ) = y` is true, then `(f(x) - y)` is divisible by `(x - γ)`

## The Quotient Polynomial

Given:
- Polynomial `f(x)`
- Challenge point `γ`
- Claimed evaluation `y = f(γ)`

We create the **quotient polynomial**:
```
Qc(x) = (f(x) - y) / (x - γ)
```

**Why this works:**
- If `y = f(γ)` is correct, then `f(γ) - y = 0`
- This means `γ` is a root of `f(x) - y`
- By the **polynomial remainder theorem**, `(x - γ)` divides `f(x) - y`
- So `Qc(x)` is a valid polynomial with no remainder

The proof is simply:
```
π = Qc(τ)·P
```

## Solution

Run the solution:

```bash
cd sageless/solutions/exercise9
source ../../../.venv/bin/activate  # Or use run.sh
python exercise9.py
```

Or using the helper script:
```bash
./run.sh sageless/solutions/exercise9/exercise9.py
```

### Algorithm

The `proof` function is identical to the `commitment` function from Exercise 8:

```python
def proof(S1, Qc):
    π = Z1  # Identity element

    for i, coeff in enumerate(Qc.coeffs):
        term = multiply(S1[i], coeff)
        π = add(π, term)

    return π
```

This computes: `π = Σᵢ bᵢ·S1[i] = Qc(τ)·P`

### Computing the Quotient

```python
# Given challenge γ = 151515
γ = 151515

# Evaluate polynomial
b = a(γ)  # Returns 1739069066686765

# Create constant polynomial
b_poly = Polynomial([b], p)

# Create polynomial variable
x = PolynomialVar(p)

# Compute quotient
Qc, remainder = (a - b_poly).quo_rem(x - γ)

# Generate proof
π = proof(S1, Qc)
```

## Expected Output

```
Challenge γ = 151515
Evaluation a(γ) = 1739069066686765

Proof π = (
  18427764633036746853571353448280965399000717707037995558464363091930831203059 :
  15823869948268955546174436172082876809321127559750802916163692992123652869945 :
  1
)
```

**Verification:**
- ✓ π x-coordinate matches expected
- ✓ π y-coordinate matches expected
- ✓ Evaluation `a(γ)` matches expected
- ✓ Remainder is zero (polynomial division exact)

## How Verification Works (Next Exercise)

The verifier will check using pairings:

```
e(π, S2 - γ·Q) ?= e(c - y·P, Q)
```

**Left side expands to:**
```
e(π, (τ - γ)·Q) = e(Qc(τ)·P, (τ - γ)·Q)
                = e(Qc(τ)·(τ - γ)·P, Q)
```

**Right side expands to:**
```
e(f(τ)·P - y·P, Q) = e((f(τ) - y)·P, Q)
```

**Both equal if:**
```
Qc(τ)·(τ - γ) = f(τ) - y
```

Which is exactly the definition of `Qc(x)`!

## Why This is Secure

**Soundness (Can't Cheat):**
- If `y ≠ f(γ)`, then `(f(x) - y)` is NOT divisible by `(x - γ)`
- The polynomial division would have a non-zero remainder
- The prover cannot create a valid `Qc(x)`
- The pairing check will fail

**Zero-Knowledge:**
- The proof `π` reveals nothing about `f(x)`
- It's just one elliptic curve point
- The verifier learns only that `f(γ) = y` is correct

**Succinctness:**
- Proof is one curve point (~48 bytes)
- Same size regardless of polynomial degree!

## Mathematical Details

### Polynomial Remainder Theorem

If `f(x)` is a polynomial and `c` is a constant:
```
f(x) = (x - c)·q(x) + r
```
where `r = f(c)` (the remainder)

Therefore:
```
f(x) - f(c) = (x - c)·q(x)
```

This is why the quotient exists!

### Bilinear Pairing Property

The verification uses bilinearity:
```
e(aP, bQ) = e(P, Q)^(ab)
```

This allows checking multiplication in the exponent:
```
e(Qc(τ)·P, (τ-γ)·Q) = e(P, Q)^(Qc(τ)·(τ-γ))
```

### Security Assumption

The proof is secure under the **q-SDH assumption**:
- Given `[P, τ·P, τ²·P, ..., τⁿ·P]`
- It's hard to compute `[1/(τ+c)·P]` for any `c`

This prevents forging proofs for incorrect evaluations.

## Example Calculation

For `a(x)` at `γ = 151515`:

**Step 1:** Evaluate
```
a(151515) = 1739069066686765
```

**Step 2:** Create quotient
```
Qc(x) = (a(x) - 1739069066686765) / (x - 151515)
```

**Step 3:** Compute proof
```
π = Qc(τ)·P = Σᵢ bᵢ·S1[i]
```

**Step 4:** Verifier checks (Exercise 10)

## Practical Applications

KZG proofs are used in:
- **PlonK zkSNARKs** - Polynomial commitment scheme
- **Ethereum Data Availability** - EIP-4844 blob commitments
- **Verkle Trees** - More efficient Merkle trees
- **Private Transactions** - Prove payment validity

## Next Steps

After Exercise 9:
- **Exercise 10**: Implement verification using pairings
- Complete the full KZG commitment scheme!

## Files

- `exercise9.py` - Complete solution with verification
- `README.md` - This file

## Related Documentation

- [KZG_COMMITMENTS_EXPLAINED.md](../docs/KZG_COMMITMENTS_EXPLAINED.md) - Full KZG explanation
- [Exercise 7](../exercise7/) - Trusted setup
- [Exercise 8](../exercise8/) - Commitment function
- [Exercise 6](../exercise6/) - Pairing bilinearity (needed for verification)

---

**Proof generated! Ready for verification!** 🎉
