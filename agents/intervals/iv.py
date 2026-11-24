"""Interval-order relaxation.  Stones 1..n in order of diagonal, letters e_k.  In a solution, call two stones
incomparable if neither is above-and-right of the other; e_k = (#incomparable later stones) - (#incomparable earlier
stones).  Relaxation: any poset with 1..n a linear extension.  Sub-case: interval orders in which stone k is
incomparable to exactly the next f(k) stones.  Then f(k) = e_k + (number of earlier intervals still open) is forced.
usage: python3 iv.py n"""
import sys
def words(n):
    out = []
    def rec(w, s):
        if len(w) == n:
            if s == 0: out.append(tuple(w))
            return
        lo = (w[-1] - 1) if w else 0
        for e in range(max(lo, -s), 2 * (n - len(w)) - 1):
            rec(w + [e], s + e)
    rec([], 0)
    return out
def run(w):
    """returns f or None"""
    n = len(w); lam = []; f = []
    for k, e in enumerate(w):
        x = e + len(lam)
        if x < 0 or x > n - 1 - k: return None
        f.append(x); lam = [p - 1 for p in lam if p > 1] + ([x] if x > 0 else [])
    return f
def comparability(n, E):
    """Golumbic: G is a comparability graph iff no implication class contains an edge in both directions."""
    par = {}
    def find(x):
        while par.setdefault(x, x) != x: par[x] = par[par[x]]; x = par[x]
        return x
    adj = [set() for _ in range(n)]
    for a, b in E: adj[a].add(b); adj[b].add(a)
    for b in range(n):
        N = sorted(adj[b])
        for i in range(len(N)):
            for j in range(i + 1, len(N)):
                a, c = N[i], N[j]
                if c not in adj[a]:
                    par[find((a, b))] = find((c, b)); par[find((b, a))] = find((b, c))
    return all(find((a, b)) != find((b, a)) for a, b in E)
if __name__ == "__main__":
    for n in range(2, int(sys.argv[1]) + 1):
        W = words(n); ok = two = 0; bad = []; bad2 = []
        for w in W:
            f = run(w)
            if f is None: bad.append(w); continue
            ok += 1
            E = [(k, j) for k in range(n) for j in range(k + 1, k + f[k] + 1)]
            if comparability(n, E): two += 1
            else: bad2.append(w)
        print(f"n = {n}: {len(W)} words; forced interval order exists for {ok}; of those 2-dimensional (a real solution): {two}",
              "| first failures:", bad[:2], "| first not 2-dim:", bad2[:2])
