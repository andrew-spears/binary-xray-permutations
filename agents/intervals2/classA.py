"""Class A: lists whose decode peels, at every step, either a current maximum or an element of current value 0.
Search top-down over lists (as states: tuple of current values in list order) with memo."""
import sys, itertools
from functools import lru_cache
from lib import valid_sets
MODE = sys.argv[2] if len(sys.argv) > 2 else "A"
@lru_cache(maxsize=None)
def ok(L):
    """L = current list (values in list order).  Is it realizable with every peel a current max (or a 0)?"""
    n = len(L)
    if n == 0: return True
    k = L[-1]
    if k < 0 or k > n - 1: return False
    if MODE == "A" and not (k == max(L) or k == 0): return False
    if MODE == "max" and k != max(L): return False
    return ok(tuple(x + 1 for x in L[:k]) + L[k:-1])
for n in range(3, int(sys.argv[1]) + 1):
    bad = []
    for D in valid_sets(n):
        if not any(ok(p) for p in itertools.permutations(D)): bad.append(D)
    print(n, MODE, "missing", len(bad), bad[:5])
