"""Are the states missed by the failed inclusions alive (completable to a permutation of some size n)?
alive(A, B, last): n and a completion: the rows [n] - A matched to the columns [n] - B with distinct sums, all > last."""
def alive(A, B, last, nmax=None):
    lo = max(max(A), max(B)); nmax = nmax or lo + 8
    for n in range(lo, nmax + 1):
        R = [r for r in range(1, n + 1) if r not in A]; C = [c for c in range(1, n + 1) if c not in B]
        def rec(i, used, sums):
            if i == len(R): return []
            for c in C:
                t = R[i] + c
                if c in used or t <= last or t in sums: continue
                got = rec(i + 1, used | {c}, sums | {t})
                if got is not None: return [(R[i], c)] + got
            return None
        got = rec(0, frozenset(), frozenset())
        if got is not None: return n, got
    return None
if __name__ == "__main__":
    cases = [("PEAK x=(3,4,3,3,2,1)", (1, 2, 3, 4, 5, 7, 11), (1, 3, 4, 5, 7, 8, 11), 14),
             ("PEAK x=(3,4,3,3,2,1)", (1, 2, 3, 4, 7, 8, 11), (1, 2, 3, 4, 7, 8, 11), 14),
             ("ZERO x=(2,3,3,2,2,1,1,0)", (1, 2, 3, 4, 5, 6, 7, 9, 12), (1, 2, 3, 4, 6, 7, 9, 10, 12), 17)]
    for name, A, B, last in cases:
        print(name, "rows", A, "cols", B, "->", alive(A, B, last))
