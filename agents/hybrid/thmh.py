"""Theorem H, checked through its proof: for every (s1, m) with m in {0,1,2}*{0,-1,-2}* coming from a valid word of length <= N, the stone
kap (last letter of m before its first negative letter) on the cell (p + q + 1 - s1, p + 1 - s1), counted from the start of m, with
p = #(0 before kap) + #(-2 after kap), q = s1 + s2 + #(1 before kap) + #(-1 after kap):
the number of pairs (u, v), u in O(s1), v in conj O(s2), with an odd number of placements of the other stones of m must be odd (and then it is not 0).
  python3 thmh.py N"""
import sys
from math import comb, factorial
N = int(sys.argv[1]); sys.argv = [sys.argv[0], str(N)]
import hybrid as h, hybrid1 as h1
def f(lam):
    c = h.l1.conj(lam) if lam else (); x = 1
    for i, a in enumerate(lam):
        for j in range(a): x *= a - j + c[j] - i - 1
    return factorial(sum(lam)) // x
def odd(u): return comb(sum(u[0]) + sum(u[1]), sum(u[0])) * f(u[0]) * f(u[1]) % 2 == 1
cj = lambda u: (h.l1.conj(u[0]), h.l1.conj(u[1]))
seen = {}; words = 0
def rec(w, s):
    global words
    n = len(w)
    if n and s == 0 and h.split(w):
        x, m, y = h.split(w)
        if h1.unimodal(m):
            words += 1; s1 = sum(x)
            if (s1, m) not in seen:
                s2 = s1 + sum(m); kap = next(i for i, e in enumerate(m) if e < 0)            # 1-based index of the stone before the first negative letter
                p = sum(e == 0 for e in m[:kap - 1]) + sum(e == -2 for e in m[kap:]); q = s1 + s2 + sum(e == 1 for e in m[:kap - 1]) + sum(e == -1 for e in m[kap:])
                cell = (p + q + 1 - s1, p + 1 - s1)
                seen[s1, m] = sum(1 for z in h1.analyse(s1, m) if z[0] == kap and z[1:3] == cell and odd(z[3]) and odd(cj(z[4])))
    if n == N: return
    L = N - n - 1
    for e in range(max((w[-1] - 1) if w else -N, -s), 2 * N):
        if s + e + L * e - L * (L + 1) // 2 > 0: break
        rec(w + (e,), s + e)
rec((), 0)
print(f"length <= {N}: {words} words with middle in {{0,1,2}}*{{0,-1,-2}}*, {len(seen)} pairs (s1, m); number of odd pairs (u, v) in O x conj O at the named cell is even for {sum(1 for v in seen.values() if v % 2 == 0)}; least number {min(seen.values())}")
