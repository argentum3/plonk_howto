# Exercise 17: Interpolating z, N, and D Polynomials

## Overview

This exercise implements the **core of PlonK's permutation argument** by computing and interpolating three critical polynomials:
- **z**: The recursive accumulator polynomial
- **N**: The numerator polynomial
- **D**: The denominator polynomial

These polynomials enable efficient verification that the permutation σ correctly encodes all copy constraints in the circuit.

## The Recursive z Function

### Definition

The z polynomial satisfies a recursive relation:

$$z(\omega^{i+1}) = z(\omega^i) \cdot \frac{\text{numerator}(i)}{\text{denominator}(i)}$$

with boundary condition:

$$z(\omega) = 1$$

### Key Property

In the multiplicative domain, the cyclic property holds:

$$z(\omega^{n+1}) = z(\omega^n \cdot \omega) = z(\omega) = 1$$

This automatically ensures the grand product equals 1 if the permutation is valid!

### Why This Works

The z polynomial "accumulates" the ratios of numerators to denominators:

```
z(ω¹) = 1                                    (base case)
z(ω²) = z(ω¹) · num(1) / den(1)
z(ω³) = z(ω²) · num(2) / den(2) = z(ω¹) · num(1)/den(1) · num(2)/den(2)
...
z(ω^(n+1)) = z(ω¹) · ∏ [num(i) / den(i)]    (grand product)
```

If the permutation is valid, this grand product equals 1, so z(ω^(n+1)) = z(ω) = 1.

## N and D Polynomials

### Numerator Polynomial N

At each point ω^i, N captures the product of numerators across all columns:

$$N(\omega^i) = \text{numerator}(i, 1, a) \cdot \text{numerator}(i, 2, b) \cdot \text{numerator}(i, 3, c)$$

### Denominator Polynomial D

At each point ω^i, D captures the product of denominators across all columns:

$$D(\omega^i) = \text{denominator}(i, 1, a) \cdot \text{denominator}(i, 2, b) \cdot \text{denominator}(i, 3, c)$$

### Purpose

Having N and D as polynomials allows the verifier to check the recursive constraint efficiently using polynomial identities rather than evaluating at every point.

## Implementation

```python
def interpolate_z_N_D(a, b, c, beta, gamma, Ω):
    n = len(Ω)
    z_values = []
    N_values = []
    D_values = []

    # Initialize z(ω) = 1
    z_current = 1

    for i in range(1, n + 1):
        # Store current z value
        z_values.append(z_current)

        # Compute N and D at this index
        num_a = numerator(i, 1, a, sigma, beta, gamma)
        num_b = numerator(i, 2, b, sigma, beta, gamma)
        num_c = numerator(i, 3, c, sigma, beta, gamma)
        N_i = (num_a * num_b * num_c) % p
        N_values.append(N_i)

        den_a = denominator(i, 1, a, sigma, beta, gamma)
        den_b = denominator(i, 2, b, sigma, beta, gamma)
        den_c = denominator(i, 3, c, sigma, beta, gamma)
        D_i = (den_a * den_b * den_c) % p
        D_values.append(D_i)

        # Update z: z(ω^(i+1)) = z(ω^i) · N(ω^i) / D(ω^i)
        D_i_inv = pow(D_i, p - 2, p)
        z_current = (z_current * N_i * D_i_inv) % p

    # Interpolate over Ω
    z = interpolate(Ω, z_values)
    N = interpolate(Ω, N_values)
    D = interpolate(Ω, D_values)

    return z, N, D
```

## Validation Checks

The solution must pass two critical checks from the notebook (cells 73-78):

### Check 1: Boundary Condition

**Property:** z(ω) = 1

**Check:** ZH divides L1*(z-1)

Where:
- **L1** = Lagrange basis polynomial for the first point in Ω
- **ZH** = x^n - 1 (vanishing polynomial for Ω)

```python
L1 = ∏_{m=2}^{n} (x - ω^m) / (ω - ω^m)
ZH = x^4 - 1

# L1*(z-1) should be divisible by ZH
assert ZH.divides(L1 * (z - 1))
```

**Why:** L1 is 1 at ω and 0 at all other points in Ω. So L1*(z-1) isolates the constraint z(ω)-1 = 0, and if this holds, ZH divides it.

### Check 2: Recursive Constraint

**Property:** z satisfies the recursive relation at all points in Ω

**Check:** ZH divides z*N - D*z(x*ω)

```python
# z*N - D*z(x*ω) should be divisible by ZH
assert ZH.divides(z * N - D * z(x * ω))
```

**Why:** The recursive constraint is:

$$z(\omega^{i+1}) = z(\omega^i) \cdot \frac{N(\omega^i)}{D(\omega^i)}$$

Rearranging: $z(\omega^i) \cdot N(\omega^i) - D(\omega^i) \cdot z(\omega^{i+1}) = 0$

As a polynomial identity: $z(x) \cdot N(x) - D(x) \cdot z(x \cdot \omega) = 0$ at all points in Ω, so ZH divides it.

## Example Results

With β=42, γ=42, n=4:

### Polynomial Degrees
```
deg(z) = 3
deg(N) = 3
deg(D) = 3
```

All polynomials have degree 3 (interpolating 4 points over Ω).

### z Values at Domain Points
```
z(ω¹) = 1                                  (base case ✓)
z(ω²) = 7854842570287149688817374956698180...
z(ω³) = 11077482521604943021473939334908530...
z(ω⁴) = 15398124345886931987743111018465873...
z(ω⁵) = z(ω) = 1                          (cyclic property ✓)
```

### Validation Results
```
✓ Check 1: ZH divides L1*(z-1) = True
✓ Check 2: ZH divides z*N - D*z(x*ω) = True
```

Both checks pass, confirming the permutation σ correctly encodes all copy constraints!

## The Succinct Argument

The power of this approach:

1. **Prover commits** to polynomials a, b, c
2. **Verifier challenges** with random β, γ
3. **Prover computes** z, N, D and commits to them
4. **Verifier checks**:
   - Boundary: z(ω) = 1
   - Recursive: z*N - D*z(x*ω) = 0 on Ω

If both checks pass, the verifier is convinced (with high probability) that:
- All copy constraints are satisfied
- The circuit is correctly wired
- The computation is valid

All without revealing individual wire values! 🎯

## Mathematical Insight

### Why z(ω^(n+1)) = 1 Implies Valid Permutation

The z polynomial encodes the cumulative product:

$$z(\omega^{n+1}) = \prod_{i=1}^{n} \prod_{col=1}^{3} \frac{\text{pos}(col,i) + \beta \cdot f(\omega^i) + \gamma}{\sigma(\text{pos}(col,i)) + \beta \cdot f(\omega^i) + \gamma}$$

Since σ is a permutation (bijection), every position appears once in numerators and once in denominators (in different orders).

If wire values match within cycles (copy constraints satisfied), the terms cancel perfectly, giving product = 1.

Therefore: **z(ω^(n+1)) = 1 ⟺ permutation is valid**

## Running the Exercise

```bash
# From repo root
./run.sh sageless/solutions/exercise17/exercise17.py

# Or with venv activated
cd sageless/solutions/exercise17
./exercise17.py
```

## Output

```
======================================================================
EXERCISE 17: INTERPOLATING Z, N, D POLYNOMIALS
======================================================================

Polynomial degrees:
  deg(z) = 3
  deg(N) = 3
  deg(D) = 3

Verifying z values at domain points:
  z(ω¹) = 1
  ✓ Base case: z(ω) = 1 (expected 1)
  ✓ Cyclic property: z(ω⁵) = z(ω) = 1

Validation checks:
  Check 1: ZH divides L1*(z-1): True
  ✓ PASS

  Check 2: ZH divides z*N - D*z(x*ω): True
  ✓ PASS

✓ Exercise 17 Complete!

The z polynomial successfully encodes the permutation argument:
  - Satisfies boundary condition z(ω) = 1
  - Satisfies recursive constraint at all points in Ω
  - Can be used to prove copy constraints without revealing wire values
```

## What's Next?

The z, N, and D polynomials are now ready to be used in the full PlonK protocol. The prover will:
1. Commit to z, N, D using KZG commitments
2. Compute opening proofs at challenge points
3. Send these to the verifier

The verifier can then efficiently check the permutation argument without evaluating at every point!

---

**PlonK Tutorial - Exercise 17**
**Interpolating z, N, D polynomials for permutation argument ✓**
