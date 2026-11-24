# One solution per arrangement, built along a canonical path (see tree.py): sigma(D') = the first repair that works,
# in a fixed order of the four repairs (s1 or s2, start at X or at Y), applied to sigma(parent of D').
# usage: tree1.py N ["rule name"]
import sys, io, contextlib, importlib.util, itertools
_a = sys.argv; sys.argv = ['x', '2']
with contextlib.redirect_stdout(io.StringIO()):
    spec = importlib.util.spec_from_file_location('refl', __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'refl.py')); R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
    sys.argv = ['x', '3']
    spec = importlib.util.spec_from_file_location('tree', __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'tree.py')); T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
sys.argv = _a
N = int(sys.argv[1]); ONLY = sys.argv[2] if len(sys.argv) > 2 else None; OPTS = [(0, 0), (0, 1), (1, 0), (1, 1)]          # (which s, which start)
best = []
for name, rule in T.RULES.items():
    if ONLY and name != ONLY: continue
    for order in itertools.permutations(OPTS):
        ok_to = 0; bad = None
        for n in range(4, N + 1):
            V = sorted(R.valid_sets(n), key=lambda D: sum(d * d for d in D), reverse=True)
            sig = {V[0]: tuple((r, n + 1 - r) for r in range(n, 0, -1))}; fail = 0
            for D in V[1:]:
                P, i, j, _ = rule(D, T.parents(D)); sol = sig.get(P); got = None
                if sol is not None:
                    (rX, cX), (rY, cY) = sol[i], sol[j]; ss = (rX + cY - 1, rY + cX + 1)
                    for (a, st) in order:
                        got = R.repair(n, list(sol), i, j, ss[a], st)
                        if got is not None: break
                if got is None: fail += 1; bad = bad or (n, D)
                else: sig[D] = tuple(got)
            if fail: break
            ok_to = n
        best.append((ok_to, name, order, bad))
best.sort(key=lambda t: -t[0])
for b in best[:12]: print(b)
print("...", len(best), "combinations; works up to n:", sorted({b[0] for b in best}))
