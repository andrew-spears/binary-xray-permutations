"""Independent audit of the automaton's step rule, with negative controls.
For every nondecreasing b majorized by (2,4,...,2n) (repeats allowed, so some have NO solution),
decide solvability (a) by the window/bitmask step of slack_dfa.py with B = max slack of b,
(b) by brute force over permutations.  They must agree on every b, solvable or not.
Usage: python3 audit_step.py nmax"""
import sys
from itertools import permutations

def cands(n):
    out = []
    def rec(k, last, tot, b):
        if k == n:
            if tot == n * (n + 1): out.append(tuple(b))
            return
        for x in range(max(last, 2), 2 * n + 1):
            t = tot + x
            if t < (k + 1) * (k + 2): continue
            if t + x * (n - k - 1) > n * (n + 1): break
            rec(k + 1, x, t, b + [x])
    rec(0, 2, 0, [])
    return out

def brute(n):
    S = set()
    for p in permutations(range(1, n + 1)):
        S.add(tuple(sorted(i + 1 + p[i] for i in range(n))))
    return S

def by_masks(b):
    n = len(b); e = [b[k] - 2 * (k + 1) for k in range(n)]
    sig = 0; B = 1
    for x in e:
        sig += x; B = max(B, sig)
    base = (1 << B) - 1
    S = {(base, base)}
    for x in e:
        T = set()
        for rm, cm in S:
            for u in range(-B, B + 1):
                v = x - u
                if v < -B or v > B: continue
                if rm >> (B + u) & 1 or cm >> (B + v) & 1: continue
                r2 = rm | 1 << (B + u); c2 = cm | 1 << (B + v)
                if not (r2 & 1 and c2 & 1): continue
                T.add((r2 >> 1, c2 >> 1))
        S = T
        if not S: return False
    return True

for n in range(2, int(sys.argv[1]) + 1):
    good = brute(n); C = cands(n)
    mism = sum(1 for b in C if by_masks(b) != (b in good))
    print(f"n={n}: {len(C)} majorized b, {sum(1 for b in C if b not in good)} unsolvable, mismatches {mism}")
