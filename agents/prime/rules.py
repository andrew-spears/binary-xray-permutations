"""Test candidate rules for prime vs decomposable against out_<n>.txt (from ./prime n).
Rules: (a) score sequence == (1,1,2,3,...,n-3,n-2,n-2); (b) #3-cycles == n-2 (min for strong);
(c) D == {d : |d|<=n-3, d = n-1 mod 2} u {+-(n-2)}.  Also prints primes in stones notation.
Usage: python3 rules.py 4 12
"""
import sys
from math import comb
lo, hi = int(sys.argv[1]), int(sys.argv[2])
for n in range(lo, hi + 1):
    rows = []
    for line in open(f"out_{n}.txt"):
        a, b = line.split("|")
        D = [int(x) for x in a.split()[1:]]
        f = b.split()
        rows.append((D, int(f[2]) == 0, int(f[0])))
    target = tuple([1, 1] + list(range(2, n - 2)) + [n - 2, n - 2])
    fam = sorted({d for d in range(-(n - 3), n - 2) if (d - n + 1) % 2 == 0} | {n - 2, -(n - 2)})
    res = {"score": [0, 0], "c3": [0, 0], "fam": [0, 0]}
    for D, prime, nw in rows:
        s = tuple(d + n - k for k, d in enumerate(D, 1))
        c3 = comb(n, 3) - sum(comb(x, 2) for x in s)
        for key, pred in (("score", s == target), ("c3", c3 == n - 2), ("fam", D == fam)):
            res[key][pred == prime] += 1
        if prime:
            st = "".join("●" if m in D else "○" for m in range(-(n - 1), n))
            print(f"n={n} prime {st} D={D} s={list(s)} c3={c3} witnesses={nw}")
    print(f"n={n} rule [wrong,right]:", res, "min c3 over all =",
          min(comb(n, 3) - sum(comb(d + n - k, 2) for k, d in enumerate(D, 1)) for D, _, _ in rows))
