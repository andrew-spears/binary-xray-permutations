"""Explore: unimodal words with x in {0,1,2}*, y of any depth.  Lists I-splits (interleaved pairing, u increasing) of least size.
Usage: python3 x2.py n [v]"""
import sys, itertools
def cls(n):
    out = []
    def rec(w, s, down):
        k = len(w)
        if k == n:
            if s == 0 and any(w): out.append(tuple(w))
            return
        lo = (w[-1] - 1) if w else 0
        for e in range(max(lo, -s), 3):
            if down and e > 0: continue
            w.append(e); rec(w, s + e, down or e < 0); w.pop()
    rec([], 0, False); return out
def isplit(e, S):
    n = len(e); m = len(S)
    u = [e[k - 1] + 2 * (k - 1 - j) for j, k in enumerate(S)]
    if u != sorted(u): return False
    v = [2 * sum(1 for j in S if j > k) - e[k - 1] for k in range(1, n + 1) if k not in S]
    if min(v) < 0 or max(v) > 2 * m: return False
    N = [sum(1 for a in v if a >= i) for i in range(1, 2 * m + 1)]
    return u[::-1] == [N[2 * i] + N[2 * i + 1] for i in range(m)]
if __name__ == "__main__":
    n = int(sys.argv[1]); tot = simple = inx = least = none = 0
    for e in cls(n):
        m = (max(-a for a in e) + 1) // 2
        if m < 2: continue
        tot += 1; t = next(i for i in range(n) if e[i] < 0)
        found = [S for S in itertools.combinations(range(1, n + 1), m) if isplit(e, S)]
        fx = [S for S in found if S[-1] <= t]
        inx += bool(fx); least += bool(found)
        if not found:
            more = [S for S in itertools.combinations(range(1, n + 1), m + 1) if isplit(e, S)]
            none += not more
            if "v" in sys.argv: print(e, "t =", t, "m =", m, "none of size m; size m+1:", more[:4])
        elif not fx and "v" in sys.argv: print(e, "t =", t, "m =", m, found[:6])
    print(f"n = {n}: {tot} words with m >= 2; I-split of size m inside x: {inx}; of size m anywhere: {least}; none of size m or m+1: {none}")
