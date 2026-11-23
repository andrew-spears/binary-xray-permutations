"""H1: symmetric D (D=-D). Exists a in A with a(-d)=a(d)?  with a(-d)=1-a(d)?
Also with a(-d) = a(d)+d (transpose-invariant) and a(-d)=a(d)+n+1 (rot-invariant)."""
import sys
from pdata import *

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 12
props = {
    'same a(-d)=a(d)': lambda a, d, n: a[-d] == a[d],
    'flip a(-d)=1-a(d)': lambda a, d, n: a[-d] == 1 - a[d],
    'transpose-fixed a(-d)=a(d)+d': lambda a, d, n: a[-d] == (a[d] + d) % 2,
    'transpose-anti a(-d)=a(d)+d+1': lambda a, d, n: a[-d] == (a[d] + d + 1) % 2,
}
for src in ('wit', 'lp'):
    for n in range(1, NMAX + 1):
        if src == 'wit':
            W = {D: v[2] for D, v in load_wit(n).items()}
        else:
            W = load_lp(n)
            if W is None: break
        sym = [D for D in W if tuple(sorted(-d for d in D)) == D]
        res = []
        for name, P in props.items():
            fails = [D for D in sym if not any(all(P(todict(D, m), d, n) for d in D) for m in W[D])]
            res.append(f'{name}: fails {len(fails)}/{len(sym)}' + (f' e.g. {fails[0]}' if fails else ''))
        print(f'[{src}] n={n} ' + ' ; '.join(res), flush=True)
