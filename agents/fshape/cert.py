"""Smallest integer Farkas certificate that a state (A, B) has no fractional placement of the sums T:
weights u_r, v_c, w_t with u_r + v_c + w_{r+c} <= 0 on every cell with r + c in T, and total weight >= 1."""
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from core import bits
def cert(A, B, T, W=3):
    R, C = bits(A), bits(B); T = list(T); n = len(T); N = 3 * n
    idx = {("r", r): i for i, r in enumerate(R)}; idx.update({("c", c): n + i for i, c in enumerate(C)}); idx.update({("t", t): 2 * n + i for i, t in enumerate(T)})
    rows = []
    for r in R:
        for c in C:
            if r + c in T:
                row = np.zeros(2 * N); 
                for key in (("r", r), ("c", c), ("t", r + c)): row[idx[key]] = 1; row[N + idx[key]] = -1
                rows.append(row)
    tot = np.concatenate([np.ones(N), -np.ones(N)])
    cons = [LinearConstraint(np.array(rows), -np.inf, 0), LinearConstraint(tot[None, :], 1, np.inf)]
    res = milp(np.ones(2 * N), constraints=cons, integrality=np.ones(2 * N), bounds=Bounds(0, W))
    if res.status != 0: return None
    z = np.round(res.x[:N] - res.x[N:]).astype(int)
    return {"rows": dict(zip(R, z[:n])), "cols": dict(zip(C, z[n:2 * n])), "sums": dict(zip(T, z[2 * n:]))}
def fmt(c): return "  ".join(f"{k}: " + " ".join(f"{a}:{int(b):+d}" for a, b in v.items() if b) for k, v in c.items())
if __name__ == "__main__":
    from core import mask
    for A, B, T in [((1, 2, 3, 4, 6, 7, 8, 9), (1, 2, 3, 4, 7, 8, 9, 10), (6, 7, 8, 9, 12, 13, 14, 15)),
                    ((1, 2, 3, 4, 5, 8, 9, 10, 11), (1, 2, 3, 4, 5, 7, 8, 9, 10), (6, 7, 8, 9, 10, 14, 15, 16, 17)),
                    ((1, 2, 3, 4, 5, 6, 7, 8, 10, 13), (1, 2, 3, 4, 5, 7, 8, 10, 11, 13), (4, 7, 9, 10, 12, 13, 15, 16, 18, 19))]:
        print(A, B, T); print("   ", fmt(cert(mask(A), mask(B), T)))
