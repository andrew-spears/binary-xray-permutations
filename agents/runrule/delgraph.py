"""Is COUNT witnessed by inserting ONE stone?  Inserting a new row i and a new column j with a stone at their crossing
turns an n x n permutation matrix into an (n+1) x (n+1) one; old stones north-west of the new one keep their
diagonal, south-east ones gain 2, the others gain 1.  Every rule is of this type on diagonals:
   DEL0     () -> (0)                 x-stones +0, new stone, y-stones +2
   RUN(a,b) u -> v (incl. (1,1): (0,0) -> (1,0,-1))    x +0, the b stones below the gap +1, new stone, the a stones above +1, y +2
Deletion graph of a step  w' = x u y  ->  w = x v y:  P in Sol(w') ~ Q in Sol(w) iff P is Q with one stone (its row and
column) deleted.  Tests, for every legal placement in words of length <= n: is there a matching that saturates
Sol(w') (then single-stone insertion gives an injection), and what are the degrees?   Usage: python3 delgraph.py n"""
import sys
from collections import defaultdict
from countlib import solutions
sys.setrecursionlimit(100000)
n = int(sys.argv[1]); sol = solutions(n)
key = {w: {tuple(sorted(s)): i for i, s in enumerate(S)} for w, S in sol.items()}
def urun(a, b):
    if (a, b) == (1, 1): return (0, 0)
    out = []
    for t in range(a - 1, -b, -1):
        out.append(t)
        if t == a - b: out.append(t)
    return tuple(out)
RULES = [("DEL0", (), (0,))] + [(f"RUN({a},{b})", urun(a, b), tuple(range(a, -b - 1, -1))) for a in range(1, 5) for b in range(1, 5) if a + b <= 6]
def delete(st, k):
    r0, c0 = st[k]
    return tuple(sorted((r - (r > r0), c - (c > c0)) for i, (r, c) in enumerate(st) if i != k))
def graph(w2, w, only=None):
    """adjacency: index of P in Sol(w2) -> set of indices of Q in Sol(w); only = stone index to delete (None: any)"""
    adj = defaultdict(set); K = key[w2]
    for q, st in enumerate(sol[w]):
        for k in (range(len(st)) if only is None else [only]):
            p = K.get(delete(st, k))
            if p is not None: adj[p].add(q)
    return adj
def matching(adj, nL):
    match = {}
    def aug(p, seen):
        for q in adj[p]:
            if q in seen: continue
            seen.add(q)
            if q not in match or aug(match[q], seen): match[q] = p; return True
        return False
    return sum(aug(p, set()) for p in range(nL))
stat = defaultdict(lambda: [0, 0, 0, None, 0, 0])     # placements, count violations, no saturating matching, example, matching with the NEW stone only fails, min degree 0
for w2 in sol:
    for name, u, v in RULES:
        fam = name if name in ("DEL0", "RUN(1,1)") else "RUN(other)"
        for i in range(len(w2) - len(u) + 1):
            if w2[i:i + len(u)] != u: continue
            w = w2[:i] + v + w2[i + len(u):]
            if w not in sol or (name == "DEL0" and not any(w2)): continue
            s = stat[fam]; s[0] += 1; nL = len(sol[w2])
            if len(sol[w]) < nL: s[1] += 1
            adj = graph(w2, w)
            if matching(adj, nL) < nL:
                s[2] += 1
                if s[3] is None or len(w) < len(s[3][1]): s[3] = (w2, w, nL, len(sol[w]), matching(adj, nL))
            if any(len(adj[p]) == 0 for p in range(nL)): s[5] += 1
for fam, s in sorted(stat.items()):
    print(f"{fam:10} placements {s[0]:6}  N(w) < N(w'): {s[1]}  no injection by one-stone insertion: {s[2]}  some solution of w' has no neighbour: {s[5]}   {s[3] if s[3] else ''}")
