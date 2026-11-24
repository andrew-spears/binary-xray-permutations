"""Small tests for REPORT3 (single start states t, Maya-diagram machine).
 class S B   : per slack s <= S and class K >= 0: number of states, m = s - K^2, least b from which N_0^b(t) = class for all t (b <= B).
 ones S B    : runs of 1.  T_b(t) = {u : slack s + b, D(u) = D(t), M_t <= M_u + b, N_t <= N_u + b, u != (lam | lam')}; prints sum over t of
               |N_1^b(t)|, |T_b(t)| for b = 1..B  (N <= T always, asserted).
 block S B   : block 1 0 -1 repeated; prints for b = 1..B the number of pairs (t, u) of slack s not joined by b blocks.
 sets S LEN  : F(x 0^b) for all legal prefixes x (distinct diagonals) with letters in [-1, 3], length <= LEN, slacks in [0, S]: least b with F(x 0^b) = union of the
               classes that F(x) meets, maximised over x of slack s; and whether F(x) meets every class."""
import sys, numpy as np
from maya import Maya, dval, parts
mode = sys.argv[1]; S = int(sys.argv[2]); B = int(sys.argv[3])
conj = lambda l: tuple(sum(1 for a in l if a > j) for j in range(l[0])) if l else ()
def run(Mo, S0, word):
    for e in word: S0 = {u for t in S0 for u in Mo.succ(t, e)}
    return S0
if mode == "class":
    for s in range(1, S + 1):
        Mo = Maya(s); L = Mo.states(s); ix = {t: i for i, t in enumerate(L)}; m = len(L)
        T = np.zeros((m, m), dtype=np.float32)
        for t in L:
            for u in Mo.succ(t, 0): T[ix[t], ix[u]] = 1
        K = [np.array([dval(Mo, t, 2 * s + 6 + p)[1] for t in L]) for p in (0, 1)]
        P = np.eye(m, dtype=np.float32); last = np.zeros(m, dtype=int)
        for b in range(1, B + 1):
            P = (P @ T > 0).astype(np.float32); Cl = (K[0][:, None] == K[b % 2][None, :]); assert not (P > Cl).any()
            last = np.where((P == Cl).all(axis=1), last, b + 1)
        bst = lambda k: (lambda v: str(v) if v <= B else f"not mixed at b = {B}")(int(last[K[0] == k].max()))
        print(f"s {s}: " + "  ".join(f"K = {k}: {int((K[0] == k).sum())} states, m = {s - k * k}, b* = {bst(k)}" for k in sorted(set(K[0])) if k >= 0), flush=True)
elif mode == "ones":
    for s in range(0, S + 1):
        Mo = Maya(s + B); L = Mo.states(s); out = []
        for b in range(1, B + 1):
            U = Mo.states(s + b); n0 = 2 * (s + B) + 8; lo = (1 << b) - 1; tot = [0, 0]
            dU = [(u, dval(Mo, u, n0 + b)[0], Mo.part(u[0]) == conj(Mo.part(u[1]))) for u in U]
            for t in L:
                N = run(Mo, {t}, (1,) * b); d = dval(Mo, t, n0)[0]
                Tb = {u for u, du, self in dU if du == d and not self and (t[0] & ~(u[0] << b | lo)) == 0 and (t[1] & ~(u[1] << b | lo)) == 0}
                assert N <= Tb; tot[0] += len(N); tot[1] += len(Tb)
            out.append(f"{tot[0]}/{tot[1]}")
        print(f"s {s}: sum over t of |N_1^b(t)| / |T_b(t)|, b = 1..{B}: " + " ".join(out), flush=True)
elif mode == "block":
    for s in range(1, S + 1):
        Mo = Maya(s + 1); L = Mo.states(s); cur = {t: {t} for t in L}; out = []
        for b in range(1, B + 1):
            cur = {t: run(Mo, cur[t], (1, 0, -1)) for t in L}; out.append(sum(len(L) - len(v) for v in cur.values()))
        print(f"s {s}: {len(L)} states; pairs (t, u) not joined by b blocks 1 0 -1, b = 1..{B}: {out}", flush=True)
elif mode == "sets":
    Mo = Maya(S); LEN = B; fam = {s: set() for s in range(S + 1)}; seen = {}
    def rec(F, s, k, last):                              # legal prefixes: distinct diagonals, i.e. next letter >= last - 1
        key = (frozenset(F), s, last)
        if seen.get(key, LEN + 1) <= k: return           # revisit a set only when reached by a shorter prefix
        seen[key] = k; fam[s].add(key[0])
        if k == LEN: return
        for e in range(max(-1, last - 1), 4):
            if 0 <= s + e <= S: rec(run(Mo, F, (e,)), s + e, k + 1, e)
    rec({(Mo.mask(()), Mo.mask(()))}, 0, 0, 0)
    for s in range(2, S + 1):
        L = Mo.states(s); Kc = lambda u, p: abs(dval(Mo, u, 2 * S + 6 + p)[1]); allK = {Kc(u, 0) for u in L}; worst = 0; meets = 0
        for F in fam[s]:
            ks = {Kc(u, 0) for u in F}; meets += ks == allK; sat = {u for u in L if Kc(u, 0) in ks}; cur = set(F); b = 0; first = None
            while b < 2 * s + 4:
                if cur == sat: first = b if first is None else first
                else: first = None
                cur = run(Mo, cur, (0,)); b += 1
            worst = max(worst, first)
        print(f"s {s}: {len(fam[s])} distinct F(x); F(x) meets every |K| for {meets}; least b with F(x 0^b') = all states with |K| in K(F(x)) for b' >= b: max over x = {worst}", flush=True)
elif mode == "shift":   # the sublattice translation tau_d (odd sites + 2d, even sites - 2d, applied to M(lam) and W = -holes(M(mu))) commutes with the letter 0
    d = B; W = S + 4 * abs(d) * (abs(d) + 2) + 4; Mo = Maya(W - 3); full = range(-W, W)
    def tau(bead, d):                                # bead: k -> bool on all of Z; in the moving frame the parity of a site flips with n,
        return lambda k: bead(k - 2 * d if k % 2 else k + 2 * d)      # so tau_d is used for n even and tau_{-d} for n odd
    def img(t, d=d):
        M = lambda k: k < -W or (k < W and t[0] >> (k + W) & 1); Wd = lambda k: k <= -W or (k < W and not t[1] >> (-k + W) & 1)   # W = {-j : j hole of N}
        M2, W2 = tau(M, d), tau(Wd, d)
        return (sum(1 << (k + W) for k in full if M2(k)), sum(1 << (j + W) for j in full if not W2(-j)))
    for s in range(1, S + 1):
        L = Mo.states(s); ds = {}
        for t in L:
            u = img(t); k = dval(Mo, t, 2 * W)[1]; s2 = sum(Mo.part(u[0])) + sum(Mo.part(u[1])); k2 = dval(Mo, u, 2 * W)[1]
            ds.setdefault(k, set()).add((s2 - s, k2))
            assert {img(v, -d) for v in Mo.succ(t, 0)} == set(Mo.succ(u, 0))
        print(f"s {s}, d = {d}: tau commutes with the letter 0 on all {len(L)} states; K -> (change of slack, new K): {dict(sorted((k, sorted(v)) for k, v in ds.items()))}", flush=True)
