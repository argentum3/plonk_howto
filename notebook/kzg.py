
from sage.all import *


def pairing(P,Q):
    #Base field for BN254
    p = 21888242871839275222246405745257275088696311157297823662689037894645226208583
    #Number of points on BN254
    n = ZZ(21888242871839275222246405745257275088548364400416034343698204186575808495617)
    k = 12
    t = 6*pow(4965661367192848881,2)+1
    out = P.ate_pairing(Q, n, k, t,p)
    return out

#Now we are going to do a tower of extensions from F_p to F_p^{12} in order to compute G2 directly inside of E(F_p^12)
# Step 1: Define F_p
p = 21888242871839275222246405745257275088696311157297823662689037894645226208583
F = GF(p)

# Step 2: Define F_{p^2}
R2 = PolynomialRing(F, 'u')
u = R2.gen()  # Get the variable u 
F2 = R2.quotient(u**2 + 1)


# Step 3: Define F_{p^{12}}
#https://hackmd.io/@Wimet/ry7z1Xj-2
R12 = PolynomialRing(F2, 'w') 
w = R12.gen()  # Get the variable u
F12 = R12.quotient(w**6 - (9 + u))


#Curve of algebraic closure as tower extension
EK = EllipticCurve(F12, [ 0, 3])

#Our G1 generator is the same
P = EK((1,2))

#Now we embed the G2 generator using the homormophism as below
#https://hackmd.io/@jpw/bn254

Q_F2 = (11559732032986387107991004021392285783925812861821192530917403151452391805634*u + 10857046999023057135944570762232829481370756359578518086990519993285655852781, 4082367875863433681332203403145435568316851327593401208105741076214120093531*u + 8495653923123431417604973247489272438418190587263600148770280649306958101930)

Q = (F12(F2(Q_F2[0])*w**2),F12(F2(Q_F2[1])*w**3))
Q = EK(Q)
