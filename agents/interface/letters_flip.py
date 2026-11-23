"""Zigzag chain on + M -, M = B_1 ... B_k (top-level blocks: zeros and irreducible + M' -), block witnesses from the
closed class K.  Each irreducible block witness has a sibling: the other end of its leapfrog path (same inner witness,
other first move).  Test: whenever the chain on (a_1, ..., a_k) closes into a loop, does it reach the top stone after
replacing ONE block witness by its sibling?  Reports, per position rule (last block, first block, any block).
Usage: python3 letters_flip.py nmax"""
import sys
from itertools import product
from functools import lru_cache
from collections import Counter
sys.argv, argv = [sys.argv[0], "0"], sys.argv
from letters_closed import chain
def blocks(w):
    out = []; s = 0; st = 0
    for i, x in enumerate(w):
        s += x
        if s == 0: out.append(w[st:i + 1]); st = i + 1
    return out
def frame(a, n): return ((1, 1),) + tuple((r + 1, c + 1) for r, c in a) + ((n, n),)
@lru_cache(None)
def KB(w):            # irreducible block or single zero: list of (witness, sibling or None)
    n = len(w)
    if n == 1: return ((((1, 1),), None),)
    out = []
    for a in KM(w[1:-1]):
        x = chain(n, frame(a, n), 0)[0]; y = chain(n, frame(a, n), 1)[0]
        if x: out.append((x, y)); out.append((y, x))
    return tuple(dict.fromkeys(out))
@lru_cache(None)
def KM(w):            # all witnesses of a word: direct sums of block witnesses
    res = [()]; off = 0
    for b in blocks(w):
        res = [a + tuple((r + off, c + off) for r, c in x) for a in res for x, _ in KB(b)]; off += len(b)
    return tuple(res)
st = Counter(); ex = {}
for n in range(4, int(argv[1]) + 1):
    for M in product((-1, 0, 1), repeat=n - 2):
        s = 0; ok = True
        for x in M:
            s += x
            if s < 0: ok = False; break
        if not ok or s: continue
        bl = blocks(M); lists = [KB(b) for b in bl]
        if any(not l for l in lists): st["block with empty class"] += 1; continue
        offs = [sum(len(b) for b in bl[:i]) for i in range(len(bl))]
        def build(choice): return tuple((r + o, c + o) for wit, o in zip(choice, offs) for r, c in wit)
        for combo in product(*lists):
            a = build([x for x, _ in combo]); st["runs"] += 1
            if chain(n, frame(a, n), 0)[0]: continue
            st["loops"] += 1
            fixes = []
            for i, (x, sib) in enumerate(combo):
                if sib is None: continue
                ch = [y for y, _ in combo]; ch[i] = sib
                if chain(n, frame(build(ch), n), 0)[0]: fixes.append(i)
            nz = [i for i, (x, sib) in enumerate(combo) if sib is not None]
            if not fixes: st["no single flip fixes"] += 1; ex.setdefault("none", (n, M))
            if nz and nz[-1] not in fixes: st["last block flip fails"] += 1; ex.setdefault("last", (n, M))
            if nz and nz[0] not in fixes: st["first block flip fails"] += 1; ex.setdefault("first", (n, M))
            if len(fixes) != len(nz): st["some flip fails"] += 1; ex.setdefault("some", (n, M))
    print(n, dict(st), flush=True)
print(ex)
