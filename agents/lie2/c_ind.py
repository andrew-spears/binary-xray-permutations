"""Part C: natural induction steps for the type C_n board problem, n <= 7.
Target m_1 > ... > m_n >= 1, even sum, m_1 + ... + m_k <= k(2n - k + 1).  deficiency c = (n(n+1) - sum m) / 2.
 (1) slices: c = 0 is type A_{n-1} (all signs +).  Tight cut at k (equality): top k values are a type A_{k-1} problem on
     rows/columns n-k+1..n with all signs +, the rest is a C_{n-k} target (proved in REPORT).  'prime' = no tight cut.
 (2) greedy: rows n, n-1, ..., 1 in turn take the largest remaining value they can read on an unused column.
 (3) last row and column: a solution with stones (n, a), (b, n), a, b < n, gives a solution of C_{n-1} for
     m' = m - {two values read by them} + {x}, x = a + b or |a - b|, with a stone at (b, a) reading x, and conversely.
     Count the prime targets for which: some reduction has m' a valid target; every valid m' lifts (has a solution
     through (b, a) reading x); the reduction with the largest two values on the two stones lifts.
Usage: python3 c_ind.py n"""
import sys, collections
from ctype import targets, solutions
n = int(sys.argv[1]); T = targets(n); top = n * (n + 1)
def valid(m, k):          # is the set m a C_k target
    m = sorted(m, reverse=True)
    if len(set(m)) != k or min(m) < 1 or sum(m) % 2: return False
    s = 0
    for i, v in enumerate(m, 1):
        s += v
        if s > i * (2 * k - i + 1): return False
    return True
def tight(m): return [k for k in range(1, n + 1) if sum(m[:k]) == k * (2 * n - k + 1)]
prime = [m for m in T if not tight(m)]
bydef = collections.Counter((top - sum(m)) // 2 for m in T)
print(f"C_{n}: {len(T)} targets; deficiency 0 (= type A_{n-1}): {bydef[0]}; with a tight cut: {len(T) - len(prime)}; prime: {len(prime)}")
# (2) greedy
def greedy(m):
    rem = set(m); used = set()
    for i in range(n, 0, -1):
        best = None
        for j in range(1, n + 1):
            if j in used: continue
            for t in (i + j, abs(i - j)):
                if t in rem and (best is None or t > best[0]): best = (t, j)
        if best is None: return False
        rem.discard(best[0]); used.add(best[1])
    return True
gf = [m for m in T if not greedy(m)]
print(f"  greedy (row n down, largest readable value) fails on {len(gf)} targets; first: {gf[:3]}")
# solutions of all C_{n-1} targets, indexed
if n >= 3:
    sols = {}
    def get(mp):
        if mp not in sols: sols[mp] = solutions(n - 1, mp)
        return sols[mp]
    stat = collections.Counter(); ex = {}
    minsol = collections.defaultdict(lambda: 10**9)
    for m in prime:
        S = solutions(n, m); c = (top - sum(m)) // 2; minsol[c] = min(minsol[c], len(S))
        ms = set(m); reds = []
        for a in range(1, n):
            for b in range(1, n):
                for va in {n + a, n - a} & ms:
                    for vb in ({n + b, n - b} & ms) - {va}:
                        for x in {a + b, abs(a - b)} - {0}:
                            rest = ms - {va, vb}
                            if x in rest: continue
                            mp = tuple(sorted(rest | {x}, reverse=True))
                            if not valid(mp, n - 1): continue
                            lift = any((b, a) in s or (b, -a) in s for s in get(mp) if
                                       ((b, a) in s and x == a + b) or ((b, -a) in s and x == abs(a - b)))
                            reds.append((va + vb, lift, (a, b, va, vb, x)))
        stat["prime"] += 1
        if not reds: stat["no valid reduction"] += 1; ex.setdefault("no valid reduction", m); continue
        if not any(r[1] for r in reds): stat["no reduction lifts"] += 1; ex.setdefault("no reduction lifts", m)
        if not all(r[1] for r in reds): stat["some valid reduction does not lift"] += 1; ex.setdefault("some valid reduction does not lift", (m, next(r[2] for r in reds if not r[1])))
        big = max(r[0] for r in reds)
        if not any(r[1] for r in reds if r[0] == big): stat["largest-values reduction does not lift"] += 1; ex.setdefault("largest-values reduction does not lift", m)
        stat["valid reductions"] += len(reds); stat["lifting reductions"] += sum(r[1] for r in reds)
    print("  last row+column:", dict(stat))
    for k, v in ex.items(): print("     first example,", k, ":", v)
    print("  least number of solutions of a prime target, by deficiency:", dict(sorted(minsol.items())))
