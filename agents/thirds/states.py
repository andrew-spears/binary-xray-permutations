# Does the fixed-third-rows claim extend to interface states?  For a set D of m diagonals (0-based d = r + c) and a
# state (rows Rw, columns Cl, |Rw| = |Cl| = m) with at least one partial placement, and a phase p:
# is there S such that the number of placements whose stones in the rows r = p (mod 3) are exactly S is odd?
# Usage: python3 states.py m [M] [rel]   (rel: R = the j-th rows of the state with j = p mod M, instead of rows r = p mod M)
#        python3 states.py m [M]     (M = modulus, default 3) prints the number of (D, state, phase) that fail, for slack 0..3
# (slack = sum of D - m(m-1); slack 0 is the full square, slack 1 the two states next to it)
import sys, itertools, collections
m = int(sys.argv[1]); M = int(sys.argv[2]) if len(sys.argv) > 2 else 3; rel = len(sys.argv) > 3   # rel: R = every M-th row OF THE STATE
tot = collections.Counter(); bad = collections.Counter(); ex = {}
for D in itertools.combinations(range(2 * m + 2), m):
    groups = collections.defaultdict(list)
    def rec(k, rows, cols, pl):
        if k == m: groups[(rows, cols)].append(tuple(pl)); return
        d = D[k]
        for r in range(d + 1):
            c = d - r
            if rows >> r & 1 or cols >> c & 1: continue
            pl.append(r); rec(k + 1, rows | 1 << r, cols | 1 << c, pl); pl.pop()
    rec(0, 0, 0, [])
    for (rows, cols), pls in groups.items():
        # slack = sum of (row + col indices) minus that of the top-left square = sum(D) - m(m-1)
        sl = sum(D) - m * (m - 1)
        rk = {r: j for j, r in enumerate(r for r in range(2 * m + 2) if rows >> r & 1)}
        for p in range(M):
            f = collections.Counter()
            for pl in pls:
                f[tuple(k for k in range(m) if (rk[pl[k]] if rel else pl[k]) % M == p)] ^= 1
            tot[sl] += 1
            if not any(f.values()):
                bad[sl] += 1
                ex.setdefault(sl, (D, [r for r in range(2*m+2) if rows >> r & 1], [c for c in range(2*m+2) if cols >> c & 1], p, len(pls)))
for sl in sorted(tot)[:4]: print(("relative rows, " if rel else "") + "m = %d, modulus %d, slack %d: (D, state, phase) with placements %d, without an odd S %d%s" % (m, M, sl, tot[sl], bad[sl], ("   e.g. D, rows, cols, phase, placements = " + str(ex[sl])) if sl in ex else ""))
