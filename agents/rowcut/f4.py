"""Character sums over the field with 4 elements.  w = primitive cube root of 1 in F_4.
For a valid D and a in {0,1,2}^n let  chi_a(D) = sum over solutions of w^(sum_k a_k * row of stone k)  in F_4.
(a_k = 2 is the same as weighting by the column, up to a constant: w^(-r) = w^(c - d).)  chi_a != 0 for some a  <=>  some
pattern of rows mod 3 occurs an odd number of times  =>  D solvable.
Usage: python3 f4.py n      tests fixed rules a_k = phi(feature of stone k) on all valid D of size n."""
import sys, itertools, numpy as np
from collections import defaultdict
n = int(sys.argv[1]); W = defaultdict(list)
def rec(r, used, sums, cur):
    if r == n: W[tuple(sorted(cur))].append(tuple(cur)); return
    for c in range(n):
        if not used >> c & 1 and not sums >> (r + c) & 1:
            cur.append(r + c + 2); rec(r + 1, used | 1 << c, sums | 1 << (r + c), cur); cur.pop()
rec(0, 0, 0, [])
def transform(D):
    """returns (A, B): chi_a = A[a] + B[a] w, arrays of shape (3,)*n over F_2"""
    f = np.zeros((3,) * n, dtype=np.uint8); pos = {d: k for k, d in enumerate(D)}
    for cur in W[D]:
        idx = [0] * n
        for r, d in enumerate(cur): idx[pos[d]] = (r + 1) % 3
        f[tuple(idx)] ^= 1
    A, B = f, np.zeros_like(f)
    for ax in range(n):
        a0, a1, a2 = (np.take(A, i, axis=ax) for i in range(3)); b0, b1, b2 = (np.take(B, i, axis=ax) for i in range(3))
        # multiply (a + b w) by w: (b) + (a + b) w ; by w^2: (a + b) + a w
        w1 = lambda a, b: (b, a ^ b); w2 = lambda a, b: (a ^ b, a)
        out = []
        for j in range(3):
            xa, xb = a0.copy(), b0.copy()
            for (a, b), p in (((a1, b1), j), ((a2, b2), 2 * j % 3)):
                if p == 1: a, b = w1(a, b)
                elif p == 2: a, b = w2(a, b)
                xa = xa ^ a; xb = xb ^ b
            out.append((xa, xb))
        A = np.stack([o[0] for o in out], axis=ax); B = np.stack([o[1] for o in out], axis=ax)
    return A, B
feats = {"sign of e": lambda e, k, s: (e[k] > 0) - (e[k] < 0) + 1, "e mod 3": lambda e, k, s: e[k] % 3, "d mod 3": lambda e, k, s: (2 * (k + 1) + e[k]) % 3,
         "k mod 3": lambda e, k, s: (k + 1) % 3, "slack before mod 3": lambda e, k, s: s % 3, "slack after mod 3": lambda e, k, s: (s + e[k]) % 3,
         "e mod 2, sign": lambda e, k, s: 0 if e[k] % 2 == 0 else (1 if e[k] > 0 else 2), "min(|e|, 2)": lambda e, k, s: min(abs(e[k]), 2)}
fails = defaultdict(list); nz = []; tot = 0
for D in sorted(W):
    e = [d - 2 * (k + 1) for k, d in enumerate(D)]
    if not any(e): continue
    tot += 1; A, B = transform(D); Z = A | B; nz.append(int(Z.sum()) / 3 ** n)
    sl = [sum(e[:k]) for k in range(n)]
    for name, f in feats.items():
        v = [f(e, k, sl[k]) for k in range(n)]
        for phi in itertools.product(range(3), repeat=3):
            if not Z[tuple(phi[x] for x in v)]: fails[name, phi].append(e)
print(f"n = {n}: {tot} valid D (not evenly spaced); share of a with chi_a != 0: min {min(nz):.3f}, mean {sum(nz) / len(nz):.3f}")
for name in feats:
    best = sorted((len(fails[name, phi]), phi) for phi in itertools.product(range(3), repeat=3))[:3]
    print(f"  a_k = phi({name}): best phi (fails, phi): {best};  e.g. {fails[name, best[0][1]][:2]}")
