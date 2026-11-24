"""BRIDGE (the G-form) on random steep middles.  python3 bridgerand.py COUNT LEN SMAX C SEED
Same middles as oddrand.py: s1 <= 4, first letter >= 2, last <= -2, slacks in [0, SMAX], letters in [-C, C].
Forward from G(s1), then counts the reached states v with conj v in G(s2)."""
import sys, random
sys.path.insert(0, "../l1sets"); sys.path.insert(0, "../l2sets")
import l1, neg0
l1.depth = lambda u: len(u[0]) + len(u[1]) + 60
def parts(n, mx=None):
    mx = n if mx is None else mx
    if n == 0: yield (); return
    for a in range(min(n, mx), 0, -1):
        for p in parts(n - a, a): yield (a,) + p
G = {s: frozenset(u for k in range(s + 1) for lam in parts(k) for nu in parts(s - k) for u in [(lam, nu)] if neg0.in_G(u)) for s in range(5)}
def legal(s1, m):
    s = s1
    for i, e in enumerate(m):
        if i and e < m[i - 1] - 1: return False
        s += e
        if s < 0: return False
    return m[0] >= 2 and m[-1] <= -2
def BRIDGE(s1, m):
    F = G[s1]
    for e in m: F = frozenset(v for u in F for k, v in l1.succs(u, e))
    return sum(1 for v in F if neg0.in_G((l1.conj(v[0]), l1.conj(v[1])))), len(F)
if sys.argv[1] == "one":
    s1 = int(sys.argv[2]); m = tuple(map(int, sys.argv[3].split())); print(s1, m, "in conj G(s2), reached:", BRIDGE(s1, m)); sys.exit()
COUNT, LEN, SMAX, C, SEED = map(int, sys.argv[1:6]); rng = random.Random(SEED); fail = 0; done = 0; peak = 0; seen = set(); least = (1, None)
while done < COUNT:
    s1 = rng.randint(0, 4); m = [rng.randint(2, C)]; s = s1 + m[0]; L = rng.randint(3, LEN)
    while len(m) < L:
        lo = max(m[-1] - 1, -s, -C); hi = min(C, SMAX - s)
        if lo > hi: break
        e = rng.randint(lo, hi) if rng.random() < .5 else (hi if len(m) < L // 2 else lo)
        m.append(e); s += e
    while m and m[-1] > -2: s -= m.pop()
    m = tuple(m)
    if len(m) < 3 or not legal(s1, m) or (s1, m) in seen: continue
    seen.add((s1, m)); done += 1; peak = max(peak, max(s1 + sum(m[:i]) for i in range(len(m) + 1)))
    a, b = BRIDGE(s1, m); least = min(least, (a / b, (s1, m)))
    if not a: fail += 1; print("BRIDGE FAILS", s1, m, flush=True)
print(f"distinct random middles: {COUNT}, length <= {LEN}, slack <= {SMAX} (largest seen {peak}), letters in [-{C}, {C}]: BRIDGE failures {fail}; least share of reached states in conj G(s2): {least[0]:.3f} at {least[1]}")
