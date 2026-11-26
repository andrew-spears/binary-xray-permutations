# The repair graph: vertices = all solutions of all valid D of size n, an edge from a solution of D to each solution
# of D' got from it by one of the four repairs (D -> D' a minimal move).  U of union.py = what the evenly spaced
# solution reaches.  Sources = solutions with no incoming edge.  Each solution outside U is reached from a source.
#                                                                          usage: sources.py N
import sys, io, os, contextlib, importlib.util
_a = sys.argv; sys.argv = ['x', '2']; here = os.path.dirname(os.path.abspath(__file__))
with contextlib.redirect_stdout(io.StringIO()):
    spec = importlib.util.spec_from_file_location('refl', os.path.join(here, 'refl.py')); R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
sys.argv = _a
for n in range(4, int(sys.argv[1]) + 1):
    V = R.valid_sets(n); S = {D: [tuple(s) for s in R.solutions(D)] for D in V}; hit = set()
    for D in V:
        for (i, j) in R.moves(D):
            for sol in S[D]:
                (rX, cX), (rY, cY) = sol[i], sol[j]
                for s in (rX + cY - 1, rY + cX + 1):
                    for st in (0, 1):
                        nw = R.repair(n, list(sol), i, j, s, st)
                        if nw is not None: hit.add(tuple(nw))
    src = [(D, s) for D in V for s in S[D] if s not in hit]
    print("n", n, "| solutions", sum(len(S[D]) for D in V), "| sources", len(src), flush=True)
    for D, s in src[:8]: print("     ", D, "columns by row:", [c for r, c in sorted(s)])
