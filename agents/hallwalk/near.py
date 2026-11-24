# Start from the one solution of the evenly spaced arrangement and use only chain reflections whose mirror line is
# r + c = s with s in {n, n+1, n+2} (these never fail).  Which solutions of each valid D are reached?
import sys, io, contextlib, importlib.util
from collections import defaultdict
_a = sys.argv; sys.argv = ['x', '2']
with contextlib.redirect_stdout(io.StringIO()):
    spec = importlib.util.spec_from_file_location('refl', 'refl.py'); R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
sys.argv = _a
N = int(sys.argv[1]); WIDTH = int(sys.argv[2]) if len(sys.argv) > 2 else 1
for n in range(3, N + 1):
    V = sorted(R.valid_sets(n), key=lambda D: sum(d * d for d in D), reverse=True)     # a move lowers the sum of squares
    reach = defaultdict(set); reach[V[0]].add(tuple((r, n + 1 - r) for r in range(n, 0, -1)))
    empty = 0; first = None; minshare = 1.0; stuck = 0; firststuck = None
    for D in V:
        S = reach[D]
        if not S: empty += 1; first = first or D; continue
        minshare = min(minshare, len(S) / len(R.solutions(D)))
        for (i, j) in R.moves(D):
            T = list(D); T[i] += 1; T[j] -= 1; order = sorted(range(n), key=lambda k: T[k]); Ts = tuple(T[k] for k in order)
            got = False
            for sol in S:
                (rX, cX), (rY, cY) = sol[i], sol[j]
                for s in (rX + cY - 1, rY + cX + 1):
                    if abs(s - (n + 1)) > WIDTH: continue
                    for st in (0, 1):
                        nw = R.repair(n, list(sol), i, j, s, st)
                        if nw is not None: reach[Ts].add(tuple(nw[k] for k in order)); got = True
            if not got: stuck += 1; firststuck = firststuck or (D, D[i], D[j])
    print("n =", n, "sets", len(V), "| sets with nothing reached:", empty, first, "| moves with no reached solution near the middle:", stuck, firststuck, "| smallest share of solutions reached %.3f" % minshare, flush=True)
