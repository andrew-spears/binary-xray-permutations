"""Check of the slack-2 formulas against brute force.  For every solvable word w of length <= n and every cut
w = x y of slack 2:   N(w) = 2 alpha beta' + 2 beta alpha' + gamma gamma',  and if y = 0 y1 also
N(w) = 2 alpha alpha' + 2 beta beta' + 2 beta gamma1' + 2 gamma beta1'   with (alpha', ..) of y1* in the second formula;
(alpha, beta, gamma) of x and of y* = y reversed and negated, computed by the interface machine.
Usage: python3 slack2check.py n"""
import sys
from collections import Counter
sys.path.insert(0, "../interface")
from count_rule import cstep
from cone import part
from countlib import solutions
n = int(sys.argv[1]); N = {w: len(s) for w, s in solutions(n).items()}; B = n + 2; base = (1 << B) - 1; memo = {}
def abg(x):
    if x not in memo:
        C = Counter({(base, base): 1})
        for e in x: C = cstep(C, e, B)
        d = {tuple(sorted((part(t[0], B), part(t[1], B)))): c for t, c in C.items()}
        memo[x] = (d.get(((), (1, 1)), 0), d.get(((), (2,)), 0), d.get(((1,), (1,)), 0))
    return memo[x]
star = lambda y: tuple(-e for e in reversed(y))
c1 = c2 = bad = 0
for w in N:
    for k in range(1, len(w)):
        if sum(w[:k]) != 2: continue
        a, b, g = abg(w[:k]); a2, b2, g2 = abg(star(w[k:])); c1 += 1
        bad += N[w] != 2 * a * b2 + 2 * b * a2 + g * g2
        if w[k] == 0:
            a2, b2, g2 = abg(star(w[k + 1:])); c2 += 1
            bad += N[w] != 2 * a * a2 + 2 * b * b2 + 2 * b * g2 + 2 * g * b2
print(f"words of length <= {n}: cuts of slack 2: {c1}, of which followed by a 0: {c2}; formula wrong: {bad}")
