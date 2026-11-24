# Keep only K solutions per arrangement (chosen by a fixed score) and use only near-middle chain reflections.
# Does every valid D still get a solution?   usage: one.py N K rule   (rule = rows, rowsrev, or any word for a random order)
import sys, io, contextlib, importlib.util
from collections import defaultdict
_a = sys.argv; sys.argv = ['x', '2']
with contextlib.redirect_stdout(io.StringIO()):
    spec = importlib.util.spec_from_file_location('refl', 'refl.py'); R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
sys.argv = _a
N = int(sys.argv[1]); K = int(sys.argv[2]); rule = sys.argv[3]
import random
SALT = random.Random(rule).random()
def score(n, sol):
    # Note: the sum over stones of (r + c - n - 1)^2 is the same for every solution of D (the sum of r*c is fixed
    # by the sum of d^2), so "nearest to the middle anti-diagonal" is not a rule.
    if rule == "rows": return tuple(r for r, c in sol)             # rows in order of diagonals, smallest first
    if rule == "rowsrev": return tuple(-r for r, c in sol)
    return hash((SALT, sol))                                        # any other word: a random fixed order
for n in range(3, N + 1):
    V = sorted(R.valid_sets(n), key=lambda D: sum(d * d for d in D), reverse=True)
    reach = defaultdict(set); reach[V[0]].add(tuple((r, n + 1 - r) for r in range(n, 0, -1)))
    empty = 0; first = None
    for D in V:
        S = sorted(reach[D], key=lambda s: score(n, s))[:K]
        if not S: empty += 1; first = first or D; continue
        for (i, j) in R.moves(D):
            T = list(D); T[i] += 1; T[j] -= 1; order = sorted(range(n), key=lambda k: T[k]); Ts = tuple(T[k] for k in order)
            for sol in S:
                (rX, cX), (rY, cY) = sol[i], sol[j]
                for s in (rX + cY - 1, rY + cX + 1):
                    if abs(s - (n + 1)) > 1: continue
                    for st in (0, 1):
                        nw = R.repair(n, list(sol), i, j, s, st)
                        if nw is not None: reach[Ts].add(tuple(nw[k] for k in order))
    print("n =", n, "K =", K, rule, "| sets", len(V), "with nothing reached:", empty, first, flush=True)
