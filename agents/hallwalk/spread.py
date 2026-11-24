# For a minimal move of X (on x) and Y (on y): t = r + c - (n+1) is the offset of a stone from the middle
# anti-diagonal.  Claim 3 of the report says: some solution has  y-x-4 <= |t_X + t_Y| <= y-x.
# Here: the set of values of t_X + t_Y over all solutions of D.  Is it an interval (steps of 2)?  How large is its maximum?
import sys, io, contextlib, importlib.util
from collections import Counter
_a = sys.argv; sys.argv = ['x', '2']
with contextlib.redirect_stdout(io.StringIO()):
    spec = importlib.util.spec_from_file_location('refl', __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'refl.py')); R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
sys.argv = _a
N = int(sys.argv[1])
for n in range(4, N + 1):
    gaps = Counter(); mx = Counter(); nmoves = 0; ex = None
    for D in R.valid_sets(n):
        sols = R.solutions(D)
        for (i, j) in R.moves(D):
            nmoves += 1; g = D[j] - D[i]
            vals = sorted({s[i][0] + s[i][1] + s[j][0] + s[j][1] - 2 * (n + 1) for s in sols})
            assert any(g - 4 <= abs(v) <= g for v in vals)
            biggest = max([b - a for a, b in zip(vals, vals[1:])] or [0]) // 2
            gaps[biggest] += 1; mx[vals[-1] - g] += 1
            if biggest >= 3 and ex is None: ex = (D, D[i], D[j], vals)
    print("n", n, "moves", nmoves, "| largest step between neighbouring values (in units of 2):", sorted(gaps.items()), "| max - (y-x):", sorted(mx.items()), "|", ex, flush=True)
