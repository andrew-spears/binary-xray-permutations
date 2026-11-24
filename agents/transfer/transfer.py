"""Order-free form of the interface machine.  A stone with SUM s sits at (a, b), a, b >= 1, a + b = s  (a = reflected
row, b = column; s_k = 2k + e_k for the k-th stone of a word).  For a set S of sums, Fset(S) = all (rows, columns)
used by a placement of S with distinct rows and distinct columns.  Fset does not depend on the order of the stones.
Question: for which pairs S, S' (same size, same total) is Fset(S) inside Fset(S')?   Here: S' = S with two stones
moved by one step each, towards each other (s_i + 1, s_j - 1) or apart.
Usage: python3 transfer.py K M     (sets of K distinct sums in [2, M] that satisfy Landau's prefix inequalities)"""
import sys
from itertools import combinations
from functools import lru_cache
def fset(S):
    cur = {(0, 0)}
    for s in S:
        nxt = set()
        for A, B in cur:
            for a in range(1, s):
                if A >> a & 1 or B >> (s - a) & 1: continue
                nxt.add((A | 1 << a, B | 1 << (s - a)))
        cur = nxt
    return frozenset(cur)
def landau(S):
    t = 0
    for i, s in enumerate(S, 1):
        t += s
        if t < i * (i + 1): return False
    return True
if __name__ == "__main__":
    K, M = int(sys.argv[1]), int(sys.argv[2])
    sets = [S for S in combinations(range(2, M + 1), K) if landau(S)]
    F = {S: fset(S) for S in sets}
    print(f"{len(sets)} Landau sets of {K} sums in [2, {M}]")
    from collections import Counter
    stat = Counter()
    ex = {}
    for S in sets:
        for i in range(K):
            for j in range(i + 1, K):
                for d, name in ((1, "together"), (-1, "apart")):
                    T = list(S); T[i] += d; T[j] -= d
                    T = tuple(sorted(T))
                    if len(set(T)) < K or T not in F or T == S: continue
                    gap = S[j] - S[i]
                    adj = (j == i + 1)
                    ok = F[S] <= F[T]
                    key = (name, "gap" + str(min(gap, 4)), "adjacent" if adj else "far")
                    stat[key, ok] += 1
                    if not ok and key not in ex: ex[key] = (S, T)
    for key in sorted({k for k, _ in stat}):
        print(key, "holds", stat[key, True], "fails", stat[key, False], ex.get(key, ""))
