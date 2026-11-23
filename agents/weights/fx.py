"""Direct enumeration of F(x) in absolute coordinates (independent of the machine), for REPORT2.
  python3 fx.py ones N        F(1^n) = P_n minus E_n for n <= N   (Theorem of REPORT2 section 1)
  python3 fx.py zeros A B     F(1^a 0^b), a <= A, b <= B, against the parity-count set
  python3 fx.py word e1 e2 .. size of F and of the parity-count set"""
import sys
from itertools import combinations
def step(S, n, e):          # stone number n with sum 2n + e
    out = set(); t = 2 * n + e
    for R, C in S:
        for r in range(1, t):
            c = t - r
            if r not in R and c not in C: out.add((R | {r}, C | {c}))
    return out
def F(word):
    S = {(frozenset(), frozenset())}
    for n, e in enumerate(word, 1): S = step(S, n, e)
    return S
def lam(R):
    n = len(R); return tuple(a for a in (r - (n - i) for i, r in enumerate(sorted(R, reverse=True))) if a)
def conj(l): return tuple(sum(1 for a in l if a > j) for j in range(l[0])) if l else ()
def nm(t): return "|".join("".join(map(str, lam(p))) or "-" for p in t)
def partitions(n, m=None):
    if m is None: m = n
    if n == 0: yield (); return
    for a in range(min(n, m), 0, -1):
        for p in partitions(n - a, a): yield (a,) + p
def states(n, s):           # all (R, C) with n stones and slack s
    out = []
    for a in range(s + 1):
        for l in partitions(a):
            if len(l) > n: continue
            R = frozenset((l[i] if i < len(l) else 0) + n - i for i in range(n))
            for m in partitions(s - a):
                if len(m) <= n: out.append((R, frozenset((m[i] if i < len(m) else 0) + n - i for i in range(n))))
    return out
odd = lambda A: sum(a % 2 for a in A)
def paritycount(word):      # card paritycount: z even letters, p odd letters
    n = len(word); z = sum(1 for e in word if e % 2 == 0); p = n - z
    return {(R, C) for R, C in states(n, sum(word)) if abs(odd(R) + odd(C) - n) <= z and (odd(R) + odd(C) - n - z) % 2 == 0
            and abs(odd(R) - odd(C)) <= p and (odd(R) - odd(C) - p) % 2 == 0}
if __name__ == "__main__":
    if sys.argv[1] == "ones":
        S = {(frozenset(), frozenset())}
        for n in range(1, int(sys.argv[2]) + 1):
            S = step(S, n, 1); P = {(R, C) for R, C in states(n, n) if odd(R) + odd(C) == n}
            E = {(R, C) for R, C in P if not R & {2 * n + 1 - c for c in C}}
            E2 = {(R, C) for R, C in P if lam(C) == conj(lam(R)) and odd(R) * 2 == n}
            print(f"n {n:2d}: |P_n| = {len(P)}, |E_n| = {len(E)}, |F(1^n)| = {len(S)}, F = P - E: {S == P - E}, E = (lam|lam') with empty 2-core: {E == E2}", flush=True)
    elif sys.argv[1] == "zeros":
        for a in range(1, int(sys.argv[2]) + 1):
            for b in range(1, int(sys.argv[3]) + 1):
                w = (1,) * a + (0,) * b; S = F(w); Q = paritycount(w); ex = sorted(nm(t) for t in Q - S)
                print(f"1^{a} 0^{b}: |F| = {len(S)}, parity-count set {len(Q)}, inside: {S <= Q}, missing {len(ex)}: {' '.join(ex[:14])}", flush=True)
    else:
        w = tuple(int(a) for a in sys.argv[2:]); S = F(w); Q = paritycount(w)
        print(f"|F| = {len(S)}, parity-count set {len(Q)}, inside: {S <= Q}")
