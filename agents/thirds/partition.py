# Tournament form of the fixed-rows claim (REPORT.md, Corollary 2).  Rows are 0-based, R_p = rows r = p (mod 3), marks
# d = row + column in 0..2n-2.  For a set Z of stones let
#     G_p(Z) = number of pairs (unordered split {A, B} of the stones outside Z; tournament with score d, 2 points a game,
#              ties 1-1 allowed only between stones in different classes of (Z, A, B))
#              with  sum_{k in A} (d_k + p) - sum_{k in B} (d_k + p)  not divisible by 3            (mod 2),
# and G_p(all stones) = 1 if D is evenly spaced (0, 2, .., 2n-2), else 0.
# Then  T(R_p, S) = sum_{Z subset of S} G_p(Z)  (mod 2);  so some T(R_p, S) is odd  <=>  some G_p(Z) is odd.
# Checks the identity by brute force for every valid D of size n, every p and every S.      Usage: python3 partition.py n
import sys, itertools, collections
n = int(sys.argv[1])
def valid():
    for D in itertools.combinations(range(2 * n - 1), n):
        if sum(D) == n * (n - 1) and all(sum(D[:k]) >= k * (k - 1) for k in range(1, n)): yield D
def solutions(D):
    out = []
    def rec(k, rows, cols, path):
        if k == n: out.append(tuple(path)); return
        d = D[k]
        for r in range(max(0, d - n + 1), min(d, n - 1) + 1):
            c = d - r
            if rows >> r & 1 or cols >> c & 1: continue
            path.append(r); rec(k + 1, rows | 1 << r, cols | 1 << c, path); path.pop()
    rec(0, 0, 0, [])
    return out
def tau(D, col):
    cur = collections.Counter({(0,) * n: 1})
    for i in range(n):
        for j in range(i + 1, n):
            nxt = collections.Counter()
            for s, v in cur.items():
                for a, b in ((2, 0), (0, 2)) + (((1, 1),) if col[i] != col[j] else ()):
                    t = list(s); t[i] += a; t[j] += b
                    if t[i] <= D[i] and t[j] <= D[j]: nxt[tuple(t)] ^= v
            cur = collections.Counter({s: v for s, v in nxt.items() if v})
    return cur.get(tuple(D), 0)
checked = bad = 0
for D in valid():
    sols = solutions(D)
    G = [[0] * (1 << n) for p in range(3)]
    for col in itertools.product(range(3), repeat=n):
        nz = [k for k in range(n) if col[k]]
        if not nz:
            for p in range(3): G[p][(1 << n) - 1] = tau(D, col)
            continue
        if col[nz[0]] != 1: continue                            # one representative of {A, B}: the first stone outside Z is in A
        if not tau(D, col): continue
        Z = sum(1 << k for k in range(n) if col[k] == 0)
        for p in range(3):
            if sum((1 if col[k] == 1 else -1) * (D[k] + p) for k in nz) % 3: G[p][Z] ^= 1
    for p in range(3):
        T = [0] * (1 << n)
        for s in sols: T[sum(1 << k for k in range(n) if s[k] % 3 == p)] ^= 1
        for S in range(1 << n):
            pred = 0; Z = S
            while True:
                pred ^= G[p][Z]
                if Z == 0: break
                Z = (Z - 1) & S
            checked += 1; bad += pred != T[S]
        assert any(T) == any(G[p])
print(f"n = {n}: (D, p, S) checked {checked}; T(R_p, S) != sum of G_p(Z) over Z in S: {bad}")
