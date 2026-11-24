"""The bridge condition.  A valid word in which a letter >= 2 precedes a letter <= -2 is  w = x m y  with x = the letters before the first
letter >= 2 (all <= 1), y = the letters after the last letter <= -2 (all >= -1), m = the rest.  By Theorem 0 and its mirror
F(x) contains G(s1) and A(y) contains conj G(s2).  Sufficient for solvability:   step_m(G(s1)) meets conj G(s2).        (BRIDGE)
Checks (BRIDGE) for every such valid word of length <= N (all letters), and prints the least size of the intersection.
  python3 bridge.py N [C]      C: only words with letters in [-C, C]
  python3 bridge.py random CNT LEN SMAX C     CNT random valid words, letters in [-C, C], about LEN letters, slacks <= SMAX"""
import sys
sys.path.insert(0, "../l1sets")
import l1
from neg0 import in_G
l1.depth = lambda u: len(u[0]) + len(u[1]) + 6 + 2 * N
RANDOM = sys.argv[1] == "random"
if RANDOM: CNT, LEN, SMAX, C, N = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), 3 * int(sys.argv[4])
else: N = int(sys.argv[1]); C = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 6
def parts(n, m=None):
    m = n if m is None else m
    if n == 0: yield (); return
    for a in range(min(n, m), 0, -1):
        for p in parts(n - a, a): yield (a,) + p
Gs = {}
def G(s):
    if s not in Gs: Gs[s] = frozenset(u for k in range(s + 1) for lam in parts(k) for nu in parts(s - k) for u in [(lam, nu)] if in_G(u))
    return Gs[s]
cG = {}
def conjG(s):
    if s not in cG: cG[s] = frozenset((l1.conj(u[0]), l1.conj(u[1])) for u in G(s))
    return cG[s]
memo = {}
def push(s1, m):
    if (s1, m) not in memo:
        if not m: memo[s1, m] = G(s1)
        else: memo[s1, m] = frozenset(v for u in push(s1, m[:-1]) for k, v in l1.succs(u, m[-1]))
    return memo[s1, m]
stat = {}
def rec(w, s):
    n = len(w)
    if n and s == 0 and n <= N:
        i = next((j for j, e in enumerate(w) if e >= 2), None); j = max((j for j, e in enumerate(w) if e <= -2), default=None)
        if i is not None and j is not None and i < j:
            x, m, y = w[:i], w[i:j + 1], w[j + 1:]; s1 = sum(x); s2 = s1 + sum(m)
            I = push(s1, m) & conjG(s2); st = stat.setdefault(n, [0, 10 ** 9, None, 0]); st[0] += 1
            if len(I) < st[1]: st[1], st[2] = len(I), w
            st[3] += not I
    if n == N: return
    L = N - n - 1
    for e in range(max((w[-1] - 1) if w else -N, -s, -C), min(2 * N, C + 1)):
        if s + e + L * e - L * (L + 1) // 2 > 0: break
        rec(w + (e,), s + e)
def split(w):
    i = next((j for j, e in enumerate(w) if e >= 2), None); j = max((j for j, e in enumerate(w) if e <= -2), default=None)
    return None if i is None or j is None or i > j else (w[:i], w[i:j + 1], w[j + 1:])
if RANDOM:
    import random
    rng = random.Random(1); done = 0; mn = (10 ** 9, None); bad = 0; smax = 0; mlen = 0
    while done < CNT:
        w = []; s = 0
        while len(w) < LEN or s:
            lo = max((w[-1] - 1) if w else -C, -s, -C); hi = min(C, SMAX - s)
            if len(w) >= LEN: hi = min(hi, lo + 1)
            if hi < lo: break
            e = rng.randint(lo, hi); w.append(e); s += e
        if s or split(tuple(w)) is None: continue
        x, m, y = split(tuple(w)); s1 = sum(x); s2 = s1 + sum(m); cur = G(s1)
        for e in m: cur = frozenset(v for u in cur for k, v in l1.succs(u, e))
        I = cur & conjG(s2); done += 1; bad += not I; smax = max(smax, max(sum(w[:i]) for i in range(len(w)))); mlen = max(mlen, len(m))
        if len(I) < mn[0]: mn = (len(I), w)
    print(f"{CNT} random valid words with a letter >= 2 before a letter <= -2, letters in [-{C}, {C}], length >= {LEN}, largest slack {smax}, longest middle {mlen}: (BRIDGE) fails for {bad}; least intersection {mn[0]} at {' '.join(map(str, mn[1]))}")
    sys.exit()
rec((), 0)
for n in sorted(stat):
    c, mn, w, bad = stat[n]; print(f"n {n}: {c} valid words with a letter >= 2 before a letter <= -2" + (f" (letters in [-{C}, {C}])" if C < 10 ** 6 else "") + f"; (BRIDGE) fails for {bad}; least |step_m(G(s1)) n conj G(s2)| = {mn} at {' '.join(map(str, w))}", flush=True)
