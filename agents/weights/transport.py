"""Does the letter e lose weight on ANY set of states (not only reachable ones)?  By Hall / max-flow, w'(N_e(S)) >= c w(S)
for every set S of states of slack s (N_e = e-successors, w, w' normalised at slack s, s + e) iff there is a flow phi >= 0 on
the transitions t -> u with  sum_u phi(t, u) = c w(t)  and  sum_t phi(t, u) <= w'(u).  Prints the largest such c (LP);
c = 1 means w(F(x e)) >= w(F(x)) for every prefix x ending at slack s.
NAME = "dim-matching": uniform weights, only transitions t -> u with dim(t) = dim(u) (e = 0); c = 1 iff the letter 0 contains
a bijection of the states that preserves dim, and then a 0 loses no weight for any w that is a function of dim.
Usage: python3 transport.py DATA NAME SMAX [e ...]"""
import sys
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, vstack, hstack, csr_matrix
from essential import *
D = Data(sys.argv[1]); name = sys.argv[2]; smax = int(sys.argv[3]); letters = [int(a) for a in sys.argv[4:]] or [0]
for e in letters:
    out = []
    for s in range(max(2, 1 - e), smax + 1):
        nm = "uniform" if name == "dim-matching" else name
        w = cands(D.lev[s], s)[nm]; w = w / w.sum(); v = cands(D.lev[s + e], s + e)[nm]; v = v / v.sum()
        T = D.T(s, e).tocoo(); T.sum_duplicates()
        if name == "dim-matching":
            dm = cands(D.lev[s], s)["dim"]; keep = dm[T.row] == dm[T.col]; T = coo_matrix((T.data[keep], (T.row[keep], T.col[keep])), shape=T.shape)
        m = T.nnz; n = len(w); k = len(v)
        A_eq = hstack([coo_matrix((np.ones(m), (T.row, np.arange(m))), shape=(n, m)), csr_matrix(-w.reshape(-1, 1))])   # out-flow = c w
        A_ub = hstack([coo_matrix((np.ones(m), (T.col, np.arange(m))), shape=(k, m)), csr_matrix((k, 1))])             # in-flow <= w'
        c = np.zeros(m + 1); c[-1] = -1
        r = linprog(c, A_ub=A_ub, b_ub=v, A_eq=A_eq, b_eq=np.zeros(n), bounds=[(0, None)] * (m + 1), method="highs")
        out.append(f"{s}: {-r.fun:.4f}")
    print(f"weights '{name}', letter {e:2d}:  " + "  ".join(out), flush=True)
