"""Test of the parity theorem.  For a prefix x (m letters, d_k = 2k + x_k distinct) and every state (R, C)
(rows and columns used by the m stones), compare
    L_x(R, C) = number of placements                                  (brute force)
with the coefficient of s_lambda(X) s_gamma(Y) in  Phi_x(X u Y),  Phi_x = sum over bijections beta: [m] -> D with
beta(i) >= 2i of prod_i h_{beta(i) - 2i}   (lambda, gamma = partitions of R, C: parts r_i - i),   modulo 2.
Usage: python3 parity.py LEN SLACK [neg]   all prefixes with letters >= 0 (or >= -SLACK with 'neg'), length <= LEN,
                                           slacks <= SLACK, distinct diagonals"""
import sys
from collections import Counter
from functools import lru_cache

def placements(x):
    cur = Counter({((), ()): 1})
    for k, e in enumerate(x, 1):
        d = 2 * k + e; nxt = Counter()
        for (R, C), v in cur.items():
            for r in range(1, d):
                c = d - r
                if r in R or c in C: continue
                nxt[(tuple(sorted(R + (r,))), tuple(sorted(C + (c,))))] += v
        cur = nxt
    return cur
def shape(S): return tuple(sorted((r - i for i, r in enumerate(S, 1)), reverse=True))
def strip(p): return tuple(a for a in p if a)

@lru_cache(None)
def kostka(lam, alpha):
    """number of semistandard tableaux of shape lam and content alpha (a composition, any order)"""
    lam = strip(lam)
    if not alpha: return 1 if not lam else 0
    a = alpha[-1]; rest = alpha[:-1]
    if sum(lam) != sum(alpha): return 0
    if a == 0: return kostka(lam, rest)
    tot = 0; L = len(lam)
    def rec(i, left, mu):                       # remove a horizontal strip of size a
        nonlocal tot
        if i == L:
            if left == 0: tot += kostka(strip(tuple(mu)), rest)
            return
        lo = lam[i + 1] if i + 1 < L else 0
        for t in range(0, min(left, lam[i] - lo) + 1): rec(i + 1, left - t, mu + [lam[i] - t])
    rec(0, a, [])
    return tot

def arrangements(x):
    m = len(x); D = [2 * k + e for k, e in enumerate(x, 1)]; out = []
    def rec(i, used, cur):
        if i > m: out.append(tuple(cur)); return
        for j, d in enumerate(D):
            if j not in used and d >= 2 * i: used.add(j); cur.append(d - 2 * i); rec(i + 1, used, cur); cur.pop(); used.discard(j)
    rec(1, set(), [])
    return out
def splits(alpha):
    if not alpha: yield (), (); return
    for a, b in splits(alpha[1:]):
        for t in range(alpha[0] + 1): yield (t,) + a, (alpha[0] - t,) + b
def predicted(x, lam, gam):
    """coefficient of s_lam(X) s_gam(Y) in Phi_x(X u Y)"""
    tot = 0
    for al in arrangements(x):
        al = tuple(a for a in al if a)
        for a, b in splits(al):
            if sum(a) == sum(lam): tot += kostka(lam, a) * kostka(gam, b)
    return tot
def partitions(n, mx=None):
    if mx is None: mx = n
    if n == 0: yield (); return
    for a in range(min(n, mx), 0, -1):
        for p in partitions(n - a, a): yield (a,) + p
def words(LEN, S, neg):
    out = []
    def rec(x, s):
        if x: out.append(tuple(x))
        if len(x) == LEN: return
        lo = max(x[-1] - 1, -s) if x else 0
        if not neg: lo = max(lo, 0)
        for e in range(lo, S - s + 1): x.append(e); rec(x, s + e); x.pop()
    rec([], 0)
    return out
if __name__ == "__main__":
    LEN, S = int(sys.argv[1]), int(sys.argv[2]); neg = len(sys.argv) > 3
    nw = ns = bad = odd = 0
    for x in words(LEN, S, neg):
        P = placements(x); nw += 1
        for (R, C), v in P.items():
            p = predicted(x, shape(R), shape(C)); ns += 1; odd += v % 2
            if (v - p) % 2: bad += 1; print("MISMATCH", x, R, C, v, p)
        sl = sum(x); reached = {(shape(R), shape(C)) for (R, C) in P}
        for a in range(sl + 1):                 # states with no placement must have an even prediction
            for lam in partitions(a):
                for gam in partitions(sl - a):
                    if (strip(lam), strip(gam)) not in {(strip(l), strip(g)) for l, g in reached} and predicted(x, lam, gam) % 2:
                        bad += 1; print("MISMATCH (no placement, odd prediction)", x, lam, gam)
    print(f"prefixes {nw} (length <= {LEN}, slacks <= {S}, {'letters of both signs' if neg else 'letters >= 0'}): "
          f"{ns} (prefix, state) pairs with a placement, {odd} with an odd number, parity mismatches {bad}")
