# Blocks of a solution: maximal groups of stones (r, c), (r+1, c-1), ... (neighbouring rows, neighbouring columns,
# diagonals c - r going down by 2).  For every valid D: fewest blocks over all solutions, and over solutions of width <= 3.
import sys
from collections import Counter
def words(n):
    out = []
    def rec(w, s):
        if len(w) == n:
            if s == 0: out.append(tuple(w))
            return
        lo = w[-1] - 1 if w else 0
        for e in range(max(lo, -s), n - len(w)):
            w.append(e); rec(w, s + e); w.pop()
    rec([], 0); return out
def sols(D, n):
    S = set(D); used = [False] * n; sig = []; out = []
    def rec(r):
        if r == n: out.append(tuple(sig)); return
        for c in range(n):
            if not used[c] and c - r in S:
                used[c] = True; S.discard(c - r); sig.append(c); rec(r + 1); sig.pop(); S.add(c - r); used[c] = False
    rec(0); return out
def lis(p):
    import bisect
    t = []
    for x in p:
        i = bisect.bisect_left(t, x)
        if i == len(t): t.append(x)
        else: t[i] = x
    return len(t)
def nblocks(p): return len(p) - sum(1 for r in range(len(p) - 1) if p[r + 1] == p[r] - 1)
def m0(D):
    S = set(D); return sum(1 for d in D if d - 2 not in S)
def runs(w): return 1 + sum(1 for i in range(len(w) - 1) if w[i] != w[i + 1])
if __name__ == "__main__":
    n = int(sys.argv[1]); tab = Counter(); worst = []
    for w in words(n):
        D = [e + 2 * (k + 1) - n - 1 for k, e in enumerate(w)]
        ss = sols(D, n); b = min(map(nblocks, ss)); b3 = min((nblocks(p) for p in ss if lis(p) <= 3), default=None)
        tab[(m0(D), runs(w), b, b3)] += 1
        worst.append((b - runs(w), b3 - b, w, b, b3, m0(D), runs(w)))
    print("n =", n, "arrangements", len(worst))
    print("fewest blocks minus runs of equal letters:", sorted(Counter(x[0] for x in worst).items()))
    print("fewest blocks with width <= 3 minus fewest blocks:", sorted(Counter(x[1] for x in worst).items()))
    print("fewest blocks minus fewest 2-strings:", sorted(Counter(x[3] - x[5] for x in worst).items()))
    for x in sorted(worst, reverse=True)[:6]: print("  ", *x[2], "| blocks", x[3], "width<=3:", x[4], "2-strings", x[5], "runs", x[6])
