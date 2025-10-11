# Exercise 21 Summary: Master Polynomial Construction

## Task Completed

Created a complete solution for Exercise 21 that builds the master polynomial by combining gate constraints and permutation constraints using random challenge α, then computes the quotient polynomial.

## Files Created

1. **[sageless/solutions/exercise21/exercise21.py](sageless/solutions/exercise21/exercise21.py)**
   - Complete implementation with detailed output
   - Builds on Exercises 19-20 transcript
   - Generates challenge α via SHA256 hashing
   - Computes L1 Lagrange polynomial
   - Builds gate and permutation constraints
   - Combines into master polynomial
   - Computes quotient polynomial
   - Full verification checks

2. **[sageless/solutions/exercise21/README.md](sageless/solutions/exercise21/README.md)**
   - Comprehensive explanation of master polynomial
   - Details on each constraint component
   - Schwartz-Zippel lemma explanation
   - Polynomial degree analysis
   - Why powers of α are crucial

3. **Updated [sageless/solutions/README.md](sageless/solutions/README.md)**
   - Added Exercise 21 entry

4. **Updated notebook cell 94**
   - Complete solution with 88 lines
   - Detailed print statements
   - Verification checks

## Solution for Notebook Cell 94

The complete solution computes:

```python
# 1. Generate challenge α
alpha = generate_challenge(transcript)
transcript = push(alpha, transcript)

# 2. Compute L1 Lagrange polynomial
L1 = ∏_{m=2}^{n} (x - ω^m) / (ω - ω^m)

# 3. Gate constraint
t_gates = qM · a_blind · b_blind + qL · a_blind + qR · b_blind - c_blind

# 4. Permutation constraints
t_perm_start = (z_poly - 1) · L1
z_shifted = z_poly(x · ω)
t_perm_step = z_poly · N_poly - D_poly · z_shifted

# 5. Master polynomial
bigt = t_gates + α · t_perm_start + α² · t_perm_step

# 6. Quotient polynomial
quotient_poly = bigt / ZH

# 7. Commit and push
c_t = kzg.commit(quotient_poly)
transcript = push(c_t, transcript)
```

## What Exercise 21 Does

### The Master Polynomial Concept

Instead of checking each constraint separately:
- Gate constraint: qM·a·b + qL·a + qR·b = c
- Permutation boundary: z(ω) = 1
- Permutation recursive: z(ω^(i+1)) = z(ω^i)·N(ω^i)/D(ω^i)

We combine them all into ONE polynomial using a random challenge α:

```
bigt = t_gates + α·t_perm_start + α²·t_perm_step
```

### Why This Works

By the **Schwartz-Zippel lemma**, if bigt = 0 at all domain points, then with overwhelming probability:
- t_gates = 0 at all domain points
- t_perm_start = 0 at all domain points
- t_perm_step = 0 at all domain points

This means ALL constraints are satisfied!

### The Quotient Polynomial

If all constraints hold:
- Each component t_i(ω^j) = 0 for all domain points ω^j
- Therefore bigt(ω^j) = 0 for all domain points
- Therefore ZH(x) divides bigt(x) exactly
- The quotient quotient_poly = bigt / ZH exists with no remainder

The verifier will later check this quotient to verify all constraints.

## Polynomial Breakdown

### Inputs to Master Polynomial

| Polynomial | Degree | Meaning |
|------------|--------|---------|
| a_blind, b_blind, c_blind | 5 | Blinded witness (degree 3 + blinding) |
| z_poly, N_poly, D_poly | 3 | Permutation accumulator and products |
| qL, qR, qM | 3 | Selector polynomials |
| L1 | 3 | Lagrange basis for first point |
| ZH | 4 | Vanishing polynomial x^4 - 1 |

### Constraint Polynomials

| Constraint | Formula | Degree | What it checks |
|------------|---------|--------|----------------|
| t_gates | qM·a_blind·b_blind + qL·a_blind + qR·b_blind - c_blind | 13 | All gate constraints |
| t_perm_start | (z_poly - 1)·L1 | 6 | z(ω) = 1 (boundary) |
| t_perm_step | z_poly·N_poly - D_poly·z_poly(x·ω) | 6 | Recursive relation |

### Output

| Polynomial | Degree | Purpose |
|------------|--------|---------|
| bigt | 13 | Combined constraints |
| quotient_poly | 9 | Proof that ZH divides bigt |

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
  bigt = t_gates + α·t_perm_start + α²·t_perm_step
  bigt: degree 13

Computing quotient polynomial...
  quotient_poly = bigt / ZH
  quotient_poly: degree 9
  ✓ ZH divides bigt exactly

Verification:
  ZH divides t_gates: True ✓
  ZH divides t_perm_start: True ✓
  ZH divides t_perm_step: True ✓
  ZH divides bigt (master): True ✓

✓✓✓ ALL VERIFICATION CHECKS PASSED ✓✓✓
```

## Key Technical Details

### Selector Polynomials (Important Fix!)

The correct selector values are:
```python
SL = {1: 1, 2: 1, 3: 1, 4: 0}  # Gates 1-3: addition, Gate 4: no left input
SR = {1: 1, 2: 1, 3: 1, 4: 0}  # Gates 1-3: addition, Gate 4: no right input
SM = {1: 0, 2: 0, 3: 0, 4: 1}  # Gates 1-3: no mult, Gate 4: multiplication
```

This represents:
- Gates 1-3: **Addition gates** (a + b = c)
- Gate 4: **Multiplication gate** (a · b = c)

### Why Powers of α?

Using α, α², α³ for different constraints is CRUCIAL for security:

**Bad (without powers):**
```
bigt = t1 + t2 + t3
```
Problem: Could have t1 = α, t2 = -α, t3 = 0 → bigt = 0, but constraints not satisfied!

**Good (with powers):**
```
bigt = t1 + α·t2 + α²·t3
```
For bigt = 0, we need: t1 + α·t2 + α²·t3 = 0

This is a polynomial equation in α. By Schwartz-Zippel, for random α, this holds with high probability only if:
- Coefficient of α^0: t1 = 0
- Coefficient of α^1: t2 = 0
- Coefficient of α^2: t3 = 0

Therefore each individual constraint must be satisfied!

### The L1 Polynomial

L1 is the Lagrange basis polynomial for the first domain point:

```python
L1(x) = ∏_{m=2}^{n} (x - ω^m) / (ω - ω^m)
```

Properties:
- L1(ω^1) = L1(ω) = 1
- L1(ω^2) = 0
- L1(ω^3) = 0
- L1(ω^4) = 0

This "selects" the first point, allowing us to enforce z(ω) = 1:
```
t_perm_start = (z_poly - 1) · L1
```
At ω: t_perm_start(ω) = (z(ω) - 1) · 1 = 0 → z(ω) = 1 ✓
At other points: t_perm_start(ω^i) = (z(ω^i) - 1) · 0 = 0 ✓

### Polynomial Shifting

`z_shifted = z_poly(x · ω)` shifts the polynomial evaluation by one step:

- z_poly(ω^1) evaluates at ω^1
- z_shifted(ω^1) = z_poly(ω^1 · ω) = z_poly(ω^2)

This allows comparing consecutive values:
```
t_perm_step = z_poly · N_poly - D_poly · z_shifted
```

At ω^i:
```
t_perm_step(ω^i) = z(ω^i) · N(ω^i) - D(ω^i) · z(ω^(i+1))
```

For this to be zero:
```
z(ω^i) · N(ω^i) = D(ω^i) · z(ω^(i+1))
z(ω^(i+1)) = z(ω^i) · N(ω^i) / D(ω^i)
```

This is exactly the recursive relation we need!

## Transcript State After Exercise 21

1. ✓ Public inputs/outputs
2. ✓ Witness commitments (c_a, c_b, c_c)
3. ✓ Challenge β
4. ✓ Challenge γ
5. ✓ Permutation commitment (c_z)
6. ✓ Challenge α
7. ✓ Quotient commitment (c_t)

## Testing

```bash
./run.sh sageless/solutions/exercise21/exercise21.py
```

Expected: All verification checks pass ✓

## Next Steps

Exercise 22 will:
- Generate evaluation challenge ζ
- Evaluate polynomials at ζ
- Compute opening proofs
- Complete the proof assembly

## Connection to PlonK Protocol

Exercise 21 represents the third major phase of PlonK:

**Phase 1 (Ex 19):** Commit to witness polynomials
**Phase 2 (Ex 20):** Generate permutation challenges, commit to z
**Phase 3 (Ex 21):** ← We are here - Combine all constraints, commit to quotient
**Phase 4 (Ex 22+):** Evaluation and opening proofs

The quotient polynomial is the heart of PlonK - it proves that all constraints (both gates and permutations) are satisfied simultaneously, in a succinct way that the verifier can check efficiently.
