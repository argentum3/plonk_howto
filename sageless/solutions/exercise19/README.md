# Exercise 19: Building Fiat-Shamir Transcript - Step 1

## Overview

This exercise implements the first step of building a non-interactive proof using the Fiat-Shamir transform. We create a transcript by systematically adding public values and cryptographic commitments, then compute opening proofs to verify witness values.

## What is a Transcript?

A **transcript** is a sequential record of all public values and commitments exchanged during a cryptographic protocol. In the Fiat-Shamir transform:
- The transcript accumulates protocol messages in order
- Hashing the transcript generates deterministic challenges
- This converts an interactive proof into a non-interactive one

Think of it as a "proof of work" that both prover and verifier agree upon.

## Step 1: Public Inputs/Outputs and Commitments

### 1. Evaluate Witness Polynomials

We evaluate the witness polynomials at specific points to get the public inputs and output:

```python
# Inputs at ω (first domain point)
value_a = a(ω)  # Should be 0
value_b = b(ω)  # Should be 1

# Output at ω^4 (fourth domain point)
value_c = c(ω^4)  # Should be 9
```

**Why these points?**
- `ω` is the first element of our multiplicative domain
- These values represent the actual circuit inputs and output
- They must be public for the verifier to check

### 2. Build the Transcript

Push the public values to an initially empty transcript:

```python
transcript = ""
transcript = push(value_a, transcript)  # Add 0
transcript = push(value_b, transcript)  # Add 1
transcript = push(value_c, transcript)  # Add 9
```

The `push` function appends each value with a delimiter ("|") to build a string representation.

### 3. Compute KZG Commitments

Commit to the **blinded** witness polynomials (from Exercise 18):

```python
c_a = commitment(S1, a_blind)
c_b = commitment(S1, b_blind)
c_c = commitment(S1, c_blind)
```

**Key points:**
- We commit to the blinded versions for zero-knowledge
- Commitments are elliptic curve points (hiding the actual polynomial)
- The trusted setup `S1 = [P, τP, τ²P, ..., τˡP]` enables the commitment scheme

### 4. Push Commitments to Transcript

Add the commitments to the transcript:

```python
transcript = push(c_a, transcript)
transcript = push(c_b, transcript)
transcript = push(c_c, transcript)
```

After this, the transcript contains:
- Public input values: `a(ω) = 0`, `b(ω) = 1`
- Public output value: `c(ω^4) = 9`
- Commitments: `c_a`, `c_b`, `c_c`

### 5. Compute Opening Proofs (Not Added to Transcript)

Opening proofs demonstrate that the committed polynomials evaluate to the claimed values:

```python
# Prove a_blind(ω) = 0
proof_value_a = prove(S1, a_blind, ω)

# Prove b_blind(ω) = 1
proof_value_b = prove(S1, b_blind, ω)

# Prove c_blind(ω^4) = 9
proof_output = prove(S1, c_blind, ω^4)
```

**Important:** Opening proofs are **NOT** added to the transcript at this stage. They are computed for later verification.

## KZG Opening Proof

An opening proof for polynomial `p(x)` at point `γ` with value `v = p(γ)` works as follows:

1. **Quotient Polynomial:** Compute `Q(x) = (p(x) - v) / (x - γ)`
   - This is well-defined because `p(γ) = v` means `(x - γ)` divides `p(x) - v`

2. **Commitment:** Compute `π = commitment(S1, Q)` (the proof)

3. **Verification:** Check the pairing equation:
   ```
   e(C - vP, G2) = e(π, τG2 - γG2)
   ```
   where `C = commitment(S1, p)` is the original polynomial commitment.

## Why This Ordering?

The transcript must be built in a **specific order** that both prover and verifier agree upon:

1. **Public values first** - These are known to both parties
2. **Commitments next** - These hide the witness but bind the prover
3. **Challenges later** (next exercise) - Derived from the transcript hash

This ordering prevents the prover from cheating by choosing challenges after seeing commitments.

## Verification

The solution verifies that all opening proofs are correct:

```python
assert verify(c_a, proof_value_a, ω, value_a) == True
assert verify(c_b, proof_value_b, ω, value_b) == True
assert verify(c_c, proof_output, ω^4, value_c) == True
```

## Example Output

```
Inputs (at ω):
  a(ω) = 0 (expected 0)
  b(ω) = 1 (expected 1)

Output (at ω^4):
  c(ω^4) = 9 (expected 9)

Transcript state after Step 1:
  Length: 479 characters
  Contains: inputs (a(ω), b(ω)), output (c(ω^4)), commitments (c_a, c_b, c_c)

Verifying opening proofs:
  Verify a(ω) = 0: True
  Verify b(ω) = 1: True
  Verify c(ω^4) = 9: True
```

## Next Step (Exercise 20)

After building the initial transcript with public values and commitments, the next step will:
1. Generate challenge values β and γ by hashing the transcript
2. Interpolate the permutation polynomials z, N, D
3. Commit to the z polynomial
4. Continue building the transcript for the full proof

## Running the Solution

```bash
# From repo root - detailed version with manual commitment/proof functions
./run.sh sageless/solutions/exercise19/exercise19.py

# Simplified version using kzg.commit() and kzg.prove() API
./run.sh sageless/solutions/exercise19/exercise19_notebook_solution.py
```

## Notebook Solution (Cell 90)

The notebook provides a simplified API via `kzg.commit()` and `kzg.prove()` that wraps the lower-level `commitment(S1, poly)` and `proof(S1, Qc)` functions.

**Important:** Make sure to run cell 88 first to initialize the KZG setup:

```python
# Cell 88: Initialize KZG with trusted setup
kzg.set_trusted_setup(S1, S2)
```

Then the solution for cell 90:

```python
transcript = ""
value_a = a(ω)
value_b = b(ω)
value_c = c(pow(ω, 4, p))
transcript = push(value_a, transcript)
transcript = push(value_b, transcript)
transcript = push(value_c, transcript)
c_a = kzg.commit(a_blind)
c_b = kzg.commit(b_blind)
c_c = kzg.commit(c_blind)
transcript = push(c_a, transcript)
transcript = push(c_b, transcript)
transcript = push(c_c, transcript)
proof_value_a = kzg.prove(a_blind, ω)
proof_value_b = kzg.prove(b_blind, ω)
proof_output = kzg.prove(c_blind, pow(ω, 4, p))
```

## Key Concepts

- **Fiat-Shamir Transform:** Converting interactive to non-interactive proofs
- **Transcript:** Sequential record of protocol messages
- **KZG Commitments:** Hiding polynomial data with elliptic curve points
- **Opening Proofs:** Demonstrating polynomial evaluations without revealing the polynomial
- **Blinding:** Using vanishing polynomial multiples for zero-knowledge
- **Deterministic Challenges:** Deriving randomness from transcript hashes
