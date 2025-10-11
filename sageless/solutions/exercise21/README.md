# Exercise 21: Master Polynomial Construction

## Overview

This exercise builds the "master polynomial" that combines both gate constraints and permutation constraints into a single polynomial, which is more efficient than checking each constraint separately. The master polynomial is then divided by the vanishing polynomial to produce the quotient polynomial that will be verified.

## What This Exercise Does

### 1. Generate Challenge α

Generate a random challenge α by hashing the transcript (which now contains witness commitments, β, γ, and z commitment):

```python
alpha = generate_challenge(transcript)
transcript = push(alpha, transcript)
```

**Purpose of α:** Used to combine multiple constraint polynomials into one, preventing the prover from satisfying individual constraints independently while failing overall.

### 2. Compute L1 Lagrange Polynomial

L1 is the Lagrange basis polynomial for the first domain point ω:

```python
L1(x) = ∏_{m=2}^{n} (x - ω^m) / (ω - ω^m)
```

**Properties:**
- L1(ω) = 1
- L1(ω^i) = 0 for i ≠ 1

**Purpose:** Used to enforce boundary conditions (specifically z(ω) = 1)

### 3. Compute Gate Constraint Polynomial

The gate constraint encodes all circuit gates:

```python
t_gates = qM · a_blind · b_blind + qL · a_blind + qR · b_blind - c_blind
```

**Meaning:** At each domain point ω^i, this should equal zero if the gate constraint is satisfied:
- Gates 1-3: Multiplication gates (qM=0, qL=1, qR=1) → a + b = c
- Gate 4: Addition gate (qM=1, qL=0, qR=0) → a · b = c

### 4. Compute Permutation Constraints

Two permutation constraints ensure copy constraints are satisfied:

#### Boundary Constraint (Permutation Start)

```python
t_perm_start = (z_poly - 1) · L1
```

This ensures z(ω) = 1 (the accumulator starts at 1).

#### Recursive Constraint (Permutation Step)

```python
z_shifted = z_poly(x · ω)
t_perm_step = z_poly · N_poly - D_poly · z_shifted
```

This ensures the recursive relation holds:
```
z(ω^(i+1)) = z(ω^i) · N(ω^i) / D(ω^i)
```

### 5. Build Master Polynomial

Combine all constraints using powers of α:

```python
bigt = t_gates + α · t_perm_start + α² · t_perm_step
```

**Why use powers of α?**
- Different constraints are "separated" by α
- Prevents the prover from finding a polynomial that satisfies the combination without satisfying each individual constraint
- Uses the Schwartz-Zippel lemma: if bigt = 0 at all domain points, then (with high probability) each component is also zero

### 6. Compute Quotient Polynomial

Divide the master polynomial by the vanishing polynomial:

```python
quotient_poly = bigt / ZH
```

**Key property:** If all constraints are satisfied, then:
- bigt(ω^i) = 0 for all i (all constraints hold at all domain points)
- Therefore ZH divides bigt exactly
- The quotient polynomial exists and has no remainder

## Why This Works

### The Vanishing Polynomial

ZH(x) = x^n - 1 has the special property that:
- ZH(ω^i) = 0 for all i in the domain
- ZH(x) ≠ 0 for x outside the domain

### Constraint Encoding

If a polynomial t(x) equals zero at all domain points:
- t(ω^1) = 0
- t(ω^2) = 0
- ...
- t(ω^n) = 0

Then ZH(x) divides t(x), meaning t(x) = Q(x) · ZH(x) for some quotient Q(x).

### Combining Constraints

The master polynomial satisfies:
```
bigt(ω^i) = t_gates(ω^i) + α · t_perm_start(ω^i) + α² · t_perm_step(ω^i)
```

At each domain point ω^i, all three components must be zero for bigt(ω^i) to be zero. The random α ensures that if any component is non-zero, bigt won't be zero (except with negligible probability).

## Example Output

```
Generated α from transcript:
  α = 12464028492477784364728600744235585500676832950276579604946694877271139099497

Computing L1 polynomial...
  L1: degree 3

Computing t_gates...
  t_gates: degree 13

Computing t_perm_start...
  t_perm_start: degree 6

Computing t_perm_step...
  t_perm_step: degree 6

Computing master polynomial bigt...
  bigt: degree 13

Computing quotient polynomial...
  quotient_poly: degree 9
  ✓ ZH divides bigt exactly (remainder is zero)

Verification checks:
  ZH divides t_gates: True
  ZH divides t_perm_start: True
  ZH divides t_perm_step: True
  ZH divides bigt: True

✓✓✓ ALL VERIFICATION CHECKS PASSED ✓✓✓
```

## Polynomial Degrees

Understanding the degrees helps verify correctness:

- **a_blind, b_blind, c_blind:** degree 3 + blinding (degree 5)
- **z_poly, N_poly, D_poly:** degree 3
- **qL, qR, qM:** degree 3
- **L1:** degree 3
- **ZH:** degree 4

**t_gates = qM · a_blind · b_blind + qL · a_blind + qR · b_blind - c_blind**
- Degree: max(deg(qM) + deg(a_blind) + deg(b_blind), deg(qL) + deg(a_blind), ...) = 3+5+5 = 13

**t_perm_start = (z_poly - 1) · L1**
- Degree: deg(z_poly) + deg(L1) = 3 + 3 = 6

**t_perm_step = z_poly · N_poly - D_poly · z_shifted**
- Degree: max(deg(z_poly) + deg(N_poly), deg(D_poly) + deg(z_poly)) = 3 + 3 = 6

**bigt**
- Degree: max(deg(t_gates), deg(t_perm_start), deg(t_perm_step)) = 13

**quotient_poly = bigt / ZH**
- Degree: deg(bigt) - deg(ZH) = 13 - 4 = 9

## Notebook Solution (Cell 94)

```python
alpha = generate_challenge(transcript)
transcript = push(alpha, transcript)

# Compute L1 polynomial
L1_factors = []
for m in range(2, n + 1):
    ω_m = pow(ω, m, p)
    numerator_poly = x - ω_m
    denominator_scalar = (ω - ω_m) % p
    denominator_inv = pow(denominator_scalar, p - 2, p)
    factor = numerator_poly * denominator_inv
    L1_factors.append(factor)

L1 = Polynomial([1], p)
for factor in L1_factors:
    L1 = L1 * factor

# Gate constraint
t_gates = qM * a_blind * b_blind + qL * a_blind + qR * b_blind - c_blind

# Permutation constraints
t_perm_start = (z_poly - 1) * L1
z_shifted = z_poly(x * ω)
t_perm_step = z_poly * N_poly - D_poly * z_shifted

# Master polynomial
bigt = t_gates + alpha * t_perm_start + (alpha * alpha) * t_perm_step

# Quotient polynomial
quotient_poly, remainder = bigt.quo_rem(ZH)

# Commit and push to transcript
c_t = kzg.commit(quotient_poly)
transcript = push(c_t, transcript)
```

## Running the Solution

```bash
# From repo root
./run.sh sageless/solutions/exercise21/exercise21.py
```

## Connection to PlonK Protocol

After this step, the transcript contains:
1. **Public inputs/outputs** (a(ω), b(ω), c(ω^4))
2. **Witness commitments** (c_a, c_b, c_c)
3. **Permutation challenges** (β, γ)
4. **Permutation commitment** (c_z)
5. **Combination challenge** (α)
6. **Quotient commitment** (c_t)

Next steps (Exercise 22+):
- Generate evaluation challenge ζ
- Compute polynomial evaluations at ζ
- Compute opening proofs for all evaluations
- Final verification by the verifier

## Key Concepts

- **Master Polynomial:** Combines all constraints into single polynomial
- **Random Linear Combination:** Using α to combine constraints securely
- **Schwartz-Zippel Lemma:** Ensures component constraints are satisfied
- **Quotient Polynomial:** Proves all constraints hold by exact division
- **Vanishing Polynomial:** ZH(x) = x^n - 1 is zero on the domain
- **L1 Lagrange Polynomial:** Selects the first domain point for boundary conditions
- **Polynomial Shifting:** z_poly(x·ω) shifts evaluations by one step in the domain
- **Blinded Witness:** Uses a_blind, b_blind, c_blind for zero-knowledge

## Why Powers of α?

Using α, α², α³, ... for different constraints is crucial:

**Without powers:** `bigt = t1 + t2 + t3`
- If t1(x) = α, t2(x) = -α, t3(x) = 0, then bigt(x) = 0
- But individual constraints are NOT satisfied!

**With powers:** `bigt = t1 + α·t2 + α²·t3`
- For bigt(x) = 0, we need: t1(x) + α·t2(x) + α²·t3(x) = 0
- This is a polynomial equation in α
- By Schwartz-Zippel, with high probability, each coefficient must be zero
- Therefore t1(x) = 0, t2(x) = 0, t3(x) = 0

This ensures that satisfying the combined constraint implies satisfying each individual constraint.
