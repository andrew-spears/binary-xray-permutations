"""Is there a pairing t <-> t' of states such that every F(x) (last letter 0 or 1) contains t or t'?
G = graph on the states of slack s, t ~ t' iff no minimal reachable set at (s, 0), (s, 1) misses both.  A universal state
is adjacent to everything.  Prints the number of covering pairs of non-universal states, the number of states in one,
and the size of a greedy matching (lowest degree first; a maximum matching is at most half the states in some pair).   Usage: python3 pairing.py DATA SMAX"""
import sys
from load import *
D = Data(sys.argv[1], False)
for s in range(2, int(sys.argv[2]) + 1):
    M = np.vstack([D.sets(1, s, 0), D.sets(1, s, 1)]).astype(np.int64); Z = 1 - M; n = M.shape[1]
    uni = np.flatnonzero(Z.sum(0) == 0); adj = (Z.T @ Z) == 0; np.fill_diagonal(adj, False)
    adj[uni, :] = False; adj[:, uni] = False
    deg = adj.sum(1); nodes = int((deg > 0).sum()); edges = int(adj.sum()) // 2; used = np.zeros(n, bool); m = 0
    for t in np.argsort(deg):
        if used[t] or not deg[t]: continue
        c = [u for u in np.flatnonzero(adj[t]) if not used[u]]
        if c: u = min(c, key=lambda u: deg[u]); used[t] = used[u] = True; m += 1
    print(f"s {s:2d}: {n} states, {len(uni)} in every set, {edges} covering pairs among the others, on {nodes} states; greedy matching {m} pairs", flush=True)
print("natural involutions: number of states t (not in every set) with {t, i(t)} a covering pair / number with i(t) != t")
inv = {"conjugate both": lambda t: (conj(t[0]), conj(t[1])), "conjugate first": lambda t: (conj(t[0]), t[1]),
       "conjugate + swap": lambda t: (conj(t[1]), conj(t[0]))}
for s in range(2, int(sys.argv[2]) + 1):
    M = np.vstack([D.sets(1, s, 0), D.sets(1, s, 1)]).astype(bool); row = []
    for name, f in inv.items():
        p = D.sigma(s, f); cov = (M | M[:, p]).all(0); non = ~M.all(0) & (p != np.arange(len(p)))
        row.append(f"{name} {int((cov & non).sum())}/{int(non.sum())}")
    print(f"s {s:2d}: " + ";  ".join(row))
