"""Root-system helpers in fundamental-weight coordinates (same conventions as ../lie/prv_gen.py)."""
import sys
from fractions import Fraction as Fr
sys.path.insert(0, "../lie")
from prv_gen import cartan
class RS:
    def __init__(s, T, n):
        s.T, s.n = T, n; s.C = C = cartan(T, n); rng = s.rng = range(n)
        s.simple = [tuple(C[i]) for i in rng]
        # symmetriser: d_i = (alpha_i, alpha_i)/2 up to scale, d_i C[i][j] = d_j C[j][i]
        d = [None] * n; d[0] = Fr(1); todo = [0]
        while todo:
            i = todo.pop()
            for j in rng:
                if C[i][j] and d[j] is None: d[j] = d[i] * C[j][i] / C[i][j]; todo.append(j)
        m = max(d); s.d = d = [x / m for x in d]            # long roots: d = 1, (alpha, alpha) = 2
        # positive roots: (root in weight coords, root in simple-root coords)
        pos = {s.simple[i]: tuple(int(i == j) for j in rng) for i in rng}; todo = list(pos)
        while todo:
            r = todo.pop()
            for i in rng:
                if r[i] < 0:
                    q = tuple(r[j] - r[i] * C[i][j] for j in rng)      # s_i r = r - <r, a_i^vee> a_i, higher root
                    if q not in pos:
                        c = list(pos[r]); c[i] -= r[i]; pos[q] = tuple(c); todo.append(q)
        s.pos = pos
        # (w_i, w_j) = d_j * (C^-1)[i][j]... use (a_i, w_j) = d_j delta_ij and a_i = sum_k C[i][k] w_k
        s.G = inv([[Fr(C[i][k]) for k in rng] for i in rng])            # G[k][j] with sum_k C[i][k] G[k][j] = delta_ij
        s.G = [[s.G[k][j] * d[j] for j in rng] for k in rng]            # (w_k, w_j)
        s.rho = (1,) * n
        s.len = {r: sum(c[i] * c[j] * s.ip_simple(i, j) for i in rng for j in rng) for r, c in pos.items()}
        L = max(s.len.values()); s.long = [r for r in pos if s.len[r] == L]; s.short = [r for r in pos if s.len[r] != L]
        half = lambda R: tuple(Fr(sum(r[i] for r in R), 2) for i in rng)
        s.rho_l, s.rho_s = half(s.long), half(s.short)
    def ip_simple(s, i, j): return s.d[j] * s.C[i][j]                   # (a_i, a_j) = <a_i, a_j^vee> (a_j, a_j)/2
    def ip(s, u, v): return sum(u[i] * v[j] * s.G[i][j] for i in s.rng for j in s.rng)
    def refl(s, v, i): return tuple(v[j] - v[i] * s.C[i][j] for j in s.rng)
    def dom(s, v):
        while True:
            for i in s.rng:
                if v[i] < 0: v = s.refl(v, i); break
            else: return v
    def orbit(s, v):
        O = {tuple(v)}; todo = [tuple(v)]
        while todo:
            x = todo.pop()
            for i in s.rng:
                y = s.refl(x, i)
                if y not in O: O.add(y); todo.append(y)
        return O
    def below(s, top):
        B = {top}; todo = [top]
        while todo:
            m = todo.pop()
            for r in s.pos:
                q = tuple(a - b for a, b in zip(m, r))
                if min(q) >= 0 and q not in B: B.add(q); todo.append(q)
        return B
    def group(s):
        """Weyl group as matrices acting on weight coordinates: list of tuples of images of the basis w_1..w_n"""
        e = tuple(tuple(int(i == j) for j in s.rng) for i in s.rng); G = {e}; todo = [e]
        while todo:
            g = todo.pop()
            for i in s.rng:
                h = tuple(s.refl(row, i) for row in g)
                if h not in G: G.add(h); todo.append(h)
        return G
    def act(s, g, v): return tuple(sum(v[i] * g[i][j] for i in s.rng) for j in s.rng)
    def coords(s, v):
        """v (weight coords) in simple-root coordinates"""
        Ci = inv([[Fr(s.C[i][k]) for k in s.rng] for i in s.rng])       # w_k = sum_i Ci[k][i] a_i
        return tuple(sum(v[k] * Ci[k][i] for k in s.rng) for i in s.rng)
def inv(M):
    n = len(M); A = [list(M[i]) + [Fr(int(i == j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0); A[c], A[p] = A[p], A[c]
        A[c] = [x / A[c][c] for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0: A[r] = [x - A[r][c] * y for x, y in zip(A[r], A[c])]
    return [row[n:] for row in A]
