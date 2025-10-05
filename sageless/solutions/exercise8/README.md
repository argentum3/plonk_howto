# Exercise 8: KZG Polynomial Commitment Function

## Problem

Implement the **commitment function** for KZG polynomial commitments:

```python
def commitment(S1, p):
    # Compute commitment c to polynomial p
    return c
```

**Inputs:**
- `S1`: Trusted setup vector `[P, τ·P, τ²·P, ..., τˡ·P]` from Exercise 7
- `p`: A polynomial with coefficients `[a₀, a₁, a₂, ..., aₙ]`

**Output:**
- `c`: A commitment point on the elliptic curve

**Formula:**
```
c = Σᵢ aᵢ · S1[i] = a₀·P + a₁·(τ·P) + a₂·(τ²·P) + ... + aₙ·(τⁿ·P)
  = (a₀ + a₁·τ + a₂·τ² + ... + aₙ·τⁿ) · P
  = p(τ) · P
```

## What is a Polynomial Commitment?

A **commitment** is a cryptographic way to "lock in" a polynomial without revealing it. Think of it like:
- Putting a sealed envelope containing your polynomial in a public place
- Everyone can see the envelope (the commitment)
- But nobody can open it to see what's inside (the polynomial remains hidden)
- Later, you can prove properties about the polynomial without revealing it

## Solution

Run the solution:

```bash
cd sageless/solutions/exercise8
source ../../../.venv/bin/activate  # Or use run.sh
python exercise8.py
```

Or using the helper script:
```bash
./run.sh sageless/solutions/exercise8/exercise8.py
```

### Algorithm

1. **Start with identity**: `c = Z1` (point at infinity, the identity element)

2. **For each coefficient** `aᵢ` in polynomial:
   ```python
   term = multiply(S1[i], aᵢ)  # Scalar multiplication
   c = add(c, term)             # Point addition
   ```

3. **Return** the commitment point `c`

### Implementation Details

```python
from py_ecc.bn128 import multiply, add, Z1

def commitment(S1, p):
    coeffs = p.coeffs
    c = Z1  # Identity element (point at infinity)

    for i, coeff in enumerate(coeffs):
        term = multiply(S1[i], coeff % kzg.n)
        c = add(c, term)

    return c
```

**Key operations:**
- `multiply(P, k)`: Scalar multiplication - add point P to itself k times
- `add(P, Q)`: Point addition on elliptic curve
- `Z1`: Point at infinity (identity element for addition)

## Expected Output

When tested on polynomial `a(x)` from the Fibonacci example:

```
Commitment c = (
  19772988533509128204934208855583299243034568734268587639600165428945857082832 :
  21198549198844316278609987090510616007059968516882705878791833422348082226388 :
  1
)
```

**Verification:**
- ✓ Matches expected x-coordinate
- ✓ Matches expected y-coordinate
- ✓ Valid point on BN254 curve

## Why This Works

The commitment `c = p(τ)·P` has special properties:

### 1. **Binding** (Can't Change Polynomial)
Once you commit, you're locked in. Computing a different `c'` for polynomial `p'(x)` would give a completely different point.

### 2. **Hiding** (Polynomial Stays Secret)
Given `c`, you cannot work backwards to recover `p(x)`. This relies on the **discrete logarithm problem** being hard.

### 3. **Succinct** (Tiny Size)
No matter how large your polynomial degree:
- Commitment is **one curve point** (~48 bytes for BN254)
- Compare to sending all coefficients (could be megabytes!)

### 4. **Homomorphic** (Can Compute on Commitments)
```
commit(p + q) = commit(p) + commit(q)
commit(k·p) = k·commit(p)
```
This enables powerful zero-knowledge proof techniques!

## The Magic of the Trusted Setup

Why does this work without knowing τ?

```
c = a₀·S1[0] + a₁·S1[1] + a₂·S1[2] + ...
  = a₀·P + a₁·(τ·P) + a₂·(τ²·P) + ...
  = (a₀ + a₁·τ + a₂·τ²  + ...)·P
  = p(τ)·P
```

We compute `p(τ)·P` **without knowing τ**! This is the power of the trusted setup - it gives us "encrypted" powers of τ that we can use for computation.

## Security

The commitment is secure if:
1. **Discrete Log is Hard**: Can't compute τ from τ·P
2. **Trusted Setup is Honest**: τ was destroyed after creating S1
3. **q-SDH Assumption**: Can't forge commitments or proofs

## Use in KZG Protocol

The full KZG protocol flow:

```
1. SETUP:    Compute S1 = [P, τ·P, τ²·P, ...]    (Exercise 7)
2. COMMIT:   c = commitment(S1, p)                (Exercise 8) ← We are here!
3. EVALUATE: Prover claims p(z) = y
4. PROVE:    Create proof π that p(z) = y         (Exercise 9+)
5. VERIFY:   Check proof using pairings           (Exercise 9+)
```

Exercise 8 implements step 2 - creating the commitment that gets sent to the verifier.

## Practical Applications

KZG commitments are used in:
- **PlonK** - Polynomial IOPs become SNARKs
- **Ethereum's EIP-4844** - Blob transactions use KZG commitments
- **zkRollups** - Scaling solutions for blockchain
- **Private computation** - Prove you computed something without revealing inputs

## Mathematical Properties

### Elliptic Curve Point Addition

Points on an elliptic curve form a group:
- **Identity**: Point at infinity (Z1)
- **Addition**: Geometric line intersection
- **Scalar multiplication**: Repeated addition

### Commutative and Associative

```
(a₀·S1[0]) + (a₁·S1[1]) + (a₂·S1[2])
```
Order doesn't matter - same result!

## Example Calculation

For polynomial `a(x) = 0 + 1·x + 1·x² + 3·x³`:

```
c = 0·S1[0] + 1·S1[1] + 1·S1[2] + 3·S1[3]
  = 1·(τ·P) + 1·(τ²·P) + 3·(τ³·P)
  = (τ + τ² + 3τ³)·P
  = a(τ)·P
```

With τ = 424242, this evaluates to the expected commitment point!

## Next Steps

After Exercise 8, you can:
- **Exercise 9**: Create evaluation proofs (prove `p(z) = y`)
- **Exercise 10+**: Verify proofs using pairings
- Build the complete KZG commitment scheme!

## Files

- `exercise8.py` - Complete solution with verification
- `README.md` - This file

## Related Documentation

- [KZG_COMMITMENTS_EXPLAINED.md](../docs/KZG_COMMITMENTS_EXPLAINED.md) - Full KZG explanation
- [Exercise 7](../exercise7/) - Trusted setup (prerequisite)
- [Exercise 6](../exercise6/) - Pairing bilinearity (needed for verification)

---

**Commitment computed! Ready for the next step: creating proofs!** 🎉
