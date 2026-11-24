import sys, itertools
from collections import Counter
from lib import *
def perms_by_inv(n, r):
    """all permutations of range(n) with exactly r inversions (as tuples), via inversion tables"""
    out = []
    def rec(t, left, code):
        if t == n:
            if left == 0:
                # code[i] = number of larger elements before position... build perm by insertion
                p = []
                for i, c in enumerate(code): p.insert(len(p) - c, i)
                out.append(tuple(p))
            return
        for c in range(0, min(t, left) + 1): rec(t + 1, left - c, code + [c])
    rec(0, r, [])
    return out
for n in range(5, int(sys.argv[1]) + 1):
    V = valid_sets(n); P = {r: perms_by_inv(n, r) for r in range(0, 4)}
    hist = Counter(); ex = {}
    for D in V:
        for r in range(0, 4):
            good = [p for p in P[r] if decode(tuple(D[i] for i in p)) is not None]
            if good: break
        else: r = 99; good = []
        hist[r] += 1
        if r >= 1: ex.setdefault(r, []).append((D, good))
    print(n, len(V), sorted(hist.items()))
    for r in ex:
        for D, good in ex[r][:int(sys.argv[2])]:
            print("   ", r, D, [D[i] - (2 * i - n + 1) for i in range(n)], [tuple(D[i] for i in p) for p in good])
