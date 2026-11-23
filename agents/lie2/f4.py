"""Part B: the two failing weights of F_4 (and G_2) in detail.  mu = x + y with x, y in W rho needs
(N1) |mu|^2 = 2|rho|^2 + 2(rho, w rho) for some w;  (N2) some x in W rho with (mu, x) = |mu|^2 / 2;  (N3) mu - x in W rho.
Prints, for each failing mu: the values |mu - x|^2 - |rho|^2 over x in W rho (0 would be needed and is then sufficient
only if mu - x is in W rho), and the number of x on the bisecting hyperplane.   Usage: python3 f4.py TYPE rank"""
import sys, collections
from rs import *
T, n = sys.argv[1], int(sys.argv[2]); R = RS(T, n); rho = R.rho
O = R.orbit(rho); P = {R.dom(tuple(a + b for a, b in zip(rho, v))) for v in O}
reg = sorted(m for m in R.below(tuple(2 * x for x in rho)) if min(m) >= 1)
n2 = R.ip(rho, rho)
print(f"{T}{n}: |rho|^2 = {n2}; values of (rho, w rho): {sorted(str(x) for x in {R.ip(rho, v) for v in O})}")
stats = collections.Counter()
for m in reg:
    c = collections.Counter()
    for x in O:
        y = tuple(a - b for a, b in zip(m, x)); c[R.ip(y, y) - n2] += 1
    on = c[0]; ok = m in P; stats[(ok, on > 0)] += 1
    if not ok:
        print(f"  FAIL mu = {m}, 2rho - mu = {[str(x) for x in R.coords(tuple(2 - a for a in m))]}, |mu|^2 = {R.ip(m, m)}")
        print(f"     x in W rho with |mu - x| = |rho|: {on};  smallest | |mu - x|^2 - |rho|^2 | = {min(abs(k) for k in c)}")
        if on:
            ys = {R.dom(tuple(a - b for a, b in zip(m, x))) for x in O if R.ip(tuple(a - b for a, b in zip(m, x)), tuple(a - b for a, b in zip(m, x))) == n2}
            print("     dominant conjugates of those mu - x:", sorted(ys), "(rho is", rho, ")")
print("  (is PRV, has x on the bisector):", dict(stats))
