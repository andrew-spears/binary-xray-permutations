"""Theorem H2 (Theorem B of ../oddsplit/REPORT2.md through the transfer): m = a b, a in {0,1,2}*, b in {0,-1,...,-4}* with a letter <= -3,
T = sum over the letters e <= -3 of m of (|e| - 2), and s1 < T.  In the normal word 1^s1 m (-1)^s2 the two stones of Theorem B
(k_1 = first k with P(k) >= T, k_2 = t + 1 or t + 2) lie inside m and form an RR-split (criterion of ../oddsplit/ext.py).
Checked for every (s1, m) of this kind coming from a valid word of length <= N; also the mirror class by mirroring the word.
  python3 thmh2.py N"""
import sys
sys.path.insert(0, "../oddsplit")
from ext import crit
N = int(sys.argv[1])
def split(w):
    i = next((j for j, e in enumerate(w) if e >= 2), None); j = max((j for j, e in enumerate(w) if e <= -2), default=None)
    return None if i is None or j is None or i > j else (w[:i], w[i:j + 1], w[j + 1:])
def btype(m):
    t = next(i for i, e in enumerate(m) if e < 0)
    return all(0 <= e <= 2 for e in m[:t]) and all(-4 <= e <= 0 for e in m[t:]) and min(m) <= -3
seen = {}; cnt = [0, 0, 0]
def check(s1, m):
    if (s1, m) in seen: return seen[s1, m]
    s2 = s1 + sum(m); e = (1,) * s1 + m + (-1,) * s2; T = sum(-a - 2 for a in m if a <= -3); t = next(i for i, a in enumerate(e) if a < 0)   # t = number of rising stones
    P = 0
    for k1 in range(1, len(e) + 1):
        P += e[k1 - 1]
        if P >= T: break
    k2 = t + 1 if P == T else t + 2
    ok = s1 < k1 and k2 <= s1 + len(m) and "RR" in crit(e, 1 << (k1 - 1) | 1 << (k2 - 1))
    seen[s1, m] = ok; return ok
def rec(w, s):
    n = len(w)
    if n and s == 0 and split(w):
        for v in (w, tuple(-a for a in reversed(w))):
            x, m, y = split(v)
            if btype(m):
                cnt[0] += 1; T = sum(-a - 2 for a in m if a <= -3)
                if sum(x) < T: cnt[1] += 1; cnt[2] += not check(sum(x), m)
    if n == N: return
    L = N - n - 1
    for e in range(max((w[-1] - 1) if w else -N, -s), 2 * N):
        if s + e + L * e - L * (L + 1) // 2 > 0: break
        rec(w + (e,), s + e)
rec((), 0)
print(f"length <= {N}: {cnt[0]} (word, orientation) with middle in {{0,1,2}}*{{0..-4}}* and a letter <= -3; with s1 < T: {cnt[1]}; of these the two stones of Theorem B are not an RR-split inside m: {cnt[2]}")
