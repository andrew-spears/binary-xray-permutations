# U(D') = all solutions of D' got by a chain reflection from a solution in U(D), over ALL parents D (no rule).
# How much of Sol(D') is U(D')?  Which solutions are missing?        usage: union.py N [show]
import sys, io, os, contextlib, importlib.util
from collections import Counter
from fractions import Fraction
_a = sys.argv; sys.argv = ['x', '2']; here = os.path.dirname(os.path.abspath(__file__))
with contextlib.redirect_stdout(io.StringIO()):
    spec = importlib.util.spec_from_file_location('refl', os.path.join(here, 'refl.py')); R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
sys.argv = _a
N = int(sys.argv[1]); SHOW = len(sys.argv) > 2
for n in range(4, N + 1):
    V = sorted(R.valid_sets(n), key=lambda D: sum(d * d for d in D), reverse=True)
    U = {D: set() for D in V}; U[V[0]] = {tuple((r, n + 1 - r) for r in range(n, 0, -1))}
    for D in V:                                   # parents come before children: a move lowers the sum of squares
        for (i, j) in R.moves(D):
            D2 = list(D); D2[i] += 1; D2[j] -= 1; D2 = tuple(D2)
            for sol in U[D]:
                (rX, cX), (rY, cY) = sol[i], sol[j]
                for s in (rX + cY - 1, rY + cX + 1):
                    for st in (0, 1):
                        nw = R.repair(n, list(sol), i, j, s, st)
                        if nw is not None: U[D2].add(tuple(nw))
    tot = 0; got = 0; full = 0; worst = (Fraction(2), None); miss = []
    for D in V:
        al = R.solutions(D); tot += len(al); got += len(U[D]); full += len(al) == len(U[D])
        worst = min(worst, (Fraction(len(U[D]), len(al)), D))
        if len(al) != len(U[D]): miss.append((D, [s for s in al if tuple(s) not in U[D]]))
    print("n", n, "| arrangements", len(V), "| with every solution reached:", full, "| solutions reached", got, "of", tot,
          "| smallest share", worst[0], "for", worst[1], flush=True)
    if SHOW:
        for D, m in miss[:12]: print("    ", D, "missing", len(m), "e.g. columns by row:", [c for r, c in sorted(m[0])])
