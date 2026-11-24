"""More on zero runs from single states.  For slack s <= S and b <= B prints
 exc(b)  = number of pairs (t, u) with K right and containment M_t <= M_u + b, N_t <= N_u + b but u not in N_0^b(t);
 mono(b) = number of pairs with u in N_0^b(t) but not in N_0^(b+2)(t);  and the least b0 with mono(b) = 0 for all b >= b0.
  python3 mix2.py S B"""
import sys, numpy as np
from maya import Maya, dval
if __name__ == "__main__":
    S = int(sys.argv[1]); B = int(sys.argv[2])
    for s in range(1, S + 1):
        Mo = Maya(s + B // 2 + 2); L = Mo.states(s); ix = {t: i for i, t in enumerate(L)}; m = len(L); W = Mo.W
        T = np.zeros((m, m), dtype=np.float32)
        for t in L:
            for u in Mo.succ(t, 0): T[ix[t], ix[u]] = 1
        K = [np.array([dval(Mo, t, 2 * W + p)[1] for t in L]) for p in (0, 1)]
        P = [np.eye(m, dtype=np.float32)]
        for b in range(1, B + 3): P.append((P[-1] @ T > 0).astype(np.float32))
        exc = []; mono = []
        for b in range(1, B + 1):
            Cl = (K[0][:, None] == K[b % 2][None, :]); lo = (1 << b) - 1
            cont = np.array([[(t[0] & ~(u[0] << b | lo)) == 0 and (t[1] & ~(u[1] << b | lo)) == 0 for u in L] for t in L])
            assert not (P[b] > (Cl & cont)).any(), (s, b)
            exc.append(int((Cl & cont).sum() - P[b].sum())); mono.append(int((P[b] > P[b + 2]).sum()))
        b0 = max([b + 1 for b in range(1, B + 1) if mono[b - 1]] or [1])
        print(f"s {s}: exc(b), b = 1..{B}: {exc}\n      mono(b): {mono}   monotone from b0 = {b0}", flush=True)
