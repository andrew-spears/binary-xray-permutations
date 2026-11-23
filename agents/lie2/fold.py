"""Part B: folding.  A diagram automorphism s of a simply-laced type X whose orbits of simple roots are mutually
orthogonal gives a type Y (nodes of Y = orbits; D4 -> G2, E6 -> F4, A_{2n-1} -> B_n, D_{n+1} -> C_n).  A weight of Y
is the same thing as an s-symmetric weight of X (same fundamental-weight coordinates on each orbit).  Checks:
  (i)   regular dominant weights <= 2 rho of Y  =  s-symmetric regular dominant weights <= 2 rho of X;
  (ii)  those of the form  dom(rho + w rho), w in W(Y)  =  those of the form dom(rho + x), x in W(X) rho, x symmetric;
  (iii) which symmetric weights have a witness w in W(X) but no symmetric one.
Usage: python3 fold.py            (about 1 minute)"""
from rs import *
def run(X, N, Y, n, orb):
    big, small = RS(X, N), RS(Y, n)
    up = lambda v: tuple(v[next(k for k in range(n) if i in orb[k])] for i in range(N))
    sym = lambda v: all(len({v[i] for i in o}) == 1 for o in orb)
    reg = lambda S: {v for v in S if min(v) >= 1}
    A = {up(v) for v in reg(small.below((2,) * n))}
    B = {v for v in reg(big.below((2,) * N)) if sym(v)}
    Ob = big.orbit(big.rho)
    Ps = {up(small.dom(tuple(1 + x for x in v))) for v in small.orbit(small.rho)}
    Pb = {big.dom(tuple(1 + x for x in v)) for v in Ob}
    Pbs = {big.dom(tuple(1 + x for x in v)) for v in Ob if sym(v)}
    bad = sorted(v for v in B if v in Pb and v not in Pbs)
    print(f"{X}{N} -> {Y}{n}: (i) {A == B} ({len(A)} weights)  (ii) {Ps == Pbs & B | Ps and Ps == {v for v in Pbs}}"
          f"  no witness at all: {len(B - Pb)}  witness but no symmetric witness: {len(bad)} {bad}")
run("D", 4, "G", 2, [[0, 2, 3], [1]])
run("E", 6, "F", 4, [[0, 4], [1, 3], [2], [5]])
for n in (2, 3, 4): run("A", 2 * n - 1, "B", n, [[i, 2 * n - 2 - i] for i in range(n - 1)] + [[n - 1]])
for n in (3, 4, 5, 6): run("D", n + 1, "C", n, [[i] for i in range(n - 1)] + [[n - 1, n]])
