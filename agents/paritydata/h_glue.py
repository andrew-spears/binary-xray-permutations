"""H3 gluing.
(i) Tight cut at k (skew sum, bottom-left k-block + top-right (n-k)-block):
    D_low = first k stones + (n-k) (valid for k), D_high = rest - k (valid for n-k).
    a(d) = a_low(d+n-k) + (n-k) on low stones, a(d) = a_high(d-k) on high stones.
    Test A(D) == product (exact).
(ii) Direct sum: D = D1 u D2 (disjoint, unshifted), D1 valid for k, D2 valid for n-k.
    product: a = a1 on D1, a2 + k on D2.  Always contained in A(D) (direct sum of witnesses / LP solutions).
    Test: for such D, does the union of products over all splittings equal A(D)?"""
import sys
from itertools import combinations
from pdata import *

NMAX = int(sys.argv[1]); src = sys.argv[2]
Ws = {}
for n in range(1, NMAX + 1):
    Ws[n] = {D: v[2] for D, v in load_wit(n).items()} if src == 'wit' else load_lp(n)

for n in range(2, NMAX + 1):
    W = Ws[n]
    t_tot = t_eq = 0; t_bad = None
    ds_tot = ds_cont = ds_eq = 0; ds_bad = None; ds_ex = None
    for D, A in W.items():
        k = tight(n, D)
        if k:
            t_tot += 1
            lo = tuple(d + n - k for d in D[:k]); hi = tuple(d - k for d in D[k:])
            if lo in Ws[k] and hi in Ws[n - k]:
                P = set()
                for m1 in Ws[k][lo]:
                    for m2 in Ws[n - k][hi]:
                        a = {}
                        for i, d in enumerate(D[:k]): a[d] = ((m1 >> i) & 1) ^ ((n - k) & 1)
                        for i, d in enumerate(D[k:]): a[d] = (m2 >> i) & 1
                        P.add(tomask(D, a))
                if P == A: t_eq += 1
                elif t_bad is None: t_bad = (D, k, len(P), len(A))
            elif t_bad is None: t_bad = (D, k, 'pieces invalid')
        # direct sums
        U = set(); found = False
        for k in range(1, n):
            for D1 in combinations(D, k):
                if D1 not in Ws[k]: continue
                D2 = tuple(d for d in D if d not in D1)
                if D2 not in Ws[n - k]: continue
                found = True
                for m1 in Ws[k][D1]:
                    for m2 in Ws[n - k][D2]:
                        a = {d: (m1 >> i) & 1 for i, d in enumerate(D1)}
                        for i, d in enumerate(D2): a[d] = ((m2 >> i) & 1) ^ (k & 1)
                        U.add(tomask(D, a))
        if found:
            ds_tot += 1
            if U <= A: ds_cont += 1
            elif ds_bad is None: ds_bad = D
            if U == A: ds_eq += 1
            elif ds_ex is None: ds_ex = (D, len(U), len(A))
    print(f'[{src}] n={n} tight: {t_eq}/{t_tot} exact-product (first bad {t_bad}) | direct-sum D: {ds_tot}, '
          f'products contained {ds_cont}, union==A {ds_eq} (first gap {ds_ex}, first non-contained {ds_bad})', flush=True)
