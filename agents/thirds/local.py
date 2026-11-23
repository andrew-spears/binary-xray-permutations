# Local failure patterns of a slack-1 prefix.  A = e_1..e_m with prefix sums >= 1 (no tight cut) and sum 1.
# State "row": rows 1..m-1, m+1 and columns 1..m are used; state "col": rows 1..m and columns 1..m-1, m+1.
# F(A, t) = the row patterns w in {0,1}^(m+1) (R = rows with w = 1) for which no set S of stones has an odd number of
# placements of A in state t with the stones in the rows of R exactly S.
# Usage: python3 local.py mmax       prints F(A, t) for every A of length <= mmax with F nonempty (don't-care rows as '.')
import sys, itertools, collections
mmax = int(sys.argv[1])
def placements(e, t):
    m = len(e); rows_ok = set(range(m - 1)) | {m} if t == "row" else set(range(m)); cols_ok = set(range(m)) if t == "row" else set(range(m - 1)) | {m}
    out = []
    def rec(k, rows, cols, pl):
        if k == m: out.append(tuple(pl)); return
        d = 2 * k + e[k]
        for r in rows_ok:
            c = d - r
            if c in cols_ok and not rows >> r & 1 and not cols >> c & 1: rec(k + 1, rows | 1 << r, cols | 1 << c, pl + [r])
    rec(0, 0, 0, []); return out
def words(m):
    out = []
    def rec(k, e, s):
        if k == m:
            if s == 1: out.append(tuple(e))
            return
        lo = e[-1] - 1 if e else 1
        for x in range(max(lo, 1 - s), m + 1):
            if s + x + (m - 1 - k) * x - (m - 1 - k) * (m - k) // 2 > 1: break
            rec(k + 1, e + [x], s + x)
    rec(0, [], 0); return out
for m in range(1, mmax + 1):
    for e in words(m):
        for t in ("row", "col"):
            pls = placements(e, t); rows = sorted(set(pls[0])) if pls else []
            bad = set()
            for bits in itertools.product("01", repeat=len(rows)):
                w = dict(zip(rows, bits)); f = collections.Counter()
                for pl in pls: f[tuple(k for k in range(m) if w[pl[k]] == "1")] ^= 1
                if not any(f.values()): bad.add("".join(w.get(r, ".") for r in range(m + 1)))
            if bad: print("A = %s, %s state, %d placements: F = %s" % (" ".join(map(str, e)), t, len(pls), " ".join(sorted(bad))))
