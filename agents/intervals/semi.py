"""Semiorders (unit interval orders): Dyck path, j-th up-step matched to j-th down-step.
e_j = (height just after the j-th down-step) - (height just before the j-th up-step).
Which legal words arise?   usage: python3 semi.py n"""
import sys
from iv import words
def dyck(n):
    out = []
    def rec(p, u, d):
        if u == n and d == n: out.append(tuple(p)); return
        if u < n: p.append(1); rec(p, u + 1, d); p.pop()
        if d < u: p.append(0); rec(p, u, d + 1); p.pop()
    rec([], 0, 0)
    return out
def word(p):
    h = 0; U = []; V = []
    for s in p:
        if s: U.append(h); h += 1
        else: h -= 1; V.append(h)
    return tuple(v - u for u, v in zip(U, V))
for n in range(2, int(sys.argv[1]) + 1):
    W = set(words(n)); got = {}
    for p in dyck(n):
        w = word(p)
        if w in W: got[w] = got.get(w, 0) + 1
    miss = sorted(W - set(got))
    print(f"n = {n}: {len(W)} words; from semiorders: {len(got)}; missing {len(miss)}", miss[:3], "max multiplicity", max(got.values()))
