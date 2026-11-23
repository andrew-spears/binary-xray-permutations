"""Which combinations of chain choices make the next chain close into a cycle?  Each block + M - of a word gets a
chirality string: its own first move (R/C) followed by the strings of its inner blocks, e.g. R(C) for + + 0 - -.
Usage: python3 letters_chir.py '+0-++0--' ..."""
import sys
sys.argv, argv = [sys.argv[0], "0"], sys.argv
from letters_closed import chain
def build(e):                 # list of (witness, chirality string) for the word e
    n = len(e)
    if n == 0: return [((), "")]
    s = 0
    for i, x in enumerate(e):
        s += x
        if s == 0: break
    i += 1
    if i < n: return [(a + tuple((r + i, c + i) for r, c in b), sa + sb) for a, sa in build(e[:i]) for b, sb in build(e[i:])]
    if n == 1: return [(((1, 1),), "0")]
    out = []
    for a, sa in build(e[1:-1]):
        for f in (0, 1):
            res = chain(n, ((1, 1),) + tuple((r + 1, c + 1) for r, c in a) + ((n, n),), f)[0]
            out.append((res, "RC"[f] + "(" + sa + ")" if res else None))
    return [(w, s) for w, s in out if w]
for word in argv[1:]:
    e = tuple({"+": 1, "0": 0, "-": -1}[ch] for ch in word); n = len(e) + 2
    good = []; bad = []
    for a, sa in build(e):
        ok = chain(n, ((1, 1),) + tuple((r + 1, c + 1) for r, c in a) + ((n, n),), 0)[0] is not None
        (good if ok else bad).append(sa)
    print(word, "-> chain ok for", len(good), "cycles for", len(bad)); print("   ok:    ", " ".join(good)); print("   cycle: ", " ".join(bad))
