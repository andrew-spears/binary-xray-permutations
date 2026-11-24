# tree.py with only some of the four repairs allowed.  Repair (a, st): a = 0 for s1 = r_X + c_Y - 1, a = 1 for
# s2 = r_Y + c_X + 1; st = 0 chain started at X, st = 1 started at Y.  Prints, for each rule and each set of allowed
# repairs, the largest n <= N up to which no arrangement is left without a solution.     usage: treesub.py N
import sys, io, contextlib, importlib.util, itertools
_a = sys.argv; sys.argv = ['x', '2']
with contextlib.redirect_stdout(io.StringIO()):
    spec = importlib.util.spec_from_file_location('refl', 'refl.py'); R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
    sys.argv = ['x', '3']
    spec = importlib.util.spec_from_file_location('tree', 'tree.py'); T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
sys.argv = _a
N = int(sys.argv[1]); OPTS = [(0, 0), (0, 1), (1, 0), (1, 1)]
VS = {n: sorted(R.valid_sets(n), key=lambda D: sum(d * d for d in D), reverse=True) for n in range(4, N + 1)}
for name, rule in T.RULES.items():
    out = []
    for k in (1, 2, 3):
        for sub in itertools.combinations(OPTS, k):
            ok = 3
            for n in range(4, N + 1):
                V = VS[n]; A = {V[0]: {tuple((r, n + 1 - r) for r in range(n, 0, -1))}}; good = True
                for D in V[1:]:
                    P, i, j, _ = rule(D, T.parents(D)); S = set()
                    for sol in A[P]:
                        (rX, cX), (rY, cY) = sol[i], sol[j]; ss = (rX + cY - 1, rY + cX + 1)
                        for (a, st) in sub:
                            nw = R.repair(n, list(sol), i, j, ss[a], st)
                            if nw is not None: S.add(tuple(nw))
                    if not S: good = False; break
                    A[D] = S
                if not good: break
                ok = n
            out.append(("".join("s%d%s" % (a + 1, "XY"[st]) for a, st in sub), ok))
    print(name, "|", "  ".join("%s:%d" % o for o in out), flush=True)
