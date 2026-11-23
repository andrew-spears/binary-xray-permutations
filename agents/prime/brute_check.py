"""Independent brute-force check for n<=NMAX: over all n! permutations, group by diagonal set;
a no-tight-cut D is prime iff every witness is simple (no interval of size 2..n-1).
Compares with out_<n>.txt.  Usage: python3 brute_check.py 9
"""
import sys
from itertools import permutations
NMAX = int(sys.argv[1])

def simple(p):
    n = len(p)
    for a in range(n):
        lo = hi = p[a]
        for b in range(a + 1, n):
            lo, hi = min(lo, p[b]), max(hi, p[b])
            if hi - lo == b - a and b - a + 1 < n:
                return False
    return True

for n in range(4, NMAX + 1):
    allsimple = {}
    for p in permutations(range(n)):
        D = tuple(sorted(p[i] - i for i in range(n)))
        if len(set(D)) < n:
            continue
        allsimple[D] = allsimple.get(D, True) and simple(p)
    mine = {}
    for line in open(f"out_{n}.txt"):
        a, b = line.split("|")
        mine[tuple(int(x) for x in a.split()[1:])] = int(b.split()[2]) == 0
    bad = sum(allsimple[D] != pr for D, pr in mine.items())
    print(n, "checked", len(mine), "mismatches", bad, "primes", sum(mine.values()))
