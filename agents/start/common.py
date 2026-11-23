"""Square board n: Landau D generation, placement DFS, (restricted) LP."""
import numpy as np
from scipy.optimize import linprog


def landau_D(n):
    """All Landau D (sorted tuples) for the n x n board, via score sequences."""
    out = []
    def rec(k, prev, tot, s):
        if k == n:
            if tot == n * (n - 1) // 2:
                out.append(tuple(s[i] - (n - 1 - i) for i in range(n)))  # d_k = s_k - n + k (k 1-based)
            return
        for v in range(prev, n):
            t = tot + v
            if t < (k + 1) * k // 2: continue
            # remaining n-k-1 entries each >= v, sum must not overshoot: t + v*(n-k-1) <= C(n,2)
            if t + v * (n - k - 1) > n * (n - 1) // 2: break
            s.append(v); rec(k + 1, v, t, s); s.pop()
    rec(0, 0, 0, [])
    return out


def tight_cut(n, D):
    s = [D[i] + n - 1 - i for i in range(n)]
    t = 0
    for k in range(1, n):
        t += s[k - 1]
        if t == k * (k - 1) // 2: return True
    return False


def placement(n, D):
    """DFS row by row; returns dict d->row or None."""
    Ds = list(D)
    sol = {}
    def rec(r, usedD, usedC):
        if r > n: return True
        for i, d in enumerate(Ds):
            c = r + d
            if not (usedD >> i) & 1 and 1 <= c <= n and not (usedC >> c) & 1:
                sol[d] = r
                if rec(r + 1, usedD | (1 << i), usedC | (1 << c)): return True
        return False
    return dict(sol) if rec(1, 0, 0) else None


def lp(n, D, a=None, ret=False):
    """Plain LP (a=None) or LP restricted to cells with r = a[d] mod 2."""
    Ds = list(D); Di = {d: i for i, d in enumerate(Ds)}
    cells = [(r, r + d) for d in Ds for r in range(1, n + 1)
             if 1 <= r + d <= n and (a is None or r % 2 == a[d])]
    A = np.zeros((3 * n, len(cells)))
    for j, (r, c) in enumerate(cells):
        A[r - 1, j] = 1; A[n + c - 1, j] = 1; A[2 * n + Di[c - r], j] = 1
    if not cells or np.any(A.sum(axis=1) == 0): return (False, None) if ret else False
    res = linprog(np.zeros(len(cells)), A_eq=A, b_eq=np.ones(3 * n), bounds=(0, None), method="highs")
    ok = res.status == 0
    if ret: return ok, (cells, res.x if ok else None)
    return ok


def counts_ok(n, D, a):
    odd_r = sum(a[d] for d in D)
    odd_c = sum((a[d] + d) % 2 for d in D)
    return odd_r == (n + 1) // 2 and odd_c == (n + 1) // 2


def parity_test(n, D, a):
    return counts_ok(n, D, a) and lp(n, D, a)
