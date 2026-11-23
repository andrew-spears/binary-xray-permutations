"""Gurvits one-variable peeling test for P_D.
P_D as explicit monomial table; q_S = coefficient of prod_{d in S} x_d^1 (peeling S), a polynomial in D\\S.
cap(q) = inf_{x>0} q(x)/prod x  (log-convex program in t = log x)."""
import sys, numpy as np
sys.path.insert(0, '/home/claude/agents/capacity')
from caplib import strong_score_sequences, D_from_scores
from scipy.optimize import minimize
from scipy.special import logsumexp

def poly(D, n):
    """dict exponent-tuple -> coeff for per(M), M_ij = x_{j-i}."""
    m = len(D); idx = {d: k for k, d in enumerate(D)}
    cur = {0: {(0,)*m: 1}}
    for r in range(n):
        nxt = {}
        for mask, pd in cur.items():
            for d in D:
                j = r + d
                if 0 <= j < n and not (mask >> j) & 1:
                    nm = mask | (1 << j); k = idx[d]
                    tgt = nxt.setdefault(nm, {})
                    for e, c in pd.items():
                        e2 = e[:k] + (e[k]+1,) + e[k+1:]
                        tgt[e2] = tgt.get(e2, 0) + c
        cur = nxt
    return cur[(1 << n) - 1]

def logcap(E, C):
    """E: (N,m) exponent array, C: coeffs. returns log cap."""
    E = np.asarray(E, float); lc = np.log(np.asarray(C, float)); m = E.shape[1]
    if m == 1:
        return lc[0] if len(C)==1 else None
    def f(t):
        t = t - t.mean()
        z = E @ t + lc; L = logsumexp(z); w = np.exp(z - L)
        return L - t.sum(), w @ E - 1.0
    best = None
    for t0 in [np.zeros(m)]:
        r = minimize(f, t0, jac=True, method='BFGS', options={'gtol': 1e-11, 'maxiter': 10000})
        best = r.fun if best is None else min(best, r.fun)
    return best

def restrict(P, S, m):
    """coefficient of prod_{k in S} x_k^1; returns (exps over remaining vars, coeffs, remaining idx)."""
    rem = [k for k in range(m) if k not in S]
    E = []; C = []
    for e, c in P.items():
        if all(e[k] == 1 for k in S):
            E.append([e[k] for k in rem]); C.append(c)
    return np.array(E), np.array(C), rem

def g(k):
    return 1.0 if k <= 1 else ((k-1)/k)**(k-1)

def canon_Ds(n):
    out = []
    for s in strong_score_sequences(n):
        D = D_from_scores(s, n)
        ind = [1 if v in D else 0 for v in range(-(n-1), n)]
        if ind >= ind[::-1]:
            out.append(D)
    return out
