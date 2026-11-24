"""HYBRID-1: w = x m y as in hybrid.py.  Is there u in G(s1), v in conj G(s2), a stone kap of m and a cell for it such that the number of ways
to place the OTHER stones of m (from u to v) is odd?  And the same with the others row-extreme (chain form of Lemma R: the sorted rows and the
sorted columns of the others, paired in order, have sums 2i + sorted letters).
  python3 hybrid1.py N [v] [uni]     all valid words of length <= N not covered by Theorem 0'  (uni: only m in {0,1,2}*{0,-1,-2}*)"""
import sys
import hybrid as h
from hybrid import l1, G, conjG, RC
N = h.N; VERB = "v" in h.ARGV[2:]; UNI = "uni" in h.ARGV[2:]
res = {}
def chain(R, C, lets):
    """lets = [(index among all, letter)] of the stones to place, in the frame where stone j of m has diagonal 2j + m_j"""
    w = sorted(2 * j + e - 2 * i for i, (j, e) in enumerate(lets, 1))
    return len(R) == len(C) == len(w) and all(r + c - 2 * i == x for i, (r, c, x) in enumerate(zip(R, C, w), 1))
def analyse(s1, m):
    """list of (kap, row, col, u, v, extreme) with an odd number of placements of the other stones"""
    if (s1, m) in res: return res[s1, m]
    k = len(m); s2 = s1 + sum(m); g = G(s1); cg = sorted(conjG(s2))
    bwd = [None] * (k + 1); bwd[k] = {v: 1 << i for i, v in enumerate(cg)}
    for i in range(k - 1, -1, -1):
        d = {}
        for t1, b in bwd[i + 1].items():
            for kk, t in l1.preds(t1, m[i]): d[t] = d.get(t, 0) ^ b
        bwd[i] = {t: b for t, b in d.items() if b}
    out = []
    for kap in range(1, k + 1):
        P = {}
        for t, a in h.push(s1, m[:kap - 1]).items():
            for kk, t1 in l1.succs(t, m[kap - 1]):
                b = bwd[kap].get(t1)
                if b:
                    row = P.setdefault(kk, {}); i = 0
                    while a >> i:
                        if a >> i & 1: row[i] = row.get(i, 0) ^ b
                        i += 1
        for kk, row in P.items():
            r = kap + kk + 1; c = 2 * kap + m[kap - 1] - r; lets = [(j, e) for j, e in enumerate(m, 1) if j != kap]
            for i, b in row.items():
                j = 0
                while b >> j:
                    if b >> j & 1:
                        R, C = RC(g[i], cg[j], k); assert r in R and c in C
                        out.append((kap, r, c, g[i], cg[j], chain([z for z in R if z != r], [z for z in C if z != c], lets)))
                    j += 1
    res[s1, m] = out; return out
stat = {}
def unimodal(m):
    t = next((i for i, e in enumerate(m) if e < 0), len(m))
    return all(0 <= e <= 2 for e in m[:t]) and all(-2 <= e <= 0 for e in m[t:])
def rec(w, s):
    n = len(w)
    if n and s == 0 and h.split(w):
        x, m, y = h.split(w)
        if not UNI or unimodal(m):
            o = analyse(sum(x), m); st = stat.setdefault(n, [0, 0, 0, None, None]); st[0] += 1; e = [z for z in o if z[5]]
            st[1] += not o; st[2] += not e
            if not o and st[3] is None: st[3] = w
            if not e and st[4] is None: st[4] = w
            if VERB: print(" ".join(map(str, w)), "| s1", sum(x), "m", m, "odd (stone, cell, u, v):", len(o), "extreme:", len(e), "stones:", sorted({z[0] for z in e}))
    if n == N: return
    L = N - n - 1
    for e in range(max((w[-1] - 1) if w else -N, -s), 2 * N):
        if s + e + L * e - L * (L + 1) // 2 > 0: break
        rec(w + (e,), s + e)
if __name__ == "__main__":
    rec((), 0)
    f = lambda w: " ".join(map(str, w)) if w else "-"
    for n in sorted(stat):
        c, b1, b2, w1, w2 = stat[n]
        print(f"n {n}: {c} words; no odd one-stone hybrid {b1} (first {f(w1)}); none with the others row-extreme {b2} (first {f(w2)})", flush=True)
