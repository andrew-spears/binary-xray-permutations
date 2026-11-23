"""Zigzag-chain induction for L_1.  Word w = + M - of length n (M: letters -1,0,1, prefix sums >= 0, total 0).
Start: any witness of M on rows/columns 2..n-1 plus corner stones (1,1), (n,n)  (a witness of 0 M 0).
Chain: stone 1 moves up one row (swapping rows with the stone above); the stone that lost 1 is repaired by moving it
up one row or right one column, pushing another stone down/left; stop when the pushed stone is stone n.
Reports, per word: does the alternating chain (row, column, row, ...) or (column, row, ...) succeed from every /
some witness of M?   Usage: python3 letters_zigzag.py nmax"""
import sys
from itertools import product
def witnesses(m, e):          # all witnesses of the word e on rows/cols 1..m, as lists of cells per stone
    out = []
    def rec(k, R, C, acc):
        if k > m: out.append(list(acc)); return
        for r in range(1, m + 1):
            c = 2 * k + e[k - 1] - r
            if 1 <= c <= m and not (R >> r & 1) and not (C >> c & 1):
                acc.append((r, c)); rec(k + 1, R | 1 << r, C | 1 << c, acc); acc.pop()
    rec(1, 0, 0, []); return out
def chain(n, cells, first):   # cells[k] = (r, c) for stone k = 0..n-1; returns True if the alternating chain ends on stone n
    pos = list(cells); byrow = {p[0]: k for k, p in enumerate(pos)}; bycol = {p[1]: k for k, p in enumerate(pos)}
    cur = 0; mode = first; steps = 0
    while steps < 4 * n * n:
        steps += 1; r, c = pos[cur]
        if mode == 0:
            if r == n: return False
            o = byrow[r + 1]; pos[cur] = (r + 1, c); pos[o] = (r, pos[o][1]); byrow[r + 1] = cur; byrow[r] = o
        else:
            if c == n: return False
            o = bycol[c + 1]; pos[cur] = (r, c + 1); pos[o] = (pos[o][0], c); bycol[c + 1] = cur; bycol[c] = o
        if o == n - 1: return True
        cur = o; mode ^= 1
    return False
for n in range(3, int(sys.argv[1]) + 1):
    m = n - 2; tot = allw = somew = 0; bad = None
    for e in product((-1, 0, 1), repeat=m):
        s = 0; ok = True
        for x in e:
            s += x
            if s < 0: ok = False; break
        if not ok or s: continue
        tot += 1; ws = witnesses(m, e)
        res = [any(chain(n, [(1, 1)] + [(r + 1, c + 1) for r, c in w] + [(n, n)], f) for f in (0, 1)) for w in ws]
        allw += all(res); somew += any(res)
        if not any(res) and bad is None: bad = e
    print(f"n={n}: {tot} words + M -; chain works from every witness of M: {allw}; from some witness: {somew}; first total failure: {bad}", flush=True)
