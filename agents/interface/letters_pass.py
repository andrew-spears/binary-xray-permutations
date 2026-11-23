"""Rounds and passing, for the zigzag chain on + M -, M = B_1 ... B_k, block witnesses from the class K.
(1) Rounds lemma (proved in letters_notes.md), checked here: the mark only ever passes between neighbouring blocks;
    whenever it comes back down out of a block it returns to the bottom stone, and at that moment every block below
    the one that sent it back is where it was when the round started.
(2) Passing claim: every block (+ M' -) has, for each first move m in {R, C}, a witness in K that lets a mark
    entering by m through to the top (tested between two corner stones).
Usage: python3 letters_pass.py nmax      (blocks up to length nmax - 2, chains up to size nmax)"""
import sys
sys.argv, argv = [sys.argv[0], "0"], sys.argv
from itertools import product
from collections import Counter
from letters_flip import blocks, frame
from letters_bits import KBw
from letters_scatter import beh
sym = lambda b: "".join("+0-"[1 - x] for x in b)
def run(n, cells, first, owner):
    """Chain with a rounds check.  Returns (reached top?, last move, violations)."""
    pos = list(cells); byrow = {p[0]: k for k, p in enumerate(pos)}; bycol = {p[1]: k for k, p in enumerate(pos)}
    home = list(cells); cur = 0; mode = first; start = None; bad = 0; down = None
    while True:
        st = (tuple(pos), cur, mode)
        if st == start: return False, None, bad
        if start is None: start = st
        r, c = pos[cur]
        if mode == 0:
            o = byrow[r + 1]; pos[cur] = (r + 1, c); pos[o] = (r, pos[o][1]); byrow[r + 1] = cur; byrow[r] = o
        else:
            o = bycol[c + 1]; pos[cur] = (r, c + 1); pos[o] = (pos[o][0], c); bycol[c + 1] = cur; bycol[c] = o
        a, b = owner[cur], owner[o]
        if abs(a - b) > 1: bad += 1                       # jumped over a block
        if b < a and down is None: down = a               # block a sent the mark back
        if b > a and down is not None: bad += 1           # went up again before reaching the bottom stone
        if o == 0:
            if down is None or any(pos[k] != home[k] for k in range(n) if owner[k] < down): bad += 1
            down = None; home = list(pos)                 # next round starts from here
        if o == n - 1: return True, mode, bad
        cur = o; mode ^= 1
if __name__ == "__main__":
    nmax = int(argv[1]); st = Counter(); fails = []
    for n in range(3, nmax + 1):
        for M in product((-1, 0, 1), repeat=n - 2):
            s = 0; ok = True
            for x in M:
                s += x
                if s < 0: ok = False; break
            if not ok or s: continue
            bl = blocks(M); lists = [KBw(b) for b in bl]
            offs = [sum(len(b) for b in bl[:i]) for i in range(len(bl))]
            owner = [0] + [i + 1 for i, b in enumerate(bl) for _ in b] + [len(bl) + 1]
            for combo in product(*lists):
                a = tuple((r + o, c + o) for (wit, _), o in zip(combo, offs) for r, c in wit)
                for m in (0, 1):
                    okk, last, bad = run(n, frame(a, n), m, owner); st["chain runs"] += 1; st["rounds violations"] += bad
            if len(bl) == 1 and len(M) > 1:
                st["blocks"] += 1
                bs = [beh(tuple(sorted(b))) for b in {frozenset(wit) for wit, _ in lists[0]}]   # distinct boards
                for i, m in enumerate("RC"):
                    if not any(b.split("/")[i] != "F" for b in bs): fails.append((sym(M), m))
                st["block witnesses"] += len(bs); st["block witnesses reflecting both moves"] += sum(b == "F/F" for b in bs)
        print(n, dict(st), "blocks with no passing witness for some move:", len(fails), fails[:3], flush=True)
