"""Static form of the zigzag chain.  Witness W of 0 M 0 (corner stones (1,1), (n,n)).  Graph on stones: row edge
i -> o if row(o) = row(i)+1, column edge if col(o) = col(i)+1.  The alternating walk from stone 1 (row edge first, or
column edge first) is injective on (stone, next edge type), so it always ends at stone n.  If it visits no stone
twice, moving every visited stone along its out-edge gives a witness of + M -.
Per word M: is there a witness whose alternating walk is simple?  Which extremal witnesses have a simple walk?
Usage: python3 letters_static.py nmax"""
import sys
from itertools import product
def witnesses(m, e):
    out = []
    def rec(k, R, C, acc):
        if k > m: out.append(tuple(acc)); return
        for r in range(1, m + 1):
            c = 2 * k + e[k - 1] - r
            if 1 <= c <= m and not (R >> r & 1) and not (C >> c & 1):
                acc.append((r, c)); rec(k + 1, R | 1 << r, C | 1 << c, acc); acc.pop()
    rec(1, 0, 0, []); return out
def walk(n, cells, first):      # list of stones visited (0-based), or None if some stone is visited twice
    byrow = {p[0]: k for k, p in enumerate(cells)}; bycol = {p[1]: k for k, p in enumerate(cells)}
    cur = 0; mode = first; seen = [0]
    while cur != n - 1:
        r, c = cells[cur]
        cur = byrow[r + 1] if mode == 0 else bycol[c + 1]; mode ^= 1
        if cur in seen: return None
        seen.append(cur)
    return seen
crit = {
 "min sum |u|": lambda w: sum(abs(r - k - 1) for k, (r, c) in enumerate(w)),
 "min sum u^2": lambda w: sum((r - k - 1) ** 2 for k, (r, c) in enumerate(w)),
 "min max |u|": lambda w: max(abs(r - k - 1) for k, (r, c) in enumerate(w)),
 "min inversions(rows)": lambda w: sum(1 for i in range(len(w)) for j in range(i) if w[j][0] > w[i][0]),
 "min inv(rows)+inv(cols)": lambda w: sum(1 for i in range(len(w)) for j in range(i) if w[j][0] > w[i][0]) + sum(1 for i in range(len(w)) for j in range(i) if w[j][1] > w[i][1]),
 "lex smallest rows": lambda w: tuple(r for r, c in w),
 "lex largest rows": lambda w: tuple(-r for r, c in w),
}
if __name__ == "__main__":
    for n in range(3, int(sys.argv[1]) + 1):
        m = n - 2; tot = some = 0; good = {c: 0 for c in crit}; anygood = {c: 0 for c in crit}; first = None
        for e in product((-1, 0, 1), repeat=m):
            s = 0; ok = True
            for x in e:
                s += x
                if s < 0: ok = False; break
            if not ok or s: continue
            tot += 1; ws = witnesses(m, e)
            full = lambda w: ((1, 1),) + tuple((r + 1, c + 1) for r, c in w) + ((n, n),)
            simple = {w: any(walk(n, full(w), f) for f in (0, 1)) for w in ws}
            if any(simple.values()): some += 1
            elif first is None: first = e
            for cn, f in crit.items():
                best = min(f(w) for w in ws); ext = [w for w in ws if f(w) == best]
                good[cn] += all(simple[w] for w in ext); anygood[cn] += any(simple[w] for w in ext)
        print(f"n={n}: {tot} words; some witness has a simple walk: {some}; first failure {first}")
        for cn in crit: print(f"     {cn}: all extremal witnesses simple for {good[cn]}, some extremal simple for {anygood[cn]}")
        sys.stdout.flush()
