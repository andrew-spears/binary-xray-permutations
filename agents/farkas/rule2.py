"""Rule R*: top-row cell e is BAD iff for every parity choice a of the peeled board P,
 (i) the parity counts mismatch, or (ii) forced-move propagation on the a-restricted board P_a
 (cells (r,c) with r = a(c-r) mod 2) reaches an empty row/column/diagonal.
Sound automatically (a placement's own a survives both), so only bad cells are tested.
Also checks R (no parity: propagation alone) and reports escapes.
Usage: python3 rule2.py m h"""
import sys, time, itertools
from collections import Counter
sys.path.insert(0, '/home/claude/agents/cell'); sys.path.insert(0, '/home/claude/agents/farkas')
from core import cells_of, peel, passes, lp
from classify import boards


def dies(R, C, D, a=None):
    """propagation on a-restricted board; True if some line becomes empty."""
    R, C, D = tuple(R), tuple(C), tuple(D)
    while R:
        cnt = {}
        for (r, c) in cells_of(R, C, D, a):
            for k in (('R', r), ('C', c), ('D', c - r)): cnt.setdefault(k, []).append((r, c))
        if len(cnt) < 3 * len(R): return True
        f = next((v[0] for v in cnt.values() if len(v) == 1), None)
        if f is None: return False
        R, C, D = peel(R, C, D, f)
    return False


def rstar_bad(R, C, D):
    Ds = sorted(D); nr1 = sum(r % 2 for r in R); nc1 = sum(c % 2 for c in C)
    for t in itertools.product((0, 1), repeat=len(Ds)):
        if sum(t) != nr1 or sum((x + d) % 2 for x, d in zip(t, Ds)) != nc1: continue
        if not dies(R, C, D, dict(zip(Ds, t))): return False
    return True


if __name__ == '__main__':
    m, h = int(sys.argv[1]), int(sys.argv[2]); t = time.time()
    st = Counter(); ex = {}
    for R, C, D in boards(m, h):
        if not passes(R, C, D): continue
        st['boards'] += 1
        for d in sorted(D):
            if 1 + d not in C: continue
            P = peel(R, C, D, (1, 1 + d)); st['cells'] += 1
            if passes(*P): continue
            st['bad'] += 1
            if dies(*P): st['R:caught'] += 1; continue
            if rstar_bad(*P):
                st['R*:caught(parity needed)'] += 1
                st['  of which plainLP ' + ('feasible' if lp(*P) is not None else 'infeasible')] += 1
                continue
            st['ESCAPE'] += 1; ex.setdefault('escape', (C, D, d))
            st['  escape plainLP ' + ('feasible' if lp(*P) is not None else 'infeasible')] += 1
    line = f'm={m} h={h} {dict(st)} ex={ex} time={time.time()-t:.0f}s'
    open(f'/home/claude/agents/farkas/rule2_m{m}_h{h}.txt', 'w').write(line + '\n'); print(line)
