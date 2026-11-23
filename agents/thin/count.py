"""States per slack: all pairs of partitions, and T(a, b).   Usage: python3 count.py [maxslack]"""
import sys
S = int(sys.argv[1]) if len(sys.argv) > 1 else 40
# c[k][n] = number of partitions of n with exactly k part sizes (k <= 3)
K = 4
c = [[0] * (S + 1) for _ in range(K + 1)]; c[0][0] = 1
for p in range(1, S + 1):                      # add part size p with multiplicity m >= 1
    new = [row[:] for row in c]
    for k in range(K):
        for n in range(S + 1):
            if c[k][n]:
                for m in range(1, (S - n) // p + 1): new[k + 1][n + p * m] += c[k][n]
    c = new
P = [1] + [0] * S
for p in range(1, S + 1):
    for n in range(p, S + 1): P[n] += P[n - p]
le = lambda a, n: sum(c[k][n] for k in range(a + 1))
def T(a, b, s):
    return sum(le(a, i) * le(b, s - i) + le(b, i) * le(a, s - i) - le(min(a, b), i) * le(min(a, b), s - i) for i in range(s + 1))
print("slack   all pairs    T(1,2)    T(1,3)    T(2,2)")
for s in (4, 8, 12, 16, 20, 24, 32, 40):
    if s <= S: print(f"{s:5d} {sum(P[i] * P[s - i] for i in range(s + 1)):11d} {T(1, 2, s):9d} {T(1, 3, s):9d} {T(2, 2, s):9d}")
