"""HYBRID: for a valid word w = x m y (m from the first letter >= 2 to the last letter <= -2; s1, s2 the slacks before and after m) count the
m-walks from u in G(s1) to v in conj G(s2) modulo 2.  (HYBRID): some pair (u, v) has an odd number.
  python3 hybrid.py N            all valid words of length <= N not covered by Theorem 0'
Per word also: H0 = an odd pair with u, v among the four hook states (s|-), (-|s), (1^s|-), (-|1^s);  RX = an odd pair whose (R, C) is row-extreme
(sorted rows and sorted columns paired in order have the sums 2i + sorted letters of m)."""
import sys
sys.path.insert(0, "../l1sets"); sys.path.insert(0, "../l2sets")
sys.argv, ARGV = [sys.argv[0], "0"], sys.argv
import l1
from neg0 import in_G
N = int(ARGV[1]); VERB = "v" in ARGV[2:]
l1.depth = lambda u: len(u[0]) + len(u[1]) + 6 + 2 * N
def parts(n, m=None):
    m = n if m is None else m
    if n == 0: yield (); return
    for a in range(min(n, m), 0, -1):
        for p in parts(n - a, a): yield (a,) + p
Gs, cG = {}, {}
def G(s):
    if s not in Gs: Gs[s] = sorted(u for k in range(s + 1) for lam in parts(k) for nu in parts(s - k) for u in [(lam, nu)] if in_G(u))
    return Gs[s]
def conjG(s):
    if s not in cG: cG[s] = frozenset((l1.conj(u[0]), l1.conj(u[1])) for u in G(s))
    return cG[s]
def hooks(s):                                                 # states are (lam, nu), nu = mu'
    return {((s,), ()), ((1,) * s, ()), ((), (s,)), ((), (1,) * s)} if s else {((), ())}
memo = {}
def push(s1, m):
    """dict v -> bitmask over G(s1): parity of the number of m-walks u -> v"""
    if (s1, m) not in memo:
        if not m: memo[s1, m] = {u: 1 << i for i, u in enumerate(G(s1))}
        else:
            out = {}
            for u, msk in push(s1, m[:-1]).items():
                for k, v in l1.succs(u, m[-1]): out[v] = out.get(v, 0) ^ msk
            memo[s1, m] = {v: b for v, b in out.items() if b}
    return memo[s1, m]
DEP = 3 * N + 8
def rows(u, k): return {b + k + 1 for b in l1.beads(u[0], DEP)}                       # used rows, relative, after k more stones (all rows >= -DEP + k + 1)
def freecols(u, k): return {k - y for y in l1.beads(u[1], DEP)}
def RC(u, v, k):
    R = rows(v, k) - rows(u, 0); C = freecols(u, 0) - freecols(v, k)
    return tuple(sorted(r for r in R if r > -DEP + k + 2)), tuple(sorted(c for c in C if c < DEP - 2))
def rowextreme(R, C, m):
    return len(R) == len(C) == len(m) and all(r + c == 2 * i + e for i, (r, c, e) in enumerate(zip(R, C, sorted(m)), 1))
def split(w):
    i = next((j for j, e in enumerate(w) if e >= 2), None); j = max((j for j, e in enumerate(w) if e <= -2), default=None)
    return None if i is None or j is None or i > j else (w[:i], w[i:j + 1], w[j + 1:])
stat = {}
def test(w):
    x, m, y = split(w); s1 = sum(x); s2 = s1 + sum(m); P = push(s1, m); g = G(s1); cg = conjG(s2); h1 = hooks(s1); h2 = hooks(s2)
    odd = [(g[i], v) for v, b in P.items() if v in cg for i in range(len(g)) if b >> i & 1]
    h0 = [p for p in odd if p[0] in h1 and p[1] in h2]
    rx = [p for p in odd if rowextreme(*RC(p[0], p[1], len(m)), m)]
    return len(odd), len(h0), len(rx), len({RC(u, v, len(m)) for u, v in odd})
def rec(w, s):
    n = len(w)
    if n and s == 0 and split(w):
        o, h, r, nrc = test(w); st = stat.setdefault(n, [0, 0, 0, 0, 10 ** 9, None, None, None]); st[0] += 1
        st[1] += not o; st[2] += not h; st[3] += not r
        if o < st[4]: st[4], st[5] = o, w
        if not h and st[6] is None: st[6] = w
        if not r and st[7] is None: st[7] = w
        if VERB: print(" ".join(map(str, w)), "odd pairs", o, "hook pairs", h, "row-extreme", r, "distinct (R, C)", nrc)
    if n == N: return
    L = N - n - 1
    for e in range(max((w[-1] - 1) if w else -N, -s), 2 * N):
        if s + e + L * e - L * (L + 1) // 2 > 0: break
        rec(w + (e,), s + e)
if __name__ == "__main__":
    rec((), 0)
    f = lambda w: " ".join(map(str, w)) if w else "-"
    for n in sorted(stat):
        c, bo, bh, br, mn, w, wh, wr = stat[n]
        print(f"n {n}: {c} words; HYBRID fails {bo} (least number of odd pairs {mn} at {f(w)}); no odd hook pair {bh} (first {f(wh)}); no odd row-extreme pair {br} (first {f(wr)})", flush=True)
