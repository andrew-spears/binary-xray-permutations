"""A2: for a 0/1 word x (length m, s ones) list permutations pi of [m+1] with pi(m+1) = m+1-s and sums
{k + pi(k), k <= m} = {2k + x_k}.  Prints the count and the cycles of each solution (at most 4).
Usage: python3 a2look.py m      (all words 1...0 of length m)   or   python3 a2look.py x1 x2 ... xm"""
import sys
from itertools import permutations, product
def sols(x):
    m = len(x); s = sum(x); h = m + 1 - s; D = sorted(2 * (k + 1) + e for k, e in enumerate(x)); out = []
    cols = [c for c in range(1, m + 2) if c != h]
    def rec(k, used, cur):          # place the stones in order of diagonal
        if k == m: out.append(dict(cur)); return
        d = D[k]
        for r in range(max(1, d - m - 1), min(m, d - 1) + 1):
            c = d - r
            if c == h or c > m + 1 or r in cur or c in used: continue
            cur[r] = c; used.add(c); rec(k + 1, used, cur); used.discard(c); del cur[r]
    rec(0, set(), {})
    return out, h
def cycles(p):
    seen = set(); cs = []
    for i in sorted(p):
        if i in seen: continue
        c = []; j = i
        while j not in seen: seen.add(j); c.append(j); j = p[j]
        cs.append(c)
    return cs
if __name__ == "__main__":
    a = [int(t) for t in sys.argv[1:]]
    words = [tuple(a)] if len(a) > 1 else [(1,) + w + (0,) for w in product((0, 1), repeat=a[0] - 2)]
    for x in words:
        S, h = sols(x); m = len(x)
        print("".join(map(str, x)), f"h={h}", len(S), "solutions")
        for p in S[:4]:
            p[m + 1] = h
            print("    ", " ".join("(" + " ".join(map(str, c)) + ")" for c in cycles(p)))
