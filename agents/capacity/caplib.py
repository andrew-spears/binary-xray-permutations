"""Capacity of P_D(x) = per(M(x)), M_ij = x_{j-i} if j-i in D.
Permanent by subset DP over used columns (all-positive sums, no cancellation)."""
import numpy as np
from scipy.optimize import minimize
from functools import lru_cache

@lru_cache(None)
def layers(n):
    masks = np.arange(1 << n)
    pc = np.array([bin(m).count("1") for m in masks])
    return [masks[pc == r] for r in range(n + 1)]

def forward_backward(D, x, n):
    """f[mask]: weight of filling rows 0..r-1 (r=popcount) using columns mask.
    g[mask]: weight of completing rows r..n-1 given mask used."""
    L = layers(n)
    N = 1 << n
    f = np.zeros(N); f[0] = 1.0
    for r in range(n):
        ms = L[r]
        for d, xd in zip(D, x):
            j = r + d
            if 0 <= j < n:
                sel = ms[(ms >> j) & 1 == 0]
                f[sel | (1 << j)] += f[sel] * xd   # targets unique per (r,d)
    g = np.zeros(N); g[N - 1] = 1.0
    for r in range(n - 1, -1, -1):
        ms = L[r]
        for d, xd in zip(D, x):
            j = r + d
            if 0 <= j < n:
                sel = ms[(ms >> j) & 1 == 0]
                g[sel] += xd * g[sel | (1 << j)]
    return f, g

def perm_and_grad(D, x, n):
    """returns P and x_d dP/dx_d for each d."""
    f, g = forward_backward(D, x, n)
    P = f[(1 << n) - 1]
    L = layers(n)
    xg = np.zeros(len(D))
    for r in range(n):
        ms = L[r]
        for k, (d, xd) in enumerate(zip(D, x)):
            j = r + d
            if 0 <= j < n:
                sel = ms[(ms >> j) & 1 == 0]
                xg[k] += np.sum(f[sel] * xd * g[sel | (1 << j)])
    return P, xg

def logcap(D, n, t0=None, tol=1e-12):
    D = list(D)
    m = len(D)
    def fun(t):
        t = t - t.mean()          # homogeneity: f invariant under t + c
        x = np.exp(t)
        P, xg = perm_and_grad(D, x, n)
        return np.log(P) - t.sum(), xg / P - 1.0
    t0 = np.zeros(m) if t0 is None else t0
    res = minimize(fun, t0, jac=True, method="BFGS", options={"gtol": 1e-10, "maxiter": 5000})
    t = res.x - res.x.mean()
    return res.fun, t, res

def witnesses(D, n):
    """count permutations whose displacements pi(i)-i are distinct and lie in D."""
    Dset = list(D)
    cnt = 0
    used_c = [False] * n
    used_d = set()
    def rec(i):
        nonlocal cnt
        if i == n:
            cnt += 1; return
        for d in Dset:
            if d in used_d: continue
            j = i + d
            if 0 <= j < n and not used_c[j]:
                used_c[j] = True; used_d.add(d)
                rec(i + 1)
                used_c[j] = False; used_d.discard(d)
    rec(0)
    return cnt

def Pn(n):
    return sorted({-(n - 2), n - 2} | {d for d in range(-(n - 3), n - 2) if (d - (n - 1)) % 2 == 0})

def scores(D, n):
    D = sorted(D)
    return [D[k] + n - 1 - k for k in range(n)]

def strong_score_sequences(n):
    out = []
    def rec(seq, tot):
        k = len(seq)
        if k == n:
            if tot == n * (n - 1) // 2: out.append(tuple(seq))
            return
        lo = seq[-1] if seq else 0
        for s in range(lo, n):
            t = tot + s; k1 = k + 1
            need = k1 * (k1 - 1) // 2
            if k1 < n and t <= need: continue
            if k1 == n and t != need: continue
            # prune: remaining entries >= s, total must reach n(n-1)/2 exactly; max possible
            if t + (n - k1) * (n - 1) < n * (n - 1) // 2: continue
            if t + (n - k1) * s > n * (n - 1) // 2: break
            rec(seq + [s], t)
    rec([], 0)
    return out

def D_from_scores(s, n):
    return [s[k] - n + 1 + k for k in range(n)]
