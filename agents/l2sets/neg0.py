"""Task 0: words with all letters <= 1 (next letter >= last - 1).  Family: G(s) = Central minus T after a last letter 0 / 1, G-(s) = Central minus U after a negative letter.
 check S      : (bitsets, slack <= S)  G-(s) = Central(s) n step_-1(G(s+1));  G-(s) inside step_-k(G-(s+k)) for k = 2..S-s;  G(s) inside step_-k(G(s+k)) fails only for k = 2, 4 | s+2... (printed);
                general predecessor counts for the letters -1..-6 on all states of slack <= min(S, 9).
 all N        : the algorithm on every valid word of length <= N with letters <= 1.
 random C LEN : random valid words with deep negative letters.
  python3 neg0.py check 13 | all 11 | random 200 300"""
import sys, itertools, random
sys.path.insert(0, "../l1sets"); sys.path.insert(0, "../weights")
import l1
l1.depth = lambda u: len(u[0]) + len(u[1]) + 6 + DEEP        # l1.preds / succs look DEEP + 6 places below the diagrams: enough for letters >= -DEEP
DEEP = 40
def in_U(u):
    s = l1.slack(u)
    if s == 0 or s % 4: return False
    m = l1.isqrt(s // 4)
    if 4 * m * m != s: return False
    if m not in l1._A: l1._A[m] = l1.A_set(m)
    return all(t in l1._A[m] for k, t in l1.preds(u, -1))
def in_G(u): return u == ((), ()) if l1.slack(u) == 0 else (l1.central(u) and not l1.in_T(u))
def in_Gm(u): return l1.central(u) and not in_U(u)
def half(w, u, rng=None):
    """stones of a prefix w (letters <= 1) ending in the state u; backwards, predecessors in G / G- by the previous letter"""
    stones = []
    for N in range(len(w), 0, -1):
        e = w[N - 1]; fam = in_Gm if N > 1 and w[N - 2] < 0 else in_G
        cand = [(k, t) for k, t in l1.preds(u, e) if fam(t)]
        assert cand, ("step fails", w, N, u)
        k, t = rng.choice(cand) if rng else cand[0]
        r = N + k + 1; stones.append((r, 2 * N + e - r)); u = t
    assert u == ((), ())
    return stones
def verify(w, stones):
    n = len(w)
    assert sorted(r for r, c in stones) == list(range(1, n + 1)) == sorted(c for r, c in stones), (w, stones)
    assert sorted(r + c for r, c in stones) == sorted(2 * k + x for k, x in enumerate(w, 1)), (w, stones)
def solve(w, rng=None):
    """w valid, all letters <= 1"""
    st = half(w, ((), ()), rng); verify(w, st); return st
def solve_split(w, rng=None):
    """w valid, no letter >= 2 before a letter <= -2: cut before the first letter >= 2, cut state (s | -)"""
    m = next((i for i, e in enumerate(w) if e >= 2), len(w)); x, y = w[:m], w[m:]; s = sum(x); n = len(w)
    assert all(e >= -1 for e in y)
    if not y: return solve(w, rng)
    z = tuple(-e for e in reversed(y))
    st = half(x, ((s,), ()), rng) if s else half(x, ((), ()), rng)
    st2 = half(z, ((1,) * s, ()), rng)
    st = st + [(n + 1 - r, n + 1 - c) for r, c in st2]; verify(w, st); return st
if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "all":
        N = int(sys.argv[2]); cnt = [0] * (N + 1); deep = [0] * (N + 1)
        def rec(w, s):
            if s == 0 and w: solve(w); cnt[len(w)] += 1; deep[len(w)] += min(w) <= -2
            if len(w) == N: return
            for e in range((w[-1] - 1) if w else -1, 2):
                if s + e >= 0 and N - len(w) - 1 >= 0: rec(w + (e,), s + e)
        rec((), 0)
        for n in range(1, N + 1): print(f"n {n}: {cnt[n]} valid words with letters <= 1 solved ({deep[n]} with a letter <= -2)", flush=True)
    elif mode == "hooks":
        S = int(sys.argv[2])
        assert all(in_G(((s,), ())) and in_G(((1,) * s, ())) for s in range(1, S + 1))
        print(f"(s | -) and (1^s | -) are in G(s) for 1 <= s <= {S}")
    elif mode == "split":
        N = int(sys.argv[2]); cnt = [0] * (N + 1); big = [0] * (N + 1)
        def rec(w, s, seen2):
            if s == 0 and w: solve_split(w); cnt[len(w)] += 1; big[len(w)] += max(w) >= 2 and min(w) <= -2
            if len(w) == N: return
            L = N - len(w) - 1                                          # letters left after this one; they are >= e - 1, e - 2, ...
            for e in range(max((w[-1] - 1) if w else -N, -s), 2 * N):
                if s + e + L * e - L * (L + 1) // 2 > 0: break
                if e <= -2 and seen2: continue
                rec(w + (e,), s + e, seen2 or e >= 2)
        rec((), 0, False)
        for n in range(1, N + 1): print(f"n {n}: {cnt[n]} valid words with no letter >= 2 before a letter <= -2 solved ({big[n]} of them with letters >= 2 and <= -2)", flush=True)
    elif mode == "splitrandom":
        C, LEN = int(sys.argv[2]), int(sys.argv[3]); rng = random.Random(9); mx = hi = lo = 0
        for it in range(C):
            w = []; s = 0
            while len(w) < LEN or s > 0 or len(w) < 2 * LEN:            # first part: letters <= 1; second part: letters >= -1
                first = len(w) < LEN; low = (w[-1] - 1) if w else -1
                if first: e = rng.choice((1, 1, 1, 0, 0, -1, -2, -3, -5))
                elif len(w) < 2 * LEN: e = rng.choice((-1, -1, -1, 0, 0, 1, 2, 3, 5))
                else: e = -1
                e = max(e, low, -s); e = min(e, 1) if first else max(e, -1)
                if not first and e < -1: e = -1
                if s + e < 0: e = 0 if low <= 0 else low
                w.append(e); s += e
                if len(w) >= 2 * LEN and s == 0: break
            solve_split(tuple(w), rng); mx = max(mx, max(itertools.accumulate(w))); hi = max(hi, max(w)); lo = min(lo, min(w))
        print(f"{C} random valid words (letters <= 1, then letters >= -1), length >= {2 * LEN}: all solved; largest slack {mx}, letters from {lo} to {hi}")
    elif mode == "random":
        C, LEN = int(sys.argv[2]), int(sys.argv[3]); rng = random.Random(5); mx = mn = 0
        for it in range(C):
            w = []; s = 0; up = rng.choice((0.5, 0.7, 0.9))
            while len(w) < LEN or s > 0:
                lo = (w[-1] - 1) if w else -1
                if len(w) < LEN and rng.random() < up: e = rng.choice((1, 1, 0))
                else: e = rng.randint(max(lo, -s), min(1, max(lo, -s) + 2)) if max(lo, -s) <= 1 else 1
                e = max(e, lo, -s); e = min(e, 1); w.append(e); s += e
            solve(tuple(w), rng); mx = max(mx, max(itertools.accumulate(w))); mn = min(mn, min(w))
        print(f"{C} random valid words with letters <= 1, length >= {LEN}: all solved; largest slack {mx}, lowest letter {mn}")
    else:
        S = int(sys.argv[2]); sys.argv = [sys.argv[0], "1", str(S)]
        from maya import Maya
        Mo = Maya(S + 1); St = [Mo.states(s) for s in range(S + 1)]; ix = [{t: i for i, t in enumerate(L)} for L in St]
        U = [[(Mo.part(t[0]), l1.conj(Mo.part(t[1]))) for t in L] for L in St]
        def step(A, s, e):
            out = 0
            for i, t in enumerate(St[s]):
                if A >> i & 1:
                    for v in Mo.succ(t, e): out |= 1 << ix[s + e][v]
            return out
        cen = [sum(1 << i for i, u in enumerate(L) if l1.central(u)) for L in U]
        G = [sum(1 << i for i, u in enumerate(L) if in_G(u)) for L in U]; Gm = [sum(1 << i for i, u in enumerate(L) if in_Gm(u)) for L in U]
        cnt = lambda A: bin(A).count("1"); bad = []
        for s in range(S):
            assert Gm[s] == cen[s] & step(G[s + 1], s + 1, -1), s
            for k in range(2, S - s + 1):
                A = G[s + k]; B = Gm[s + k]
                for e in range(-1, -k - 1, -1): pass
                def down(A0):
                    return step2(A0, s + k, -k)
                # one letter -k from slack s + k
                img = 0
                for i, t in enumerate(St[s + k]):
                    if B >> i & 1:
                        for v in l1.succs(U[s + k][i], -k): img |= 1 << ix[s][(Mo.mask(v[1][0]), Mo.mask(l1.conj(v[1][1])))]
                assert Gm[s] & ~img == 0, (s, k)
                imgG = 0
                for i, t in enumerate(St[s + k]):
                    if A >> i & 1:
                        for v in l1.succs(U[s + k][i], -k): imgG |= 1 << ix[s][(Mo.mask(v[1][0]), Mo.mask(l1.conj(v[1][1])))]
                if G[s] & ~imgG: bad.append((s + k, k, cnt(G[s] & ~imgG)))
        print(f"slack <= {S}: G-(s) = Central(s) n step_-1(G(s+1)) for all s; G-(s) inside step_-k(G-(s+k)) for all k >= 2; |Central minus G-| = {[cnt(cen[s] & ~Gm[s]) for s in range(S + 1)]}")
        print(f"G(s-k) not inside step_-k(G(s)) at (s, k, missing): {bad}")
        tot = 0
        for s in range(1, min(S, 9) + 1):
            for u in U[s]:
                a, b = l1.c0(u[0]), l1.c0(u[1]); c = a + b
                for e in range(-6, 3):
                    pr = l1.preds(u, e); ev = [t for k, t in pr if k % 2 == 0]; od = [t for k, t in pr if k % 2]; f = e // 2
                    if e % 2 == 0: assert len(ev) >= c - f and len(od) >= 1 - c - f and all(l1.cls(t) == 2 - c for t in ev) and all(l1.cls(t) == -c for t in od)
                    else: assert len(ev) >= a - b - f and len(od) >= b - a - f and all(l1.cls(t) == 1 - c for k, t in pr)
                    assert sum(1 for k, t in pr if l1.is_E0(t)) <= 1; tot += 1
        print(f"predecessor counts and classes for the letters -6..2, and 'at most one predecessor in E0': ok on {tot} (state, letter) pairs, slack <= {min(S, 9)}")
