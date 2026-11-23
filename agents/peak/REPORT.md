# HIT (disproofs): PEAK fails at slack 17, NONNEG fails at slack 17 (last letter ≥ 2) and 26 (last letter 1)

Notation as in `../interface/SHORTEN_BRIEF.md` and `../majority/REPORT.md`: F(x) = interface states after the
prefix x, A(y) = states from which the suffix y reaches the empty state. Nothing here is a proof of a positive
statement; the counterexamples are exact and rechecked by independent brute force, everything else is "tested".

## 1. PEAK: F(x 0) ⊆ F(x 1 0 −1) is false
**Shortest failing prefix** x = 3 4 3 3 2 1 (sums 5, 8, 9, 11, 12, 13; slack 16, so x 1 has slack 17).
|F(x 0)| = 3426, |F(x 1 0 −1)| = 4657, and 3 states of F(x 0) are missing (rows | columns, before the shift):
{1,2,3,4,7,8,11} | {1,2,3,4,7,8,11}, {1,3,4,5,7,8,11} | {1,2,3,4,5,7,11} and its transpose.
x has no negative letter and ends in 1, so it is inside the scope the induction needs.

**Range where PEAK holds** (all legal prefixes with every slack ≤ B, `peak_check`):
| prefixes | B | tests | failures |
|---|---|---|---|
| all | 16 | 4,100 | 0 |
| all | 17 | 5,959 | 1 (the x above) |
| all | 20 | 16,477 | 5: x above, 3 4 3 2 3 2 1, 2 1 3 4 3 3 2 1, 3 2 4 3 3 2 1 0, 3 4 3 3 2 1 2 1 |
| letters ≤ 3 | 21 | 14,440 | 0 |
| letters in [−1, 2] | 24 | 3,533 | 0 |
| letters in [−1, 1] | 31 | 289 | 0 |

Every failure found contains the letter 4. Lookahead does not repair it: for the failing x, F(x 0 y) ⊆ F(x 1 0 −1 y)
still fails for 7 of the 13 legal y with |y| ≤ 3 (bound 17). The 3 missing states of the shortest failure pass the
parity count and fail the same count mod 4 (`modq.py`); the missing states of the next two failures pass it mod 4 and 8.

**Recheck.** `python3 agents/peak/cex.py` (1 second, absolute coordinates, no machine).
`cd agents/peak && g++ -O2 -o peak_check peak_check.cpp && ./peak_check 17` (40 seconds).

## 2. NONNEG (claim A of `../nonneg/NOTES.md`) is false; the form with last letter 0 survives to slack 27
**Shortest failing prefix** x = 4 3 2 1 3 2 1 0 −1 2 (single dip; end slack 17, last letter 2, |F(x)| = 7842 of
8470 states). There are 393 inclusion-minimal sets F(x') with x' nonnegative ending at (17, 2); none is inside F(x).
Closest: x' = 2 1 5 4 3 2 (|F| = 2500, 6 states outside F(x), e.g. rows {1..7,9,10,11} | columns
{1..5,7,9,10,11,17}). Allowing a smaller last letter for x' does not help.

| last letter l of x | NONNEG holds for all prefixes with slacks ≤ | first failure |
|---|---|---|
| any | 16 | slack 17 |
| ≥ 2 | 16 | 4 3 2 1 3 2 1 0 −1 k fails for every k = 2..12 (end slack 15 + k) |
| 1 | 25 | 5 4 3 2 4 3 2 1 0 −1 2 1 (slack 26; closest x' = 3 3 2 5 4 3 2 1 2 1, 34 states outside) |
| 0 | 27 | none found |

(Bound 27: 191,451 inclusion-minimal sets tested, 31 failures, two with l = 1, none with l = 0.)
The last row is the one that matters: at the last maximum of the slack the last letter is 0, so the reduction to
unimodal words in `NOTES.md` only uses NONNEG with l = 0. The reduction to single-dip words no longer applies to
it as stated (it passes through intermediate letters e ≥ 2); what remains provable is the reduction to words
p n y with p nonnegative ending in 0, n a run of negative letters, y nonnegative ending in 0. Given how the
l = 2 and l = 1 forms died (17, 26), the l = 0 form should not be believed beyond the tested range.

**(A') x' only required to never rise above its end slack:** 0 failures among 41,236 minimal sets, all prefixes
with slacks ≤ 22 (every last letter ≥ 0). Note that (A') is trivial for the failing x above (it never rises above
its end slack, so x' = x); it only has content for prefixes that come down from a higher slack.

**Canonical x'.** For l = 0 exactly one nonnegative x' lies inside every other F(x) at slack 8, 9, 11, 12, 13
(3 2 2 1 0, 3 3 2 1 0, 3 2 3 2 1 0, 4 3 2 2 1 0, 4 3 3 2 1 0), two at slack 10, and none from slack 14 on; for l = 1 none
from slack 10 on (`logs/common_16.log`). So the witness x' has to depend on x, not only on (s, l).

**Recheck.** `python3 agents/peak/cexA.py` (1 second, absolute coordinates; the 6 states for x' = 2 1 5 4 3 2).
`python3 agents/peak/verify_nonneg.py` (10 seconds, Python machine: all 393 minimal sets).
`cd agents/peak && g++ -O2 -o cut_check cut_check.cpp && ./cut_check 22` (45 seconds: A, A', B);
`./cut_check 26 1 0 0 0 0` (3 minutes, 4 GB: A only; bound 27: 7 minutes, 7 GB).

## 3. Universal cut states (claim B of `../majority/REPORT.md`) survive to slack 24
For every s = 1..24 and l in {0, 1} there is a state lying in F(x) for every legal prefix x ending at (s, l) and in
A(y) for every suffix y from slack s with first letter ≥ l − 1 (all prefixes and suffixes with slacks ≤ 24). Number
of such states at s = 15..24: l = 0: 36, 78, 128, 182, 270, 344, 358, 916, 1730, 2460; l = 1: 40, 78, 136, 184,
270, 348, 366, 924, 1740, 2476 (s ≤ 14 agrees with `core.py`). Unlike PEAK, ZERO, RUN and NONNEG, this claim shows
no sign of strain in the steep regime: the count grows with s.

**Recheck.** `./cut_check 22 | grep "last  [01]"` (45 seconds); `./cut_check 24 1 0 0 0` (2 minutes, 1.7 GB).

## Files
`peak_check.cpp` (PEAK, BFS over situations), `cut_check.cpp` (A, A', B on inclusion-minimal sets; the pruning is
explained at the top of the file), `cex.py`, `cexA.py`, `explore.py` (absolute-coordinate brute force),
`verify_nonneg.py`, `modq.py`, `runs.sh` (all runs quoted here), `logs/`.
