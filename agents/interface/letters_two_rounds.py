"""Rounds with two marks (see letters_two.py).  A D-round: the bottom mark runs (first move R or C, then alternating)
until it meets the top stone (success) or is back on the bottom stone.  An E-round: the same from the top, downwards.
For every witness w of every M:  (a) does some single round succeed?  (b) is a success reachable by a sequence of
failed rounds of either kind followed by a successful one?  (c) by D-rounds alone (= the zigzag chain)?
Usage: python3 letters_two_rounds.py nmax"""
import sys
from itertools import product
from letters_two import witnesses
def round_(p, N, mark, step, mode):
    """Returns ('ok', None) or ('back', new positions)."""
    home = mark; other = N - 1 - mark; p = list(p); cur = mark
    while True:
        r, c = p[cur]; line = (r, c)[mode] + step
        o = next(k for k in range(N) if p[k][mode] == line)
        p[cur] = (r + step, c) if mode == 0 else (r, c + step)
        p[o] = (p[o][0] - step, p[o][1]) if mode == 0 else (p[o][0], p[o][1] - step)
        if o == other: return "ok", None
        if o == home: return "back", tuple(p)
        cur = o; mode ^= 1
MOVES = [(0, 1, 0), (0, 1, 1), (-1, -1, 0), (-1, -1, 1)]          # (mark: 0 = bottom, -1 = top; step; first move)
def explore(start, N, kinds):
    seen = {start}; todo = [start]; first = True; single = False
    while todo:
        p = todo.pop()
        for mk, step, mode in kinds:
            res, q = round_(p, N, mk % N, step, mode)
            if res == "ok":
                if first: single = True
                return True, single
            if q not in seen: seen.add(q); todo.append(q)
        first = False
    return False, False
if __name__ == "__main__":
    for N in range(3, int(sys.argv[1]) + 1):
        tot = nosingle = noseq = noD = 0; ex = None
        for M in product((-1, 0, 1), repeat=N - 2):
            s = 0; ok = True
            for x in M:
                s += x
                if s < 0: ok = False; break
            if not ok or s: continue
            for w in witnesses([2 * (k + 1) + x for k, x in enumerate(M)]):
                pos = ((1, 1),) + tuple((r + 1, c + 1) for r, c in w) + ((N, N),); tot += 1
                good, single = explore(pos, N, MOVES)
                if not single: nosingle += 1
                if not good:
                    noseq += 1
                    if ex is None: ex = (M, w)
                if not explore(pos, N, MOVES[:2])[0]: noD += 1
        print(f"n = {N}: {tot} witnesses; no single round succeeds: {nosingle}; no sequence of D- and E-rounds succeeds: {noseq}; D-rounds alone fail: {noD}", ex or "", flush=True)
