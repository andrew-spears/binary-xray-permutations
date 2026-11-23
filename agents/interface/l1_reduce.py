"""Three inclusions that would prove the class l1 (letters -1, 0, +1) by induction on the length.
F(x) = set of interface states reachable after the prefix x.
  (A)  F(x 0)  is a subset of  F(x 0 0)
  (B)  F(x 0)  is a subset of  F(x + 0 -)
  (C)  F(x)    is a subset of  F(x + -)        (only needed when '+ -' adjacent, a diagonal used twice, is allowed)
for every prefix x with letters in {-1, 0, +1} and partial sums >= 0, '+ -' adjacent allowed (card l1 allows it; the
prefixes with distinct diagonals are among them).  The step map is monotone, so (A) gives 'x 0 y solvable => x 0 0 y
solvable', (B) gives 'x 0 y solvable => x + 0 - y solvable', (C) gives 'x y solvable => x + - y solvable'.
Every valid word with a + contains + 0^j - (j >= 0).  j = 0: remove it by (C).  j >= 1: shorten it to + 0 - by (A),
then to 0 by (B).  The all-zero word is the anti-diagonal.  So (A), (B), (C) for all x imply l1; (A), (B) for x without
'+ -' imply l1 for distinct diagonals (the shortened word again has no '+ -').
This script checks them for every prefix x whose slacks stay <= B - 1 (so that x + ... stays inside the machine).
Usage: python3 l1_reduce.py B"""
import sys
from rewrite_l1 import sits_l1, run
if __name__ == "__main__":
    B = int(sys.argv[1]); sits, step = sits_l1(B, True)
    for name, u, v in (("(A) 0 -> 0 0", (0,), (0, 0)), ("(B) 0 -> + 0 -", (0,), (1, 0, -1)), ("(C) empty -> + -", (), (1, -1))):
        t = bad = 0; top = 0
        for S, s, last in sits:
            a = run(S, s, last, u, B, step, True); b = run(S, s, last, v, B, step, True)
            if a is None or b is None: continue
            t += 1; top = max(top, s)
            if not a <= b: bad += 1
        print(f"B = {B}: {name}: {t} distinct (reachable set, slack, last letter) with slack up to {top}; fails: {bad}", flush=True)
