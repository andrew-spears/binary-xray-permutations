# Three-chain solutions as two words a (rows) and b (columns) in letters A, B, C.  Flipped convention: stone (i, c) on line i + c,
# chains increasing; letters of the chains are assigned by greedy (patience) so the word pair is canonical for the solution.
import sys
from blocks import sols, lis
def ab(D, n, w=3):
    out = []
    for p in sols(D, n):
        q = p[::-1]                       # flip rows: stone (i, q[i]) on line i + q[i] = n - 1 - r + c
        if lis([-x for x in q]) > w: continue
        last = []; col = []
        for c in q:                       # greedy cover by increasing sequences
            b = -1
            for j, l in enumerate(last):
                if l < c and (b < 0 or l > last[b]): b = j
            if b < 0: last.append(c); col.append(len(last) - 1)
            else: last[b] = c; col.append(b)
        a = "".join("ABC"[j] for j in col); bw = [""] * n
        for i, c in enumerate(q): bw[c] = "ABC"[col[i]]
        out.append((a, "".join(bw), q))
    return out
if __name__ == "__main__":
    w = [int(x) for x in sys.argv[1:]]; n = len(w); D = [e + 2 * (k + 1) - n - 1 for k, e in enumerate(w)]
    r = ab(D, n); print(*w, "| D", D, "|", len(r), "solutions with at most three chains")
    for a, b, q in sorted(r)[:40]: print("  a =", a, " b =", b, " lines", [i + c + 2 for i, c in enumerate(q)])
