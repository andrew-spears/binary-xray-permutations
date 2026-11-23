"""Largest slack-only family for L1 inside slack <= S:  G(0) = {empty}, G(s) = step_1(G(s-1)) n step_0(G(s)) n step_-1(G(s+1)) (greatest fixed point).
Also I(s) = intersection of F(x) over all L1 prefixes x with slacks <= S ending at slack s, and P(s) = intersection over x in {0,1}* (slack s).
  python3 fam.py S [show]"""
import sys
sys.path.insert(0, "../weights")
from maya import Maya, dval
S = int(sys.argv[1]); show = len(sys.argv) > 2
Mo = Maya(S + 1); St = [Mo.states(s) for s in range(S + 1)]; ix = [{t: i for i, t in enumerate(L)} for L in St]
conj = lambda l: tuple(sum(1 for a in l if a > j) for j in range(l[0])) if l else ()
cj = [[ix[s][(Mo.mask(conj(Mo.part(t[0]))), Mo.mask(conj(Mo.part(t[1]))))] for t in St[s]] for s in range(S + 1)]
succ = {}   # (s, e) -> list of bitmasks of successors
for s in range(S + 1):
    for e in (-1, 0, 1):
        if 0 <= s + e <= S: succ[s, e] = [sum(1 << ix[s + e][u] for u in set(Mo.succ(t, e))) for t in St[s]]
def step(A, s, e):
    out = 0; L = succ[s, e]; i = 0
    while A:
        if A & 1: out |= L[i]
        A >>= 1; i += 1
    return out
full = [(1 << len(L)) - 1 for L in St]
def gfp():
    G = [1] + full[1:]
    while True:
        ch = False
        for s in range(1, S + 1):
            g = G[s] & step(G[s - 1], s - 1, 1) & step(G[s], s, 0)
            if s < S: g &= step(G[s + 1], s + 1, -1)
            if g != G[s]: G[s] = g; ch = True
        g0 = 1 & step(G[0], 0, 0) & step(G[1], 1, -1)
        if g0 != G[0]: G[0] = g0; ch = True
        if not ch: return G
def inter(letters):
    I = list(full); seen = set(); stack = [(1, 0)]
    while stack:
        F, s = stack.pop()
        if (F, s) in seen: continue
        seen.add((F, s)); I[s] &= F
        for e in letters:
            if 0 <= s + e <= S: stack.append((step(F, s, e), s + e))
    return I, len(seen)
def conjset(A, s): return sum(1 << cj[s][i] for i in range(len(St[s])) if A >> i & 1)
names = lambda A, s: " ".join(Mo.name(St[s][i]) for i in range(len(St[s])) if A >> i & 1)
if __name__ == "__main__":
    G = gfp(); P, nP = inter((0, 1)); I, nI = inter((-1, 0, 1))
    print(f"bound {S}: {nP} distinct (F, slack) for 0/1 words, {nI} for L1 prefixes")
    for s in range(S + 1):
        U = P[s] & conjset(P[s], s)
        print(f"s {s}: {len(St[s])} states; |G| = {bin(G[s]).count('1')}  |I| = {bin(I[s]).count('1')}  |P| = {bin(P[s]).count('1')}  |P n conj P| = {bin(U).count('1')}"
              f"  G = I: {G[s] == I[s]}  G = P n conj P: {G[s] == U}  G conj-closed: {conjset(G[s], s) == G[s]}")
        if show: print("   not in G:", names(full[s] & ~G[s], s))
