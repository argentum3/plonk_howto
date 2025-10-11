# Exercise 14: Computing Permutation for Copy Constraints

## Overview

This exercise computes a **permutation σ** that encodes the **copy constraints** (wiring) between the three columns of a PlonK circuit.

## What is a Copy Constraint?

In a circuit, values can be **reused** across different gates:
- An output from gate 1 might become an input to gate 3
- This means those two positions must have **equal values**

**Copy constraints** enforce these equality relationships.

## The Permutation σ

Instead of explicitly listing all equalities, PlonK uses a clever encoding:
- A **permutation** σ: {1, 2, ..., 12} → {1, 2, ..., 12}
- Positions in the **same cycle** must have **equal values**

### Position Mapping

For a circuit with **n = 4 gates** and **3 columns** (a, b, c):

```
pos(column, index) = (column - 1) * n + index
```

| Position | Column | Gate | Notation |
|----------|--------|------|----------|
| 1-4      | a      | 1-4  | a[1..4]  |
| 5-8      | b      | 1-4  | b[1..4]  |
| 9-12     | c      | 1-4  | c[1..4]  |

## Circuit Values

Our example circuit computes F₄² = 9:

```
Gate 1: a[1]=0, b[1]=1, c[1]=1  →  0 + 1 = 1
Gate 2: a[2]=1, b[2]=1, c[2]=2  →  1 + 1 = 2
Gate 3: a[3]=1, b[3]=2, c[3]=3  →  1 + 2 = 3
Gate 4: a[4]=3, b[4]=3, c[4]=9  →  3 * 3 = 9
```

## Wiring Analysis

Tracing how values flow through the circuit:

1. **c[1] = 1** → reused as **a[2] = 1** and **b[2] = 1**
2. **c[2] = 2** → reused as **b[3] = 2**
3. **c[3] = 3** → reused as **a[4] = 3** and **b[4] = 3**
4. **c[4] = 9** → final output (not reused)

Additionally:
- **a[2] = 1** and **b[1] = 1** (both are the constant input 1)

## The Permutation σ

### Cycle Notation

A **cycle** like (3 → 9 → 6 → 3) means:
- σ[3] = 9
- σ[9] = 6
- σ[6] = 3

All positions in a cycle must have **equal values**.

### Our Permutation (6 cycles)

```python
# 1. Self-cycle: a[1] = 0 (constant input)
sigma[1] = 1

# 2. Cycle: a[2] ↔ b[1] (both = 1)
sigma[2] = 5
sigma[5] = 2

# 3. Cycle: c[1] → b[2] → a[3] (all = 1)
sigma[9] = 6
sigma[6] = 3
sigma[3] = 9

# 4. Cycle: c[2] ↔ b[3] (both = 2)
sigma[10] = 7
sigma[7] = 10

# 5. Cycle: c[3] → a[4] → b[4] (all = 3)
sigma[11] = 4
sigma[4] = 8
sigma[8] = 11

# 6. Self-cycle: c[4] = 9 (final output)
sigma[12] = 12
```

### Verification

The permutation must satisfy:
1. **Length = 12**: All positions mapped
2. **No repeats**: Each position appears exactly once in domain
3. **Domain = Image = {1..12}**: Valid permutation
4. **Specific cycle check**: (3, 9, 6) forms a cycle

## Why Use a Permutation?

### Traditional Approach (Expensive)
For each equality, add a constraint: "position i equals position j"
- Many constraints
- Hard to verify efficiently

### PlonK's Approach (Efficient)
Encode all equalities in a **single permutation**
- One permutation argument proves all copy constraints
- Uses polynomial commitments
- Very efficient!

## Key Insight

**If positions are in the same cycle, their values must be equal.**

The permutation σ encodes the **equivalence relation** of the wiring:
- Values that must be equal are linked in cycles
- The prover commits to these cycles
- The verifier checks the permutation argument

## Running the Exercise

```bash
# From repo root
./run.sh sageless/solutions/exercise14/exercise14.py

# Or with venv activated
cd sageless/solutions/exercise14
./exercise14.py
```

## Output

```
======================================================================
PERMUTATION σ
======================================================================

σ[1]  = 1   (self-cycle: a[1]=0)
σ[2]  = 5   }
σ[5]  = 2   } cycle: a[2]=1, b[1]=1

σ[3]  = 9   }
σ[9]  = 6   } cycle: c[1]=1, b[2]=1, a[3]=1
σ[6]  = 3   }

σ[10] = 7   }
σ[7]  = 10  } cycle: c[2]=2, b[3]=2

σ[11] = 4   }
σ[4]  = 8   } cycle: c[3]=3, a[4]=3, b[4]=3
σ[8]  = 11  }

σ[12] = 12  (self-cycle: c[4]=9)

✓ All checks passed!
```

## What's Next?

In the following exercises, this permutation σ will be used in PlonK's **permutation argument** to prove that all wired values are equal **without revealing them**!

---

**PlonK Tutorial - Exercise 14**
**Permutation encoding for copy constraints ✓**
