"""The failures of ZERO and RUN(2,1) at slack 14, in absolute coordinates."""
from core import *
def show(name, x, u, v):
    c = len(v) - len(u)
    Fu = Fx(x + u); Fv = Fx(x + v)
    miss = [a for a in Fu if (sh(a[0], c), sh(a[1], c)) not in Fv]
    print(f"{name}: x = {x}, slack {sum(x)};  |F(xu)| = {len(Fu)}, |F(xv)| = {len(Fv)}, missing {len(miss)}")
    print("   sums of x u:", sums(x + u)); print("   sums of x v:", sums(x + v))
    for a in miss: print("   state (rows, cols) of x u:", bits(a[0]), bits(a[1]), " partitions", part(a[0], len(x + u)), part(a[1], len(x + u)))
    return miss
if __name__ == "__main__":
    show("ZERO", (2, 3, 3, 2, 2, 1, 1, 0), (-1,), (0, -1))
    show("RUN(2,1)", (4, 3, 2, 1), (1, 1, 0), (2, 1, 0, -1))
    show("RUN(2,1)", (4, 3, 2, 1, 0), (1, 1, 0), (2, 1, 0, -1))
