"""Independent recheck (Python, on the machine of ../interface/rewrite.py) of a failure of NONNEG found by cut_check.
For the prefix x (letters on the command line; default: the shortest failing prefix) with end slack s and last
letter l: builds the inclusion-minimal sets F(x') over ALL prefixes x' with letters >= 0 that end at (s, l), and
tests whether one of them lies inside F(x).  Sets are Python integers used as bitsets.
(Only minimal sets are extended: if F(x1) is inside F(x2) at the same (s, l) then F(x1 y) is inside F(x2 y).)
Usage: python3 verify_nonneg.py [letters of x]        (default: 10 seconds)"""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "interface"))
from rewrite import machine
x = tuple(int(t) for t in sys.argv[1:]) or (4, 3, 2, 1, 3, 2, 1, 0, -1, 2)
s_end, l_end = sum(x), x[-1]
B = max(sum(x[:i]) for i in range(1, len(x) + 1))
step, start = machine(B)
ids = {start: 0}; states = [start]; cache = {}
def succ(i, e):
    k = (i, e)
    if k not in cache:
        m = 0
        for t in step(frozenset([states[i]]), e):
            if t not in ids: ids[t] = len(states); states.append(t)
            m |= 1 << ids[t]
        cache[k] = m
    return cache[k]
one = re.compile("1")
def bstep(S, e):
    out = 0; b = bin(S)[:1:-1]
    for m in one.finditer(b): out |= succ(m.start(), e)
    return out
Fx = 1; s = 0
for e in x: Fx = bstep(Fx, e); s += e
anti = {}                      # (slack, last letter) -> minimal sets [set, word]
queue = [(1, 0, None, ())]; n = 0
while queue:
    nxt = []
    for S, s, l, w in queue:
        if l is not None and not any(S is T for T, _ in anti[(s, l)]): continue     # no longer minimal
        for e in range(0 if l is None else max(0, l - 1), s_end - s + 1):
            if s + e == s_end and e != l_end: continue
            T = bstep(S, e); fam = anti.setdefault((s + e, e), [])
            if any(U & T == U for U, _ in fam): continue
            fam[:] = [(U, v) for U, v in fam if U & T != T]; fam.append((T, w + (e,))); nxt.append((T, s + e, e, w + (e,))); n += 1
    queue = nxt
fam = anti[(s_end, l_end)]
inside = [v for U, v in fam if U & Fx == U]
print(f"x = {x}: end slack {s_end}, last letter {l_end}, |F(x)| = {bin(Fx).count('1')}")
print(f"{len(fam)} minimal sets F(x') with x' nonnegative ending at ({s_end}, {l_end});  inside F(x): {len(inside)}", inside[:3])
best = sorted(fam, key=lambda a: bin(a[0] & ~Fx).count("1"))[:3]
for U, v in best: print(f"   x' = {v}: |F(x')| = {bin(U).count('1')}, {bin(U & ~Fx).count('1')} states outside F(x)")
