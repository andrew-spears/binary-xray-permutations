"""Unreachable states of legal prefixes that pass the plain LP, or even the parity test (card `parity`).  A few seconds."""
from core import *
from lp import lp, plp
from counts import count_ok
for x, A, B in [((2, 1, 1, 1, 1, 0), (1, 2, 3, 4, 5, 8), (1, 2, 4, 5, 6, 7)),          # first LP survivor (slack 6)
                ((1, 1, 1, 0, 1, 2, 2), (1, 2, 3, 4, 5, 6, 8), (1, 2, 3, 4, 7, 8, 10)),  # first parity-test survivor (slack 8)
                ((2, 2, 1, 2, 3, 3), (1, 3, 4, 5, 6, 8), (1, 2, 3, 6, 7, 9))]:           # a shorter one (slack 13)
    T = sums(x); a = (mask(A), mask(B))
    print(f"x = {x}, sums {T}, rows {A}, columns {B}: reachable {a in Fx(x)}, plain LP {lp(*a, T)}, parity test {plp(*a, T, 2)}, "
          f"mod-4 test {plp(*a, T, 4)}, mod-3 test {plp(*a, T, 3)}, residue counts fail mod {[m for m in range(2, 12) if not count_ok(*a, T, m)]}")
