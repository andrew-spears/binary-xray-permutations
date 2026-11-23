"""Item 3: letters in {-2..2} inside slack <= S.  (a) largest slack-only family (greatest fixed point) -- sizes; (b) the same when the family may
depend on (slack, last letter); (c) I(s, last letter) = intersection of F(x) over all prefixes x (distinct diagonals: next letter >= last - 1);
(d) number of states of slack s with no predecessor under the letter 2 / under 1.
  python3 l2.py S"""
import sys
sys.path.insert(0, "../weights")
from maya import Maya
S = int(sys.argv[1]); Mo = Maya(S + 2); St = [Mo.states(s) for s in range(S + 1)]; ix = [{t: i for i, t in enumerate(L)} for L in St]
LET = (-2, -1, 0, 1, 2); full = [(1 << len(L)) - 1 for L in St]
succ = {(s, e): [sum(1 << ix[s + e][u] for u in set(Mo.succ(t, e))) for t in St[s]] for s in range(S + 1) for e in LET if 0 <= s + e <= S}
def step(A, s, e):
    out = 0; L = succ[s, e]; i = 0
    while A:
        if A & 1: out |= L[i]
        A >>= 1; i += 1
    return out
cnt = lambda A: bin(A).count("1")
G = [1] + full[1:]; ch = True
while ch:
    ch = False
    for s in range(S + 1):
        g = G[s]
        for e in LET:
            if 0 <= s - e <= S: g &= step(G[s - e], s - e, e)
        if g != G[s]: G[s] = g; ch = True
print("(a) slack-only family, sizes by slack:", [cnt(g) for g in G])
ok = lambda l, e: l is None or e >= l - 1
I = {}; seen = set(); stack = [(1, 0, None)]
while stack:
    F, s, l = stack.pop()
    if (F, s, l) in seen: continue
    seen.add((F, s, l)); I[s, l] = I.get((s, l), full[s]) & F
    for e in LET:
        if 0 <= s + e <= S and ok(l, e): stack.append((step(F, s, e), s + e, e))
print(f"(c) {len(seen)} distinct (F, slack, last letter); sizes of the intersections, rows = slack, columns = last letter -2..2:")
for s in range(S + 1): print("   ", s, [cnt(I.get((s, l), 0)) if (s, l) in I else "." for l in LET])
H = {k: full[k[0]] for k in I}; H[0, None] = 1; ch = True
while ch:
    ch = False
    for (s, l) in list(H):
        if l is None: continue
        g = H[s, l]; src = [(s - l, p) for p in list(LET) + [None] if (s - l, p) in H and ok(p, l)] if 0 <= s - l <= S else []
        for q in src: g &= step(H[q], q[0], l)
        if not src: g = 0
        if g != H[s, l]: H[s, l] = g; ch = True
print("(b) family depending on (slack, last letter); sizes, rows = slack, columns = last letter -2..2:")
for s in range(S + 1): print("   ", s, [cnt(H[s, l]) if (s, l) in H else "." for l in LET])
print("(d) states with no predecessor, by slack: letter 2:", [len(St[s]) - cnt(step(full[s - 2], s - 2, 2)) for s in range(2, S + 1)], " letter 1:", [len(St[s]) - cnt(step(full[s - 1], s - 1, 1)) for s in range(1, S + 1)])
