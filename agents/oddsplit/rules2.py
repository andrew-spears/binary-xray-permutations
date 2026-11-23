"""Items 2 and 3: fixed rules for S against the criteria RR and E (= RR, CC, RC or CR), words without a tight cut.
Rules: pos = {e_k > 0}; nonneg = {e_k >= 0}; turn = stones before the first negative letter; odd = odd diagonals;
win(w) = some S inside the w stones centred at the turn (reports the least w that works for every word).
Usage: python3 rules2.py n"""
import sys
from ext import words, parts, shape, conj, splits, crit
def rr(e, S):
    if S == 0 or S == (1 << len(e)) - 1: return False
    w1, w2 = parts(e, S)
    if min(w1) < 0 or min(w2) < 0: return False
    return splits(conj(shape(w2)[0]), shape(w1)[0])
n = int(sys.argv[1]); tot = 0; R = {}; E = {}; worst = 0; wex = None
for e in words(n, False):
    if not any(e) or any(sum(e[:k]) == 0 for k in range(1, n)): continue
    tot += 1; t = next(i for i in range(n) if e[i] < 0)
    rules = {"pos": sum(1 << k for k in range(n) if e[k] > 0), "nonneg": sum(1 << k for k in range(n) if e[k] >= 0),
             "turn": (1 << t) - 1, "odd": sum(1 << k for k in range(n) if e[k] % 2)}
    for name, S in rules.items():
        R[name] = R.get(name, 0) + rr(e, S); E[name] = E.get(name, 0) + bool(S and S != (1 << n) - 1 and crit(e, S))
    good = [S for S in range(1, (1 << n) - 1) if rr(e, S)]
    # least window [t - a, t + b) containing an RR-split, measured by its length
    w = min(max(k for k in range(n) if S >> k & 1) - min(k for k in range(n) if S >> k & 1) + 1 for S in good)
    if w > worst: worst = w; wex = e
print(f"n = {n}: {tot} words.  RR by rule: {R};  E by rule: {E}")
print(f"   least span (last - first + 1) of an RR-split S, worst word: {worst} for {wex}")
