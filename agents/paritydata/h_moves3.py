"""H2 universal 'equal transfer': for all a in A(D) with a(x)=a(x+3)=u, is a' (u on x+1,x+2) in A(D')?
And backward: for all a' in A(D') with a'(x+1)=a'(x+2)=u, is a (u on x,x+3) in A(D)?
Also: for all a with a(x)!=a(x+3), does keep or swap work?"""
import sys
from pdata import *
src = sys.argv[2]; NMAX = int(sys.argv[1])
for n in range(2, NMAX + 1):
    W = {D: v[2] for D, v in load_wit(n).items()} if src == 'wit' else load_lp(n)
    f = {'fwd_eq': [0, 0, None], 'bwd_eq': [0, 0, None], 'fwd_neq_keep_or_swap': [0, 0, None]}
    for D, A in W.items():
        S = set(D)
        for x in D:
            if not (x + 3 in S and x + 1 not in S and x + 2 not in S): continue
            D2 = tuple(sorted((S - {x, x + 3}) | {x + 1, x + 2})); A2 = W[D2]
            for m in A:
                a = todict(D, m); u, v = a[x], a[x + 3]
                b = dict(a); del b[x]; del b[x + 3]
                if u == v:
                    b[x + 1] = b[x + 2] = u; k = 'fwd_eq'; ok = tomask(D2, b) in A2
                else:
                    k = 'fwd_neq_keep_or_swap'; b[x + 1], b[x + 2] = u, v; ok = tomask(D2, b) in A2
                    b[x + 1], b[x + 2] = v, u; ok = ok or tomask(D2, b) in A2
                f[k][0] += 1
                if not ok:
                    f[k][1] += 1
                    if f[k][2] is None: f[k][2] = (D, x, m)
            for m in A2:
                b = todict(D2, m); u, v = b[x + 1], b[x + 2]
                if u != v: continue
                a = dict(b); del a[x + 1]; del a[x + 2]; a[x] = a[x + 3] = u
                f['bwd_eq'][0] += 1
                if tomask(D, a) not in A:
                    f['bwd_eq'][1] += 1
                    if f['bwd_eq'][2] is None: f['bwd_eq'][2] = (D, x, m)
    print(f'[{src}] n={n} [tested, failed, first]: {f}', flush=True)
