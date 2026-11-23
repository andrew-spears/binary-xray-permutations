"""LINE on steep and random middles (meet in the middle).  python3 linerand.py fam | python3 linerand.py rand COUNT LEN SMAX C SEED
A middle (s1, m): first letter >= 2, last letter <= -2, next letter >= last - 1, all slacks >= 0.
LINE: m carries one of the four line states of slack s1 to one of the four line states of slack s2."""
import sys, random
sys.path.insert(0, "../l1sets")
import l1
l1.depth = lambda u: len(u[0]) + len(u[1]) + 60
E = ((), ())
def line(s): return [E] if s == 0 else [((1,), ()), ((), (1,))] if s == 1 else [((s,), ()), ((), (s,)), ((1,) * s, ()), ((), (1,) * s)]
def LINE(s1, m):
    s2 = s1 + sum(m); h = len(m) // 2
    F = frozenset(line(s1))
    for e in m[:h]: F = frozenset(v for u in F for k, v in l1.succs(u, e))
    B = frozenset(line(s2))
    for e in reversed(m[h:]): B = frozenset(v for u in B for k, v in l1.preds(u, e))
    return len(F & B), len(F), len(B)
def legal(s1, m):
    s = s1
    for i, e in enumerate(m):
        if i and e < m[i - 1] - 1: return False
        s += e
        if s < 0: return False
    return m[0] >= 2 and m[-1] <= -2
if sys.argv[1] == "fam":
    fams = []
    for k in range(2, 8):
        st = tuple(range(k, -k - 1, -1))
        for s1 in (0, 1, 2, 5): fams.append((f"staircase {k}..-{k}", s1, st))
    for a in range(1, 7):
        for s1 in (0, 1, 3):
            fams.append((f"2^{a} 1 0 -1 (-2)^{a}", s1, (2,) * a + (1, 0, -1) + (-2,) * a))
            fams.append((f"2^{a} 1^3 0 (-1)^3 (-2)^{a}", s1, (2,) * a + (1, 1, 1, 0, -1, -1, -1) + (-2,) * a))
            fams.append((f"(2 1)^{a} 0 (-1 -2)^{a}", s1, (2, 1) * a + (0,) + (-1, -2) * a))
    for a in range(1, 5):
        for s1 in (0, 2):
            fams.append((f"4^{a} 3 2 1 0 -1 -2 -3 (-4)^{a}", s1, (4,) * a + (3, 2, 1, 0, -1, -2, -3) + (-4,) * a))
            fams.append((f"3^{a} 2 1 0 -1 -2 (-3)^{a}", s1, (3,) * a + (2, 1, 0, -1, -2) + (-3,) * a))
            fams.append((f"2^{a} 1 0 -1 -2 -3 ... down to slack {s1}", s1, (2,) * a + tuple(range(1, -40, -1))))
    for name, s1, m in fams:
        if name.endswith(f"slack {s1}"):
            s = s1; mm = []
            for e in m:
                if s + e < 0: break
                mm.append(e); s += e
            m = tuple(mm)
        if not legal(s1, m): continue
        j, f, b = LINE(s1, m)
        print("OK  " if j else "FAIL", name, "s1 =", s1, "len", len(m), "peak slack", max(s1 + sum(m[:i]) for i in range(len(m) + 1)), "meet", j, "of", f, b, flush=True)
else:
    COUNT, LEN, SMAX, C, SEED = map(int, sys.argv[2:7]); rng = random.Random(SEED); fail = 0; done = 0; peak = 0
    while done < COUNT:
        s1 = rng.randint(0, 4); m = [rng.randint(2, C)]; s = s1 + m[0]; L = rng.randint(3, LEN)
        while len(m) < L:
            lo = max(m[-1] - 1, -s, -C); hi = min(C, SMAX - s)
            if lo > hi: break
            e = rng.randint(lo, hi) if rng.random() < .5 else (hi if len(m) < L // 2 else lo)
            m.append(e); s += e
        while m and m[-1] > -2: s -= m.pop()
        if len(m) < 3 or not legal(s1, tuple(m)): continue
        done += 1; peak = max(peak, max(s1 + sum(m[:i]) for i in range(len(m) + 1)))
        j, f, b = LINE(s1, tuple(m))
        if not j: fail += 1; print("FAIL", s1, m, flush=True)
    print(f"random middles: {COUNT}, length <= {LEN}, slack <= {SMAX} (largest seen {peak}), letters in [-{C}, {C}]: failures {fail}")
