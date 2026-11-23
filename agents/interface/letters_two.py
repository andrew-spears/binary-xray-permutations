"""Two marks.  Take ANY witness w of M (letters -1, 0, +1, prefix sums >= 0, total 0) and add corner stones: 0 M 0.
For + M - the bottom stone is one short (mark D) and the top stone one over (mark E).  Moves: D's stone swaps its row
or column with the next one (the mark passes to the other stone); E's stone swaps with the previous one.  When D and E
land on the same stone they cancel and the position is a witness of + M -.
Test: from every witness w of every M, is a witness of + M - reachable when BOTH marks may move (in any order)?
(With D alone this is the zigzag chain, which loops from some w at n = 10.)
Usage: python3 letters_two.py nmax [cap]     (cap = max states explored per start, default 200000)"""
import sys
from itertools import product
def witnesses(t):                      # all placements (r_k, c_k), r_k + c_k = t_k, rows and columns permutations of 1..n
    n = len(t); out = []; rows = [0] * n
    def go(k, ur, uc):
        if k == n: out.append(tuple(rows)); return
        for r in range(max(1, t[k] - n), min(n, t[k] - 1) + 1):
            c = t[k] - r
            if not ur >> r & 1 and not uc >> c & 1:
                rows[k] = r; go(k + 1, ur | 1 << r, uc | 1 << c)
    go(0, 0, 0); return [tuple((r, t[k] - r) for k, r in enumerate(w)) for w in out]
def reach(pos, N, cap):
    """BFS over (positions, D stone, E stone).  Returns (found a witness?, states explored)."""
    start = (pos, 0, N - 1); seen = {start}; todo = [start]
    while todo:
        if len(seen) > cap: return None, len(seen)
        p, d, e = todo.pop()
        for mark, step in ((d, 1), (e, -1)):
            r, c = p[mark]
            for axis in (0, 1):
                line = (r, c)[axis] + step
                if line < 1 or line > N: continue
                o = next(k for k in range(N) if p[k][axis] == line)
                q = list(p)
                q[mark] = (r + step, c) if axis == 0 else (r, c + step)
                q[o] = (p[o][0] - step, p[o][1]) if axis == 0 else (p[o][0], p[o][1] - step)
                if o == (e if mark == d else d): return True, len(seen)
                st = (tuple(q), o, e) if mark == d else (tuple(q), d, o)
                if st not in seen: seen.add(st); todo.append(st)
    return False, len(seen)
if __name__ == "__main__":
    nmax = int(sys.argv[1]); cap = int(sys.argv[2]) if len(sys.argv) > 2 else 200000
    for N in range(3, nmax + 1):
        m = N - 2; tot = bad = unknown = 0; worst = 0; ex = None
        for M in product((-1, 0, 1), repeat=m):
            s = 0; ok = True
            for x in M:
                s += x
                if s < 0: ok = False; break
            if not ok or s: continue
            for w in witnesses([2 * (k + 1) + x for k, x in enumerate(M)]):
                pos = ((1, 1),) + tuple((r + 1, c + 1) for r, c in w) + ((N, N),)
                res, cnt = reach(pos, N, cap); tot += 1; worst = max(worst, cnt)
                if res is None: unknown += 1
                elif not res:
                    bad += 1
                    if ex is None: ex = (M, w)
        print(f"n = {N}: {tot} witnesses of middle words; no witness of + M - reachable: {bad}; undecided (cap): {unknown}; most states explored: {worst}", ex or "", flush=True)
