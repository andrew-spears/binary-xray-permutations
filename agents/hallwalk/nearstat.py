import sys, io, contextlib, importlib.util
from collections import defaultdict, Counter
_a = sys.argv; sys.argv = ['x', '2']
with contextlib.redirect_stdout(io.StringIO()):
    spec = importlib.util.spec_from_file_location('refl', __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'refl.py')); R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
sys.argv = _a
def closure(n, WIDTH=1):
    V = sorted(R.valid_sets(n), key=lambda D: sum(d * d for d in D), reverse=True)
    reach = defaultdict(set); reach[V[0]].add(tuple((r, n + 1 - r) for r in range(n, 0, -1)))
    for D in V:
        for (i, j) in R.moves(D):
            T = list(D); T[i] += 1; T[j] -= 1; order = sorted(range(n), key=lambda k: T[k]); Ts = tuple(T[k] for k in order)
            for sol in reach[D]:
                (rX, cX), (rY, cY) = sol[i], sol[j]
                for s in (rX + cY - 1, rY + cX + 1):
                    if abs(s - (n + 1)) > WIDTH: continue
                    for st in (0, 1):
                        nw = R.repair(n, list(sol), i, j, s, st)
                        if nw is not None: reach[Ts].add(tuple(nw[k] for k in order))
    return V, reach
def width(sol):      # largest set of stones pairwise not (higher and further right): longest chain in the other order
    pts = sorted(sol); best = []
    for (r, c) in pts:
        b = 1 + max([best[k] for k, (r2, c2) in enumerate(pts[:len(best)]) if c2 < c] or [0]); best.append(b)
    return max(best)
if __name__ == "__main__":
    n = int(sys.argv[1]); V, reach = closure(n)
    dev = Counter(); devall = Counter(); w = Counter(); wall = Counter()
    for D in V:
        for sol in R.solutions(D):
            sol = tuple(sol); m = max(abs(r + c - n - 1) for r, c in sol); k = width(sol)
            devall[m] += 1; wall[k] += 1
            if sol in reach[D]: dev[m] += 1; w[k] += 1
    print("n", n, "max |r+c-(n+1)| : reached", sorted(dev.items()), "all", sorted(devall.items()))
    print("   longest run of stones each lower-right of the last: reached", sorted(w.items()), "all", sorted(wall.items()))
