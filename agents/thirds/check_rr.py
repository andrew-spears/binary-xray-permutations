# Brute-force check of ./rrfixed: for every RR-split (word, S, columns C) it prints, the number of placements of S on
# (rows R, columns C) and of the other stones on the other rows and columns must both be odd.
# Usage: ./rrfixed 9 010 p | python3 check_rr.py 010
import sys
pat = sys.argv[1]; nchk = 0; bad = 0
def count(ds, rows, cols):   # placements of the diagonals ds (1-based r + c = d + 2 ... here 0-based r + c = d) on rows x cols
    if not ds: return 1
    d = ds[0]; t = 0
    for r in rows:
        c = d - r
        if c in cols: t += count(ds[1:], rows - {r}, cols - {c})
    return t
for line in sys.stdin:
    if not line.startswith("RR"): continue
    w, S, C = [list(map(int, x.split())) for x in line[2:].split("|")]
    n = len(w); d = [2 * k + w[k] for k in range(n)]
    R = frozenset(r for r in range(n) if pat[r % len(pat)] == "1"); C = frozenset(c - 1 for c in C); S = [k - 1 for k in S]
    a = count([d[k] for k in S], R, C); b = count([d[k] for k in range(n) if k not in S], frozenset(range(n)) - R, frozenset(range(n)) - C)
    nchk += 1; bad += (a * b) % 2 == 0
print("RR-splits checked: %d; not odd: %d" % (nchk, bad))
