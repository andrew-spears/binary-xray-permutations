# Level-1 theorem (REPORT.md): for a set D of n marks in 0..2n-2 (0-based d = row + column) with sum n(n-1), and a stone k,
#     sum_r N(k, r) u^r  =  c u^a (1 + u)^b   (mod 2),          N(k, r) = number of solutions with stone k in row r (0-based),
# where the other n - 1 stones are matched to the n - 1 segments [2h, 2h+2], h = 0..n-2 (a stone goes to a segment that
# contains its mark; the stone-segment graph is a forest, so there is at most one perfect matching):
#     c = 1 if the matching exists, else 0;   b = number of other stones on odd marks;
#     a = number of other stones on even marks matched to the segment on their right.
# Checks the formula against brute force, and the corollary: if N is even and some N(k, r) is odd then for every p in
# {0,1,2} some stone k has an odd number of solutions with stone k in a row = p (mod 3).
# Usage: python3 formula.py n [all]     words without a tight cut (default) or all n-subsets of 0..2n-2 with sum n(n-1) (all; valid or not)
import sys, itertools
n = int(sys.argv[1]); allsets = len(sys.argv) > 2
def brute(D):
    M = [0] * n; cnt = [0]
    def rec(k, rows, cols, path):
        if k == n:
            cnt[0] += 1
            for i, r in enumerate(path): M[i] ^= 1 << r
            return
        d = D[k]
        for r in range(max(0, d - n + 1), min(d, n - 1) + 1):
            c = d - r
            if rows >> r & 1 or cols >> c & 1: continue
            path.append(r); rec(k + 1, rows | 1 << r, cols | 1 << c, path); path.pop()
    rec(0, 0, 0, [])
    return M, cnt[0]
def predicted(D, k):
    rest = set(D) - {D[k]}; used = set(); a = 0
    for h in range(n - 1):
        must = [m for m in (2 * h, 2 * h + 1) if m in rest and m not in used]
        if len(must) > 1: return None
        if must: m = must[0]; a += m == 2 * h
        elif 2 * h + 2 in rest: m = 2 * h + 2
        else: return None
        used.add(m)
    if used != rest: return None
    b = sum(m & 1 for m in rest)
    return a, b
def words():
    e = [0] * n
    def rec(k, sl):
        if k == n:
            if sl == 0: yield [2 * i + e[i] for i in range(n)]
            return
        lo = e[k - 1] - 1 if k else 1
        for x in range(max(lo, -sl), n):
            s2 = sl + x
            if k < n - 1 and s2 <= 0: continue
            if s2 + (n - 1 - k) * x - (n - 1 - k) * (n - k) // 2 > 0: break
            e[k] = x; yield from rec(k + 1, s2)
    yield from rec(0, 0)
src = (list(D) for D in itertools.combinations(range(2 * n - 1), n) if sum(D) == n * (n - 1)) if allsets else words()
tot = bad = lev1 = badcor = 0
for D in src:
    M, N = brute(D); tot += 1; ts = set()
    for k in range(n):
        ab = predicted(D, k); row = 0
        if ab:
            a, b = ab
            for i in range(b + 1):
                if (i & (b - i)) == 0 and a + i < n: row |= 1 << (a + i)      # C(b, i) odd  <=>  i is a submask of b
                if (i & (b - i)) == 0 and a + i >= n: row = -1
            ts.add((a + 2 * b) % 3)
        if row != M[k]: bad += 1; print("  MISMATCH", D, k, ab, bin(M[k]))
    if N % 2 == 0 and any(M):
        lev1 += 1
        ok = all(any(bin(M[k] & sum(1 << r for r in range(p, n, 3))).count('1') & 1 for k in range(n)) for p in range(3))
        if not ok or len(ts) < 2: badcor += 1; print("  COROLLARY FAILS", D)
print(f"n = {n}, {'all n-subsets of 0..2n-2 with sum n(n-1)' if allsets else 'words without a tight cut'}: {tot}; (D, k) where the formula is wrong: {bad}; D with N even and M != 0: {lev1}; of these, without an odd single-stone count for some phase: {badcor}")
