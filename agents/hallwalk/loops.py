# Is the rule-free set U(D) of union.py a union of classes under loop reflections (Claim 1 (a), any s)?
# And does it meet every class?                usage: loops.py N
import sys, io, os, contextlib, importlib.util
_a = sys.argv; sys.argv = ['x', '2']; here = os.path.dirname(os.path.abspath(__file__))
with contextlib.redirect_stdout(io.StringIO()):
    spec = importlib.util.spec_from_file_location('refl', os.path.join(here, 'refl.py')); R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
sys.argv = _a
def loop_nbrs(n, sol):
    rowof = {c: k for k, (r, c) in enumerate(sol)}; rows = {r: k for k, (r, c) in enumerate(sol)}; out = set()
    for s in range(2, 2 * n + 1):
        seen = set()
        for r0 in range(1, n + 1):
            if r0 in seen: continue
            cyc = []; x = r0; ok = True
            while True:
                c = s - x
                if not 1 <= c <= n: ok = False; break
                k = rowof[c]; cyc.append(k); x = sol[k][0]
                if x == r0: break
            seen.update(sol[k][0] for k in cyc); seen.add(r0)
            if not ok: continue
            new = list(sol)
            for k in cyc: r, c = sol[k]; new[k] = (s - c, s - r)
            if new != list(sol): out.add(tuple(new))
    return out
def U_of(n):
    V = sorted(R.valid_sets(n), key=lambda D: sum(d * d for d in D), reverse=True)
    U = {D: set() for D in V}; U[V[0]] = {tuple((r, n + 1 - r) for r in range(n, 0, -1))}
    for D in V:
        for (i, j) in R.moves(D):
            D2 = list(D); D2[i] += 1; D2[j] -= 1; D2 = tuple(D2)
            for sol in U[D]:
                (rX, cX), (rY, cY) = sol[i], sol[j]
                for s in (rX + cY - 1, rY + cX + 1):
                    for st in (0, 1):
                        nw = R.repair(n, list(sol), i, j, s, st)
                        if nw is not None: U[D2].add(tuple(nw))
    return V, U
for n in range(4, int(sys.argv[1]) + 1):
    V, U = U_of(n); split = 0; missed = 0; ncls = 0; ex = None
    for D in V:
        rest = {tuple(s) for s in R.solutions(D)}
        while rest:
            s0 = rest.pop(); cls = {s0}; st = [s0]
            while st:
                for t in loop_nbrs(n, st.pop()):
                    if t not in cls: cls.add(t); st.append(t); rest.discard(t)
            ncls += 1; k = len(cls & U[D])
            if 0 < k < len(cls): split += 1; ex = ex or (D, len(cls), k)
            if k == 0: missed += 1
    print("n", n, "| loop classes", ncls, "| split by U:", split, "| missed by U entirely:", missed, "|", ex, flush=True)
