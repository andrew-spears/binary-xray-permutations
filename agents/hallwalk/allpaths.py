# Every path of minimal moves from the evenly spaced arrangement, instead of one fixed path (tree.py).
# State = (D, A), A = the solutions of D got along the path by the four chain reflections.
# Prints every (state, move) whose repaired set is empty, with the path that leads to the state.   usage: allpaths.py N
import sys, io, contextlib, importlib.util
_a = sys.argv; sys.argv = ['x', '2']
with contextlib.redirect_stdout(io.StringIO()):
    spec = importlib.util.spec_from_file_location('refl', __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'refl.py')); R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
sys.argv = _a
for n in range(4, int(sys.argv[1]) + 1):
    D0 = tuple(range(-(n - 1), n, 2)); start = (D0, frozenset([tuple((r, n + 1 - r) for r in range(n, 0, -1))]))
    par = {start: None}; todo = [start]; bad = []
    while todo:
        nxt = []
        for (D, A) in todo:
            for (i, j) in R.moves(D):
                T = list(D); T[i] += 1; T[j] -= 1
                order = sorted(range(n), key=lambda k: T[k]); Ts = tuple(T[k] for k in order); S = set()
                for sol in A:
                    (rX, cX), (rY, cY) = sol[i], sol[j]
                    for s in (rX + cY - 1, rY + cX + 1):
                        for st in (0, 1):
                            nw = R.repair(n, list(sol), i, j, s, st)
                            if nw is not None: S.add(tuple(nw[k] for k in order))
                if not S: bad.append(((D, A), (D[i], D[j]), Ts)); continue
                st = (Ts, frozenset(S))
                if st not in par: par[st] = ((D, A), (D[i], D[j])); nxt.append(st)
        todo = nxt
    print("n", n, "| states (D, A):", len(par), "| (state, move) with empty result:", len(bad))
    for b in bad[:2]:
        path = []; st = b[0]
        while par[st] is not None: path.append(par[st][1]); st = par[st][0]
        print("   moves:", path[::-1], "reach", b[0][0], "with", len(b[0][1]), "solutions; then move", b[1], "->", b[2], "has none")
