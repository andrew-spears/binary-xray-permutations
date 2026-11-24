"""RR-splits (see ../oddsplit/REPORT.md).  rr(e, S) -> (lam, gam) or None.   Usage: python3 rr.py n [m]"""
import sys, itertools
def words(n):
    """valid words without a tight cut: letters fall by at most 1, slacks > 0 strictly inside, total 0 (both mirror images listed)"""
    out = []
    def rec(w, s):
        k = len(w)
        if k == n:
            if s == 0: out.append(tuple(w))
            return
        for e in range(max(w[-1] - 1 if w else -s, -s + (1 if k < n - 1 else 0)), n):
            m = n - k - 1                                   # the remaining m letters can remove at most m(m+1)/2 - m*(e-1)... : crude bound
            if s + e > m * (m + 1) // 2 + m * max(0, 1 - e): break
            w.append(e); rec(w, s + e); w.pop()
    rec([], 0); return out
def rr(e, S):
    n = len(e); m = len(S); Sset = set(S)
    u = []; a = 0; j = 0
    for k in range(n):
        if k in Sset: j += 1; u.append(e[k] + 2 * a)
        else: a += 1
    if min(u) < 0: return None
    v = []; b = m
    for k in range(n):
        if k in Sset: b -= 1
        else:
            x = 2 * b - e[k]
            if x < 0 or x > 2 * m: return None
            v.append(x)
    N = [sum(1 for x in v if x >= t) for t in range(1, 2 * m + 1)]; us = sorted(u, reverse=True)
    for I in itertools.combinations(range(2 * m), m):
        if I[0] != 0: break
        lam = [N[i] for i in I]; gam = [N[i] for i in range(2 * m) if i not in I]
        if [x + y for x, y in zip(lam, gam)] == us: return lam, gam
    return None
if __name__ == "__main__":
    n = int(sys.argv[1]); W = [w for w in words(n)]
    print(len(W), "words without a tight cut")
    for w in W[:: max(1, len(W) // 14)]:
        mx = max(abs(x) for x in w); res = []
        for m in range(1, n):
            res = [(S, rr(w, S)) for S in itertools.combinations(range(n), m)]; res = [(S, r) for S, r in res if r]
            if res: break
        print(" ".join(map(str, w)), "| m", m, "|", "; ".join(",".join(str(k + 1) for k in S) for S, r in res[:8]))
