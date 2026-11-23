"""The prefixes x attaining a(l) = min w(F(x)) for l = 0, 1 (and the three smallest values).
Usage: python3 argmin.py DATA NAME"""
import sys
from weights import *
D = Data(sys.argv[1], False); name = sys.argv[2]
for s in range(2, D.B + 1):
    w = candidates(D.lev[s], s)[name]; w = w / w.sum()
    for l in (0, 1):
        v = D.sets(1, s, l) @ w; o = np.argsort(v)[:2]; words = D.F[(s, l)][1]
        print(f"s {s:2d} l {l}: " + ";  ".join(f"{v[i]:.3f} |F| {int(D.sets(1, s, l)[i].sum())}/{len(w)} x = {' '.join(map(str, words[i]))}" for i in o))
