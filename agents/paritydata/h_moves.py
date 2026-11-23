"""H2: minimal moves D -> D' (stones x, x+3 slide to x+1, x+2).
(a) exists a in A(D), a' in A(D') agreeing off the moving stones
(b) for all a in A(D) exists such a'        (c) for all a' in A(D') exists such a
(d) a fixed local rule f(a(x), a(x+3), x mod 2, n mod 2) -> (a'(x+1), a'(x+2)) valid for ALL a in A(D)
(e) weakest rule form: every D' other than the all-same-parity one has SOME incoming move with (a)."""
import sys
from collections import defaultdict
from pdata import *

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 12
src = sys.argv[2] if len(sys.argv) > 2 else 'wit'


def rest(D, a, skip):
    return tuple((d, a[d]) for d in D if d not in skip)


allowed = {}  # (x%2, n%2, a(x), a(x+3)) -> set of outputs allowed so far
first_fail = {}
for n in range(2, NMAX + 1):
    W = {D: v[2] for D, v in load_wit(n).items()} if src == 'wit' else load_lp(n)
    if W is None: break
    cnt = defaultdict(int); fails = {}
    incoming_ok = set()
    for D, A in W.items():
        S = set(D)
        for x in D:
            if x + 3 in S and x + 1 not in S and x + 2 not in S:
                D2 = tuple(sorted((S - {x, x + 3}) | {x + 1, x + 2}))
                if D2 not in W:
                    cnt['D2 invalid'] += 1; continue
                cnt['moves'] += 1
                A2 = W[D2]
                # index A2 by rest
                idx2 = defaultdict(set)
                for m in A2:
                    a2 = todict(D2, m); idx2[rest(D2, a2, {x + 1, x + 2})].add((a2[x + 1], a2[x + 2]))
                fw = []
                for m in A:
                    a = todict(D, m)
                    fw.append(((a[x], a[x + 3]), idx2.get(rest(D, a, {x, x + 3}), set())))
                ok_a = any(o for _, o in fw)
                ok_b = all(o for _, o in fw)
                restsA = {rest(D, todict(D, m), {x, x + 3}) for m in A}
                ok_c = all(r in restsA for r in idx2)
                for tag, ok in (('a', ok_a), ('b', ok_b), ('c', ok_c)):
                    if not ok:
                        cnt['fail_' + tag] += 1
                        fails.setdefault(tag, (D, x, D2))
                if ok_a: incoming_ok.add(D2)
                for (u, v), o in fw:
                    key = (x % 2, n % 2, u, v)
                    allowed[key] = allowed.get(key, {(0, 0), (0, 1), (1, 0), (1, 1)}) & o
                    if not allowed[key] and key not in first_fail: first_fail[key] = (n, D, x, D2)
    samepar = [D for D in W if len({d % 2 for d in D}) == 1]
    no_in = [D for D in W if D not in incoming_ok and D not in samepar]
    print(f'[{src}] n={n} {dict(cnt)} first fails: {fails} | D\' with no good incoming move (e): {len(no_in)}' +
          (f' e.g. {no_in[:3]}' if no_in else ''), flush=True)
print('local rule allowed sets per key (x%2, n%2, a(x), a(x+3)):')
for k in sorted(allowed): print('  ', k, sorted(allowed[k]), 'first emptied at', first_fail.get(k))
