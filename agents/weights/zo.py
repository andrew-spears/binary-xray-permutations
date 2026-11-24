"""All words in {0,1}^n, n <= N: F(x) against the parity-count set Q(x) (card paritycount).  python3 zo.py N"""
import sys
from fx import *
N = int(sys.argv[1]); tot = 0; bad = []
def Q(n, s, z, p):
    return {(R, C) for R, C in states(n, s) if abs(odd(R) + odd(C) - n) <= z and (odd(R) + odd(C) - n - z) % 2 == 0
            and abs(odd(R) - odd(C)) <= p and (odd(R) - odd(C) - p) % 2 == 0}
memo = {}
def rec(w, S):
    global tot
    n = len(w)
    if n:
        s = sum(w); k = (n, s)
        if k not in memo: memo[k] = Q(n, s, n - s, s)
        q = memo[k]; assert S <= q; tot += 1
        if S != q: bad.append((w, len(q), sorted(nm(t) for t in q - S)))
    if n < N:
        for e in (0, 1): rec(w + (e,), step(S, n + 1, e))
rec((), {(frozenset(), frozenset())})
print(f"{tot} words in {{0,1}}^n, n <= {N}: F(x) inside Q(x) always; F(x) = Q(x) except for {len(bad)} words:")
for w, q, ex in bad: print(" ", "".join(map(str, w)), f"|Q| = {q}, missing {len(ex)}:", " ".join(ex[:12]), "..." if len(ex) > 12 else "")
