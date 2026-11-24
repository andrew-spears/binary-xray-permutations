# Words with letters in {-1, 0, 1} (no 1 directly followed by -1): does the two-chain machine always succeed?
import sys
from collections import Counter
from m2 import solvable, runs, stepA, stepB
def mwords(n):
    out = []
    def rec(w, s):
        if len(w) == n:
            if s == 0: out.append(tuple(w))
            return
        for e in (-1, 0, 1):
            if s + e < 0 or s + e > n - len(w) - 1: continue
            if w and w[-1] == 1 and e == -1: continue
            w.append(e); rec(w, s + e); w.pop()
    rec([], 0); return out
if __name__ == "__main__":
    for n in range(2, int(sys.argv[1]) + 1):
        ws = mwords(n); bad = [w for w in ws if not solvable(w)]
        print("n =", n, "words", len(ws), "without a two-chain solution:", len(bad), *bad[:2])
