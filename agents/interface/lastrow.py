"""T(D) = set of stones k that sit in the last row (r' = n) in some witness of D.  Candidates: 1 <= b_k - n <= n.
Usage: python3 lastrow.py n [-v]"""
import sys
from collections import Counter
n = int(sys.argv[1]); V = "-v" in sys.argv
def valid(N):
    def rec(pre, sig):
        k = len(pre)
        if k == N:
            if sig == 0: yield tuple(pre)
            return
        lo = pre[-1] - 1 if pre else 0
        for e in range(max(lo, -sig), N):
            pre.append(e); yield from rec(pre, sig + e); pre.pop()
    yield from rec([], 0)
def T(b):
    N = len(b); out = set()
    def rec(k, R, C, top):
        if k == N: out.add(top); return
        for r in range(1, N + 1):
            c = b[k] - r
            if 1 <= c <= N and not R >> r & 1 and not C >> c & 1: rec(k + 1, R | 1 << r, C | 1 << c, k + 1 if r == N else top)
    rec(0, 0, 0, None); return out
if __name__ == "__main__":
    st = Counter()
    for e in valid(n):
        b = [2 * k + e[k - 1] for k in range(1, n + 1)]
        cand = [k for k in range(1, n + 1) if 1 <= b[k - 1] - n <= n]; t = sorted(T(b))
        st["words"] += 1; st["T = all candidates"] += t == cand; st["top stone in T"] += n in t
        st["T is a set of consecutive candidates"] += all(x in t for x in cand if t[0] <= x <= t[-1])
        if V and t != cand: print("".join("+" if x > 0 else "-" if x < 0 else "0" for x in e) if max(map(abs, e)) < 2 else e, "cand", cand, "T", t)
    print(n, dict(st))
