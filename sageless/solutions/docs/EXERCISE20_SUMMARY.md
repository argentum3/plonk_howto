# Exercise 20 Summary: Challenges and Permutation Polynomials

## Task Completed

Created a complete solution for Exercise 20 that generates cryptographic challenges β and γ from the Fiat-Shamir transcript and computes the permutation polynomials z, N, and D.

## Files Created

1. **[sageless/solutions/exercise20/exercise20.py](sageless/solutions/exercise20/exercise20.py)**
   - Complete implementation with detailed comments
   - Builds on Exercise 19 transcript
   - Generates challenges via SHA256 hashing
   - Computes permutation polynomials
   - Commits to z polynomial
   - Full verification checks

2. **[sageless/solutions/exercise20/README.md](sageless/solutions/exercise20/README.md)**
   - Comprehensive explanation of the permutation argument
   - Details on β and γ challenges
   - Grand product argument theory
   - Verification checks explained
   - Connection to full PlonK protocol

3. **Updated [sageless/solutions/README.md](sageless/solutions/README.md)**
   - Added Exercise 20 entry with key features

4. **Updated notebook cell 92**
   - Proper template with placeholders

## Solution for Notebook Cell 92

```python
beta = generate_challenge(transcript)
transcript = push(beta, transcript)
gamma = generate_challenge(transcript)
transcript = push(gamma, transcript)
z_poly, N_poly, D_poly = interpolate_z_N_D(a_blind, b_blind, c_blind, beta, gamma, Ω)
c_z = kzg.commit(z_poly)
transcript = push(c_z, transcript)
```

## What Exercise 20 Does

### 1. Generate Challenge β
- Hash the transcript (containing public values and witness commitments from Exercise 19)
- β = SHA256(transcript) mod p
- Push β to transcript

**Purpose:** Randomizes position values in the permutation argument, preventing adaptive attacks.

### 2. Generate Challenge γ
- Hash the updated transcript (now including β)
- γ = SHA256(transcript) mod p
- Push γ to transcript

**Purpose:** Provides additional randomization for the grand product argument.

### 3. Compute Permutation Polynomials

Using `interpolate_z_N_D(a_blind, b_blind, c_blind, beta, gamma, Ω)`:

**z polynomial (accumulator):**
- Starts with z(ω) = 1
- Recursive: z(ω^(i+1)) = z(ω^i) · N(ω^i)/D(ω^i)
- Encodes whether copy constraints are satisfied

**N polynomial (numerator):**
- At each ω^i: product of (pos(col,i) + β·f(ω^i) + γ) across all columns
- Represents "before permutation" side

**D polynomial (denominator):**
- At each ω^i: product of (σ(pos(col,i)) + β·f(ω^i) + γ) across all columns
- Represents "after permutation" side

### 4. Commit to z Polynomial
- Compute KZG commitment: c_z = kzg.commit(z_poly)
- Push c_z to transcript
- Binds prover to the permutation polynomial

## Verification Checks

The solution verifies two critical properties:

### ✓ Boundary Constraint
```python
ZH.divides(L1*(z_poly - 1))  # True
```
Ensures z(ω) = 1 (base case for the accumulator)

### ✓ Recursive Constraint
```python
ZH.divides(z_poly*N_poly - D_poly*z_poly(x*ω))  # True
```
Ensures the recursive relation holds at all domain points:
z(ω^(i+1)) = z(ω^i) · N(ω^i)/D(ω^i)

## Example Output

```
Generated β from transcript:
  β = 7224896729028834562147655171186897061331430588527250603518635716474580271817

Generated γ from transcript:
  γ = 16971512203087827843483978066304851308454453825779853063148616973330593773830

Computing permutation polynomials...
  z_poly: degree 3
  N_poly: degree 3
  D_poly: degree 3

Verification: z(ω) = 1 ✓

Verification checks:
  ZH divides L1*(z-1): True ✓
  ZH divides z*N - D*z(x*ω): True ✓
```

## Key Concepts

### Grand Product Argument
The permutation argument uses a grand product to efficiently verify all copy constraints at once:

```
∏(position + β·f(ω^i) + γ) / ∏(σ(position) + β·f(ω^i) + γ) = 1
```

This equals 1 if and only if all values in each equivalence class (defined by σ) are equal.

### Why β and γ?
- **β:** Prevents the prover from finding polynomial values that satisfy the check without actually satisfying copy constraints
- **γ:** Ensures soundness when some numerators/denominators might be zero
- **Together:** Make it cryptographically hard to cheat the permutation check

### The z Accumulator
Rather than checking the full product at once, z builds it up incrementally:
- z(ω^1) = 1
- z(ω^2) = z(ω^1) · N(ω^1)/D(ω^1)
- z(ω^3) = z(ω^2) · N(ω^2)/D(ω^2)
- z(ω^4) = z(ω^3) · N(ω^3)/D(ω^3)

If copy constraints hold, z should cycle back to 1 after completing the domain.

## Transcript State After Exercise 20

The transcript now contains:
1. ✓ Public inputs/outputs (a(ω), b(ω), c(ω^4))
2. ✓ Witness commitments (c_a, c_b, c_c)
3. ✓ Challenge β
4. ✓ Challenge γ
5. ✓ Permutation commitment (c_z)

## Testing

```bash
# Run the solution
./run.sh sageless/solutions/exercise20/exercise20.py

# Expected output: All verification checks pass ✓
```

## Next Steps

Exercise 21 will:
- Generate challenge α for combining constraints
- Build the master polynomial combining gate and permutation constraints
- Continue building toward the quotient polynomial

## Connection to PlonK Protocol

Exercise 20 completes the second major phase of PlonK proof generation:

**Phase 1 (Ex 19):** Commit to witness polynomials
**Phase 2 (Ex 20):** ← We are here - Generate permutation challenges and commit to z
**Phase 3 (Ex 21+):** Combine constraints and compute quotient polynomial
**Phase 4:** Evaluation and opening proofs

The permutation argument is one of PlonK's key innovations, allowing efficient verification of arbitrary copy constraints across the circuit.
