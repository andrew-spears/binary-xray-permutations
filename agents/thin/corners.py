"""Corners needed by single words.  T(a, b) = states whose numbers of part sizes are <= a and <= b in some order.
For a word, lists the minimal (a, b), a <= b, such that some walk stays in T(a, b).
Usage: python3 corners.py            (pyramids j, j-1, ..., -j and double staircases)
       python3 corners.py 4 3 5 ...  (one word)"""
import sys
from lazy import *
cn = lambda p: len(set(p))
def walk(word, a, b):
    S = {((), ())}
    for e in word:
        S = {t for st in S for t in succ(st, e) if (cn(t[0]) <= a and cn(t[1]) <= b) or (cn(t[0]) <= b and cn(t[1]) <= a)}
        if not S: return False
    return ((), ()) in S
def need(word, top=7):
    out = []
    for a in range(top + 1):
        for b in range(a, top + 1):
            if any(x <= a and y <= b for x, y in out): continue
            if walk(word, a, b): out.append((a, b))
    return out
if __name__ == "__main__":
    if len(sys.argv) > 1: print(need(tuple(map(int, sys.argv[1:])))); sys.exit()
    for j in range(1, 8):
        w = tuple(range(j, -j - 1, -1)); print(f"pyramid {j} .. {-j}: slack {j * (j + 1) // 2:2d}, needs", need(w), flush=True)
    for j in range(1, 6):
        w = tuple(range(j, -1, -1)) + tuple(range(0, -j - 1, -1)); print(f"pyramid with two zeros {j} .. 0 0 .. {-j}: slack {j * (j + 1) // 2:2d}, needs", need(w), flush=True)
