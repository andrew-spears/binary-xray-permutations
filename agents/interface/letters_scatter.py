"""Scattering of a mark by one block.  Put a block witness from K between two corner stones and send the mark in
from the bottom stone by a row move (R) or a column move (C).  It either comes out at the top stone ('T' followed by
the last move) or comes back to the bottom stone ('F', reflected).  Prints, for sibling pairs of block witnesses
(same inner witness, first move R / C), how often each pair of behaviours occurs.
Usage: python3 letters_scatter.py maxlen [-v]"""
import sys
sys.argv, argv = [sys.argv[0], "0"], sys.argv
from itertools import product
from collections import Counter
from letters_flip import frame, KM
from letters_trace import trace
from letters_closed import chain
sym = lambda b: "".join("+0-"[1 - x] for x in b)
def beh(wit):
    n = len(wit) + 2; owner = [0] + [1] * len(wit) + [2]; out = []
    for m in (0, 1):
        seq, why = trace(n, frame(wit, n), m, owner)
        k = next(i for i, s in enumerate(seq) if s[1] != 1 and i > 0) if len(seq) > 1 else 0
        a, b, mv, _, _ = seq[k]
        out.append("T" + mv if b == 2 else "F")
    return "/".join(out)
if __name__ == "__main__":
    L = int(argv[1]); verbose = "-v" in argv; tab = Counter(); single = Counter()
    for n in range(1, L + 1):
        for w in product((-1, 0, 1), repeat=n):
            s = 0; ok = True
            for i, x in enumerate(w):
                s += x
                if s < 0 or (s == 0 and i < n - 1): ok = False; break
            if not ok or s: continue
            if n == 1: print("0", beh(((1, 1),))); continue
            per = Counter()
            for a in KM(w[1:-1]):
                res = []
                for f in (0, 1):
                    w2 = chain(n, frame(a, n), f)[0]
                    if w2 is None: res = None; break
                    res.append(beh(w2))
                if res is None: per["inner loops"] += 1; continue
                per[tuple(res)] += 1; tab[tuple(res)] += 1
            if verbose: print(sym(w), dict(per))
    ff = sum(v * (k[0] == "F/F") + v * (k[1] == "F/F") for k, v in tab.items())
    both = sum(v for k, v in tab.items() if any(x.split("/")[i] == "F" and y.split("/")[i] == "F" for i in (0, 1) for x, y in [k]))
    print("block witnesses that reflect both moves:", ff, "; sibling pairs that reflect the same move:", both)
    print("sibling pairs (behaviour of R-first witness, of C-first witness), behaviour = on R entry / on C entry:")
    for k, v in sorted(tab.items(), key=lambda kv: -kv[1]): print("  ", k, v)
