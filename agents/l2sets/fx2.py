"""Exact reachable sets for words with letters in [-C, C] (distinct diagonals: next letter >= last - 1), slacks <= S, against
'saturation j letters back':  F(x' w) = step_w(Sat(Gamma(x')))  for |w| = j ?   Sat(G) = all states of that slack whose class a + b is in G,
Gamma(x') = set of classes on F(x').  Nodes = distinct (F, slack, last J letters, Sat j letters back for j <= J).
  python3 fx2.py C S J"""
import sys
sys.path.insert(0, "../weights"); sys.path.insert(0, "../l1sets")
from maya import Maya
C, S = int(sys.argv[1]), int(sys.argv[2]); J = int(sys.argv[3]) if len(sys.argv) > 3 else 0
Mo = Maya(S + C); St = [Mo.states(s) for s in range(S + 1)]; ix = [{t: i for i, t in enumerate(L)} for L in St]
LET = tuple(range(-C, C + 1)); full = [(1 << len(L)) - 1 for L in St]
succ = {(s, e): [sum(1 << ix[s + e][u] for u in set(Mo.succ(t, e))) for t in St[s]] for s in range(S + 1) for e in LET if 0 <= s + e <= S}
def step(A, s, e):
    out = 0; L = succ[s, e]; i = 0
    while A:
        if A & 1: out |= L[i]
        A >>= 1; i += 1
    return out
def c0(m):
    W = Mo.W
    return sum(1 for k in range(0, W) if k % 2 == 0 and m >> (k + W) & 1) - sum(1 for k in range(-W, 0) if k % 2 == 0 and not m >> (k + W) & 1)
cl = [[c0(t[0]) + c0(t[1]) for t in L] for L in St]
clsmask = [{c: sum(1 << i for i in range(len(St[s])) if cl[s][i] == c) for c in set(cl[s])} for s in range(S + 1)]
def sat(F, s): return sum(m for c, m in clsmask[s].items() if F & m)
cnt = lambda A: bin(A).count("1")
names = lambda A, s: " ".join(Mo.name(St[s][i]) for i in range(len(St[s])) if A >> i & 1)
if __name__ == "__main__":
    # node: (F, s, w = last <= J letters, hist = tuple of (sat j letters back pushed through the last j letters) for j = 0..len(w))
    seen = {}; stack = [(1, 0, (), (1,), ())]
    while stack:
        F, s, w, hist, word = stack.pop()
        key = (F, s, w, hist)
        if key in seen: continue
        seen[key] = word
        for e in LET:
            if not 0 <= s + e <= S or (w and e < w[-1] - 1): continue
            F2 = step(F, s, e); h2 = (sat(F2, s + e),) + tuple(step(h, s, e) for h in hist)
            stack.append((F2, s + e, (w + (e,))[-J:], h2[:J + 1], word + (e,)))
    print(f"letters [-{C}, {C}], slack <= {S}: {len(seen)} nodes (F, slack, last {J} letters, history); distinct (F, slack): {len({(k[0], k[1]) for k in seen})}")
    for j in range(0, J + 1):
        tot = ok = 0; worst = {}
        for (F, s, w, hist), word in seen.items():
            if len(hist) <= j: continue
            tot += 1; assert F & ~hist[j] == 0
            if F == hist[j]: ok += 1
            else:
                d = cnt(hist[j] & ~F)
                if w[-j - 1:] not in worst or worst[w[-j - 1:]][0] < d: worst[w[-j - 1:]] = (d, s, word)
        print(f"  j = {j}: F(x'w) = step_w(Sat(x')) for {ok} of {tot} nodes; failing suffixes (last j+1 letters: largest defect, slack, word): " +
              "; ".join(f"{' '.join(map(str, k))}: {v[0]} at s {v[1]} ({''.join('+' if e > 0 else '-' if e < 0 else '0' for e in v[2]) if C == 1 else ' '.join(map(str, v[2]))})" for k, v in sorted(worst.items())[:40]))
