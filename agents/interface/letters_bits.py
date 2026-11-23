"""For + M -, M = B_1 ... B_k: which choices of the blocks' own first moves (R = 0 / C = 1, one bit per block that is
not 0 or + -) make the chain on + M - loop?  Block witnesses from the class K (see letters_flip.py).
Prints, for every M with a loop: the blocks, whether looping depends only on these top-level bits, and the looping
bit vectors.  Usage: python3 letters_bits.py nmax"""
import sys
from itertools import product
from functools import lru_cache
from collections import defaultdict
sys.argv, argv = [sys.argv[0], "0"], sys.argv
from letters_closed import chain
from letters_flip import blocks, frame, KM
sym = lambda b: "".join("+0-"[1 - x] for x in b)
@lru_cache(None)
def KBb(w):           # (witness, first-move bit or None)
    n = len(w)
    if n <= 2: return ((tuple((i + 1, i + 1) for i in range(1)) if n == 1 else ((1, 2), (2, 1)), None),) if n == 1 else None
    out = []
    for a in KM(w[1:-1]):
        for f in (0, 1):
            x = chain(n, frame(a, n), f)[0]
            if x: out.append((x, f))
    return tuple(dict.fromkeys(out))
def KBw(w):
    if len(w) == 2:
        x = chain(2, frame((), 2), 0)[0]; return ((x, None),)
    return KBb(w)
if __name__ == "__main__":
    nmax = int(argv[1]); tot = dep = 0
    for n in range(4, nmax + 1):
        for M in product((-1, 0, 1), repeat=n - 2):
            s = 0; ok = True
            for x in M:
                s += x
                if s < 0: ok = False; break
            if not ok or s: continue
            bl = blocks(M); lists = [KBw(b) for b in bl]
            offs = [sum(len(b) for b in bl[:i]) for i in range(len(bl))]
            res = defaultdict(set)
            for combo in product(*lists):
                a = tuple((r + o, c + o) for (wit, _), o in zip(combo, offs) for r, c in wit)
                bits = "".join("." if f is None else "RC"[f] for _, f in combo)
                res[bits].add(chain(n, frame(a, n), 0)[0] is None)
            if not any(True in v for v in res.values()): continue
            tot += 1
            mixed = [b for b, v in res.items() if len(v) == 2]
            dep += bool(mixed)
            loops = sorted(b for b, v in res.items() if v == {True})
            print(n, " ".join(sym(b) for b in bl), "| loops:", " ".join(loops), "| of", len(res), "| depends on inner bits:" , " ".join(sorted(mixed)) or "no", flush=True)
    print("words with a loop:", tot, "; looping depends on more than the top-level bits:", dep)
