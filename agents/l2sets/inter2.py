"""Intersections I(s, l) of F(x) over all prefixes x with letters in [-C, C] (distinct diagonals), slacks <= S, ending in the letter l at slack s.
Prints sizes, the states for small sets, and whether the hooks (s|-), (-|s), (1^s|-), (-|1^s) and G(s) n conj G(s) meet I(s, l).
  python3 inter2.py C S"""
import sys
from fx2 import *
import l1
tol1 = lambda t: (Mo.part(t[0]), l1.conj(Mo.part(t[1])))
U = [[tol1(t) for t in L] for L in St]
inG = lambda u: u == ((), ()) if l1.slack(u) == 0 else (l1.central(u) and not l1.in_T(u))
GG = [sum(1 << i for i, u in enumerate(L) if inG(u) and inG((l1.conj(u[0]), l1.conj(u[1])))) for L in U]
I = {}; seen = set(); stack = [(1, 0, None)]
while stack:
    F, s, l = stack.pop()
    if (F, s, l) in seen: continue
    seen.add((F, s, l)); I[s, l] = I.get((s, l), full[s]) & F
    for e in LET:
        if 0 <= s + e <= S and (l is None or e >= l - 1): stack.append((step(F, s, e), s + e, e))
for l in LET:
    print(f"last letter {l}:")
    for s in range(S + 1):
        if (s, l) not in I: continue
        A = I[s, l]; hooks = [nm for nm, u in (("(s|-)", ((s,), ())), ("(-|s)", ((), (1,) * s)), ("(1^s|-)", ((1,) * s, ())), ("(-|1^s)", ((), (s,)))) if s and A >> U[s].index(u) & 1]
        print(f"   s {s}: |I| = {cnt(A)} of {len(St[s])}; in G n conj G: {cnt(A & GG[s])}; hooks in I: {' '.join(hooks)}" + (f"; I = {names(A, s)}" if cnt(A) <= 12 else ""))
