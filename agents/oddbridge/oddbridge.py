"""BRIDGE-ODD: does the middle m carry a state reached by 1^{s1} in an odd number of ways to a state from which (-1)^{s2}
finishes in an odd number of ways?  This is exactly what Theorem T (agents/hybrid/REPORT.md) can use: an odd count of the
padded word with stones of m fixed on cells exists iff such a pair of states is joined by m.
  python3 oddbridge.py N        all valid words of length <= N with a letter >= 2 before a letter <= -2
  python3 oddbridge.py pairs    the 13 pairs left open in agents/hybrid/REPORT.md section 5"""
import sys
sys.path.insert(0, "../l1sets")
import l1
l1.depth = lambda u: len(u[0]) + len(u[1]) + 40
E = ((), ())
def odd_fwd(s):
    P = {E: 1}
    for _ in range(s):
        Q = {}
        for u, c in P.items():
            for k, v in l1.succs(u, 1): Q[v] = Q.get(v, 0) ^ c
        P = {u: 1 for u, c in Q.items() if c}
    return frozenset(P)
def odd_bwd(s):
    P = {E: 1}
    for _ in range(s):
        Q = {}
        for u, c in P.items():
            for k, v in l1.preds(u, -1): Q[v] = Q.get(v, 0) ^ c
        P = {u: 1 for u, c in Q.items() if c}
    return frozenset(P)
OF, OB = {}, {}
def test(s1, m, s2):
    if s1 not in OF: OF[s1] = odd_fwd(s1)
    if s2 not in OB: OB[s2] = odd_bwd(s2)
    F = OF[s1]
    for e in m: F = frozenset(v for u in F for k, v in l1.succs(u, e))
    return len(F & OB[s2]), len(OF[s1]), len(OB[s2])
def words(n):
    out = []; w = []
    def rec(s):
        if len(w) == n:
            if s == 0: out.append(tuple(w))
            return
        k = len(w); lo = 0 if k == 0 else max(-s, w[-1] - 1)
        for e in range(lo, n + 1):
            L = n - k - 1
            if s + e + L * e > L * (L + 1) // 2: break
            w.append(e); rec(s + e); w.pop()
    rec(0); return out
def split(w):
    i = next((i for i, e in enumerate(w) if e >= 2), None)
    j = max((j for j, e in enumerate(w) if e <= -2), default=None)
    if i is None or j is None or j < i: return None
    return sum(w[:i]), w[i:j + 1], -sum(w[j + 1:]) if False else sum(w[:j + 1])
if sys.argv[1] == "pairs":
    P = [(1, "3 2 1 0 -1 -2"), (4, "2 1 0 -1 -2 -3"), (0, "2 3 2 1 0 -1 -2"), (1, "3 2 1 0 0 -1 -2"), (2, "3 2 1 0 -1 -2 -3"),
         (4, "2 1 0 -1 -1 -2 -3"), (4, "2 1 0 0 -1 -2 -3"), (5, "2 1 0 -1 -2 -3 -2"), (5, "2 1 0 -1 -2 -2 -3"), (4, "2 2 1 0 -1 -2 -3 -3"),
         (4, "3 2 1 0 -1 -2 -3 -4"), (1, "4 3 2 1 0 -1 -2 -3 -3"), (2, "3 3 2 1 0 -1 -2 -3 -4")]
    for s1, m in P:
        m = tuple(map(int, m.split())); s2 = s1 + sum(m)
        print("s1 =", s1, " m =", *m, " s2 =", s2, " joined odd pairs, |Odd(s1)|, |Odd'(s2)|:", test(s1, m, s2))
else:
    N = int(sys.argv[1])
    for n in range(5, N + 1):
        seen = set(); bad = []
        for w in words(n):
            t = split(w)
            if t is None or t in seen: continue
            seen.add(t)
            if test(*t)[0] == 0: bad.append(t)
        print(f"n = {n}: {len(seen)} triples (s1, m, s2); not joined: {len(bad)}", *bad[:6])
