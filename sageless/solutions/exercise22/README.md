# Exercise 22: Evaluation Challenge and Opening Proofs

## Overview

This exercise generates the evaluation challenge ζ (zeta) and computes polynomial evaluations and KZG opening proofs. These are the final components needed for the verifier to check the proof without knowing the full polynomials.

## What This Exercise Does

### 1. Generate Evaluation Challenge ζ

Generate ζ by hashing the transcript (which now contains all commitments including the quotient):

```python
zeta = generate_challenge(transcript)
transcript = push(zeta, transcript)
```

**Purpose of ζ:** The verifier will check polynomial constraints at this random point ζ instead of checking at all domain points. By the Schwartz-Zippel lemma, if constraints hold at random ζ, they hold everywhere (with high probability).

### 2. Compute Polynomial Evaluations

Evaluate all key polynomials at ζ:

```python
a_zeta = a_blind(ζ)
b_zeta = b_blind(ζ)
c_zeta = c_blind(ζ)
z_zeta = z_poly(ζ)
t_zeta = quotient_poly(ζ)
```

Also evaluate z_poly at the shifted point ζ·ω:

```python
z_zeta_omega = z_poly(ζ·ω)
```

**Why ζ·ω?** The permutation recursive constraint compares z(x) with z(x·ω), so we need both evaluations.

### 3. Compute KZG Opening Proofs

For each evaluation, compute a proof that the polynomial actually has that value at that point:

```python
proof_a = kzg.prove(a_blind, ζ)
proof_b = kzg.prove(b_blind, ζ)
proof_c = kzg.prove(c_blind, ζ)
proof_z = kzg.prove(z_poly, ζ)
proof_t = kzg.prove(quotient_poly, ζ)
proof_z_omega = kzg.prove(z_poly, ζ·ω)
```

**What these prove:** Given a commitment C and claimed evaluation v at point γ, the proof π convinces the verifier that the committed polynomial actually evaluates to v at γ.

## Why These Evaluations?

The verifier needs these specific evaluations to reconstruct and verify the constraints:

### Gate Constraint at ζ

```
qM(ζ)·a_zeta·b_zeta + qL(ζ)·a_zeta + qR(ζ)·b_zeta - c_zeta
```

The verifier knows qM, qL, qR (public selector polynomials) and receives a_zeta, b_zeta, c_zeta from the prover.

### Permutation Start Constraint at ζ

```
(z_zeta - 1)·L1(ζ)
```

The verifier can compute L1(ζ) and receives z_zeta.

### Permutation Step Constraint at ζ

```
z_zeta · N(ζ) - D(ζ) · z_zeta_omega
```

The verifier can compute N(ζ) and D(ζ) from a_zeta, b_zeta, c_zeta and the permutation, and receives z_zeta and z_zeta_omega.

### Master Polynomial at ζ

```
t_gates(ζ) + α·t_perm_start(ζ) + α²·t_perm_step(ζ) = t_zeta · ZH(ζ)
```

The verifier can compute the left side from the evaluations above, and checks it equals t_zeta · ZH(ζ).

## The Opening Proof Protocol

For each polynomial p(x) with commitment C:

**Prover:**
1. Evaluates p(ζ) = v
2. Computes quotient Q(x) = (p(x) - v) / (x - ζ)
3. Computes proof π = Commit(Q)
4. Sends (v, π) to verifier

**Verifier:**
1. Receives commitment C, evaluation v, proof π
2. Verifies using pairing: e(C - vP, G2) ?= e(π, τG2 - ζG2)
3. This checks that p(ζ) = v without seeing p(x)

## Example Output

```
Generated ζ (zeta) from transcript:
  ζ = 4158651032974719439585929646923335258436936715866417430608850796987394005713

Evaluations at ζ:
  a_zeta = 20664302584436598926469537324561239532762815253061058625991781083976010202796
  b_zeta = 18821052363287104524690128587564915310107795625653425361383458368388242729744
  c_zeta = 17150435577054964976610611931657240199150165091352473932720726585516478232438
  z_zeta = 12105916267872840360871111822104977570094604541982494560767935982033570367735
  t_zeta = 1338698677736897310024523073368313251908315057636090488776078760468572121104

Evaluation at ζ·ω:
  z_zeta_omega = 1680703183773738770974154288061026194841137982744455453814681814340245852583

Opening proofs computed and verified:
  Verify a_blind(ζ): True ✓
  Verify b_blind(ζ): True ✓
  Verify c_blind(ζ): True ✓
  Verify z_poly(ζ): True ✓
  Verify quotient_poly(ζ): True ✓
  Verify z_poly(ζ·ω): True ✓

✓✓✓ ALL OPENING PROOFS VERIFIED SUCCESSFULLY ✓✓✓
```

## Proof Artifacts Sent to Verifier

The prover sends these to the verifier:

### Commitments (from previous exercises)
- c_a: Commitment to a_blind
- c_b: Commitment to b_blind
- c_c: Commitment to c_blind
- c_z: Commitment to z_poly
- c_t: Commitment to quotient_poly

### Evaluations (this exercise)
- a_zeta, b_zeta, c_zeta
- z_zeta
- t_zeta
- z_zeta_omega

### Opening Proofs (this exercise)
- proof_a, proof_b, proof_c
- proof_z
- proof_t
- proof_z_omega

### Public Inputs (known to both)
- a(ω) = 0
- b(ω) = 1
- c(ω^4) = 9

**Total proof size:** 5 commitments + 6 evaluations + 6 proofs = constant size regardless of circuit complexity!

## Notebook Solution (Cell 96)

```python
zeta = generate_challenge(transcript)
transcript = push(zeta, transcript)

# Evaluate polynomials at ζ
a_zeta = a_blind(zeta)
b_zeta = b_blind(zeta)
c_zeta = c_blind(zeta)
z_zeta = z_poly(zeta)
t_zeta = quotient_poly(zeta)

# Evaluate z_poly at ζ·ω
zeta_omega = (zeta * ω) % p
z_zeta_omega = z_poly(zeta_omega)

# Compute KZG opening proofs
proof_a = kzg.prove(a_blind, zeta)
proof_b = kzg.prove(b_blind, zeta)
proof_c = kzg.prove(c_blind, zeta)
proof_z = kzg.prove(z_poly, zeta)
proof_t = kzg.prove(quotient_poly, zeta)
proof_z_omega = kzg.prove(z_poly, zeta_omega)
```

## Running the Solution

```bash
# From repo root
./run.sh sageless/solutions/exercise22/exercise22.py
```

## Why Check at ζ Instead of All Domain Points?

### Naive Approach
Check constraints at all n domain points:
- Send n values for each polynomial
- Proof size: O(n)
- Not succinct!

### PlonK Approach
Check constraints at ONE random point ζ:
- Send 1 value per polynomial + opening proof
- Proof size: O(1) (constant!)
- By Schwartz-Zippel lemma: if constraints hold at random ζ, they hold everywhere with overwhelming probability

**This is why PlonK is a SNARK:** Succinct (constant size) proof!

## The Schwartz-Zippel Lemma

**Statement:** If a non-zero polynomial p(x) of degree d has at most d roots, then for random ζ:
```
Pr[p(ζ) = 0] ≤ d / |Field|
```

**Application:** If constraints are violated, the constraint polynomial is non-zero. Checking at random ζ catches violations with high probability (1 - d/|Field| ≈ 1).

## Why z_poly at Two Points?

The recursive permutation constraint is:
```
z(x) · N(x) - D(x) · z(x·ω) = 0
```

At evaluation point ζ, this becomes:
```
z(ζ) · N(ζ) - D(ζ) · z(ζ·ω) = 0
```

So we need:
- z(ζ) → z_zeta
- z(ζ·ω) → z_zeta_omega

Both evaluations (and their proofs) are necessary to check this constraint.

## Transcript State After Exercise 22

1. ✓ Public inputs/outputs
2. ✓ Witness commitments (c_a, c_b, c_c)
3. ✓ Challenge β
4. ✓ Challenge γ
5. ✓ Permutation commitment (c_z)
6. ✓ Challenge α
7. ✓ Quotient commitment (c_t)
8. ✓ Challenge ζ

The prover has now:
- Generated all challenges via Fiat-Shamir
- Computed all commitments
- Computed all evaluations and opening proofs

The proof is complete! Next step would be verifier implementation.

## Key Concepts

- **Evaluation Challenge ζ:** Random point for checking constraints
- **Opening Proofs:** Cryptographic proofs of polynomial evaluations
- **KZG Protocol:** Commit-and-prove scheme using pairings
- **Schwartz-Zippel Lemma:** Probabilistic polynomial identity testing
- **Succinctness:** Constant-size proof regardless of circuit size
- **Shifted Evaluation:** z(ζ·ω) for recursive constraint checking
- **Fiat-Shamir:** Non-interactive challenge generation from transcript
- **Proof Artifacts:** Commitments + evaluations + opening proofs

## Connection to Verifier

With all these artifacts, the verifier can:

1. **Reconstruct the transcript** (same order as prover)
2. **Generate challenges** β, γ, α, ζ (via Fiat-Shamir)
3. **Compute constraint polynomials at ζ** using the evaluations
4. **Verify opening proofs** using pairings
5. **Check master polynomial equation** holds at ζ

If all checks pass, the verifier is convinced the prover knows a valid witness satisfying the circuit, without seeing the witness itself!
