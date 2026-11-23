"""Item 2: least |S| of an RR-split and of an I-split against the window bound W(e) = least |S| such that every stone k
outside S has at least ceil(-e_k / 2) stones of S before it and at least ceil(e_k / 2) after it (a necessary condition).
Words without a tight cut.  Usage: python3 least.py n [v]"""
import sys, itertools
from ext import words, parts, shape, conj, splits
from x2 import isplit
def window(e, S):
    b = 0; n = len(e); tot = len(S); Sset = set(S)
    for k in range(1, n + 1):
        if k in Sset: b += 1
        elif -e[k - 1] > 2 * b or e[k - 1] > 2 * (tot - b): return False
    return True
def rr(e, S):
    mask = sum(1 << (k - 1) for k in S); w1, w2 = parts(e, mask)
    if min(w1) < 0 or min(w2) < 0: return False
    return splits(conj(shape(w2)[0]), shape(w1)[0])
n = int(sys.argv[1]); tab = {}; ex = {}
for e in words(n, False):
    if not any(e) or any(sum(e[:k]) == 0 for k in range(1, n)): continue
    W = R = I = None
    for m in range(1, n):
        for S in itertools.combinations(range(1, n + 1), m):
            if not window(e, S): continue
            if W is None: W = m
            if R is None and rr(e, S): R = m
            if I is None and isplit(e, S): I = m
            if R and I: break
        if R and (I or m >= R + 2): break
    key = (max(map(abs, e)) + 1) // 2, W, R - W, "none" if I is None else I - W
    tab[key] = tab.get(key, 0) + 1; ex.setdefault(key, e)
print(f"n = {n}; columns: ceil(max|e|/2), window bound W, least RR size - W, least I size - W (none = none of size <= RR + 1): number of words, first word")
for key in sorted(tab, key=str): print("  ", key, tab[key], ex[key])
