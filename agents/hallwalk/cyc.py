# Reflecting a closed chain.  For a solution (stones (r, c), lines r + c) and an integer k, phi_k(r) = row of the stone in
# column r + k.  If r_1 -> r_2 -> ... -> r_m -> r_1 is a cycle of phi_k, replace each of its stones (r, c) by (c - k, r + k):
# same lines, same set of rows, same set of columns, so again a solution of the same set.  (k = 0, all cycles: the transpose.)
# Question: are all solutions of a valid set connected by such reflections?
import sys
from hw import valid_sets, solutions
def neighbours(L, pi):
    n = len(L); col = {pi[i]: L[i] - pi[i] for i in range(n)}; rowof = {c: r for r, c in col.items()}
    out = set()
    for k in range(-(n - 1), n):
        seen = set()
        for r0 in range(1, n + 1):
            if r0 in seen: continue
            cyc = [r0]; x = r0; ok = True
            while True:
                c = x + k
                if c < 1 or c > n: ok = False; break
                x = rowof[c]
                if x == r0: break
                cyc.append(x)
            if not ok: continue
            seen.update(cyc)
            if all(col[r] == r + k for r in cyc): continue          # fixed by the reflection
            new = dict(col)
            for r in cyc: del new[r]
            for r in cyc: new[col[r] - k] = r + k
            out.add(tuple(sorted(new.items())))
    return out
N = int(sys.argv[1])
for n in range(3, N + 1):
    V = valid_sets(n); disc = 0; ex = None; maxcomp = 1
    for L in V:
        sols = solutions(L)
        S = {tuple(sorted((pi[i], L[i] - pi[i]) for i in range(n))) for pi in sols}
        start = next(iter(S)); seen = {start}; st = [start]; comps = 0
        rest = set(S)
        while rest:
            comps += 1; s0 = next(iter(rest)); st = [s0]; rest.discard(s0)
            while st:
                s = st.pop(); pi = None
                rows = {}
                for (r, c) in s: rows[r + c] = r
                p = tuple(rows[l] for l in L)
                for t in neighbours(L, p):
                    assert t in S
                    if t in rest: rest.discard(t); st.append(t)
        if comps > 1: disc += 1; ex = ex or (L, comps, len(S))
        maxcomp = max(maxcomp, comps)
    print("n =", n, "sets", len(V), "| sets whose solutions are NOT all connected by cycle reflections:", disc, "first", ex, "| most components", maxcomp, flush=True)
