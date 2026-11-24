# HIT (empirical): one hole pattern serves every past and every future at a cut after a letter 0 or 1

Notation: F(x) = interface states reachable after the prefix x; A(y) = states from which the suffix y reaches the
empty state. The word xy is solvable iff F(x) meets A(y).

## Claim (universal cut states)
For every slack s ≥ 1 and l in {0, 1} there is a state c with
- c in F(x) for every legal prefix x with slack s and last letter l, and
- c in A(y) for every suffix y that starts at slack s with first letter ≥ l − 1.

**Range.** All prefixes and suffixes with slacks ≤ 14, every s ≤ 14. Number of such states for l = 0, s = 1..14:
2, 4, 4, 6, 6, 2, 4, 12, 8, 14, 12, 22, 26, 36 (same sets at bound 12 and 14 for s ≤ 9). Examples: s = 9: no row
holes, column diagram 333, for both l; s = 6: 111|21 (l = 0), 21|3 (l = 1).

**Recheck.** `python3 agents/majority/core.py 14 | grep "last  [01]"` (about 1 minute); `core.py 10` (2 seconds).

## Weaker form at every cut (majority weights)
For other last letters there is no common state (last letter 2, slack 5: no state lies in all F; last letter −2,
slack 3: none lies in all A). But for every cut type (s, l) there are weights w ≥ 0 on the states, total 1, with
min_x w(F(x)) + min_y w(A(y)) > 1, which forces every F to meet every A. Best values at bound 14: between 1.55 and
2 at every cut (2 means a common state). `python3 agents/majority/maj.py 14 1` (30 seconds). Without the junction
condition (first letter of y ≥ last letter of x − 1) the best value drops below 1 from slack 4.

## What does NOT follow (both NOTHING)
- **Committing at the cuts** (`segment.py 8`, 1 second): the largest family G(s, l) of states from which every
  segment up to the next 0 or 1 can be walked into G again is empty at bound 8 (cuts after 0 and 1) and at bound 6
  (cuts after 0 only). A universal state works for every future, but which state to pass through at the next cut
  depends on what comes after it.
- **Invariant by slack and last letter with excursions as single blocks** (`blockinv.py 6`, 1 second): the largest
  family J(s, l) (l ≤ 1) with J(s, l) ⊆ step_w(J(s', l')) for every block w (one letter ≤ 1, or a run of letters ≥ 2
  with its closing 1) is empty at bound 6. So the common states are not produced step by step from common states.

## Reading
The half c in F(x) says: every prefix arrangement with final slack s and last letter 0 or 1 is solvable on one fixed
board with holes (rows and columns given by c). This is a Landau-type statement for a board with holes, and the two
halves are independent of each other. A proof of the conjecture along this line would need each half proved by its
own induction; the two NOTHING results say that induction cannot be the obvious one.
