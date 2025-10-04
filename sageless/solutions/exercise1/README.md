# Exercise 1: Constraint System

Implements the constraint system for computing F₄² through a circuit.

## Problem

Prove that F₄² = 9 where F₄ is the 4th Fibonacci number (F₁=0, F₂=1, F₃=1, F₄=2).

## Constraints

1. **Initial values:** LI(1) = 0, RI(1) = 1
2. **Addition gates:** LI(i) + RI(i) = O(i) for i ∈ {1, 2, 3}
3. **Wiring:** Values propagate correctly between gates
4. **Multiplication input:** LI(4) = RI(4) = O(3)
5. **Multiplication gate:** LI(4) * RI(4) = O(4)

## Circuit

```
Gate 1: 0 + 1 = 1  (F₁ + F₂ = F₃)
Gate 2: 1 + 1 = 2  (F₂ + F₃ = F₄)
Gate 3: 1 + 2 = 3  (wiring constraint)
Gate 4: 3 * 3 = 9  (F₄²)
```

## Running

```bash
cd exercise1
python3 constraints.py
```

## Output

```
All constraints satisfied!
Result: O(4) = F_4^2 = 9
```
