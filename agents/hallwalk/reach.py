# Solutions reachable from the identity (evenly spaced set) by successful Hall walks along minimal moves.
import sys
from collections import defaultdict
from hw import valid_sets, solutions, moves
def repair(L, T, pi, p, q, first, swap):
    """returns new rows tuple for lines T (same indexing) or None."""
    n = len(L); C = [(pi[i] if not swap else L[i] - pi[i]) for i in range(n)]
    Dv = [L[i] - C[i] for i in range(n)]
    holder = {Dv[i]: i for i in range(n) if i not in (p, q)}
    Fc = [C[p], C[q]]; Fd = {Dv[p], Dv[q]}
    w = Fc[first]; other = Fc[1 - first]; pend = p
    for _ in range(n + 2):
        d = T[pend] - w
        if d < 1 or d > n: return None
        if d in Fd:
            C[pend] = w; C[q] = other
            if (T[q] - other) not in Fd or T[q] - other == d: return None
            rows = tuple(C[i] if not swap else T[i] - C[i] for i in range(n))
            return rows
        i = holder[d]; holder[d] = pend; newfree = C[i]; C[pend] = w
        pend = i; w, other = other, newfree
    raise Exception("cycle")
def check(T, rows):
    n = len(T); return sorted(rows) == list(range(1, n + 1)) and sorted(T[i] - rows[i] for i in range(n)) == list(range(1, n + 1))
if __name__ == "__main__":
    N = int(sys.argv[1])
    for n in range(3, N + 1):
        V = valid_sets(n)
        grade = lambda L: sum(l * l for l in L)        # decreases by a move
        V.sort(key=grade, reverse=True)
        R = defaultdict(set); R[V[0]].add(tuple(range(1, n + 1)))
        assert V[0] == tuple(range(2, 2 * n + 1, 2))
        empty = 0; full = 0; minshare = 1; worst = None
        for L in V:
            S = R[L]
            if not S: empty += 1; worst = worst or L; continue
            tot = len(solutions(L))
            if len(S) == tot: full += 1
            if len(S) / tot < minshare: minshare = len(S) / tot
            for (x, y, T) in moves(L):
                srt = sorted(range(n), key=lambda i: T[i]); Ts = tuple(T[i] for i in srt)
                for pi in S:
                    for (p, q) in ((x, y), (y, x)):
                        for first in (0, 1):
                            for swap in (0, 1):
                                r = repair(L, T, pi, p, q, first, swap)
                                if r is not None:
                                    assert check(T, r)
                                    R[Ts].add(tuple(r[i] for i in srt))
        print("n =", n, "sets", len(V), "| nothing reachable:", empty, worst, "| every solution reachable:", full, "| smallest share reached", round(minshare, 3))
