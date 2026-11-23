"""One canonical witness per L_1 word: w(0) = one stone; w(uv) = direct sum; w(+ M -) = result of the chain started
with a row move (R) or with a column move (C) from w(M) plus corner stones, by a fixed rule.
Rules: 'R' always row first; 'C' always column first; 'alt' row first at odd nesting depth, column first at even.
Reports the first word where the rule's chain closes into a cycle.   Usage: python3 letters_canon.py nmax"""
import sys
from itertools import product
from functools import lru_cache
sys.argv, argv = [sys.argv[0], "0"], sys.argv
from letters_closed import chain
def make(rule):
    @lru_cache(None)
    def w(e, depth=0):
        n = len(e)
        if n == 0: return ()
        s = 0
        for i, x in enumerate(e):
            s += x
            if s == 0: break
        i += 1
        if i < n:
            a = w(e[:i], depth); b = w(e[i:], depth)
            return None if a is None or b is None else a + tuple((r + i, c + i) for r, c in b)
        if n == 1: return ((1, 1),)
        a = w(e[1:-1], depth + 1)
        if a is None: return None
        f = {"R": 0, "C": 1, "alt": depth & 1}[rule]
        return chain(n, ((1, 1),) + tuple((r + 1, c + 1) for r, c in a) + ((n, n),), f)[0]
    return w
for rule in ("R", "alt"):
    w = make(rule)
    for n in range(2, int(argv[1]) + 1):
        tot = bad = 0; first = None
        for e in product((-1, 0, 1), repeat=n):
            s = 0; ok = True
            for x in e:
                s += x
                if s < 0: ok = False; break
            if not ok or s: continue
            tot += 1
            if w(e) is None:
                bad += 1
                if first is None: first = e
        if bad or n == int(argv[1]): print(f"rule {rule} n={n}: {tot} words, no witness for {bad}, first {first}", flush=True)
