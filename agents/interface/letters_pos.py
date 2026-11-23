"""Canonical witness with the chirality of each block + M - fixed by a parity:
rule 'start': first move R if the block starts at an odd absolute position, C if even;
rule 'end': by the parity of its last position; rule 'len': by the parity of its length.
Usage: python3 letters_pos.py nmax"""
import sys
from itertools import product
sys.argv, argv = [sys.argv[0], "0"], sys.argv
from letters_closed import chain
def make(rule):
    memo = {}
    def w(e, off):
        key = (e, off & 1)
        if key in memo: return memo[key]
        n = len(e); res = None
        if n == 0: res = ()
        else:
            s = 0
            for i, x in enumerate(e):
                s += x
                if s == 0: break
            i += 1
            if i < n:
                a = w(e[:i], off); b = w(e[i:], off + i)
                res = None if a is None or b is None else a + tuple((r + i, c + i) for r, c in b)
            elif n == 1: res = ((1, 1),)
            else:
                a = w(e[1:-1], off + 1)
                if a is not None:
                    f = {"start": off & 1, "end": (off + n) & 1, "len": n & 1}[rule]
                    res = chain(n, ((1, 1),) + tuple((r + 1, c + 1) for r, c in a) + ((n, n),), f)[0]
        memo[key] = res; return res
    return w
for rule in ("start", "end", "len"):
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
            if w(e, 0) is None:
                bad += 1
                if first is None: first = e
        if bad or n == int(argv[1]): print(f"rule {rule} n={n}: {tot} words, no witness for {bad}, first {first}", flush=True)
