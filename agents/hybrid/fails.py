"""The words of normal.py without an extreme split inside m: distinct (s1, m), and for each the exact one-stone tests of hybrid1.py:
 P = number of (stone, cell, u, v), u in G(s1), v in conj G(s2), with an odd number of placements of the other stones of m;
 Q = number of (stone, cell) for which the normal word 1^s1 m (-1)^s2 has an odd number of solutions with that stone on that cell (exact one-stone transfer).
  python3 fails.py N"""
import sys
from math import comb, factorial
N = int(sys.argv[1])
sys.argv = [sys.argv[0], str(N)]
import hybrid as h, hybrid1 as h1, normal as nm
from collections import Counter
def f(lam):
    c = h.l1.conj(lam) if lam else (); x = 1
    for i, a in enumerate(lam):
        for j in range(a): x *= a - j + c[j] - i - 1
    return factorial(sum(lam)) // x
def odd(u): return comb(sum(u[0]) + sum(u[1]), sum(u[0])) * f(u[0]) * f(u[1]) % 2 == 1
cj = lambda u: (h.l1.conj(u[0]), h.l1.conj(u[1]))
fail = Counter()
def rec(w, s):
    n = len(w)
    if n and s == 0 and nm.split(w):
        x, m, y = nm.split(w)
        if nm.least(sum(x), m) is None: fail[sum(x), m] += 1
    if n == N: return
    L = N - n - 1
    for e in range(max((w[-1] - 1) if w else -N, -s), 2 * N):
        if s + e + L * e - L * (L + 1) // 2 > 0: break
        rec(w + (e,), s + e)
rec((), 0); noP = noQ = 0
for (s1, m), c in sorted(fail.items(), key=lambda z: (len(z[0][1]), z)):
    o = h1.analyse(s1, m); q = Counter(z[:3] for z in o if odd(z[3]) and odd(cj(z[4]))); Q = sum(1 for v in q.values() if v % 2)
    noP += not o; noQ += not Q
    print(f"s1 {s1}  m {' '.join(map(str, m))}  s2 {s1 + sum(m)}  ({c} words)  P {len(o)}  Q {Q}")
print(f"{len(fail)} pairs (s1, m) of {sum(fail.values())} words without an extreme split inside m; P = 0 for {noP}, Q = 0 for {noQ}")
