"""Sanity check of the interface-walk model: count walks for each valid D and compare with
brute-force witness counts.  Usage: python3 check_walks.py nmax"""
import sys, itertools
from math import comb

def valid_Ds(n):
    for D in itertools.combinations(range(-(n-1), n), n):
        s = [D[k] + n - (k+1) for k in range(n)]
        ps = 0; ok = True
        for k in range(n):
            ps += s[k]
            if ps < comb(k+1, 2): ok = False; break
        if ok and ps == comb(n, 2): yield D

def brute(n):
    cnt = {}
    for p in itertools.permutations(range(1, n+1)):
        d = tuple(sorted(p[i] - (i+1) for i in range(n)))
        if len(set(d)) == n: cnt[d] = cnt.get(d, 0) + 1
    return cnt

def walks(D):
    n = len(D)
    e = [D[k] + n - (k+1) - k for k in range(n)]      # e_k = s_k - (k-1), k 1-based
    cur = {(frozenset(), frozenset()): 1}
    for k in range(n):                                 # placing stone k+1
        nxt = {}
        for (R, C), w in cur.items():
            for u in range(-(k), n - k):               # r' = k+1+u in 1..n
                r = k + 1 + u
                if r in R: continue
                c = k + 1 + e[k] - u
                if c < 1 or c > n or c in C: continue
                key = (R | {r}, C | {c})
                nxt[key] = nxt.get(key, 0) + w
        cur = nxt
    return sum(cur.values())

if __name__ == "__main__":
    nmax = int(sys.argv[1])
    for n in range(2, nmax + 1):
        b = brute(n); bad = 0; tot = 0
        for D in valid_Ds(n):
            tot += 1
            if walks(D) != b.get(D, 0): bad += 1
        print(n, "valid D:", tot, "mismatches:", bad, "valid D with no witness:", sum(1 for D in valid_Ds(n) if D not in b))
