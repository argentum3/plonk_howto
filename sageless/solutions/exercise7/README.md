# Exercise 7: KZG Trusted Setup

## Problem

Compute the **trusted setup parameters** for the KZG polynomial commitment scheme:

1. **S₁**: A vector of powers of τ in G₁
   ```
   S₁ = [P, τ·P, τ²·P, τ³·P, ..., τˡ·P]
   ```

2. **S₂**: τ·Q in G₂
   ```
   S₂ = τ·Q
   ```

Where:
- **τ (tau) = 424242** - The "toxic waste" (secret random value)
- **l = 10** - Maximum polynomial degree
- **P** - Generator of G₁ (BN254 curve)
- **Q** - Generator of G₂ (BN254 curve)

## What is a Trusted Setup?

The trusted setup is a one-time ceremony that creates **public parameters** for the KZG scheme. These parameters allow:
- **Provers** to commit to polynomials
- **Verifiers** to check proofs
- Both parties to do this **without knowing τ**

### The Toxic Waste Problem

The secret τ must be **destroyed** after computing S₁ and S₂. If anyone learns τ, they can:
- Create fake proofs
- Break the entire system's security

This is why τ is called "toxic waste" - it's dangerous and must be properly disposed of!

### Real-World Solutions

In practice, **multi-party computation (MPC)** ceremonies are used:
- Many participants (sometimes thousands) each contribute randomness
- As long as **one honest person** destroys their secret, the setup is secure
- Famous examples:
  - **Zcash Powers of Tau** (2017)
  - **Ethereum KZG Ceremony** (2022-2023)

## Important: Coordinate Systems

### Affine vs Projective Coordinates

The notebook shows expected output in **projective coordinates** `(x : y : z)`, but our solution uses **affine coordinates** `(x, y)`. These represent the **same mathematical point**!

**Conversion:**
- Affine → Projective: `(x, y) → (x : y : 1)`
- Projective → Affine: `(X : Y : Z) → (X/Z, Y/Z)`

**Example:**
- Our answer: `(1, 2)` (affine)
- Notebook: `(1 : 2 : 1)` (projective)
- **Same point!** ✓

**Why the difference?**
- `py_ecc` returns affine coordinates (standard, simpler)
- Some curve libraries use projective internally for efficiency
- Both are correct - just different representations

Our solution displays **both formats** to show they're equivalent.

## Solution

Run the solution:

```bash
cd sageless/solutions/exercise7
source ../../../.venv/bin/activate  # Or use run.sh
python exercise7.py
```

Or using the helper script:
```bash
./run.sh sageless/solutions/exercise7/exercise7.py
```

### How It Works

1. **Initialize** τ = 424242, l = 10

2. **Compute S₁** (11 points total):
   ```python
   S1 = []
   τ_power = 1
   for i in range(l + 1):
       point = multiply(P, τ_power)  # Scalar multiplication in G₁
       S1.append(point)
       τ_power = (τ_power * τ) % n   # Next power
   ```

3. **Compute S₂**:
   ```python
   S2 = multiply(Q, τ)  # Scalar multiplication in G₂
   ```

### Expected Output

The solution verifies against the notebook's expected values:

```
S₁[0] = (1, 2)  # This is P, the generator
S₁[1] = (3388106087484702502772161951837520865682365219266094058038991331506090320735,
         10310862820936104897688292475187545406556140958479334534497508049176340462168)
S₁[2] = (5786299459695789788261684662131390109566181344091061986154006773045920884529,
         18198083969462810098554436542449595852850793038741994323649111219383738839374)
...
```

All checks pass ✓

## Why This Matters for KZG

The trusted setup enables the KZG commitment scheme:

1. **Prover** commits to polynomial f(x):
   ```
   C = f(τ)·P = Σᵢ aᵢ·S₁[i]
   ```
   The prover doesn't know τ, but can compute this using S₁!

2. **Verifier** checks evaluations using pairings with S₁ and S₂

3. **Security**: Without knowing τ, the prover can't fake proofs

## Mathematical Details

### Scalar Multiplication in G₁

For each power τⁱ, we compute:
```
τⁱ·P = P + P + ... + P  (τⁱ times)
```

This is done efficiently using the `multiply` function from py_ecc.

### Why Powers of τ?

The setup provides "encrypted" powers of τ:
- To commit to polynomial `f(x) = a₀ + a₁x + a₂x² + ...`
- We need to compute `f(τ) = a₀ + a₁τ + a₂τ² + ...`
- Using S₁, we can compute: `a₀·S₁[0] + a₁·S₁[1] + a₂·S₁[2] + ...`
- This equals `f(τ)·P` without knowing τ!

### Curve Parameters

- **Curve**: BN254 (also called BN128)
- **Field modulus (p)**: 21888242871839275222246405745257275088696311157297823662689037894645226208583
- **Curve order (n)**: 21888242871839275222246405745257275088548364400416034343698204186575808495617
- **G₁ generator P**: (1, 2)
- **G₂ generator Q**: ((10857046999023057135944570762232829481370756359578518086990519993285655852781, 11559732032986387107991004021392285783925812861821192530917403151452391805634), (8495653923123431417604973247489272438418190587263600148770280649306958101930, 4082367875863433681332203403145435568316851327593401208105741076214120093531))

## Security Note

⚠️ **For this exercise, τ=424242 is public (for demonstration only)!**

In a real system:
- τ would be randomly generated
- τ would be immediately destroyed after computing S₁ and S₂
- Nobody, not even the setup participants, would know τ

The security of KZG relies on the **q-Strong Diffie-Hellman (q-SDH)** assumption: given [P, τ·P, τ²·P, ..., τⁿ·P], it's computationally infeasible to compute τ or create fake proofs.

## Next Steps

After completing Exercise 7, you can use S₁ and S₂ to:
- **Exercise 8**: Implement polynomial commitments
- **Exercise 9+**: Create and verify KZG proofs

The trusted setup is the foundation for all KZG operations!

## Files

- `exercise7.py` - Complete solution with verification
- `README.md` - This file

## Related Documentation

- [KZG_COMMITMENTS_EXPLAINED.md](../docs/KZG_COMMITMENTS_EXPLAINED.md) - Full KZG explanation
- [Exercise 6](../exercise6/) - Pairing bilinearity (prerequisite concept)
