"""Count test mod m (necessary for a state to be reachable; trivial proof: sort the stones by (row mod m, column mod m)).
A state (rows R, columns C) with diagonals D passes if there are numbers n[i][j] >= 0 (i, j residues mod m) with
  sum_j n[i][j] = #{r in R: r = i},  sum_i n[i][j] = #{c in C: c = j},  sum_{i+j=t} n[i][j] = #{d in D: d = t}  (mod m).
m = 2 is the parity count already in the repo.  This script finds, for each state missing in the counterexamples to
ZERO, PEAK and RUN, the moduli m <= 12 whose count test excludes it (integer table search, exact)."""
import sys
from lib import *
def table_exists(m, rho, kap, sig):
    cells = [(i, j) for i in range(m) for j in range(m)]
    rho, kap, sig = list(rho), list(kap), list(sig)
    def rec(idx):
        if idx == len(cells): return not any(rho) and not any(kap) and not any(sig)
        i, j = cells[idx]; t = (i + j) % m
        last_in_row = j == m - 1
        hi = min(rho[i], kap[j], sig[t])
        for v in ([rho[i]] if last_in_row else range(hi, -1, -1)):
            if v > hi: return False
            rho[i] -= v; kap[j] -= v; sig[t] -= v
            ok = rec(idx + 1)
            rho[i] += v; kap[j] += v; sig[t] += v
            if ok: return True
        return False
    return rec(0)
def count_test(m, R, C, D):
    cnt = lambda X: [sum(1 for x in X if x % m == i) for i in range(m)]
    return table_exists(m, cnt(R), cnt(C), cnt(D))
def failing_moduli(R, C, D, mmax=12): return [m for m in range(2, mmax + 1) if not count_test(m, R, C, D)]
def missing(x, u, v):
    d = len(v) - len(u); X = F(sums_of(x + u)); Y = F(sums_of(x + v)); out = []
    for t in X:
        for _ in range(d): t = Sh(t)
        if t not in Y: out.append((bits(t[0]), bits(t[1])))
    return out, sums_of(x + v)
if __name__ == "__main__":
    for name, x, u, v in [("ZERO", (2,3,3,2,2,1,1,0), (-1,), (0,-1)), ("ZERO", (2,5,4,3,2,1,0), (-1,), (0,-1)),
                          ("PEAK", (3,4,3,3,2,1), (0,), (1,0,-1)), ("RUN(2,1)", (4,3,2,1), (1,1,0), (2,1,0,-1)),
                          ("RUN(3,1)", (5,4,3,2,1), (2,2,1,0), (3,2,1,0,-1))]:
        ms, D = missing(x, u, v)
        print(f"{name}, x = {x}: diagonals of x v = {D}, {len(ms)} missing states")
        for R, C in ms: print(f"    rows {R} cols {C}: excluded by the count mod m for m in {failing_moduli(R, C, D)}")
