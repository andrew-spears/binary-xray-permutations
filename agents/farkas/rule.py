"""Test the rule: top-row cell e is BAD iff the peeled board, after forced-move propagation
(repeatedly place the only cell of any row/col/diagonal that has exactly one), has a dead line,
fails the sum test (Landau prefix), or has a bipartite Hall violation (rows-diags, cols-diags, rows-cols).
Sound by construction (all steps are necessary conditions); test = no bad cell escapes.
Also reports which final test fires, and a weaker variant (no Hall).
Usage: python3 rule.py m h"""
import sys, time
from collections import Counter
sys.path.insert(0, '/home/claude/agents/cell'); sys.path.insert(0, '/home/claude/agents/farkas')
from core import cells_of, peel, sumtest, passes
from classify import hall2, boards
from prop import propagate


def why(P, use_hall=True, use_L=True):
    Q = propagate(*P)
    if Q is None: return 'dead'
    if not Q[0]: return None
    if use_L and not sumtest(*Q): return 'L'
    if use_hall:
        b = hall2(*Q)
        if b: return 'H2'
    return None


def steps(P):
    R, C, D = P; k = 0
    while R:
        cells = cells_of(R, C, D); cnt = {}
        for (r, c) in cells:
            for key in (('R', r), ('C', c), ('D', c - r)): cnt.setdefault(key, []).append((r, c))
        if any(key not in cnt for key in [('R', r) for r in R] + [('C', c) for c in C] + [('D', d) for d in D]): return k
        f = next((v[0] for v in cnt.values() if len(v) == 1), None)
        if f is None: return -1
        R, C, D = peel(R, C, D, f); k += 1
    return -2


if __name__ == '__main__':
    m, h = int(sys.argv[1]), int(sys.argv[2]); t = time.time()
    st = Counter(); ex = {}
    for R, C, D in boards(m, h):
        if not passes(R, C, D): continue
        st['boards'] += 1
        for d in sorted(D):
            if 1 + d not in C: continue
            P = peel(R, C, D, (1, 1 + d)); g = passes(*P); w = why(P)
            st['cells'] += 1
            if g:
                st['good'] += 1
                Q = propagate(*P); st['good:' + ('complete' if not Q[0] else 'stuck')] += 1
                if w: st['UNSOUND'] += 1; ex.setdefault('unsound', (C, D, d))
                continue
            st['bad:' + str(w)] += 1
            Q0 = P; nf = 0
            # number of forced placements before death
            st['bad:forced_steps=' + str(steps(P))] += 1
            if w is None: ex.setdefault('escape', (C, D, d))
            if why(P, use_hall=False) is None: st['bad_needs_hall'] += 1; ex.setdefault('needs_hall', (C, D, d))
            if why(P, use_L=False) is None: st['bad_needs_L'] += 1; ex.setdefault('needs_L', (C, D, d))
            if why(P, False, False) is None: st['bad_needs_L_or_hall'] += 1; ex.setdefault('needs_L_or_hall', (C, D, d))
    line = f'm={m} h={h} {dict(sorted(st.items()))} ex={ex} time={time.time()-t:.0f}s'
    open(f'/home/claude/agents/farkas/rule_m{m}_h{h}.txt', 'w').write(line + '\n'); print(line)
