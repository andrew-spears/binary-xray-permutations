# A canonical way back to the evenly spaced arrangement.
# In D' a maximal run of consecutive diagonals a+1, ..., b-1 (two or more) can be opened: its ends go to a and b.
# If the result D is valid, D -> D' is a minimal move.  A rule picks one run for each D'; this gives every D' one
# parent, hence one path of moves from the evenly spaced arrangement.  Follow that path with chain reflections.
#   A(D') = solutions got from A(parent) by a repair (all four, or only those with mirror line next to the middle).
# Question: is A(D') non-empty for every valid D'?      usage: tree.py N [near]
import sys, io, contextlib, importlib.util
_a = sys.argv; sys.argv = ['x', '2']
with contextlib.redirect_stdout(io.StringIO()):
    spec = importlib.util.spec_from_file_location('refl', __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'refl.py')); R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
sys.argv = _a
N = int(sys.argv[1]); NEAR = len(sys.argv) > 2
def valid(D):
    n = len(D); t = 0
    for k, d in enumerate(D):
        t += d + n - 1 - 2 * k                      # letters; partial sums must be >= 0
        if t < 0: return False
    return t == 0
def parents(D):
    """(parent set, i, j) for every run that can be opened; i, j = places of the two moved stones in the parent."""
    n = len(D); out = []; k = 0
    while k < n:
        m = k
        while m + 1 < n and D[m + 1] == D[m] + 1: m += 1
        if m > k:
            P = list(D); P[k] -= 1; P[m] += 1; P = tuple(P)
            if valid(P): out.append((P, k, m, m - k + 1))
        k = m + 1
    return out
def slack(D, k): return sum(D[i] + len(D) - 1 - 2 * i for i in range(k))
RULES = {
 "first run":   lambda D, c: c[0],
 "last run":    lambda D, c: c[-1],
 "longest run (first)":  lambda D, c: max(c, key=lambda p: (p[3], -p[1])),
 "shortest run (first)": lambda D, c: min(c, key=lambda p: (p[3], p[1])),
 "run nearest the middle": lambda D, c: min(c, key=lambda p: (abs(D[p[1]] + D[p[2]]), p[1])),
 "run furthest from the middle": lambda D, c: max(c, key=lambda p: (abs(D[p[1]] + D[p[2]]), -p[1])),
 "run at the greatest slack": lambda D, c: max(c, key=lambda p: (max(slack(D, t) for t in range(p[1] + 1, p[2] + 1)), -p[1])),
 "run at the least slack": lambda D, c: min(c, key=lambda p: (min(slack(D, t) for t in range(p[1] + 1, p[2] + 1)), p[1])),
}
for name, rule in RULES.items():
    line = []
    for n in range(4, N + 1):
        V = sorted(R.valid_sets(n), key=lambda D: sum(d * d for d in D), reverse=True)
        A = {V[0]: {tuple((r, n + 1 - r) for r in range(n, 0, -1))}}; empty = 0; first = None; big = 0
        for D in V[1:]:
            c = parents(D); assert c
            P, i, j, _ = rule(D, c); S = set()
            for sol in A[P]:
                (rX, cX), (rY, cY) = sol[i], sol[j]
                for s in (rX + cY - 1, rY + cX + 1):
                    if NEAR and abs(s - (n + 1)) > 1: continue
                    for st in (0, 1):
                        nw = R.repair(n, list(sol), i, j, s, st)
                        if nw is not None: assert sorted(c - r for r, c in nw) == list(D); S.add(tuple(nw))
            A[D] = S; big = max(big, len(S))
            if not S: empty += 1; first = first or D
        line.append("n=%d: %d empty of %d%s (largest A %d)" % (n, empty, len(V), " first " + str(first) if first and n <= 8 else "", big))
        if empty > 20: break
    print(name, "|", " ; ".join(line), flush=True)
