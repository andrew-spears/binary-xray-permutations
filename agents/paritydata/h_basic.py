"""Sanity checks, exact symmetries, freedom statistics (H1 transforms, H5, A_lp vs A_wit)."""
import sys
from collections import Counter
from pdata import *

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 12


def tr(D, a, kind, n):
    """transform parity dict under symmetry; returns (D', a')"""
    if kind == 'transpose':      # (r,c)->(c,r): d->-d, row' = r+d
        return tuple(sorted(-d for d in D)), {-d: (a[d] + d) % 2 for d in D}
    if kind == 'rot180':         # (r,c)->(n+1-r,n+1-c): d->-d, row' = n+1-r
        return tuple(sorted(-d for d in D)), {-d: (a[d] + n + 1) % 2 for d in D}
    if kind == 'antidiag':       # (r,c)->(n+1-c,n+1-r): d->d, row' = n+1-r-d
        return D, {d: (a[d] + d + n + 1) % 2 for d in D}


for n in range(1, NMAX + 1):
    W = load_wit(n); L = load_lp(n)
    # symmetries
    bad = Counter()
    for D, (_, _, A) in W.items():
        for kind in ('transpose', 'rot180', 'antidiag'):
            for m in A:
                D2, a2 = tr(D, todict(D, m), kind, n)
                if tomask(D2, a2) not in W[D2][2]: bad[kind] += 1
    # freedom
    uniq = [D for D, v in W.items() if len(v[2]) == 1]
    allsame = [D for D in W if len({d % 2 for d in D}) == 1]
    line = f'n={n} #D={len(W)} symfail={dict(bad)} uniqueA_wit={len(uniq)} (all-same-parity D: {len(allsame)}, uniq==samepar: {set(uniq)==set(allsame)})'
    tot_w = sum(len(v[2]) for v in W.values())
    line += f' mean|A_wit|={tot_w/len(W):.2f}'
    if L:
        eq = sum(1 for D in W if L[D] == W[D][2])
        sub = all(W[D][2] <= L[D] for D in W)
        tot_l = sum(len(v) for v in L.values())
        uniqL = sum(1 for v in L.values() if len(v) == 1)
        line += f' | A_wit<=A_lp:{sub} A_lp==A_wit for {eq}/{len(W)} mean|A_lp|={tot_l/len(W):.2f} uniqueA_lp={uniqL}'
        ex = [(D, sorted(L[D] - W[D][2]), sorted(W[D][2])) for D in W if L[D] != W[D][2]][:2]
        for e in ex: line += f'\n    LP-extra example D={e[0]} extra={e[1]} wit={e[2]}'
    print(line, flush=True)
    # histogram of |A_wit|
    print('   |A_wit| hist:', sorted(Counter(len(v[2]) for v in W.values()).items())[:25])
