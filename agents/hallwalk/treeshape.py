# What do the sets A(D') of tree.py look like?  For each n: the sets for the eight rules, their common part,
# the share of A(parent) that can be repaired, and A as a share of all solutions.      usage: treeshape.py N
import sys, io, contextlib, importlib.util
_a = sys.argv; sys.argv = ['x', '2']
with contextlib.redirect_stdout(io.StringIO()):
    spec = importlib.util.spec_from_file_location('refl', 'refl.py'); R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
    sys.argv = ['x', '3']
    spec = importlib.util.spec_from_file_location('tree', 'tree.py'); T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
sys.argv = _a
for n in range(5, int(sys.argv[1]) + 1):
    V = sorted(R.valid_sets(n), key=lambda D: sum(d * d for d in D), reverse=True)
    nsol = {D: len(R.solutions(D)) for D in V}
    As = {}
    for name, rule in T.RULES.items():
        A = {V[0]: {tuple((r, n + 1 - r) for r in range(n, 0, -1))}}; worst = 1.0
        for D in V[1:]:
            P, i, j, _ = rule(D, T.parents(D)); S = set(); used = 0
            for sol in A[P]:
                (rX, cX), (rY, cY) = sol[i], sol[j]; hit = False
                for s in (rX + cY - 1, rY + cX + 1):
                    for st in (0, 1):
                        nw = R.repair(n, list(sol), i, j, s, st)
                        if nw is not None: S.add(tuple(nw)); hit = True
                used += hit
            A[D] = S; worst = min(worst, used / len(A[P]))
        As[name] = (A, worst)
    common = {D: set.intersection(*[As[k][0][D] for k in As]) for D in V}
    print("n", n, "| arrangements", len(V), "| common part empty for", sum(1 for D in V if not common[D]),
          "| smallest share of A(parent) repaired, per rule:", " ".join("%.2f" % As[k][1] for k in As))
    print("     A (first run) as a share of all solutions: min %.3f, median %.3f" % tuple(sorted(len(As["first run"][0][D]) / nsol[D] for D in V)[k] for k in (0, len(V) // 2)),
          "| arrangements with A = one solution:", sum(1 for D in V if len(As["first run"][0][D]) == 1), "of which with only one solution:", sum(1 for D in V if nsol[D] == 1))
