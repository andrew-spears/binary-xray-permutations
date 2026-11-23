"""The repair statement (X) after one letter 2, and its analogues after a high block.
(X): for z = 1^j 0 y e, j >= 1, y in {0,1}*:   G(s) (e = 0, 1) resp. G-(s) (e = -1) is inside step_z(step_2(G(s0))).
  python3 exit.py all S0 L SMAX      every s0 <= S0, every 1^j 0 y with at most L letters, slacks <= SMAX (forward sets)
  python3 exit.py true SMAX          G(s) minus F(x 2 z) for explicit prefixes x, against the sets computed from G(s0)
  python3 exit.py random N SLACK     N random targets of slack about SLACK: backward search for a chain through e, y, 0, 1^j, 2 into G(s0)
  python3 exit.py block SMAX         the same after the high blocks 3 2, 4 3 2, 2 2, 2 1 2"""
import sys, itertools, random
from oh import *
mode = sys.argv[1]
def tails(L):
    for n in range(L):
        for y in itertools.product((0, 1), repeat=n):
            if 0 in y: yield (1,) + y                                   # z' = 1 ... containing a zero; the exit letter is appended after a zero or anywhere
if mode == "all":
    S0, L, SM = map(int, sys.argv[2:5]); setup(SM + 2); res = {}
    for s0 in range(S0 + 1):
        J0 = step(G(s0), 2)
        for n in range(1, L + 1):
            for y in itertools.product((0, 1), repeat=n - 1):
                z = (1,) + y
                if 0 not in z or s0 + 2 + sum(z) > SM: continue
                J = run(J0, z); s = s0 + 2 + sum(z); first = z.index(0) == len(z) - 1          # first: z = 1^j 0
                for e, fam in ((0, G), (1, G), (-1, Gm)):
                    if e == -1 and z[-1] != 0 or s + e > SM: continue
                    miss = fam(s + e) - step(J, e)
                    key = (e, "s0 >= 3" if s0 >= 3 else "s0 <= 2"); r = res.setdefault(key, [0, 0, []]); r[0] += 1
                    if miss: r[1] += 1; r[2].append((s0, " ".join(map(str, z + (e,))), sorted(map(nm, miss))))
    for (e, grp), r in sorted(res.items()):
        print(f"e = {e:2d}, {grp}: {r[0]} words 2 1^j 0 y e (slack <= {SM}), {r[1]} with a state of {'G-' if e < 0 else 'G'} missing")
        for f in r[2][:12]: print("      s0 =", f[0], " after 2", f[1], " missing", " ".join(f[2]))
elif mode == "true":
    SM = int(sys.argv[2]); setup(SM + 2); n = bad = 0
    for x in ((), (1, 1, 1), (1, 1, 1, 0), (1, 1, 1, 1, 0, -1), (1, 0, 1, 1), (1, 1, 1, 1, 1, 0, -1, -2), (0, 0, 1, 1, 1, 1), (1, 1, 1, 1, 1), (1, 1, 0, 0, 1, 1, 1)):
        s0 = sum(x); Fx = run(frozenset([((), ())]), x); assert G(s0) <= Fx
        F2, J2 = step(Fx, 2), step(G(s0), 2); out = []
        for z in ((), (1,), (1, 1), (1, 1, 1), (1, 0), (1, 1, 0), (1, 1, 1, 0), (1, 0, 0), (1, 1, 0, 1), (1, 0, -1), (1, 1, 0, -1)):
            s = s0 + 2 + sum(z)
            if s > SM: continue
            a, b = G(s) - run(F2, z), G(s) - run(J2, z); n += 1; bad += a != b
            out.append(f"{' '.join(map(str, z)) or '(none)'}: {len(a)}" + ("" if a == b else f" (from G(s0) alone: {len(b)})"))
        print(f"x = {' '.join(map(str, x)) or '(empty)'}, s0 = {s0}, |F(x)| = {len(Fx)}, |G(s0)| = {len(G(s0))}.  |G(s) minus F(x 2 z)| for z = " + "; ".join(out))
    print(f"{n} prefixes x 2 z: the missing part of G(s) differs from the one computed from G(s0) in {bad} cases")
elif mode == "random":
    N, SL = int(sys.argv[2]), int(sys.argv[3]); setup(SL + 20); rng = random.Random(1); done = fail = 0; sys.setrecursionlimit(10000)
    def rpart(n):
        p = []
        while n: k = rng.randint(1, max(1, min(n, rng.choice((2, 3, 5, 8, n))))); p.append(k); n -= k
        return tuple(sorted(p, reverse=True))
    def search(u, back, dead):
        if not back: return inG(u)
        if (u, len(back)) in dead: return False
        pr = list(preds(u, back[0])); rng.shuffle(pr)
        for k, t in pr:
            if search(t, back[1:], dead): return True
        dead.add((u, len(back))); return False
    while done < N:
        e = rng.choice((-1, -1, 0, 1)); j = rng.randint(1, 5); y = tuple(rng.randint(0, 1) for _ in range(rng.randint(0, 6)))
        z = (1,) * j + (0,) + y
        if e == -1 and z[-1] != 0: z += (0,)
        s = SL + rng.randint(-6, 6); s0 = s - e - sum(z) - 2
        if s0 < 3: continue
        a = rng.randint(0, s); u = (rpart(a), rpart(s - a))
        if not (inGm(u) if e < 0 else inG(u)): continue
        done += 1
        if not search(u, (e,) + tuple(reversed(z)) + (2,), set()): fail += 1; print("NO CHAIN:", nm(u), "after 2", z, e, "s0 =", s0)
    print(f"{N} random targets (slack {SL - 6}..{SL + 6}, s0 >= 3, j <= 5, up to 6 more letters 0/1): {fail} without a chain into G(s0)")
elif mode == "block":
    SM = int(sys.argv[2]); setup(SM + 2)
    for blk in ((3, 2), (4, 3, 2), (2, 2), (2, 1, 2), (3, 2, 1, 2)):
        res = {}
        for s0 in range(3, SM):
            if s0 + sum(blk) > SM: continue
            J0 = run(G(s0), blk)
            for j in range(1, 6):
                s = s0 + sum(blk) + j
                if s > SM: break
                J = run(J0, (1,) * j); r = res.setdefault("1^j", [0, 0, 0]); m = G(s) - J; r[0] += 1; r[1] += bool(m); r[2] = max(r[2], len(m))
                Jz = step(J, 0); r = res.setdefault("1^j 0", [0, 0, 0]); m = G(s) - Jz; r[0] += 1; r[1] += bool(m); r[2] = max(r[2], len(m))
                for e, fam in ((0, G), (1, G), (-1, Gm)):
                    if s + e > SM: continue
                    r = res.setdefault(f"1^j 0 {e}", [0, 0, 0]); m = fam(s + e) - step(Jz, e); r[0] += 1; r[1] += bool(m); r[2] = max(r[2], len(m))
                    for e2, fam2 in ((0, G), (1, G), (-1, Gm)):
                        if e2 == -1 and e == 1 or not 0 <= s + e + e2 <= SM: continue
                        r = res.setdefault(f"1^j 0 {e} {e2}", [0, 0, 0]); m = fam2(s + e + e2) - run(Jz, (e, e2)); r[0] += 1; r[1] += bool(m); r[2] = max(r[2], len(m))
        print("block", " ".join(map(str, blk)), "(s0 >= 3, slack <= %d):" % SM, "; ".join(f"after {k}: {v[1]} of {v[0]} incomplete (largest missing {v[2]})" for k, v in res.items()))
if mode == "thin":                                              # python3 exit.py thin SLACK : all targets with <= 1 and <= 2 part sizes (thin shapes: hooks, rectangles, fat hooks)
    SL = int(sys.argv[2]); setup(SL + 8); sys.setrecursionlimit(10000); n = fail = 0
    def two(n_, k):
        out = set()
        for a in range(1, n_ + 1):
            for i in range(1, n_ // a + 1):
                r = n_ - a * i
                if r == 0: out.add((a,) * i)
                elif k == 2:
                    for b in range(1, a):
                        if r % b == 0: out.add((a,) * i + (b,) * (r // b))
        return out if n_ else {()}
    def search(u, back, dead):
        if not back: return inG(u)
        if (u, len(back)) in dead: return False
        for k, t in preds(u, back[0]):
            if search(t, back[1:], dead): return True
        dead.add((u, len(back))); return False
    for s in range(SL - 1, SL + 1):
        targets = {(l, m) for a in range(s + 1) for k1, k2 in ((1, 2), (2, 1)) for l in two(a, k1) for m in two(s - a, k2)}
        for j in (1, 2, 4):
            for e in (-1, 0, 1):
                dead = set()
                for u in targets:
                    if not (inGm(u) if e < 0 else inG(u)): continue
                    n += 1
                    if not search(u, (e, 0) + (1,) * j + (2,), dead): fail += 1; print("NO CHAIN:", nm(u), "after 2 1^%d 0 %d" % (j, e))
    print(f"{n} (target, word) pairs: every target of slack {SL - 1}, {SL} in G (G- for e = -1) with at most 1 and 2 part sizes, words 2 1^j 0 e, j = 1, 2, 4: {fail} without a chain into G(s0)")
if mode == "ones":                                              # python3 exit.py ones SMAX : G(s) minus step_{2 1^j [0]}(G(s0)), hooks apart
    SM = int(sys.argv[2]); setup(SM + 2)
    hk = lambda s: {((s,), ()), ((), (s,)), ((1,) * s, ()), ((), (1,) * s)}
    print("number of states of G(s) missing after 2 1^j from G(s0), written  hooks + others ;  after 2 1^j 0 in brackets")
    for s0 in range(0, SM - 3):
        J = step(G(s0), 2); row = []
        for j in range(1, 7):
            s = s0 + 2 + j
            if s > SM: break
            J = step(J, 1); m = G(s) - J; m0 = G(s) - step(J, 0)
            row.append(f"j={j}: {len(m & hk(s))}+{len(m - hk(s))} [{len(m0 & hk(s))}+{len(m0 - hk(s))}]")
        print(f"  s0 = {s0}: " + "  ".join(row))
