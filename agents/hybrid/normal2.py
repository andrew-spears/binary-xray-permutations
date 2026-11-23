"""Transfer with general normal forms.  A prefix z (letters >= 0) is NORMAL if every state with an odd number of placements of z lies in G(slack z).
1^s is normal (Lemma O).  If z, z' are normal with slacks s1, s2 and the diagonals of  z m (-reverse z')  have an odd split with S inside m, then
every valid x m y (x letters <= 1, slack s1; y letters >= -1) is solvable.
For every (s1, m) of the valid words of length <= N for which normal.py finds nothing with z = 1^s1, z' = 1^s2, this tries all normal z, z' of length <= LZ
(first letter >= 1, distinct diagonals in the combined word) and the extreme splits of Theorem E.
  python3 normal2.py N LZ"""
import sys, itertools
N, LZ = int(sys.argv[1]), int(sys.argv[2])
sys.argv = [sys.argv[0], str(N + LZ)]
import hybrid as h, normal as nm
from ext import crit
from collections import Counter
nm.N = N
Z = {}
def rec(z, s, odd, smax):
    if z and all(h.in_G(u) for u in odd): Z.setdefault(s, []).append(z)
    if len(z) == LZ: return
    for e in range(max(0 if z else 1, (z[-1] - 1) if z else 1), smax - s + 1):
        nxt = {}
        for u in odd:
            for k, v in h.l1.succs(u, e): nxt[v] = nxt.get(v, 0) ^ 1
        rec(z + (e,), s + e, {v for v, b in nxt.items() if b}, smax)
fail = Counter()
def words(w, s):
    n = len(w)
    if n and s == 0 and nm.split(w):
        x, m, y = nm.split(w)
        if nm.least(sum(x), m) is None: fail[sum(x), m] += 1
    if n == N: return
    L = N - n - 1
    for e in range(max((w[-1] - 1) if w else -N, -s), 2 * N):
        if s + e + L * e - L * (L + 1) // 2 > 0: break
        words(w + (e,), s + e)
words((), 0)
smax = max([0] + [max(s1, s1 + sum(m)) for s1, m in fail]); rec((), 0, {((), ())}, smax); Z[0] = [()]
print("normal prefixes of length <=", LZ, "by slack:", {s: len(Z.get(s, [])) for s in range(smax + 1)})
def search(s1, m):
    for z in sorted(Z.get(s1, []), key=len):
        for z1 in sorted(Z.get(s1 + sum(m), []), key=len):
            d = [(2 * i + e, 0) for i, e in enumerate(z, 1)] + [(2 * (len(z) + i) + e, 1) for i, e in enumerate(m, 1)] + \
                [(2 * (len(z) + len(m) + i) + e, 0) for i, e in enumerate([-a for a in reversed(z1)], 1)]
            d.sort()
            if len({a for a, t in d}) < len(d): continue
            e = tuple(a - 2 * i for i, (a, t) in enumerate(d, 1)); pos = [i for i, (a, t) in enumerate(d) if t]
            for size in range(1, min(len(pos), 4) + 1):
                for S in itertools.combinations(pos, size):
                    c = crit(e, sum(1 << k for k in S))
                    if c: return z, z1, e, tuple(k + 1 for k in S), c.strip()
    return None
left = 0
for (s1, m), c in sorted(fail.items(), key=lambda t: (len(t[0][1]), t)):
    r = search(s1, m); left += c * (r is None)
    print(f"s1 {s1}  m {' '.join(map(str, m))}  s2 {s1 + sum(m)}  ({c} words):", "NONE" if r is None else f"z = {' '.join(map(str, r[0])) or '-'}, z' = {' '.join(map(str, r[1])) or '-'}, word {' '.join(map(str, r[2]))}, S = {r[3]} {r[4]}", flush=True)
print(f"{len(fail)} pairs (s1, m), {sum(fail.values())} words; still nothing for {left} words")
