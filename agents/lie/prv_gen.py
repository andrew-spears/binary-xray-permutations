"""Same question as prv.py for any finite root system, in fundamental-weight coordinates.
Is every regular dominant weight mu <= 2 rho conjugate to rho + w rho for some w in the Weyl group?
Usage: python3 prv_gen.py TYPE rank      (TYPE in A B C D E F G)"""
import sys
def cartan(T, n):
    C = [[2 if i == j else 0 for j in range(n)] for i in range(n)]
    def link(i, j, a=-1, b=-1): C[i][j] = a; C[j][i] = b
    if T in 'ABCFG':
        for i in range(n - 1): link(i, i + 1)
    if T == 'B': C[n - 2][n - 1] = -2          # alpha_{n-1} long, alpha_n short
    if T == 'C': C[n - 1][n - 2] = -2
    if T == 'F': C[1][2] = -2
    if T == 'G': C[0][1] = -3
    if T == 'D':
        for i in range(n - 2): link(i, i + 1)
        link(n - 3, n - 1)
    if T == 'E':
        for i in range(n - 2): link(i, i + 1)   # chain 0..n-2, extra node n-1 attached to node 2
        link(2, n - 1)
    return C
def run(T, n):
    C = cartan(T, n); rng = range(n)
    refl = lambda v, i: tuple(v[j] - v[i] * C[i][j] for j in rng)
    def dom(v):
        while True:
            for i in rng:
                if v[i] < 0: v = refl(v, i); break
            else: return v
    rho = (1,) * n
    orbit = {rho}; todo = [rho]
    while todo:
        v = todo.pop()
        for i in rng:
            w = refl(v, i)
            if w not in orbit: orbit.add(w); todo.append(w)
    prv = {}
    for v in orbit:
        d = dom(tuple(1 + x for x in v)); prv[d] = prv.get(d, 0) + 1
    # positive roots in fundamental-weight coordinates
    simple = [tuple(C[i]) for i in rng]; roots = set(simple); todo = list(simple)
    while todo:
        r = todo.pop()
        for i in rng:
            s = refl(r, i)
            if s not in roots and s != tuple(-x for x in simple[i]):
                if tuple(-x for x in s) not in roots: roots.add(s); todo.append(s)
    # keep positive ones: orbit closure of simple roots under reflections avoiding sign flips gives positives only
    top = (2,) * n; below = {top}; todo = [top]
    while todo:
        m = todo.pop()
        for r in roots:
            q = tuple(a - b for a, b in zip(m, r))
            if min(q) >= 0 and q not in below: below.add(q); todo.append(q)
    assert set(prv) <= below
    reg = [m for m in below if min(m) >= 1]; miss = sorted(m for m in reg if m not in prv)
    print(f"type {T}{n}: |W| = {len(orbit)}, positive roots {len(roots)}, dominant weights <= 2rho: {len(below)}, of the form rho + w rho: {len(prv)}, regular: {len(reg)}, regular and not of that form: {len(miss)}", flush=True)
    for m in miss[:8]: print("   mu =", m, "(fundamental-weight coordinates)")
if __name__ == "__main__": run(sys.argv[1], int(sys.argv[2]))
