"""States in the coordinates of REPORT.md: u = (lam, nu), nu = mu' (conjugate of the column diagram); M = M(lam), B = M(nu) (beads lam_i - i).
Letter e forward:  M' = (M - 1) u {k},  B' = (B + 1) minus {k + 1 - e}        (k not in M - 1, k + 1 - e in B + 1).
e-predecessors of u: k in M with k + 1 - e not in B:  t_k = ((M minus k) + 1, (B u {k + 1 - e}) - 1).
Structural sets: SC, E0, A and T(s); all tests work on partitions of any size (no enumeration of states)."""
from math import isqrt
def conj(l): return tuple(sum(1 for a in l if a > j) for j in range(l[0])) if l else ()
def beads(l, d): return [(l[i - 1] if i <= len(l) else 0) - i for i in range(1, d + 1)]          # all beads >= -d (needs d >= len(l))
def part(bs):                                                                                    # bs = all beads >= -len(bs)
    return tuple(x for x in (k + i for i, k in enumerate(sorted(bs, reverse=True), 1)) if x > 0)
def depth(u): return len(u[0]) + len(u[1]) + 6
def preds(u, e):
    """list of (k, t_k)"""
    d = depth(u); M = beads(u[0], d); B = set(beads(u[1], d)); out = []
    for k in M:
        y = k + 1 - e
        if y >= -d and y not in B:
            out.append((k, (part([b + 1 for b in M if b != k]), part([b - 1 for b in B | {y}]))))
    return out
def succs(u, e):
    d = depth(u) + 2; M1 = {b - 1 for b in beads(u[0], d)}; B1 = [b + 1 for b in beads(u[1], d)]; out = []
    for y in B1:
        k = y - 1 + e
        if k not in M1 and k >= -d - 1:
            out.append((k, (part(list(M1 | {k})), part([b for b in B1 if b != y]))))
    return out
def c0(l):                                                                                       # 2-core charge
    d = len(l) + 2 + (len(l) % 2); bs = set(beads(l, d))
    return sum(1 for k in bs if k >= 0 and k % 2 == 0) - sum(1 for k in range(-d, 0) if k % 2 == 0 and k not in bs)
def cls(u): return c0(u[0]) + c0(u[1])                                                           # c = a + b  (c0(mu) = c0(mu'))
def slack(u): return sum(u[0]) + sum(u[1])
def central(u): return cls(u) == slack(u) % 2
def is_SC(u): return u[0] == u[1]
def is_E0(u):
    """M, B unions of pairs {2i, 2i+1}, and M = (B - 2) + one more pair."""
    d = depth(u) + (depth(u) % 2); M = set(beads(u[0], d)); B = set(beads(u[1], d))               # d even: window [-d, ..) is a union of pairs
    if any((k ^ 1) not in S for S in (M, B) for k in S): return False
    B2 = {b - 2 for b in B} | {-d, -d + 1}                                                        # (B - 2) on the window... B - 2 lies below; restore the window bottom
    B2 = {b for b in B2 if b >= -d}
    return B2 <= M and len(M - B2) == 2
def double(l): return tuple(2 * a for a in l for _ in range(2))
def stair(i): return tuple(range(i, 0, -1))
def A_set(m):
    """A(4m^2+1): the states whose only 1-predecessor is in E0; built from the E0 states (2 delta 2 | conj-free form) of slack 4m^2."""
    out = set()
    for t in ((double(stair(m - 1)), double(stair(m))), (double(stair(m)), double(stair(m - 1)))):
        assert is_E0(t) and slack(t) == 4 * m * m, t
        for k, u in succs(t, 1):
            if len(preds(u, 1)) == 1: out.add(u)
    return out
_A = {}
def in_T(u):
    s = slack(u)
    if s == 0: return False
    if s % 4 == 0: return is_SC(u) or is_E0(u)
    if s % 4 == 1:
        m = isqrt((s - 1) // 4)
        if m >= 1 and 4 * m * m + 1 == s:
            if m not in _A: _A[m] = A_set(m)
            return u in _A[m]
    return False
def name(u): return "|".join("".join(map(str, p)) if p and max(p) < 10 else ".".join(map(str, p)) or "-" for p in (u[0], conj(u[1])))
