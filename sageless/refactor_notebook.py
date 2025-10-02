#!/usr/bin/env python3
"""
Script to refactor PlonK-Tutorial.ipynb from SageMath to pure Python
"""

import json
import sys

def get_polynomial_class():
    """Return the Python polynomial class implementation"""
    return '''import numpy as np
from functools import reduce
import random

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
        """Evaluate polynomial at x"""
        result = 0
        x_power = 1
        for coeff in self.coeffs:
            result = (result + coeff * x_power) % self.modulus
            x_power = (x_power * x) % self.modulus
        return result

    def __add__(self, other):
        if isinstance(other, int):
            new_coeffs = self.coeffs.copy()
            if len(new_coeffs) == 0:
                new_coeffs = [0]
            new_coeffs[0] = (new_coeffs[0] + other) % self.modulus
            return Polynomial(new_coeffs, self.modulus)
        max_len = max(len(self.coeffs), len(other.coeffs))
        new_coeffs = []
        for i in range(max_len):
            a = self.coeffs[i] if i < len(self.coeffs) else 0
            b = other.coeffs[i] if i < len(other.coeffs) else 0
            new_coeffs.append((a + b) % self.modulus)
        return Polynomial(new_coeffs, self.modulus)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, int):
            new_coeffs = self.coeffs.copy()
            if len(new_coeffs) == 0:
                new_coeffs = [0]
            new_coeffs[0] = (new_coeffs[0] - other) % self.modulus
            return Polynomial(new_coeffs, self.modulus)
        max_len = max(len(self.coeffs), len(other.coeffs))
        new_coeffs = []
        for i in range(max_len):
            a = self.coeffs[i] if i < len(self.coeffs) else 0
            b = other.coeffs[i] if i < len(other.coeffs) else 0
            new_coeffs.append((a - b) % self.modulus)
        return Polynomial(new_coeffs, self.modulus)

    def __rsub__(self, other):
        return Polynomial([other], self.modulus).__sub__(self)

    def __mul__(self, other):
        if isinstance(other, int):
            return Polynomial([c * other for c in self.coeffs], self.modulus)
        # Polynomial multiplication
        result = [0] * (len(self.coeffs) + len(other.coeffs) - 1)
        for i, a in enumerate(self.coeffs):
            for j, b in enumerate(other.coeffs):
                result[i + j] = (result[i + j] + a * b) % self.modulus
        return Polynomial(result, self.modulus)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        """Polynomial division, returns quotient"""
        q, r = self.quo_rem(other)
        return q

    def __floordiv__(self, other):
        """Polynomial floor division"""
        if isinstance(other, Polynomial):
            q, r = self.quo_rem(other)
            return q
        else:
            # Division by constant
            inv = pow(other, self.modulus - 2, self.modulus)
            return Polynomial([c * inv % self.modulus for c in self.coeffs], self.modulus)

    def __mod__(self, other):
        """Polynomial modulo"""
        q, r = self.quo_rem(other)
        return r

    def __pow__(self, n):
        """Polynomial exponentiation"""
        if n == 0:
            return Polynomial([1], self.modulus)
        if n == 1:
            return self
        if n % 2 == 0:
            half = self.__pow__(n // 2)
            return half * half
        else:
            return self * self.__pow__(n - 1)

    def __eq__(self, other):
        if isinstance(other, int):
            return len(self.coeffs) == 1 and self.coeffs[0] == other % self.modulus
        if not isinstance(other, Polynomial):
            return False
        return self.coeffs == other.coeffs

    def __repr__(self):
        if not self.coeffs or all(c == 0 for c in self.coeffs):
            return "0"
        terms = []
        for i, c in enumerate(self.coeffs):
            if c != 0:
                if i == 0:
                    terms.append(str(c))
                elif i == 1:
                    if c == 1:
                        terms.append("x")
                    else:
                        terms.append(f"{c}*x")
                else:
                    if c == 1:
                        terms.append(f"x^{i}")
                    else:
                        terms.append(f"{c}*x^{i}")
        return " + ".join(terms) if terms else "0"

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
        q, r = other.quo_rem(self)
        return r == 0

# Symbolic variable x
class PolynomialVar:
    """Represents the polynomial variable x"""
    def __init__(self, modulus=p):
        self.modulus = modulus
        self.poly = Polynomial([0, 1], modulus)  # x = 0 + 1*x

    def __pow__(self, n):
        return self.poly ** n

    def __mul__(self, other):
        return self.poly * other

    def __rmul__(self, other):
        return self.poly * other

    def __add__(self, other):
        return self.poly + other

    def __radd__(self, other):
        return self.poly + other

    def __sub__(self, other):
        return self.poly - other

    def __rsub__(self, other):
        return Polynomial([other], self.modulus) - self.poly

    def __call__(self, val):
        return self.poly(val)

x = PolynomialVar()

def prod(iterable):
    """Product of all elements in iterable"""
    return reduce(lambda a, b: a * b, iterable, 1)

def random_polynomial(degree, modulus=p):
    """Generate a random polynomial of given degree"""
    coeffs = [random.randint(0, modulus - 1) for _ in range(degree + 1)]
    return Polynomial(coeffs, modulus)'''

def refactor_notebook(input_path, output_path):
    """Refactor the notebook from SageMath to pure Python"""

    # Read the notebook
    with open(input_path, 'r') as f:
        nb = json.load(f)

    changes = []

    # 1. Update kernel metadata
    old_kernel = nb['metadata'].get('kernelspec', {})
    changes.append(f"Kernel: {old_kernel.get('display_name', 'Unknown')} -> Python 3")
    nb['metadata']['kernelspec'] = {
        'display_name': 'Python 3',
        'language': 'python',
        'name': 'python3'
    }

    # Update language_info if present
    nb['metadata']['language_info'] = {
        'name': 'python',
        'version': '3.8.0',
        'mimetype': 'text/x-python',
        'codemirror_mode': {
            'name': 'ipython',
            'version': 3
        },
        'pygments_lexer': 'ipython3',
        'nbconvert_exporter': 'python',
        'file_extension': '.py'
    }

    # 2. Replace cell 10 (polynomial setup)
    poly_class = get_polynomial_class()
    cell_10_new = poly_class + '''

def interpolate(I, Y):
    """
    Given two lists I and Y of the same length n:
      I = [x1, x2, ..., x_n]
      Y = [y1, y2, ..., y_n]
    where all x_i are distinct, return the Lagrange interpolation polynomial f(x)
    such that f(x_i) = y_i for each i.
    """
    n = len(I)
    # Initialize result as zero polynomial
    result = Polynomial([0], p)

    for i in range(n):
        # Build Lagrange basis polynomial L_i(x)
        numerator = Polynomial([1], p)
        denominator = 1

        for j in range(n):
            if i != j:
                # numerator *= (x - I[j])
                numerator = numerator * (x - I[j]).poly
                # denominator *= (I[i] - I[j])
                denominator = (denominator * (I[i] - I[j])) % p

        # L_i(x) = numerator / denominator
        # In GF(p), division by d is multiplication by d^(-1) mod p
        denominator_inv = pow(denominator, p - 2, p)
        basis = numerator * denominator_inv

        # Add Y[i] * L_i(x) to result
        result = result + (basis * Y[i])

    return result

# Field setup - p is already defined above as BN254 curve order

SL= {1:1,2:1,3:1,4:0} #Similar as before, we use dictionaries to map 1..4 to selectors for each gate
SR=
SM=

qL = interpolate(I,list(SL.values())) #We interpolate over indexes i in I and the images SL[i]
qR =
qM =

a =
b =
c ='''

    nb['cells'][10]['source'] = cell_10_new.split('\n')
    changes.append("Cell 10: Replaced SageMath polynomial setup with Python Polynomial class")

    # 3. Replace cell 18 (show -> print)
    cell_18_source = ''.join(nb['cells'][18]['source'])
    cell_18_new = cell_18_source.replace('show(', 'print(')
    nb['cells'][18]['source'] = cell_18_new.split('\n')
    changes.append("Cell 18: Replaced show() with print()")

    # 4. Replace cell 26 (pairing function)
    cell_26_new = '''import kzg
from py_ecc.bn128 import pairing

def e(P, Q):
    """
    Compute pairing using py_ecc library
    P: point in G1
    Q: point in G2
    Returns: pairing result in F_p^12
    """
    # py_ecc.bn128.pairing expects (G2, G1) order
    return pairing(Q, P)

# BN254 curve parameters are in kzg module
p = kzg.p  # Base field
n = kzg.n  # Curve order'''

    nb['cells'][26]['source'] = cell_26_new.split('\n')
    changes.append("Cell 26: Replaced SageMath pairing with py_ecc pairing")

    # 5. Replace cell 27 (show -> print)
    cell_27_new = '''P = kzg.P
Q = kzg.Q

print("P:", P)
print("Q:", Q)
print("e(P,Q):", e(P,Q))'''

    nb['cells'][27]['source'] = cell_27_new.split('\n')
    changes.append("Cell 27: Replaced show() with print()")

    # 6. Replace cell 29 (Integer -> int)
    cell_29_source = ''.join(nb['cells'][29]['source'])
    cell_29_new = cell_29_source.replace('Integer(', 'int(')
    nb['cells'][29]['source'] = cell_29_new.split('\n')
    changes.append("Cell 29: Replaced Integer() with int()")

    # 7. Replace cell 73 (prod and divides)
    cell_73_new = '''L1 = prod((x - ω**m)//(ω - ω**m) for m in range(2,n+1))
if isinstance(L1, int):
    L1 = Polynomial([L1], p)
ZH = x**n - 1
divisible = ZH.divides(L1*(z-1))
print("ZH divides L1*(z-1):", divisible)'''

    nb['cells'][73]['source'] = cell_73_new.split('\n')
    changes.append("Cell 73: Replaced prod() and .divides() with Python equivalents")

    # 8. Replace cell 75 (divides)
    cell_75_new = '''divisible = ZH.divides(z*N - D*z(x*ω))
print("ZH divides z*N - D*z(x*ω):", divisible)'''

    nb['cells'][75]['source'] = cell_75_new.split('\n')
    changes.append("Cell 75: Replaced .divides() with Python equivalent")

    # 9. Replace cell 77 (show)
    cell_77_new = '''print("z*N - D*z(x*ω) =", z*N - D*z(x*ω))'''

    nb['cells'][77]['source'] = cell_77_new.split('\n')
    changes.append("Cell 77: Replaced show() with print()")

    # 10. Replace cell 81 (random_element and show)
    cell_81_new = '''k = 2

p_poly = random_polynomial(degree=k-1, modulus=p)
print("p(x) =", p_poly)
a_blind = a + p_poly*ZH
print("a_blind =", a_blind)
print("Degree of a_blind:", a_blind.degree())'''

    nb['cells'][81]['source'] = cell_81_new.split('\n')
    changes.append("Cell 81: Replaced .random_element() and show() with Python equivalents")

    # 11. Replace cell 85 (divides)
    cell_85_new = '''assert ZH.divides(z_poly_blind*N_poly - D_poly*z_poly_blind(x*ω)) == True, "Something went wrong"'''

    nb['cells'][85]['source'] = cell_85_new.split('\n')
    changes.append("Cell 85: Replaced .divides() with Python equivalent")

    # Write the refactored notebook
    with open(output_path, 'w') as f:
        json.dump(nb, f, indent=1)

    return changes

if __name__ == '__main__':
    input_path = '/Users/boy/projects/plonk/sageless/PlonK-Tutorial.ipynb'
    output_path = '/Users/boy/projects/plonk/sageless/PlonK-Tutorial.ipynb'

    changes = refactor_notebook(input_path, output_path)

    print("Refactoring complete!")
    print("\nChanges made:")
    for i, change in enumerate(changes, 1):
        print(f"{i}. {change}")
