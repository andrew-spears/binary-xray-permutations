"""Block invariant.  Read a word in BLOCKS: a single letter e <= SMALL, or an excursion b_1 ... b_j (all > SMALL)
followed by its closing letter SMALL (forced: letters fall by at most 1).  Look for the largest family
J(s, l)  (slack s, last letter l <= SMALL)  with  J(0, .) = {empty}  and
    J(s, l)  subset of  step_w( J(s', l') )   for every block w leading from (s', l') to (s, l).
Then J(s, l) is inside F(x) for EVERY prefix x with slack s and last letter l.  If all J are nonempty (in particular
J(0, .) keeps the empty state), every word with slacks <= B is solvable, by an invariant that depends only on the
slack and the last letter.           Usage: python3 blockinv.py B [SMALL=1]"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "interface"))
from rewrite import machine
from core import name
from segment import levels
def solve(B, SMALL=1, verbose=True):
    step, start = machine(B); lev = levels(B, step, start)
    # realizable situations (slack, last letter <= SMALL)
    seen = set(); todo = [(0, min(SMALL, 1))]      # the first letter may be any e >= 0
    while todo:
        s, l = todo.pop()
        if (s, l) in seen: continue
        seen.add((s, l))
        for e in range(max(l - 1, -s), B - s + 1): todo.append((s + e, e))
    keys = sorted(k for k in seen if k[1] <= SMALL)
    J = {k: (frozenset([start]) if k[0] == 0 else frozenset(lev[k[0]])) for k in keys}
    rounds = 0
    while True:
        rounds += 1; cons = {}
        def add(k, S):
            cons[k] = S if k not in cons else cons[k] & S
        for (s, l) in keys:
            S = J[(s, l)]
            for e in range(max(l - 1, -s), min(SMALL, B - s) + 1): add((s + e, e), step(S, e))
            memo = set(); st = [(step(S, b), s + b, b) for b in range(SMALL + 1, B - s + 1)]
            while st:
                S2, s2, last = st.pop()
                if (S2, s2, last) in memo: continue
                memo.add((S2, s2, last))
                if last == SMALL + 1 and s2 + SMALL <= B and s2 + SMALL >= 0: add((s2 + SMALL, SMALL), step(S2, SMALL))
                for b in range(max(SMALL + 1, last - 1), B - s2 + 1): st.append((step(S2, b), s2 + b, b))
        changed = False
        for k in keys:
            if k in cons:
                new = J[k] & cons[k]
                if new != J[k]: J[k] = new; changed = True
        if verbose: print(f"  round {rounds}: empty families {sum(1 for k in keys if not J[k])} of {len(keys)}", flush=True)
        if not changed: break
    return J, lev, start
if __name__ == "__main__":
    B = int(sys.argv[1]); SMALL = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    J, lev, start = solve(B, SMALL)
    print(f"B = {B}, SMALL = {SMALL}: all families nonempty: {all(J.values())}")
    for (s, l) in sorted(J):
        if s and l >= -1: print(f"slack {s:2d} last {l:2d}: {len(J[(s, l)]):4d} of {len(lev[s]):4d}  ", " ".join(sorted(name(t, B) for t in J[(s, l)]))[:120])
