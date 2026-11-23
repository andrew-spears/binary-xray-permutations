"""The owner's candidate for item 1: S for which both part-words have letters in {0, 1} (then the state (1^s|-) is odd on both sides;
this is the case rho_1 = kappa_2 = 1^s of the E-split).  Also counts the family of Theorem A and {0,1}*{0,-1}*.
Usage: python3 zo.py n"""
import sys
from ext import words, parts
n = int(sys.argv[1]); tot = z = A = old = uni = uz = 0; ex = []
for e in words(n, False):
    if not any(e) or any(sum(e[:k]) == 0 for k in range(1, n)): continue
    tot += 1; p = max(i for i in range(n) if e[i] > 0)
    u = all(x >= 0 for x in e[:p]) and all(x <= 0 for x in e[p:][1:]); uni += u
    A += u and max(map(abs, e)) <= 2; old += u and max(map(abs, e)) <= 1
    ok = False
    for S in range(1, (1 << n) - 1):
        w1, w2 = parts(e, S)
        if set(w1) <= {0, 1} and set(w2) <= {0, 1}: ok = True; break
    z += ok; uz += ok and u
    if u and not ok and len(ex) < 3: ex.append(e)
print(f"n = {n}: {tot} valid words without a tight cut, {uni} unimodal; letters |e| <= 1 and unimodal: {old}; Theorem A (|e| <= 2, unimodal): {A}; "
      f"some S with both part-words in {{0,1}}: {z} (unimodal: {uz}); unimodal examples without: {ex}")
