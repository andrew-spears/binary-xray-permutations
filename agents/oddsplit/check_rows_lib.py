"""count(D, R, C) = number of bijections R -> C whose sums r + c are exactly the list D (distinct values)."""
def count(D, R, C):
    # number of bijections R -> C whose sums are exactly the set D
    R = sorted(R); C = sorted(C); m = len(R); memo = {}
    def rec(i, usedC, usedD):
        if i == m: return 1
        key = (i, usedC, usedD)
        if key in memo: return memo[key]
        t = 0
        for a, c in enumerate(C):
            if usedC >> a & 1: continue
            s = R[i] + c
            if s in D:
                b = D.index(s)
                if not usedD >> b & 1: t += rec(i + 1, usedC | 1 << a, usedD | 1 << b)
        memo[key] = t; return t
    return rec(0, 0, 0)
