"""NONNEG: for every legal prefix x ending at slack s with last letter l >= 0 there is a prefix x' with ALL letters
>= 0, the same end slack and the same last letter, and F(x') inside F(x).   (Then x'y is legal whenever xy is, and
x'y solvable implies xy solvable.)   Checks all prefixes with slacks <= B.   Usage: python3 nonneg.py B"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "interface"))
from rewrite import machine
def explore(B, nonneg):
    step, start = machine(B)
    word = {(frozenset([start]), 0, None): ()}; layer = list(word)
    while layer:
        nxt = []
        for S, s, last in layer:
            w = word[(S, s, last)]
            lo = 0 if (last is None or nonneg) else -s
            if last is not None: lo = max(lo, last - 1)
            for e in range(lo, B - s + 1):
                x = (step(S, e), s + e, e)
                if x not in word: word[x] = w + (e,); nxt.append(x)
        layer = nxt
    return word
if __name__ == "__main__":
    B = int(sys.argv[1])
    allw = explore(B, False); pos = explore(B, True)
    by = {}
    for (S, s, l) in pos:
        if l is not None: by.setdefault((s, l), []).append(S)
    tested = bad = 0; ex = None
    for (S, s, l), w in allw.items():
        if l is None or l < 0 or (S, s, l) in pos: continue
        tested += 1
        if not any(S2 <= S for S2 in by.get((s, l), ())):
            bad += 1
            if ex is None or len(w) < len(ex): ex = w
    print(f"B = {B}: {len(pos) - 1} reachable sets from nonnegative prefixes, {tested} other sets with last letter >= 0, failures {bad}", ex or "")
