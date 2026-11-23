"""Conjecture P (polygon inequalities), uniform in the slack.
For a beginning x of slack s and a pair of diagrams (nu|mu) with |nu| + |mu| = s - 1, let Add(nu|mu) be the states
obtained by adding one box to nu or to mu.  P: among the numbers L_x(k), k in Add(nu|mu), none exceeds the sum of the
others.  (s = 1: L(1|-) = L(-|1), the transposition symmetry.  s = 2: the triangle inequalities of COUNT2_REPORT.)
Tests P, and that the sum over Add(nu|mu) is even, on all legal beginnings with slacks <= B and length <= N, and with
'formal' as 4th argument on all formal words (any letters, slacks in [0, B]) of length <= N.
Usage: python3 polygon.py B N [formal]"""
import sys
from collections import Counter, defaultdict
sys.path.insert(0, "../interface")
from count_rule import cstep
from cone import part, prefixes
Bd, N = int(sys.argv[1]), int(sys.argv[2]); formal = len(sys.argv) > 3
def partitions(n, m=None):
    m = n if m is None else m
    if n == 0: yield (); return
    for k in range(min(n, m), 0, -1):
        for p in partitions(n - k, k): yield (k,) + p
def add(p):
    out = []
    for i in range(len(p) + 1):
        q = list(p) + [0]; q[i] += 1
        if i == 0 or q[i] <= q[i - 1]: out.append(tuple(x for x in q if x))
    return out
POLY = {s: [[(a, mu) for a in add(nu)] + [(nu, b) for b in add(mu)] for k in range(s) for nu in partitions(k) for mu in partitions(s - 1 - k)] for s in range(1, Bd + 1)}
def formal_words(B, N):
    Bm = B + 2; base = (1 << Bm) - 1
    def rec(w, C, s):
        yield w, C, s
        if len(w) == N: return
        for e in range(-s, B - s + 1):
            D = cstep(C, e, Bm)
            if D: yield from rec(w + (e,), D, s + e)
    yield from rec((), Counter({(base, base): 1}), 0)
stat = defaultdict(lambda: [0, 0, 0, None, 0]); Bm = Bd + 2; which = defaultdict(Counter)
for w, C, s in (formal_words(Bd, N) if formal else prefixes(Bd, N)):
    if s == 0 or not w: continue
    d = {(part(t[0], Bm), part(t[1], Bm)): c for t, c in C.items()}; st = stat[s]; st[0] += 1
    for poly in POLY[s]:
        v = [d.get(k, 0) for k in poly]; st[4] += 1
        if 2 * max(v) > sum(v):
            st[1] += 1; which[s][tuple(sorted(poly))] += 1
            if st[3] is None or len(w) < len(st[3][0]): st[3] = (w, poly, v)
        if sum(v) % 2: st[2] += 1
print(("formal words" if formal else "legal beginnings") + f", slacks <= {Bd}, length <= {N}")
for s in sorted(stat):
    st = stat[s]
    print(f"   slack {s}: {st[0]} words, {len(POLY[s])} polygons each ({st[4]} tests): polygon inequality fails {st[1]}, odd sum {st[2]}  {st[3] or ''}")
    for poly, c in sorted(which[s].items(), key=lambda z: -z[1])[:8]: print(f"        fails {c} times: {list(poly)}")
