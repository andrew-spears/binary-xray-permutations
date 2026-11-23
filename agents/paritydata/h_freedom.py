"""H5: D with Delta_k = s_k-(k-1) in {-1,0,1} ('near-transitive').  Test |A_wit| = |A_lp| = 2^{#(Delta_k=+1)},
and whether every D with |A_wit| a power of 2 is near-transitive."""
from pdata import *
from math import comb
for n in range(2, 13):
    W = load_wit(n); L = load_lp(n)
    near = ok = okl = 0; bad = None; pow2_not_near = 0; ex = None
    for D, (_, _, A) in W.items():
        Dl = [D[k] + n - 1 - k - k for k in range(n)]
        if all(abs(x) <= 1 for x in Dl):
            near += 1; j = Dl.count(1)
            if len(A) == 2 ** j: ok += 1
            elif bad is None: bad = (D, Dl, len(A), 2 ** j)
            if L and len(L[D]) == 2 ** j: okl += 1
        elif len(A) & (len(A) - 1) == 0:
            pow2_not_near += 1; ex = ex or (D, Dl, len(A))
    print(f'n={n} near-transitive D={near} |A_wit|=2^j holds {ok} |A_lp|=2^j holds {okl if L else "-"} first bad {bad} | pow2 but not near: {pow2_not_near} e.g. {ex}')
