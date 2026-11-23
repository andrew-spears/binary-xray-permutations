"""Lower bound on any accepting family, slack by slack.  A cut of a valid word x.y (slacks <= B) at slack s has the
cut set I(x, y) = F(x) & A(y); an accepting family must contain a state of every cut set.  A(y) = conj F(-reverse y)
(universal/REPORT.md section 1), so cut sets are F(x) & conj F(x') with last(x') <= 1 - last(x).
h_B(s) = least number of states of slack s meeting every cut set at slack s (exact, by integer programming).
Usage: python3 hit.py B [show]"""
import sys, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from thin import *
B = int(sys.argv[1]); m = M(B); n = len(m.states); show = len(sys.argv) > 2
cj = [m.idx[conj(l), conj(mu)] for l, mu in m.states]
def cmask(S):
    out = 0
    while S:
        b = S & -S; S ^= b; out |= 1 << cj[b.bit_length() - 1]
    return out
# all determinised forward sets with last letter and slack
seen = {(1, None): 0}; todo = [(1, None, 0)]; k = 0
while k < len(todo):
    S, last, sl = todo[k]; k += 1
    for e in m.letters(sl, last):
        R = m.step(S, e, m.full)
        if (R, e) not in seen: seen[R, e] = sl + e; todo.append((R, e, sl + e))
fw = {}
for (S, last), sl in seen.items():
    if last is not None and sl > 0: fw.setdefault(sl, {}).setdefault(last, set()).add(S)
def minimal(sets):
    out = []
    for S in sorted(set(sets), key=lambda S: bin(S).count("1")):
        if not any(R & S == R for R in out): out.append(S)
    return out
tot = 0
for s in range(1, B + 1):
    F = {l: minimal(v) for l, v in fw[s].items()}
    A = {l: [cmask(S) for S in v] for l, v in F.items()}          # conj F(x'), keyed by last(x')
    cuts = [X & Y for l, Fs in F.items() for l2, As in A.items() if l2 <= 1 - l for X in Fs for Y in As]
    assert all(cuts), "empty cut set: an unsolvable word"
    cuts = minimal(cuts)
    lev = [i for i in range(n) if m.slack[i] == s]; pos = {i: j for j, i in enumerate(lev)}
    Amat = np.zeros((len(cuts), len(lev)))
    for r, c in enumerate(cuts):
        while c:
            b = c & -c; c ^= b; Amat[r, pos[b.bit_length() - 1]] = 1
    res = milp(np.ones(len(lev)), constraints=LinearConstraint(Amat, 1, np.inf), integrality=np.ones(len(lev)), bounds=Bounds(0, 1))
    pick = [lev[j] for j in range(len(lev)) if res.x[j] > 0.5]; tot += len(pick)
    small = min(bin(c).count("1") for c in cuts)
    print(f"slack {s:2d}: {len(lev):5d} states, {len(cuts):5d} minimal cut sets (smallest has {small}), h = {len(pick)}"
          + (":  " + " ".join(m.name(i) for i in pick) if show else ""), flush=True)
print("total lower bound", tot + 1, "of", n)
