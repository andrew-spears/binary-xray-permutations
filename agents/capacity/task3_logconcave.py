"""Log-concavity / Lorentzian tests for P_D, n<=7, all strong D up to mirror."""
import itertools, math, json, sys
import numpy as np
from collections import Counter
from caplib import *

def expand(D, n):
    idx = {d: k for k, d in enumerate(D)}
    C = Counter()
    for p in itertools.permutations(range(n)):
        a = [0] * n
        ok = True
        for i in range(n):
            d = p[i] - i
            if d not in idx: ok = False; break
            a[idx[d]] += 1
        if ok: C[tuple(a)] += 1
    return C

def evalP(C, x):
    """value, gradient, Hessian of p at x."""
    m = len(x); v = 0.0; g = np.zeros(m); H = np.zeros((m, m))
    for a, c in C.items():
        a = np.array(a); mon = c * np.prod(x ** a)
        v += mon
        g += mon * a / x
        H += mon * (np.outer(a, a) - np.diag(a)) / np.outer(x, x)
    return v, g, H

def hess_logp_maxeig(C, x):
    v, g, H = evalP(C, x)
    L = H / v - np.outer(g, g) / v ** 2
    return np.linalg.eigvalsh(L).max() / np.abs(np.linalg.eigvalsh(L)).max()

def lorentzian_viol(C, m, deg, weight):
    """for each alpha with |alpha|=deg-2, Hessian of d^alpha q (q = sum weight(a)c_a x^a)
    must have <=1 positive eigenvalue. Returns worst (2nd eigenvalue / top) and alpha."""
    worst = (-1, None)
    for alpha in set(tuple(np.subtract(a, b)) for a in C for b in []) or []:
        pass
    alphas = set()
    for a in C:
        for i in range(m):
            for j in range(i, m):
                b = list(a); b[i] -= 1; b[j] -= 1
                if min(b) >= 0: alphas.add(tuple(b))
    for al in alphas:
        Q = np.zeros((m, m))
        for i in range(m):
            for j in range(m):
                gam = list(al); gam[i] += 1; gam[j] += 1; gam = tuple(gam)
                if gam in C:
                    coef = weight(gam) * C[gam]
                    # d^alpha x^gam = gam!/(gam-alpha)! x^(e_i+e_j); Hessian entry of that quadratic
                    f = math.prod(math.factorial(g) // math.factorial(g - a) for g, a in zip(gam, al))
                    Q[i, j] = coef * f * (2 if i == j else 1)  # d^2/dx_i dx_j of x_i x_j (=1) or x_i^2 (=2)
        ev = np.sort(np.linalg.eigvalsh(Q))[::-1]
        r = ev[1] / ev[0] if ev[0] > 0 else 0
        if r > worst[0]: worst = (r, al)
    return worst

def mconvex(C, m):
    """exchange property: for a,b in supp and i with a_i>b_i, exists j with a_j<b_j and a-e_i+e_j in supp."""
    S = set(C)
    for a in S:
        for b in S:
            for i in range(m):
                if a[i] > b[i]:
                    if not any(a[j] < b[j] and tuple(a[k] - (k == i) + (k == j) for k in range(m)) in S for j in range(m)):
                        return False, (a, b, i)
    return True, None

rng = np.random.default_rng(1)
out = []
for n in range(3, 8):
    for s in strong_score_sequences(n):
        rev = tuple(n - 1 - v for v in reversed(s))
        if s < rev: continue
        D = D_from_scores(s, n); m = n
        C = expand(D, n)
        # (a) Hessian of log P at random points and at the cap minimizer
        worst_rand = max(hess_logp_maxeig(C, np.exp(rng.normal(0, 1, m))) for _ in range(200))
        lc, t, _ = logcap(D, n)
        at_min = hess_logp_maxeig(C, np.exp(t))
        mc, wit = mconvex(C, m)
        lor = {name: lorentzian_viol(C, m, n, w) for name, w in [
            ("p", lambda g: 1.0),
            ("N(p)=c/a!", lambda g: 1.0 / math.prod(math.factorial(v) for v in g)),
            ("denorm c*a!", lambda g: float(math.prod(math.factorial(v) for v in g)))]}
        row = dict(n=n, D=D, s=list(s), nmon=len(C), logconc_rand_maxrel=worst_rand, logconc_at_min=at_min,
                   Mconvex=mc, Mconvex_witness=str(wit),
                   lorentz={k: (v[0], v[1]) for k, v in lor.items()})
        out.append(row)
        print(n, D, "mon=%d" % len(C), "Hlog maxrel rand=%.3g min=%.3g" % (worst_rand, at_min), "Mconv=%s" % mc,
              " ".join("%s:%.3g@%s" % (k, v[0], v[1]) for k, v in lor.items()), flush=True)
json.dump(out, open("task3.json", "w"), indent=0, default=str)
