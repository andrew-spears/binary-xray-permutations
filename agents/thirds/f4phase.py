# The F_4 phase identity (REPORT.md):  for u in {1, w, w^2}^n  (w^2 + w + 1 = 0),
#     F(u) = sum over solutions of prod_k u_k^(row of stone k)  =  prod_k u_k^(-d_k) * tau(u),      tau(u) in {0, 1},
# tau(u) = parity of the number of tournaments with score d (2 points a game) whose ties (1 - 1) are between stones of
# different colours u_i != u_j only.  Checks both statements by brute force for every valid D of size n and every u.
# Usage: python3 f4phase.py n
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
def tau(D, col):      # parity of the number of tournaments with ties only between different colours and score D
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    cur = collections.Counter({(0,) * n: 1})
    for i, j in pairs:
        nxt = collections.Counter()
        for s, v in cur.items():
            for a, b in ((2, 0), (0, 2)) + (((1, 1),) if col[i] != col[j] else ()):
                t = list(s); t[i] += a; t[j] += b
                if t[i] <= D[i] and t[j] <= D[j]: nxt[tuple(t)] ^= v
        cur = collections.Counter({s: v for s, v in nxt.items() if v})
    return cur.get(tuple(D), 0)
tot = bad = nz = 0
for D in valid():
    sols = solutions(D)
    for col in itertools.product(range(3), repeat=n):
        cnt = [0, 0, 0]
        for s in sols: cnt[(sum(c * r for c, r in zip(col, s)) + sum(c * d for c, d in zip(col, D))) % 3] ^= 1
        # F(u) * prod u_k^(d_k) = cnt[0] + cnt[1] w + cnt[2] w^2;  it is 0 iff cnt = 000 or 111, and 1 iff cnt = 100 or 011
        val = {(0, 0, 0): 0, (1, 1, 1): 0, (1, 0, 0): 1, (0, 1, 1): 1}.get(tuple(cnt))
        tot += 1; nz += val == 1
        if val is None or val != tau(D, col): bad += 1
print(f"n = {n}: (valid D, u) pairs {tot}; F(u) != 0 for {nz}; pairs where F(u) prod u^d is not the 0/1 number tau(u): {bad}")
