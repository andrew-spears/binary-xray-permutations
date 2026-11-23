"""Zero mixing from a single state.  For every slack s <= S: T = letter-0 transition matrix on the states of slack s;
target class of t after b zeros: Cl_b(t) = {u : K_b(u) = K_0(t)}, K_m(u) = #odd(R) - #odd(C) in the picture with m + (even) stones
(zeros conserve K; as a function of the two diagrams K changes sign with the parity of the number of stones).
Prints b*(s) = least b with N_0^b'(t) = Cl_b'(t) for all t and all b' in [b, BMAX], the states attaining it, the number of classes,
and the least b with |D(u) - D(t)| <= b for all u in Cl_b(t) (the trivial lower bound).
  python3 mix.py S BMAX"""
import sys, numpy as np
from maya import Maya, dval
if __name__ == "__main__":
    S = int(sys.argv[1]); B = int(sys.argv[2])
    for s in range(1, S + 1):
        Mo = Maya(s); L = Mo.states(s); ix = {t: i for i, t in enumerate(L)}; m = len(L)
        T = np.zeros((m, m), dtype=np.float32)
        for t in L:
            for u in Mo.succ(t, 0): T[ix[t], ix[u]] = 1
        n0 = 2 * s + 6
        K = [np.array([dval(Mo, t, n0 + p)[1] for t in L]) for p in (0, 1)]
        D = [np.array([dval(Mo, t, n0 + p)[0] for t in L]) for p in (0, 1)]
        P = np.eye(m, dtype=np.float32); first = np.full(m, -1); ok = (P == (K[0][:, None] == K[0][None, :])).all(axis=1); first[ok] = 0; triv = 0   # b = 0: singleton classes
        for b in range(1, B + 1):
            P = (P @ T > 0).astype(np.float32)
            Cl = (K[0][:, None] == K[b % 2][None, :])
            assert not (P > Cl).any()
            eq = (P == Cl).all(axis=1)
            first = np.where(eq & ~ok, b, first); ok = eq
            if (np.abs(D[0][:, None] - D[b % 2][None, :]) > b)[Cl].any(): triv = b + 1
        if not ok.all(): print(f"s {s}: {int((~ok).sum())} of {m} states not mixed at b = {B}: {' '.join(Mo.name(L[i]) for i in np.where(~ok)[0][:8])}", flush=True); continue
        bs = int(first.max()); w = [Mo.name(L[i]) for i in np.where(first == bs)[0]]
        print(f"s {s}: {m} states, {len(set(K[0]))} classes (K = {min(K[0])}..{max(K[0])}); b*(s) = {bs}, attained by {len(w)} states: {' '.join(w[:8])}; "
              f"D-distance bound {triv}; histogram of first b {dict(zip(*map(lambda a: a.tolist(), np.unique(first, return_counts=True))))}", flush=True)
