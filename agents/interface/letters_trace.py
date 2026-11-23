"""Trace the zigzag chain on + M - block by block.  For each choice of block witnesses from K, print the sequence of
visits: block number, how the mark entered (from below '>' or above '<', with the move R/C that brought it in),
how many times a stone inside was marked (the entry counts), and where it left.  Usage: python3 letters_trace.py '+0-++0--' [first]"""
import sys
sys.argv, argv = [sys.argv[0], "0"], sys.argv
from itertools import product
from letters_flip import blocks, frame
from letters_bits import KBw
def trace(n, cells, first, owner):
    pos = list(cells); byrow = {p[0]: k for k, p in enumerate(pos)}; bycol = {p[1]: k for k, p in enumerate(pos)}
    cur = 0; mode = first; start = None; seq = []
    while True:
        st = (tuple(pos), cur, mode)
        if st == start: return seq, "loop"
        if start is None: start = st
        r, c = pos[cur]
        if mode == 0:
            o = byrow[r + 1]; pos[cur] = (r + 1, c); pos[o] = (r, pos[o][1]); byrow[r + 1] = cur; byrow[r] = o
        else:
            o = bycol[c + 1]; pos[cur] = (r, c + 1); pos[o] = (pos[o][0], c); bycol[c + 1] = cur; bycol[c] = o
        seq.append((owner[cur], owner[o], "RC"[mode], cur, o))
        if o == n - 1: return seq, "ok"
        cur = o; mode ^= 1
if __name__ == "__main__":
    word = argv[1]; first = int(argv[2]) if len(argv) > 2 else 0
    M = tuple({"+": 1, "0": 0, "-": -1}[ch] for ch in word); n = len(M) + 2
    bl = blocks(M); lists = [KBw(b) for b in bl]; offs = [sum(len(b) for b in bl[:i]) for i in range(len(bl))]
    owner = [0] + [i + 1 for i, b in enumerate(bl) for _ in b] + [len(bl) + 1]
    for combo in product(*lists):
        a = tuple((r + o, c + o) for (wit, _), o in zip(combo, offs) for r, c in wit)
        bits = "".join("." if f is None else "RC"[f] for _, f in combo)
        seq, why = trace(n, frame(a, n), first, owner)
        out = []; inside = 0
        for a_, b_, m, cur, o in seq:
            if a_ == b_: inside += 1
            else:
                out.append(f"{inside + 1}" if out else ""); out.append(f" {'>' if b_ > a_ else '<'}{m} [{b_}]:"); inside = 0
        print(bits, why, len(seq), "".join(out))
