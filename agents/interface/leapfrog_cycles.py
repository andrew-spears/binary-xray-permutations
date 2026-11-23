"""Leapfrog graph X(b_1..b_n) for valid words of length N = n+1 ending in -1: count path and cycle components.
Usage: python3 leapfrog_cycles.py Nmin Nmax [L1]     (L1: only words with letters in -1,0,1)"""
import sys
sys.argv, argv = [sys.argv[0], "2"], sys.argv
from leapfrog_check import words
def wit(b, n):                      # all placements (tuple col-by-row) of stones with sums b on [n]^2
    out = []; colof = [0] * (n + 1)
    def rec(k, R, C):
        if k == n: out.append(tuple(colof[1:])); return
        for r in range(1, n + 1):
            c = b[k] - r
            if 1 <= c <= n and not R >> r & 1 and not C >> c & 1:
                colof[r] = c; rec(k + 1, R | 1 << r, C | 1 << c)
    rec(0, 0, 0); return out
for N in range(int(argv[1]), int(argv[2]) + 1):
    n = N - 1; nw = withcyc = totc = totp = 0; ex = None; l1 = len(argv) > 3
    for e in words(N):
        if l1 and max(map(abs, e)) > 1: continue
        b = [2 * k + e[k - 1] for k in range(1, N + 1)]
        X = set()
        for j in range(n):
            b2 = b[:n]; b2[j] -= 1
            for p in wit(b2, n):
                m = next(i for i in range(n) if i + 1 + p[i] == b2[j] and (j == 0 or b2[j] != b2[j - 1] or True))
                # the marked stone is the one on sum b2[j]; if two stones share that sum, both marks are states
                for i in range(n):
                    if i + 1 + p[i] == b2[j]: X.add((p, i))
        def R(st):
            p, m = st
            if m == n - 1: return None
            q = list(p); q[m], q[m + 1] = q[m + 1], q[m]; return (tuple(q), m)
        def C(st):
            p, m = st; c = p[m]
            if c == n: return None
            q = list(p); j = q.index(c + 1); q[m], q[j] = c + 1, c; return (tuple(q), j)
        seen = set(); paths = cycles = 0
        for s in X:
            if s in seen: continue
            comp = {s}; stack = [s]; end = False
            while stack:
                x = stack.pop()
                for t in (R(x), C(x)):
                    if t is None: end = True
                    elif t not in comp: comp.add(t); stack.append(t)
            seen |= comp
            if end: paths += 1
            else: cycles += 1
        nw += 1; totc += cycles; totp += paths
        if cycles:
            withcyc += 1
            if ex is None: ex = (e, paths, cycles)
        assert paths > 0
    print(f"N={N}: {nw} words; total paths {totp}, cycles {totc}; words with a cycle {withcyc}; first {ex}", flush=True)
