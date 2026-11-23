"""Proposition C: the two core pairs (d_a|d_{a+1}), (d_{a+1}|d_a) (d_a = staircase a, a-1, ..., 1; slack (a+1)^2) are each other's only 0-predecessor and have no 2-predecessor.
Consequence shown: two old prefixes with the same slack 11 and the same last letters 2 0 0 0 with different missing parts of G(11)."""
from oh import *
setup(13)
st = lambda a: tuple(range(a, 0, -1))
for a in range(0, 7):
    u, v = (st(a), st(a + 1)), (st(a + 1), st(a))
    assert [t for k, t in preds(u, 0)] == [v] and [t for k, t in preds(v, 0)] == [u] and not preds(u, 2) and not preds(v, 2) and central(u)
print("Proposition C checked for a <= 6")
def F(w):
    S = frozenset([((), ())])
    for e in w: S = step(S, e)
    return S
G = lambda s: frozenset(u for u in states(s) if inG(u))
for w in [(1,) * 7 + (2, 0, 0, 0), (1,) * 7 + (2, 0, 0, 2, 0, 0, 0), (1,) * 9 + (2, 0, 0, 0), (1,) * 9 + (2, 0, 0, 0, 0, 0, 0), (1,) * 7 + (2, 0, 0, 2, 0, 0, 0, 0, 0, 0)]:
    s = sum(w); D = G(s) - F(w)
    print(" ".join(map(str, w)), ": slack", s, "G(s) - F:", len(D), " ".join(sorted(nm(u) for u in D)))
u = ((2,), (1,))
print("0-predecessors of 2|1:", [nm(t) for k, t in preds(u, 0)], " in G(3):", inG(u), " 2|1 in F(2 1 0 0):", u in F((2, 1, 0, 0)), " 3|- in F(2 1 0):", ((3,), ()) in F((2, 1, 0)),
      " -|21 in F(2 1 0):", ((), (2, 1)) in F((2, 1, 0)), " -|21 central:", central(((), (2, 1))))
u = ((10,), (1,))
print("0-predecessors of 10|1:", [(nm(t), "central" if central(t) else "level 2") for k, t in preds(u, 0)])
