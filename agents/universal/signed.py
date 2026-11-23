"""Signed and unsigned numbers of placements per state (sign = sign of the row order times sign of the column order,
i.e. the coefficient of z^d in a_{lambda+delta}(z) a_{mu+delta}(z)).  For each slack s <= B: over all prefixes with
letters >= 0, at most L letters, no leading 0, ending at (s, 0), list the universal states (from cores_24.txt) whose
signed count is nonzero for every such prefix.   Usage: python3 signed.py B L"""
import sys
from collections import defaultdict
from load import load, nm
B, L = int(sys.argv[1]), int(sys.argv[2])
D = load("cores_24.txt")

def adds(lam):
    out = []
    for h in range((lam[0] if lam else 0) + len(lam) + B + 2):
        j = sum(1 for p in lam if p > h)
        out.append((h - j, tuple(p for p in tuple(q - 1 for q in lam[:j]) + (h,) + lam[j:] if p), -1 if j & 1 else 1))
    return out
cache = {}
def step(V, e):
    W = defaultdict(lambda: [0, 0])
    for (lam, mu), (n, sg) in V.items():
        key = (lam, mu, e)
        if key not in cache:
            A = adds(lam); Bm = {u: (m, s) for u, m, s in adds(mu)}
            cache[key] = [((a, Bm[e - u][0]), sa * Bm[e - u][1]) for u, a, sa in A if e - u in Bm]
        for st, s2 in cache[key]:
            W[st][0] += n; W[st][1] += sg * s2
    return W
res = defaultdict(list)
def go(V, s, last, k):
    if last == 0 and s >= 1: res[s].append(V)
    if k == L: return
    for e in range(max(last - 1, 0) if k else 1, B - s + 1):
        go(step(V, e), s + e, e, k + 1)
go({((), ()): [1, 1]}, 0, 0, 0)
for s in range(1, B + 1):
    U = D[(s, 0)][0] & D[(s, 0)][1]
    good = [c for c in U if all(V[c][1] != 0 for V in res[s])]
    pos = [c for c in good if len({V[c][1] > 0 for V in res[s]}) == 1]
    print(f"slack {s:2d}: {len(res[s]):5d} prefixes, {len(U):3d} universal states, signed count never 0: {len(good):3d}, of constant sign: {len(pos)}",
          " ".join(sorted(nm(c) for c in good)[:6]))
