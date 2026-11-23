"""H2 local rule, existential form: for every minimal move D->D', is there a in A(D) such that
a' = a off the moving stones, with (a'(x+1), a'(x+2)) = KEEP (a(x), a(x+3))  [row parities kept in order]
or SWAP (a(x+3), a(x)) [= column parities kept in order], lies in A(D')?  Also 'either'."""
import sys
from pdata import *
src = sys.argv[2]; NMAX = int(sys.argv[1])
for n in range(2, NMAX + 1):
    W = {D: v[2] for D, v in load_wit(n).items()} if src == 'wit' else load_lp(n)
    res = {'keep': [0, None], 'swap': [0, None], 'equal-only': [0, None]}; moves = 0
    for D, A in W.items():
        S = set(D)
        for x in D:
            if not (x + 3 in S and x + 1 not in S and x + 2 not in S): continue
            D2 = tuple(sorted((S - {x, x + 3}) | {x + 1, x + 2})); A2 = W[D2]; moves += 1
            for name in res:
                ok = False
                for m in A:
                    a = todict(D, m); u, v = a[x], a[x + 3]
                    if name == 'equal-only' and u != v: continue
                    b = dict(a); del b[x]; del b[x + 3]
                    b[x + 1], b[x + 2] = (u, v) if name != 'swap' else (v, u)
                    if tomask(D2, b) in A2: ok = True; break
                if not ok:
                    res[name][0] += 1
                    if res[name][1] is None: res[name][1] = (D, x)
    print(f'[{src}] n={n} moves={moves} fails: {res}', flush=True)
