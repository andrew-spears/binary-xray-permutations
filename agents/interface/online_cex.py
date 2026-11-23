"""Smallest failure of online (no-lookahead) placement at fixed n.
For every valid D and every k, Live_k(D) = {(rows, cols) used by the k smallest diagonals in some
witness}.  Online placement needs, for D, D' agreeing on their k smallest diagonals, a common
element of Live_k.  Reports the first pair with Live_k(D) & Live_k(D') empty.
Usage: python3 online_cex.py nmax"""
import sys, itertools
from check_walks import valid_Ds
def live(n):
    L = {}
    for p in itertools.permutations(range(1, n+1)):
        cells = sorted((p[i] - (i+1), i+1, p[i]) for i in range(n))
        d = tuple(c[0] for c in cells)
        if len(set(d)) < n: continue
        R = frozenset(); C = frozenset()
        Ld = L.setdefault(d, [set() for _ in range(n+1)])
        for k, (_, r, c) in enumerate(cells):
            R = R | {r}; C = C | {c}
            Ld[k+1].add((R, C))
    return L
for n in range(2, int(sys.argv[1]) + 1):
    L = live(n); found = None
    Ds = sorted(L)
    for k in range(1, n):
        byprefix = {}
        for D in Ds: byprefix.setdefault(D[:k], []).append(D)
        for pre, group in byprefix.items():
            for D1, D2 in itertools.combinations(group, 2):
                if not (L[D1][k] & L[D2][k]):
                    found = (k, D1, D2); break
            if found: break
        if found: break
    print(n, "pairs with no common prefix placement:", found)
