"""BRIDGE-ODD and LINE on random steep middles (meet in the middle).  python3 oddrand.py COUNT LEN SMAX C SEED
A middle (s1, m): first letter >= 2, last letter <= -2, next letter >= last - 1, all slacks in [0, SMAX], s1 <= 4, letters in [-C, C]."""
import sys, random
A = sys.argv[1:]; sys.argv[1] = "none"
exec(open("linerand.py").read().split('if sys.argv[1] == "fam"')[0])
def odd(s, step, e):
    P = {E: 1}
    for _ in range(s):
        Q = {}
        for u, c in P.items():
            for k, v in step(u, e): Q[v] = Q.get(v, 0) ^ c
        P = {u: 1 for u, c in Q.items() if c}
    return frozenset(P)
OF, OB = {}, {}
def ODD(s1, m):
    s2 = s1 + sum(m); h = len(m) // 2
    if s1 not in OF: OF[s1] = odd(s1, l1.succs, 1)
    if s2 not in OB: OB[s2] = odd(s2, l1.preds, -1)
    F = OF[s1]
    for e in m[:h]: F = frozenset(v for u in F for k, v in l1.succs(u, e))
    B = OB[s2]
    for e in reversed(m[h:]): B = frozenset(v for u in B for k, v in l1.preds(u, e))
    return len(F & B)
COUNT, LEN, SMAX, C, SEED = map(int, A); rng = random.Random(SEED); fo = fl = 0; done = 0; peak = 0; seen = set()
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
    if not ODD(s1, m): fo += 1; print("BRIDGE-ODD FAILS", s1, m, flush=True)
    fl += not LINE(s1, m)[0]
print(f"distinct random middles: {COUNT}, length <= {LEN}, slack <= {SMAX} (largest seen {peak}), letters in [-{C}, {C}]: BRIDGE-ODD failures {fo}, LINE failures {fl}")
