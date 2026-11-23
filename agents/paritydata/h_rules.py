"""H4: hand-picked canonical rules a = R(n, D) (dict d -> bit).  Reports first failure / fail counts
against A_lp (n<=10) and A_wit (n<=NMAX).  Also: is the lex-first witness parity equal to a rule?"""
import sys
from pdata import *

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 12


def same_left(D, d): return sum(1 for e in D if e < d and (e - d) % 2 == 0)
def same_right(D, d): return sum(1 for e in D if e > d and (e - d) % 2 == 0)
def other_left(D, d): return sum(1 for e in D if e < d and (e - d) % 2)
def runs(D):
    out = []; cur = [D[0]]
    for d in D[1:]:
        if d == cur[-1] + 1: cur.append(d)
        else: out.append(cur); cur = [d]
    out.append(cur); return out


R = {}
for al in (0, 1):
    for be in (0, 1):
        for ga in (0, 1):
            R[f'sameL+{al}+{be}n+{ga}d'] = (lambda al, be, ga: lambda n, D: {d: (al + be * n + ga * d + same_left(D, d)) % 2 for d in D})(al, be, ga)
            R[f'sameR+{al}+{be}n+{ga}d'] = (lambda al, be, ga: lambda n, D: {d: (al + be * n + ga * d + same_right(D, d)) % 2 for d in D})(al, be, ga)


def run_rule(start):
    def f(n, D):
        a = {}; left = 0
        for ri, run in enumerate(runs(D)):
            s0 = start(n, D, run, ri, left)
            for j, d in enumerate(run): a[d] = (s0 + j) % 2
            left += len(run)
        return a
    return f


for al in (0, 1):
    R[f'runalt start=n+{al}+#stonesLeft'] = run_rule((lambda al: lambda n, D, run, ri, left: n + al + left)(al))
    R[f'runalt start=n+{al}+runindex'] = run_rule((lambda al: lambda n, D, run, ri, left: n + al + ri)(al))
    R[f'runalt start=n+{al}+#emptyLeft'] = run_rule((lambda al: lambda n, D, run, ri, left: n + al + (run[0] + n - 1 - left))(al))
    R[f'runalt start=n+{al}+sameL(first)'] = run_rule((lambda al: lambda n, D, run, ri, left: n + al + same_left(D, run[0]))(al))
    R[f'runalt start={al}+first'] = run_rule((lambda al: lambda n, D, run, ri, left: al + run[0])(al))

results = {k: [] for k in R}
for src in ('lp', 'wit'):
    for n in range(1, NMAX + 1 if src == 'wit' else 11):
        W = {D: v[2] for D, v in load_wit(n).items()} if src == 'wit' else load_lp(n)
        for name, f in R.items():
            fails = [D for D in W if tomask(D, f(n, D)) not in W[D]]
            results[name].append((src, n, len(fails), len(W), fails[0] if fails else None))
for name, res in results.items():
    firstf = next(((s, n, D) for s, n, c, t, D in res if c), None)
    s = ' '.join(f'{c}' for s_, n, c, t, D in res if s_ == 'wit')
    print(f'{name:40s} first fail {firstf}; wit fail counts n=1..: {s}')
