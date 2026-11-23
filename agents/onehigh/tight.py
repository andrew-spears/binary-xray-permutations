"""Proved statements of REPORT.md section 1, re-checked on all states of slack <= S (default 12).
2-quotient: M0 = {k/2 : k in M even}, M1 = {(k-1)/2 : k in M odd}, same for B.   python3 tight.py [S]"""
import sys
from oh import *
S = int(sys.argv[1]) if len(sys.argv) > 1 else 12; setup(S + 3)
q = lambda X: ({k // 2 for k in X if k % 2 == 0 and k > -W + 12}, {(k - 1) // 2 for k in X if k % 2 and k > -W + 12})
lo = -W // 2 + 8
sub = lambda X, Y: all(x in Y for x in X if x > lo)                      # inclusion away from the window bottom
eq = lambda X, Y: sub(X, Y) and sub(Y, X)
sh = lambda X, d: {x + d for x in X}
level = lambda u: max(cls(u), 1 - cls(u))
bad = []; n = 0
for s in range(S + 1):
    for u in states(s):
        M, B = MB(u); (M0, M1), (B0, B1) = q(M), q(B); c = cls(u); n += 1
        for e in (-1, 0, 1, 2):                                          # predecessors with k even / odd  <->  M0 minus (shifted B_q), M1 minus (...)
            ev = sorted(k // 2 for k, t in preds(u, e) if k % 2 == 0); od = sorted((k - 1) // 2 for k, t in preds(u, e) if k % 2)
            Ye, Yo = {0: (B1, sh(B0, -1)), 1: (B0, B1), 2: (sh(B1, 1), B0), -1: (sh(B0, -1), sh(B1, -1))}[e]
            if [i for i in ev if i > lo] != sorted(i for i in M0 if i not in Ye and i > lo) or [i for i in od if i > lo] != sorted(i for i in M1 if i not in Yo and i > lo): bad.append(("quotient formula", nm(u), e))
        if central(u):
            c2 = [t for k, t in preds(u, 2) if central(t)]; l2 = [t for k, t in preds(u, 2) if level(t) == 2]; z2 = [t for k, t in preds(u, 0) if level(t) == 2]
            if c == 0:
                if (not c2) != eq(M1, B0) or (not z2) != eq(M0, B1) or (not l2) != sub(M0, sh(B1, 1)): bad.append(("tight c=0", nm(u)))
            else:
                if (not c2) != eq(M0, sh(B1, 1)) or (not z2) != eq(M1, sh(B0, -1)) or (not l2) != sub(M1, B0): bad.append(("tight c=1", nm(u)))
        if level(u) == 2:
            if sum(1 for k, t in preds(u, 2) if central(t)) < 1 or sum(1 for k, t in preds(u, 0) if central(t)) < 2: bad.append(("level 2 counts", nm(u)))
            if any(level(t) != 2 for e in (1, -1) for k, t in preds(u, e)): bad.append(("level 2 under odd letters", nm(u)))
print(("ok   " if not bad else "FAIL ") + f"quotient formula for predecessors (e = -1, 0, 1, 2); Lemma A (three tightness criteria); Lemma B (level 2): {n} states, slack <= {S}", bad[:3])
bad = []
for s in range(2, S + 1):
    h = ((s,), ()); v = ((), (1,) * s)
    if [t for k, t in preds(h, 1)] != [((), (1,) * (s - 1))] or [t for k, t in preds(h, 0)] != [v]: bad.append(("hook row", s))
    if [t for k, t in preds(v, 1)] != [((), (1,) * (s - 1))] or preds(v, 2): bad.append(("hook column", s))
print(("ok   " if not bad else "FAIL ") + f"Lemma C: (s|-) has the single 1-predecessor (-|1^(s-1)) and the single 0-predecessor (-|1^s); (-|1^s) has the single 1-predecessor (-|1^(s-1)) and no 2-predecessor: 2 <= s <= {S}", bad[:3])
# Lemma D: a central state u1 with no level-2 0-predecessor ("L-tight"): every central 0-predecessor u2 has no central
# 2-predecessor; and if the common diagram (M0 = B1 for class 0, M1 = B0 - 1 for class 1) is not a half-line, every
# 1-predecessor u3 of every such u2 has a central 2-predecessor.
half = lambda X: all((x - 1) in X for x in X if x > lo + 1)
bad = []; n = h = 0
for s in range(S + 1):
    for u in states(s):
        if not central(u): continue
        if any(level(t) == 2 for k, t in preds(u, 0)): continue
        n += 1; M, B = MB(u); (M0, M1), (B0, B1) = q(M), q(B); D = M0 if cls(u) == 0 else M1; h += half(D)
        for k, u2 in preds(u, 0):
            if not central(u2): continue
            if any(central(t) for kk, t in preds(u2, 2)): bad.append(("D1", nm(u)))
            if not half(D) and any(not any(central(t) for kk, t in preds(u3, 2)) for kk, u3 in preds(u2, 1)): bad.append(("D2", nm(u)))
print(("ok   " if not bad else "FAIL ") + f"Lemma D on the {n} central states of slack <= {S} without a level-2 0-predecessor ({h} of them with a half-line)", bad[:3])
