#!/usr/bin/env python3
"""
Exercise 3 Solution: Polynomial Interpolation for PLONK
Represents the vectors LI, RI, O and selectors SL, SR, SM as polynomials over F_p
"""

import sys
sys.path.append('..')

from functools import reduce

# BN254 curve order (prime field)
p = 21888242871839275222246405745257275088548364400416034343698204186575808495617

class Polynomial:
    """
    Polynomial with coefficients in GF(p)
    Coefficients are stored as [a0, a1, a2, ...] representing a0 + a1*x + a2*x^2 + ...
    """
    def __init__(self, coeffs, modulus=p):
        self.modulus = modulus
        # Remove leading zeros
        coeffs = list(coeffs)
        while len(coeffs) > 1 and coeffs[-1] % modulus == 0:
            coeffs.pop()
        self.coeffs = [c % modulus for c in coeffs]

    def __call__(self, x):
        """
        Evaluate polynomial at x
        If x is an integer: returns f(x) as an integer
        If x is a Polynomial or PolynomialVar: returns composition f(x) as a Polynomial
        """
        # Check if x is an integer (evaluation) or polynomial-like (composition)
        if isinstance(x, int):
            # Integer evaluation
            result = 0
            x_power = 1
            for coeff in self.coeffs:
                result = (result + coeff * x_power) % self.modulus
                x_power = (x_power * x) % self.modulus
            return result
        else:
            # Polynomial composition (x is Polynomial or PolynomialVar)
            result = Polynomial([0], self.modulus)
            x_power = Polynomial([1], self.modulus)  # x^0 = 1
            for coeff in self.coeffs:
                result = result + (x_power * coeff)
                x_power = x_power * x
            return result

    def __add__(self, other):
        """Add two polynomials"""
        if isinstance(other, int):
            result = self.coeffs.copy()
            result[0] = (result[0] + other) % self.modulus
            return Polynomial(result, self.modulus)

        max_len = max(len(self.coeffs), len(other.coeffs))
        result = [0] * max_len
        for i in range(len(self.coeffs)):
            result[i] = self.coeffs[i]
        for i in range(len(other.coeffs)):
            result[i] = (result[i] + other.coeffs[i]) % self.modulus
        return Polynomial(result, self.modulus)

    def __sub__(self, other):
        """Subtract two polynomials"""
        if isinstance(other, int):
            result = self.coeffs.copy()
            result[0] = (result[0] - other) % self.modulus
            return Polynomial(result, self.modulus)

        max_len = max(len(self.coeffs), len(other.coeffs))
        result = [0] * max_len
        for i in range(len(self.coeffs)):
            result[i] = self.coeffs[i]
        for i in range(len(other.coeffs)):
            result[i] = (result[i] - other.coeffs[i]) % self.modulus
        return Polynomial(result, self.modulus)

    def __mul__(self, other):
        """Multiply two polynomials or polynomial by scalar"""
        if isinstance(other, int):
            return Polynomial([c * other for c in self.coeffs], self.modulus)

        # Handle PolynomialVar by extracting its .poly attribute
        if hasattr(other, 'poly') and not hasattr(other, 'coeffs'):
            other = other.poly

        result = [0] * (len(self.coeffs) + len(other.coeffs) - 1)
        for i, c1 in enumerate(self.coeffs):
            for j, c2 in enumerate(other.coeffs):
                result[i + j] = (result[i + j] + c1 * c2) % self.modulus
        return Polynomial(result, self.modulus)

    def __rmul__(self, other):
        """Right multiplication (for scalar * polynomial)"""
        return self.__mul__(other)

    def degree(self):
        """Return degree of polynomial"""
        return len(self.coeffs) - 1

    def quo_rem(self, other):
        """
        Polynomial division with remainder
        Returns (quotient, remainder) such that self = quotient * other + remainder
        """
        if isinstance(other, Polynomial):
            dividend = self.coeffs.copy()
            divisor = other.coeffs.copy()

            if len(divisor) == 1 and divisor[0] == 0:
                raise ZeroDivisionError("Division by zero polynomial")

            quotient = []
            while len(dividend) >= len(divisor):
                # Leading coefficient of dividend / leading coefficient of divisor
                lead_div = dividend[-1]
                lead_dvs = divisor[-1]
                # Compute modular inverse
                coeff = (lead_div * pow(lead_dvs, self.modulus - 2, self.modulus)) % self.modulus
                quotient.append(coeff)

                # Subtract divisor * coeff * x^(deg_diff) from dividend
                deg_diff = len(dividend) - len(divisor)
                for i in range(len(divisor)):
                    dividend[deg_diff + i] = (dividend[deg_diff + i] - coeff * divisor[i]) % self.modulus

                dividend.pop()

            quotient.reverse()
            if not quotient:
                quotient = [0]

            return Polynomial(quotient, self.modulus), Polynomial(dividend if dividend else [0], self.modulus)
        else:
            raise TypeError("Can only divide by another polynomial")

    def divides(self, other):
        """Check if self divides other (i.e., other % self == 0)"""
        _, remainder = other.quo_rem(self)
        return all(c == 0 for c in remainder.coeffs)

    def __eq__(self, other):
        """Check polynomial equality"""
        if isinstance(other, int):
            return len(self.coeffs) == 1 and self.coeffs[0] == other % self.modulus
        if not isinstance(other, Polynomial):
            return False
        # Compare coefficients, accounting for different lengths
        max_len = max(len(self.coeffs), len(other.coeffs))
        for i in range(max_len):
            a = self.coeffs[i] if i < len(self.coeffs) else 0
            b = other.coeffs[i] if i < len(other.coeffs) else 0
            if a != b:
                return False
        return True

    def __repr__(self):
        if len(self.coeffs) == 0:
            return "0"
        terms = []
        for i, c in enumerate(self.coeffs):
            if c != 0:
                if i == 0:
                    terms.append(str(c))
                elif i == 1:
                    terms.append(f"{c}*x" if c != 1 else "x")
                else:
                    terms.append(f"{c}*x^{i}" if c != 1 else f"x^{i}")
        return " + ".join(terms) if terms else "0"


class PolynomialVar:
    """Represents the variable x as a polynomial"""
    def __init__(self, modulus=p):
        self.poly = Polynomial([0, 1], modulus)
        self.modulus = modulus

    def __add__(self, other):
        """x + constant or polynomial"""
        return self.poly + other

    def __radd__(self, other):
        """constant + x"""
        return self.poly + other

    def __sub__(self, other):
        """x - constant"""
        return self.poly - other

    def __mul__(self, other):
        """x * constant or polynomial"""
        return self.poly * other

    def __rmul__(self, other):
        """constant * x"""
        return self.poly * other


def interpolate(I, Y):
    """
    Lagrange interpolation over GF(p)
    I: list of x-coordinates [x1, x2, ..., xn]
    Y: list of y-coordinates [y1, y2, ..., yn]
    Returns: Polynomial f(x) such that f(xi) = yi
    """
    n = len(I)
    x = PolynomialVar(p)
    result = Polynomial([0], p)

    for i in range(n):
        # Build Lagrange basis polynomial L_i(x)
        numerator = Polynomial([1], p)
        denominator = 1

        for j in range(n):
            if i != j:
                # numerator *= (x - I[j])
                # (x - I[j]) already returns a Polynomial, not PolynomialVar
                term = x - I[j]
                numerator = numerator * term
                # denominator *= (I[i] - I[j])
                denominator = (denominator * (I[i] - I[j])) % p

        # L_i(x) = numerator / denominator
        # In GF(p), division by d is multiplication by d^(-1) mod p
        denominator_inv = pow(denominator, p - 2, p)
        basis = numerator * denominator_inv

        # Add Y[i] * L_i(x) to result
        result = result + (basis * Y[i])

    return result


# Define the index set and witness values
I = [1, 2, 3, 4]
LI = {1: 0, 2: 1, 3: 1, 4: 3}  # Left input
RI = {1: 1, 2: 1, 3: 2, 4: 3}  # Right input
O = {1: 1, 2: 2, 3: 3, 4: 9}   # Output

# Define selectors
# SL, SR: 1 for addition gates (rows 1-3), 0 for multiplication gate (row 4)
# SM: 0 for addition gates (rows 1-3), 1 for multiplication gate (row 4)
SL = {1: 1, 2: 1, 3: 1, 4: 0}  # Selector for left input in addition
SR = {1: 1, 2: 1, 3: 1, 4: 0}  # Selector for right input in addition
SM = {1: 0, 2: 0, 3: 0, 4: 1}  # Selector for multiplication gate

# Interpolate selector polynomials
qL = interpolate(I, list(SL.values()))  # Interpolate over indexes i in I and the images SL[i]
qR = interpolate(I, list(SR.values()))  # Interpolate over indexes i in I and the images SR[i]
qM = interpolate(I, list(SM.values()))  # Interpolate over indexes i in I and the images SM[i]

# Interpolate witness polynomials
a = interpolate(I, list(LI.values()))  # Left input polynomial
b = interpolate(I, list(RI.values()))  # Right input polynomial
c = interpolate(I, list(O.values()))   # Output polynomial

# Verification
print("Exercise 3 Solution: Polynomial Interpolation")
print("=" * 60)

# Check 1: All polynomials should be degree 3
print("\n1. Checking polynomial degrees (should all be 3):")
print(f"   deg(a) = {a.degree()}")
print(f"   deg(b) = {b.degree()}")
print(f"   deg(c) = {c.degree()}")
print(f"   deg(qL) = {qL.degree()}")
print(f"   deg(qR) = {qR.degree()}")
print(f"   deg(qM) = {qM.degree()}")

# Check 2: Polynomials should evaluate to correct values at indices
print("\n2. Checking evaluations at indices I:")
print("   i  | LI[i]  a(i) | RI[i]  b(i) | O[i]   c(i)")
print("   " + "-" * 50)
all_correct = True
for i in I:
    a_val = a(i)
    b_val = b(i)
    c_val = c(i)
    match_a = "✓" if a_val == LI[i] else "✗"
    match_b = "✓" if b_val == RI[i] else "✗"
    match_c = "✓" if c_val == O[i] else "✗"
    print(f"   {i}  | {LI[i]:4d}  {a_val:4d} {match_a} | {RI[i]:4d}  {b_val:4d} {match_b} | {O[i]:4d}  {c_val:4d} {match_c}")
    if a_val != LI[i] or b_val != RI[i] or c_val != O[i]:
        all_correct = False

# Check 3: Test the gate constraint polynomial t(x) = a(x) + b(x) - c(x)
print("\n3. Checking gate constraint t(x) = a(x) + b(x) - c(x) at indices:")
t = a + b - c
print("   i  | t(i) | Should be 0 for i=1,2,3")
print("   " + "-" * 35)
for i in I:
    t_val = t(i)
    expected = "0" if i in [1, 2, 3] else "any"
    status = "✓" if (i in [1, 2, 3] and t_val == 0) or i == 4 else "✗"
    print(f"   {i}  | {t_val:4d} | {expected:10s} {status}")

# Check 4: Verify selector polynomial values
print("\n4. Checking selector polynomials at indices:")
print("   i  | qL(i) | qR(i) | qM(i) | Expected")
print("   " + "-" * 50)
for i in I:
    qL_val = qL(i)
    qR_val = qR(i)
    qM_val = qM(i)
    expected = "addition" if i in [1, 2, 3] else "multiplication"
    print(f"   {i}  | {qL_val:5d} | {qR_val:5d} | {qM_val:5d} | {expected}")

print("\n" + "=" * 60)
print("Polynomial a(x) coefficients:")
print(f"a(x) = {a.coeffs[0]} + {a.coeffs[1]}*x + {a.coeffs[2]}*x^2 + {a.coeffs[3]}*x^3")

print("\n✓ Exercise 3 complete!")
