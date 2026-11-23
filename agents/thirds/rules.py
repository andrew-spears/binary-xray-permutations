# Candidate rules for an odd S, R = rows r = p (mod 3) (0-based r, p = 0 is rows 1, 4, 7, ...).  For every valid D of size n:
# T(S) = number of solutions whose stones in the rows of R are exactly S.  Rules tested: S read off a canonical solution
# (lexicographically first / last as a list of columns, or of diagonals), S = stones k = c (mod 3), S with the largest T,
# and the share of odd S among the S that occur.      Usage: python3 rules.py n [p]
import sys, collections
n = int(sys.argv[1]); p = int(sys.argv[2]) if len(sys.argv) > 2 else 0
W = collections.defaultdict(list)
def rec(r, used, sums, cur):
    if r == n: W[tuple(sorted(cur))].append(tuple(cur)); return
    for c in range(n):
        if not used >> c & 1 and not sums >> (r + c) & 1:
            cur.append(r + c); rec(r + 1, used | 1 << c, sums | 1 << (r + c), cur); cur.pop()
rec(0, 0, 0, [])
fails = collections.Counter(); share = []; tot = 0
for D, sols in W.items():
    pos = {d: k for k, d in enumerate(D)}; tot += 1
    Sof = lambda s: tuple(sorted(pos[s[r]] for r in range(p, n, 3)))
    T = collections.Counter(Sof(s) for s in sols)
    odd = {S for S in T if T[S] % 2}
    share.append(len(odd) / len(T))
    cols = sorted(sols, key=lambda s: [s[r] - r for r in range(n)])
    cand = {"first solution by diagonals": Sof(min(sols)), "last solution by diagonals": Sof(max(sols)),
            "first solution by columns": Sof(cols[0]), "last solution by columns": Sof(cols[-1]),
            "S with the largest T (first)": max(sorted(T), key=lambda S: T[S]), "S with the smallest T (first)": min(sorted(T), key=lambda S: T[S])}
    for c in range(3): cand["stones k = %d (mod 3)" % c] = tuple(k for k in range(n) if k % 3 == c)
    for name, S in cand.items():
        if S not in odd: fails[name] += 1
    if not any(T[S] == 1 for S in T): fails["some S with T(S) = 1"] += 1
print("n = %d, rows = %d (mod 3), valid D: %d; share of odd S among the S that occur: min %.3f, mean %.3f" % (n, p, tot, min(share), sum(share) / len(share)))
for name in sorted(fails): print("  rule '%s' fails for %d D" % (name, fails[name]))
