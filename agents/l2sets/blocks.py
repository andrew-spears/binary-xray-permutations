"""Largest family on block ends for letters in [-2, 2] (distinct diagonals), slacks <= S.
A block = (letters outside {0, 1})* + one closing letter in {0, 1}.  Type of a prefix ending in 0 or 1 = (slack, final non-increasing run, <= WIN letters).
J = largest family with J(start) = {empty}, J(type(x w)) inside step_w(J(type(x))) n MASK(slack) for every block w.   MASK: all | central | G (= Central minus T of l1sets).
  python3 blocks.py 2 S WIN MASK [dump]"""
import sys
from fx2 import *
sys.setrecursionlimit(100000)
import l1
WIN = int(sys.argv[3]) if len(sys.argv) > 3 else 3; MASK = sys.argv[4] if len(sys.argv) > 4 else "all"
tol1 = lambda t: (Mo.part(t[0]), l1.conj(Mo.part(t[1])))
U = [[tol1(t) for t in L] for L in St]
if MASK == "all": mask = list(full)
elif MASK == "central": mask = [sum(1 << i for i, u in enumerate(L) if l1.central(u)) for L in U]
elif MASK.startswith("m"): mask = [sum(1 << i for i in range(len(St[s])) if max(cl[s][i], 1 - cl[s][i]) <= int(MASK[1:])) for s in range(S + 1)]   # classes with m = max(c, 1 - c) <= bound
elif MASK == "G": mask = [sum(1 << i for i, u in enumerate(L) if (l1.central(u) and not l1.in_T(u)) or not any(u)) for L in U]
def newrun(run, block):
    w = run + block; r = [w[-1]]
    for a, b in zip(w[-2::-1], w[::-1]):
        if a >= b and len(r) < WIN: r.append(a)
        else: break
    return tuple(reversed(r))
def blocks_from(last, s):
    """all blocks (as tuples) that may follow a prefix ending in `last` at slack s, staying in [0, S]"""
    out = []
    def rec(w, s, l):
        for e in LET:
            if (l is not None and e < l - 1) or not 0 <= s + e <= S: continue
            if e in (0, 1): out.append(w + (e,))
            else: rec(w + (e,), s + e, e)
    rec((), s, last); return out
if __name__ == "__main__":
    types = {(0, ()): 1}; trans = []   # trans: (src type, block, dst type)
    todo = [(0, ())]
    while todo:
        t = todo.pop(); s, run = t
        for w in blocks_from(run[-1] if run else None, s):
            d = (s + sum(w), newrun(run, w)); trans.append((t, w, d))
            if d not in types: types[d] = mask[d[0]]; todo.append(d)
    print(f"letters [-2, 2], slack <= {S}, window {WIN}, mask {MASK}: {len(types)} types, {len(trans)} block transitions", flush=True)
    by_src = {}
    for t, w, d in trans: by_src.setdefault(t, []).append((w, d))
    ch = True; rounds = 0; first = []
    while ch:
        ch = False; rounds += 1
        for t, lst in by_src.items():
            memo = {}
            def img(w):
                if w not in memo:
                    s0 = t[0] + sum(w[:-1]); memo[w] = step(img(w[:-1]), s0, w[-1]) if w else types[t]
                return memo[w]
            for w, d in lst:
                g = types[d] & img(w)
                if g != types[d]:
                    if not g and not first: first.append((t, w, d, rounds))
                    types[d] = g; ch = True
    empt = [t for t, v in types.items() if not v]
    print(f"{rounds} rounds; empty types: {len(empt)}; empty state in J(slack 0, run ending in 0): {all(v == 1 for (s, r), v in types.items() if s == 0)}")
    if first: print("first type to become empty: slack %d run %s, through the block %s from slack %d run %s (round %d)" % (first[0][2][0], first[0][2][1], first[0][1], first[0][0][0], first[0][0][1], first[0][3]))
    runs = sorted({r for s, r in types}, key=lambda r: (r[-1:], len(r), r))
    print("sizes |J| by run (rows) and slack 0.." + str(S) + "; first row: number of states allowed by the mask")
    print(f"{'mask':>10} " + " ".join(f"{cnt(mask[s]):5d}" for s in range(S + 1)))
    for r in runs: print(f"{' '.join(map(str, r)):>10} " + " ".join(f"{cnt(types[s, r]):5d}" if (s, r) in types else "    ." for s in range(S + 1)))
    if "dump" in sys.argv:
        for s in range(S + 1):
            for r in runs:
                if (s, r) in types: print(f"s {s} run {' '.join(map(str, r))}: missing from mask [{cnt(mask[s] & ~types[s, r])}]: {names(mask[s] & ~types[s, r], s)[:400]}")
