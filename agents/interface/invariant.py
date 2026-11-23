"""Is there an inductive invariant that only looks at a short summary of the prefix?
Summary = (sigma, last L letters).  I(summary) = greatest family of states with
  I(start) = {(empty, empty)},  I(s.e) subset of step_e(I(s)) for every legal letter e.
Then every prefix with summary s reaches all of I(s).  The summary SUFFICES (within slack <= B)
if every closing letter (e = -sigma) from every summary can be played from I(s).
Usage: python3 invariant.py B L [-v]"""
import sys
def analyse(B, L, verbose=False, upd=None, cap=None, keep=None):
    if upd is None:
        # the last letter is always needed: it decides which letters are legal next
        assert L >= 1, "L must be >= 1"
        upd = lambda hist, e, sig2: (hist + (e,))[-L:]
    last = lambda hist: hist[-1]
    def succ(mask):
        out = []
        for u in range(-B, B + 1):
            if mask >> (B + u) & 1: continue
            m = mask | (1 << (B + u))
            if not (m & 1): continue
            out.append((u, m >> 1))
        return out
    cache = {}
    def sm(m):
        if m not in cache: cache[m] = succ(m)
        return cache[m]
    def step(S, e):
        T = set()
        for (rm, cm) in S:
            for (u, r2) in sm(rm):
                v = e - u
                if v < -B or v > B or (cm >> (B + v) & 1): continue
                c2 = cm | (1 << (B + v))
                if c2 & 1: T.add((r2, c2 >> 1))
        return frozenset(T)
    base = (1 << B) - 1
    start = (0, ())
    edges = {}          # summary -> list of (e, summary2)   (closing letters: summary2 = None)
    stack = [start]; nodes = {start}
    while stack:
        s = stack.pop(); sig, hist = s
        lo = last(hist) - 1 if hist else 0
        out = []
        for e in range(max(lo, -sig), B - sig + 1):
            if cap is not None and abs(e) > cap: continue      # restricted alphabet
            s2 = sig + e
            if s2 == 0:
                if sig == 0: continue
                out.append((e, None)); continue
            if s2 + max(e, 0) * max(e - 1, 0) // 2 > B: continue      # cannot finish inside bound
            t = (s2, upd(hist, e, s2))
            out.append((e, t))
            if t not in nodes: nodes.add(t); stack.append(t)
        edges[s] = out
    # all states of each excess
    allst = {0: frozenset([(base, base)])}
    lvl = {(base, base): 0}; frontier = [(base, base)]
    # generate all pairs of masks by excess via BFS over single-bead moves is awkward; enumerate masks directly
    from itertools import combinations
    def excess(mask):
        xs = sorted((j - B + 1 for j in range(2 * B) if mask >> j & 1), reverse=True)
        return sum(x + i for i, x in enumerate(xs))
    masks = {}
    for comb in combinations(range(2 * B), B):
        m = sum(1 << j for j in comb); ex = excess(m)
        if ex <= B: masks.setdefault(ex, []).append(m)
    def allstates(sig):
        return frozenset((r, c) for a in range(sig + 1) for r in masks.get(a, []) for c in masks.get(sig - a, [])
                         if keep is None or keep(r, c))      # keep: restrict the family to a class of states
    I = {s: allstates(s[0]) for s in nodes}
    I[start] = frozenset([(base, base)])
    preds = {}
    for s, out in edges.items():
        for e, t in out:
            if t is not None: preds.setdefault(t, []).append((s, e))
    changed = True; rounds = 0
    while changed:
        changed = False; rounds += 1
        for t in nodes:
            if t == start: continue
            new = I[t]
            for (s, e) in preds.get(t, []):
                new = new & step(I[s], e)
            if new != I[t]: I[t] = new; changed = True
    fails = []
    for s, out in edges.items():
        for e, t in out:
            if t is None and not step(I[s], e): fails.append((s, e))
        if s != start and not I[s]: fails.append((s, "empty"))
    return nodes, I, fails, allstates
if __name__ == "__main__":
    B = int(sys.argv[1]); L = int(sys.argv[2])
    nodes, I, fails, allstates = analyse(B, L, "-v" in sys.argv)
    print(f"B={B} L={L}: {len(nodes)} summaries; invariant", "SUFFICES" if not fails else f"FAILS at {len(fails)} places, e.g. {sorted(fails, key=str)[:3]}")
    if "-v" in sys.argv:
        for s in sorted(nodes): print("  ", s, len(I[s]), "/", len(allstates(s[0])))
