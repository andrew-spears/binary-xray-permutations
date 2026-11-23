"""Check of the leapfrog lemma.  D valid of size N with largest diagonal N-2 (last letter e_N = -1), distinct diagonals.
X = all (permutation matrix on [n]^2, marked stone), n = N-1, whose multiset of sums r'+c, with the marked one raised
by 1, equals {b_1..b_n}.  R / C = swap the marked stone's row / column with the next one, mark stays in the line.
Claim: components of X are alternating paths and cycles, and the number of paths is W(D)/2.
Usage: python3 leapfrog_check.py Nmax"""
import sys
from itertools import permutations, product
def words(N):                       # valid words, letters e_{k+1} >= e_k - 1, prefix sums >= 0, ending in -1
    def rec(pre, sig):
        k = len(pre)
        if k == N:
            if sig == 0 and pre[-1] == -1: yield tuple(pre)
            return
        lo = pre[-1] - 1 if pre else 0
        for e in range(max(lo, -sig), N):
            pre.append(e); yield from rec(pre, sig + e); pre.pop()
    yield from rec([], 0)
def W(b, N):
    cnt = 0
    def rec(k, R, C):
        nonlocal cnt
        if k == N: cnt += 1; return
        for r in range(1, N + 1):
            c = b[k] - r
            if 1 <= c <= N and not R >> r & 1 and not C >> c & 1: rec(k + 1, R | 1 << r, C | 1 << c)
    rec(0, 0, 0); return cnt
for N in range(3, int(sys.argv[1]) + 1):
    n = N - 1; nw = bad = 0; cyc = 0
    for e in words(N):
        b = [2 * k + e[k - 1] for k in range(1, N + 1)]; target = sorted(b[:n])
        X = set()
        for p in permutations(range(1, n + 1)):
            sums = [i + 1 + p[i] for i in range(n)]
            for m in range(n):
                s2 = sums[:]; s2[m] += 1
                if sorted(s2) == target: X.add((p, m))
        def R(st):
            p, m = st
            if m == n - 1: return None
            q = list(p); q[m], q[m + 1] = q[m + 1], q[m]; return (tuple(q), m)
        def C(st):
            p, m = st; c = p[m]
            if c == n: return None
            q = list(p); j = q.index(c + 1); q[m], q[j] = c + 1, c; return (tuple(q), j)
        ends = sum((R(s) is None) + (C(s) is None) for s in X)
        assert all(t is None or t in X for s in X for t in (R(s), C(s)))
        seen = set(); paths = cycles = 0
        for s in X:
            if s in seen: continue
            comp = {s}; stack = [s]
            while stack:
                x = stack.pop()
                for t in (R(x), C(x)):
                    if t is not None and t not in comp: comp.add(t); stack.append(t)
            seen |= comp
            if any(R(x) is None or C(x) is None for x in comp): paths += 1
            else: cycles += 1
        nw += 1; cyc += cycles
        if 2 * paths != W(b, N) or ends != W(b, N): bad += 1
    print(f"N={N}: {nw} words ending in -1; W = 2 * #paths fails for {bad}; cycles seen in total {cyc}", flush=True)
