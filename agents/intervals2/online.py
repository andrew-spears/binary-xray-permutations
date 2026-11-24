"""No online rule: find a prefix x and two endings z1, z2 (x z1, x z2 legal words) such that no state of the partition
machine after x can be completed along both z1 and z2.  Then no rule that chooses m from the letters read so far
(with any memory) solves every word."""
import sys
sys.path.insert(0, "../intervals")
from iv import words
from pm import succ
from collections import defaultdict
def good_states(w, k):
    """states lam after w[:k] from which the rest of w can be completed"""
    F = {()}
    for e in w[:k]: F = {v for u in F for v in succ(u, e)}
    out = set()
    for u in F:
        G = {u}
        for e in w[k:]: G = {v for a in G for v in succ(a, e)}
        if G: out.add(u)
    return out
def search(n1, n2):
    by = defaultdict(list)
    for n in range(n1, n2 + 1):
        for w in words(n):
            for k in range(1, n): by[w[:k]].append(w)
    best = None
    for x, ws in by.items():
        gs = [(w, good_states(w, len(x))) for w in ws]
        for i in range(len(gs)):
            for j in range(i):
                if not (gs[i][1] & gs[j][1]):
                    cand = (len(gs[i][0]) + len(gs[j][0]), x, gs[j][0][len(x):], gs[i][0][len(x):], sorted(gs[j][1]), sorted(gs[i][1]))
                    if best is None or cand < best: best = cand
    return best
if __name__ == "__main__":
    b = search(int(sys.argv[1]), int(sys.argv[2]))
    if b is None: print("no witness"); sys.exit()
    tot, x, z1, z2, g1, g2 = b
    print("prefix x =", x); print("ending z1 =", z1, " states after x that can be completed:", g1)
    print("ending z2 =", z2, " states after x that can be completed:", g2)
