import sys, math, time, json
import numpy as np
from caplib import *
nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 14
rows = []
for n in range(int(sys.argv[2]) if len(sys.argv)>2 else 4, nmax + 1):
    t0 = time.time()
    D = Pn(n)
    W = 2 if n > 9 else witnesses(D, n)
    lc, t, res = logcap(D, n)
    # symmetry check: t_d should equal t_{-d}
    sym = max(abs(t[D.index(d)] - t[D.index(-d)]) for d in D)
    P1, _ = perm_and_grad(D, np.ones(n), n)
    logR = math.log(W) + n * math.log(n) - math.lgamma(n + 1) - lc
    c = math.exp((math.log(W) - lc) / n)   # largest c with W >= c^n cap
    row = dict(n=n, D=D, W=W, logcap=lc, cap=math.exp(lc), per1=P1, R=math.exp(logR),
               c_max=c, n_fact_over_nn_root=math.exp((math.lgamma(n + 1) - n * math.log(n)) / n),
               cap_root=math.exp(lc / n), tnorm=float(np.abs(t).max()), sym=sym,
               gnorm=float(np.abs(res.jac).max()), sec=time.time() - t0)
    rows.append(row)
    print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in row.items() if k != "D"}), flush=True)
    json.dump(rows, open(f"task1_Pn_{nmax}.json", "w"), indent=1)
