"""Checks of REPORT2 section 1, for every valid word without a tight cut of size n and every S:
 (1) balance form: 'S is an I-split with u weakly increasing' <=> window condition and, for every kappa in S,
     e_kappa + sum_{k<kappa, k not in S} clamp(e_k - 2 sig, 0, 2) = sum_{k>kappa, k not in S} clamp(-e_k - 2 sig, 0, 2),
     sig = number of stones of S strictly between k and kappa;
 (2) cycle picture: then r_j = N_{2m-2j+1} + j, c_j = N_{2m-2j+2} + j satisfy c_1 <= r_1 < c_2 <= r_2 < .. and r_j + c_j = d_{k_j};
 (3) for |S| = 2: RR-split <=> all v in [0, 4] and min(u) in {N3 + N4, N2 + N4}  (two.py against the general test).
Usage: python3 balance.py n"""
import sys, itertools
from ext import words, parts, shape, conj, splits
from x2 import isplit
from two import two
cl = lambda x: max(0, min(2, x))
def balance(e, S):
    n = len(e); m = len(S); Sset = set(S)
    for k in range(1, n + 1):
        if k in Sset: continue
        b = sum(1 for j in S if j < k)
        if e[k - 1] < -2 * b or e[k - 1] > 2 * (m - b): return False
    for kap in S:
        left = e[kap - 1] + sum(cl(e[k - 1] - 2 * sum(1 for j in S if k < j < kap)) for k in range(1, kap) if k not in Sset)
        right = sum(cl(-e[k - 1] - 2 * sum(1 for j in S if kap < j < k)) for k in range(kap + 1, n + 1) if k not in Sset)
        if left != right: return False
    return True
n = int(sys.argv[1]); nw = ns = ni = bad1 = bad2 = bad3 = 0
for e in words(n, False):
    if not any(e) or any(sum(e[:k]) == 0 for k in range(1, n)): continue
    nw += 1; T = {(a, b) for a, b, ty in two(e)}
    for m in range(1, n):
        for S in itertools.combinations(range(1, n + 1), m):
            ns += 1; I = isplit(e, S); bad1 += I != balance(e, S)
            if I:
                ni += 1
                v = [2 * sum(1 for j in S if j > k) - e[k - 1] for k in range(1, n + 1) if k not in S]
                N = [sum(1 for a in v if a >= i) for i in range(1, 2 * m + 2)]
                R = [N[2 * (m - j)] + j for j in range(1, m + 1)]; C = [N[2 * (m - j) + 1] + j for j in range(1, m + 1)]
                ok = all(C[j] <= R[j] for j in range(m)) and all(R[j] < C[j + 1] for j in range(m - 1)) and all(R[j] + C[j] == 2 * S[j] + e[S[j] - 1] for j in range(m))
                bad2 += not ok
            if m == 2:
                w1, w2 = parts(e, sum(1 << (k - 1) for k in S))
                r = min(w1) >= 0 and min(w2) >= 0 and splits(conj(shape(w2)[0]), shape(w1)[0])
                bad3 += r != (S in T)
print(f"n = {n}: {nw} words, {ns} pairs (word, S), {ni} I-splits with u increasing; balance form wrong: {bad1}; cycle picture wrong: {bad2}; two-stone criterion wrong: {bad3}")
