"""Leapfrog walk.  State: permutation matrix with one marked stone ('one short': its row+column sum is 1 below target).
R: swap the marked stone's row with the next row; the mark stays in the row.  C: same for columns.
R and C are involutions that keep the multiset of targets, so alternating them gives paths and cycles.
A path ends when the mark is in the last row (R due) or last column (C due).
Usage: python3 leapfrog.py     (prints the orbit of the n = 10 exception found by letters_zigzag_exc.py)"""
def orbit(n, cells, first, stop_at_last=True, limit=10**6):
    pos = list(cells); byrow = {p[0]: k for k, p in enumerate(pos)}; bycol = {p[1]: k for k, p in enumerate(pos)}
    cur = 0; mode = first; start = (tuple(pos), cur, mode); trace = [(cur, mode, pos[cur])]
    for _ in range(limit):
        r, c = pos[cur]
        if mode == 0:
            if r == n: return "end: mark in last row", trace
            o = byrow[r + 1]; pos[cur] = (r + 1, c); pos[o] = (r, pos[o][1]); byrow[r + 1] = cur; byrow[r] = o
        else:
            if c == n: return "end: mark in last column", trace
            o = bycol[c + 1]; pos[cur] = (r, c + 1); pos[o] = (pos[o][0], c); bycol[c + 1] = cur; bycol[c] = o
        cur = o; mode ^= 1; trace.append((cur, mode, pos[cur]))
        if stop_at_last and cur == n - 1: return "ok: last stone pushed", trace
        if (tuple(pos), cur, mode) == start: return "cycle", trace
    return "limit", trace
if __name__ == "__main__":
    w = [(1, 2), (3, 1), (2, 3), (4, 5), (5, 6), (8, 4), (6, 7), (7, 8)]; n = 10
    cells = [(1, 1)] + [(r + 1, c + 1) for r, c in w] + [(n, n)]
    for f in (0, 1):
        res, tr = orbit(n, cells, f)
        print("first move", "RC"[f], "->", res, "length", len(tr) - 1)
        print("   marks (stone, cell):", " ".join(f"{k + 1}@{p[0]},{p[1]}" for k, m, p in tr[:60]))
