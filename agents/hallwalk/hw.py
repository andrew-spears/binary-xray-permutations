# Hall's exchange walk (M. Hall 1952, sums of two permutations in an abelian group) run on the integers.
# A solution = permutations pi, tau of 1..n with pi(i) + tau(i) = l_i (lines 2..2n, increasing, distinct).
# Minimal move: lines a < b become a+1, b-1.  Start from a solution of the old set, take the two moved stones off,
# and re-place: the pending stone takes a free row w and the column (target - w); if another stone holds that column
# it is taken off and becomes pending, and it uses the other free row.  Stops when the column is free (success)
# or off the board (stuck).  8 variants: which moved stone is pending first, which free row first, rows/columns swapped.
import sys, itertools
from collections import Counter
def valid_sets(n):
    out = []
    def rec(k, last, s, cur):
        if k == n:
            if s == n * (n + 1): out.append(tuple(cur))
            return
        for l in range(last + 1, 2 * n + 1):
            ns = s + l
            if ns < (k + 1) * (k + 2): continue
            # remaining must be able to reach the total: upper bound check
            rem = n - k - 1
            if ns + sum(range(l + 1, l + 1 + rem)) > n * (n + 1): break
            cur.append(l); rec(k + 1, l, ns, cur); cur.pop()
    rec(0, 1, 0, []); return out
def solutions(L):
    n = len(L); res = []; used = [False] * (n + 1); pi = [0] * n; usedt = [False] * (n + 1)
    def rec(i):
        if i == n: res.append(tuple(pi)); return
        for r in range(max(1, L[i] - n), min(n, L[i] - 1) + 1):
            c = L[i] - r
            if used[r] or usedt[c]: continue
            used[r] = usedt[c] = True; pi[i] = r; rec(i + 1); used[r] = usedt[c] = False
    rec(0); return res
def walk(L, T, pi, p, q, first, swap, cap=10000):
    """L old lines, T new lines (same indexing), pi rows. returns (ok, steps)."""
    n = len(L); C = {i: (pi[i] if not swap else L[i] - pi[i]) for i in range(n)}
    Dv = {i: L[i] - C[i] for i in range(n)}
    holder = {Dv[i]: i for i in range(n) if i not in (p, q)}
    Fc = [C[p], C[q]]; Fd = {Dv[p], Dv[q]}
    w = Fc[first]; other = Fc[1 - first]; pend = p; last = q; steps = 0
    while steps < cap:
        steps += 1
        d = T[pend] - w
        if d < 1 or d > n: return (False, steps)
        if d in Fd: return (True, steps)
        i = holder[d]; holder[d] = pend; newfree = C[i]; C[pend] = w
        pend = i; w, other = other, newfree
    return (None, steps)
def moves(L):
    S = set(L); n = len(L); out = []
    for x in range(n):
        for y in range(x + 1, n):
            a, b = L[x], L[y]
            if b - a < 3 and not (b - a == 2): pass
            if a + 1 in S or b - 1 in S: 
                if not (b - a == 2): continue
            if b - a == 2: continue      # would collide
            if all(v in S for v in range(a + 2, b - 1)) and (a + 1 not in S) and (b - 1 not in S):
                T = list(L); T[x] = a + 1; T[y] = b - 1
                out.append((x, y, tuple(T)))
    return out
if __name__ == "__main__":
    N = int(sys.argv[1])
    for n in range(3, N + 1):
        nm = 0; nomove = 0; pairs = 0; okpairs = 0; res = Counter(); worst = None
        for L in valid_sets(n):
            sols = solutions(L)
            for (x, y, T) in moves(L):
                nm += 1; good = 0
                for pi in sols:
                    pairs += 1; any_ok = False
                    for (p, q) in ((x, y), (y, x)):
                        for first in (0, 1):
                            for swap in (0, 1):
                                ok, st = walk(L, T, pi, p, q, first, swap)
                                res[ok] += 1
                                if ok: any_ok = True
                    if any_ok: okpairs += 1; good += 1
                if good == 0: nomove += 1; worst = worst or (L, T)
        print("n =", n, "moves", nm, "moves where no solution can be repaired:", nomove, "| (move, solution) pairs", pairs, "repaired", okpairs, "| walks", dict(res), "| first bad", worst)
