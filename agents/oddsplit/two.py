"""Two-stone RR-splits S = {k1 < k2} (item 1).  RR <=> all v in [0, 4] and min(u) in {N3 + N4, N2 + N4}, N_t = #{v >= t}.
For every valid word without a tight cut with max |e| in {3, 4} (one stone is impossible): which (k1, k2) work, and where
they sit relative to the turn t = last stone before the first negative letter.   Usage: python3 two.py n [v]"""
import sys
from ext import words
def two(e):
    n = len(e); out = []
    for k1 in range(n):
        for k2 in range(k1 + 1, n):
            v = [4 - e[k] for k in range(k1)] + [2 - e[k] for k in range(k1 + 1, k2)] + [-e[k] for k in range(k2 + 1, n)]
            u = (e[k1] + 2 * k1, e[k2] + 2 * (k2 - 1))
            if min(u) < 0 or min(v, default=0) < 0 or max(v, default=0) > 4: continue
            N = [sum(1 for x in v if x >= t) for t in range(1, 5)]
            ty = ("a" if min(u) == N[2] + N[3] else "") + ("b" if min(u) == N[1] + N[3] else "")
            if ty: out.append((k1 + 1, k2 + 1, ty))
    return out
if __name__ == "__main__":
    n = int(sys.argv[1]); tot = has = k2turn = k1turn = strad = 0; none = []
    for e in words(n, False):
        if not any(e) or any(sum(e[:k]) == 0 for k in range(1, n)): continue
        if max(map(abs, e)) not in (3, 4): continue
        tot += 1; t = next(i for i in range(n) if e[i] < 0); r = two(e)   # stone t (1-based) is the turn
        has += bool(r); k2turn += any(k2 == t for k1, k2, ty in r); k1turn += any(k1 == t + 1 for k1, k2, ty in r)
        strad += any(k1 <= t < k2 for k1, k2, ty in r)
        if not r: none.append(e)
        if "v" in sys.argv and r: print(e, "t =", t, r[:6])
    print(f"n = {n}: {tot} words with max|e| in {{3,4}}; 2-stone RR-split: {has}; with k2 = turn: {k2turn}; with k1 = turn + 1: {k1turn}; with k1 <= turn < k2: {strad}")
    for e in none[:8]: print("   none:", e)
