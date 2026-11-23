# HIT by the criterion of the brief (at most 62 types per slack, tested for B ≤ 24), but the memory is not finite and J has no formula

Follow-up to `REPORT.md` §3 (card `meminv`). Everything here is computation except the soundness argument in §0.
B = bound on the slack of the words considered. Code: `types.cpp` (usage in its header), `sweep.sh`.

**Claim (tested for every B ≤ 24).** Put a set J only on prefixes
that end in a letter 0 or 1, and let the type of such a prefix x be

    τ(x) = (slack of x;  the last 5 letters of x, cut off at the last rise e_i > e_{i−1}).

After a rise the letters fall by 0 or 1, so there are at most 2 · (1 + 2 + 4 + 8 + 16) = 62 types per slack (62 from
slack 15 on, 58 at the top slack B; 948 in all at B = 20). Then there are nonempty sets J(t) of interface states
with J(τ(empty word)) = {start} and

    J(τ(x w)) ⊆ step_w(J(τ(x)))    for every block w = (letters outside {0, 1})* (one letter in {0, 1}),      (step)
    J(t) ∩ conj J(t') ≠ ∅          for all types t ending in 1 and t' ending in 0 at the same slack.          (pairs)

τ(x w) is a function of τ(x) and w. Recheck (8 s): `g++ -O2 -std=c++17 -o types types.cpp && KLO=0 ./types 16 A4K`
(last line `=> WORKS`). If the system works at bound B it works at every smaller bound (restrict the family). Runs:
`KLO=0 ./types 20 A4K` (a few minutes), and `./types 24 A4K` (about 20 minutes), which demands more: sets on the
prefixes ending in a negative letter too.

**What it is not.** The window length 5 is presumably not final: with windows of 2, 3, 4 letters the same system works
through B = 5, 7, 14 and then fails, so I expect 5 letters to fail somewhere beyond B = 24. The step runs over
blocks of unbounded length (checked by following the exact reachable sets through each block). And I found no rule
describing the sets J (§3). So the memory per slack is small and explicit, not finite.

## 0. Why this is enough (proved)
By induction over blocks, (step) gives J(τ(x)) ⊆ F(x) for every legal prefix x ending in 0 or 1 with slacks ≤ B
(step_w is monotone and F(x w) = step_w(F(x))). By reversal symmetry (`REPORT.md` §1), A(y) ⊇ conj J(τ(−reverse y)).
Every nonzero valid word has neighbouring letters 1, 0 (`../weights/REPORT.md` §0); cut there: the prefix ends in 1,
−reverse(suffix) ends in 0, so (pairs) gives F(x) ∩ A(y) ≠ ∅. Hence (step) + (pairs) for all B is the conjecture.
`CORE=1 ./types 11 A4K` confirms J(t) ⊆ ∩ F(x) by brute force for small B.

## 1. The candidate types of the brief, one set per prefix (no blocks)
"Works" = all sets nonempty and all pairs (types ending in 1 against conj of types ending in 0) meet, at every
slack ≤ B. Every type contains (slack, last letter); r = length of the final run falling by 1, q = length of the
final run of equal letters. `L0`..`L4` are the memories m = 1..5 of `REPORT.md` §3 (m = 5 was not run past 14 there).

| type (feature string) | works through B | types at B = 8, 12, 16 |
|---|---|---|
| nothing more (``) | 2 | 63, 124, 204 |
| r (`R`) | 4 | 155, 345, 614 |
| r, q ≤ 2 (`RQ2`); q ≤ 3 (`RQ3`) | 6; 6 | 250, 581, 1064; 319, 743, 1370 |
| r, letter before the run (`RP`) | 6 | 633, 1742, 3627 |
| r, q ≤ 2, letter before the runs (`RPQ2`) | 7 | 1040, 3002, 6457 |
| last rise: its letter and its age ≤ 3 (`M3`); age ≤ 8 (`M8`) | 6; 6 | 280, 614, 1092; 683, 1447, 2481 |
| final non-increasing run, ≤ 5 letters (`A4`); the last 5 letters cut off one letter before the last rise (`C4`) | 6; 7 | 566, 1203, 2056; 1324, 3322, 6496 |
| previous letter (`L1`) | 4 | 268, 667, 1313 |
| previous 2 letters (`L2`); with `M3` | 8; 10 | 896, 2687, 6126; 1120, 3282, 7325 |
| previous 3 letters (`L3`) | 13 | 2668, 9266, 23797 |
| previous 4 letters (`L4`) | 22 (fails at 23) | 83079 at B = 16, 280949 at B = 22 |

None of the coarse types reaches B = 16; only literal windows do, and their size is the problem.

## 2. Blocks: sets only on prefixes ending in a small letter (`K`)
As in `../majority/blockinv.py`, but with a type: a run of letters ≥ 2 and the letter 1 closing it is one block, and
J(t') ⊆ step_w(J(t)) is required for whole blocks. Types with last letter ≥ 2 then carry no set.

| type, sets on prefixes ending in a letter ≤ 1 | works through B |
|---|---|
| `K` alone; `RK`; `RQ3K` | 2; 4; 7 |
| `M3K`; `M8K`; `L2K` | 6; 11; 8 |
| `RPQ2K`; `RPQ3K` | 11; 17 (fails at 18) |
| `C3K` (the last 4 letters, cut off one letter before the last rise) | 18 (fails at 19) |
| `A1K`, `A2K`, `A3K` (final non-increasing run ≤ 2, 3, 4 letters) | 4, 7, 14 |
| `A4K` (≤ 5 letters) | 24 (not run further), 4383 types at B = 24 |

With `KLO=0` runs of negative letters are blocks too, so only prefixes ending in 0 or 1 carry a set (the Claim):
`A1K`, `A2K`, `A3K` work through 5, 7, 14, and `A4K` through 24 (run directly through 20; 21–24 follow from the
row above, which demands more). Sets carried at B = 12, 16, 20: 455, 700, 948 for `A4K`; at B = 12, 16: 277, 397 for
`A3K` and 674, 1126 for `A5K`.

So the block form is what makes a coarse type work: without blocks the same window `A4` dies at B = 7. The windows
needed (2, 3, 4, 5 letters up to B = 5, 7, 14, ≥ 24) grow slowly; if the range keeps roughly doubling, the number of
types per slack, 2^(k+2) − 2 for a window of k + 1 letters, stays polynomial in B. That is a guess from three points and a lower bound.

## 3. The sets J: no rule found
`KLO=0 ./types 14 A4K sizes` → `J_sizes_14.txt` (|J(t)| per window and slack); `KLO=0 ./types 13 A4K dump` prints the
sets for slack ≤ 8. J(t) at slack ≤ 8 is the same for B = 12 and B = 15, so the sets do not depend on the bound.
- The sets are large: 26–100% of all states of that slack (all pairs of partitions of total size s). Window
  `0 0 0 0 0`: everything for s ≤ 8, then 296 of 300, 473 of 481, 734 of 752. Rise to 1 (window `1`): 2, 4, 10, 17, 30,
  57, 66, 135, 194 of 2, 5, 10, 20, 36, 65, 110, 185, 300. Staircase `4 3 2 1 0`: 233 of 481 at s = 10.
- What is missing is mostly hooks and near-hooks, but not only. `0 0 0 0 0` at s = 9: −|9, 9|−, 21|321, 321|21;
  at s = 10: −|(10), −|1^10, −|91, 1|9 and transposes. Rise to 0 at s = 8: −|8, −|71, −|1^8, 1|7, 4|4 and transposes.
  Rise to 1 at s = 4, 5: 11|2, 2|11, 2|2; then −|311, 111|2, 11|3 and transposes. The sporadic states (21|321, 4|4,
  21|21, 3|3) rule out "largest part or number of parts below a threshold".
- At slack 12 the 28 + 31 types ending in 1 and in 0 carry 28 + 28 different sets, so types cannot be merged.
- The exact intersections C(t) = ∩ F(x) over prefixes of type t are not themselves step-closed (`CORE=1 ./types 10 L3`:
  131 of 15694 transitions fail), so J is not simply "the core of the type". `KLO=0 CORE=1 ./types 11 A4K`: J(t) = C(t)
  for 277 of the 396 types; the first difference is the window `2 1 0` after a rise at slack 6 (44 states against 50).

## 4. Other ways to shrink the window (all still windows)
- Clamping (`CLAMP`, `CLAMPL`): at B = 16, `L4` with the 4 previous letters clamped to [0, 5] works with 10763 types
  against 83079. The clamp must grow with B: [0, 3] fails at 14; [0, 4] at 16 and [0, 5] at 20 have no bad pair but
  empty sets at types that cannot be continued within the bound. Clamping the last letter too: [−1, 6] fails at 16
  (this run also demands sets at some types that no legal prefix reaches, so the failure is not conclusive).
- Window length depending on the slack (`window.py`: keep the j-th previous letter iff slack ≥ θ_j): θ = (3, 5, 8)
  works through B = 13; θ = (3, 5, 9) fails at 9; restricting further to staircases or non-increasing runs fails.
- Greedy removal of contexts (`ctx.py`): at B = 9 with `L3`, only 68–75 of the 1569 contexts (slack, last k letters)
  need one more letter, but the list depends on the order of removal and follows no pattern I could see.
