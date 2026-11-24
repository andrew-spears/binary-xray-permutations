# The two-chain machine, in the form 'numbers owed' (the same machine as agents/blocks/m2.py: lam = column lengths
# of P, mu = row lengths of Q).  Checked against complete search by two_check.py.
# State (lam, mu): the stones of chain A / chain B that still owe
# incomparable later stones of the other chain, each with the number owed (weakly increasing in time, kept sorted).
# Step with letter e and colour A: phi = e + len(mu) must be >= max(lam) (and >= 0); every part of mu drops by 1;
# phi joins lam.  Colour B: the same with lam and mu exchanged.  Start and end: (empty, empty).
import sys
from lib import *
def step(st, e):
    lam, mu = st; out = []
    for sw in (0, 1):
        l, m = (lam, mu) if sw == 0 else (mu, lam)
        phi = e + len(m)
        if phi < (l[-1] if l else 0): continue
        m2 = tuple(x - 1 for x in m if x > 1); l2 = l + (phi,) if phi > 0 else l
        out.append(((l2, m2) if sw == 0 else (m2, l2), "AB"[sw]))
    return out
def runs(e):
    """all accepted colour words"""
    out = []
    def rec(i, st, c):
        if i == len(e):
            if st == ((), ()): out.append(c)
            return
        for s2, col in step(st, e[i]): rec(i + 1, s2, c + col)
    rec(0, ((), ()), ""); return out
def accepts(e):
    S = {((), ())}
    for x in e:
        S = {s2 for st in S for s2, _ in step(st, x)}
        if not S: return False
    return ((), ()) in S
