# NOTHING for GRADED with general letters (the first 0 does not repair a letter ≥ 3; smallest prefix 1 1 1 1 1 3 2 1 0 0). HIT (tested only) for letters ≤ 2: after a 0 the missing set is the explicit N_y; closing at negative letters is free

Follow-up to `REPORT3.md` (cards `oldprefix`, `youngtail`, `norun3`) and `../lens/NOTES.md` items 3, 5. Nothing is proved.
Code: `types.cpp` (new `CLOSE=0|n`, `YCAP=c`), `fw.cpp` (new `ZERO=1`), `young.py` (families and cores by type), `zero.py`
(single words). Build: `g++ -O2 -std=c++17 -o types types.cpp && g++ -O2 -std=c++17 -o fw fw.cpp`.

**Notation.** y = young excess of the prefix (y′ = max(0, y + e − 1)); p = class of the letter before the final 0
(1 = "≥ 1", 0, −1 = negative); J*(s, τ) the table of conjecture OLD, τ = `1 0`, `0 0`, `. 0` for p = 1, 0, −1.
For a state u of slack s: d(u) = s − (longest row or column of λ or μ), and

    N_y(s) = { d(u) ≤ y − 1 } ∪ { λ or μ has a row of length ≥ s − y }        (N_0 = ∅).

|N_y ∩ J*(s, `. 0`)| = 6, 20, 50, 110, 222, 422 for y = 1..6, independent of s (s large against y). These are the 6 and the
"row ≥ s − 2" states of `lens/NOTES.md` item 3; the two one-row states are already outside J*.

## 1. J*(s, τ) ∖ F(x) for young prefixes ending in 0

**(a) N_y is always missing.** F(x) ∩ N_y(s) ∩ J* = ∅ for every x ending in 0 with young excess y that I looked at: the
words of §1c and 860 young prefixes of 300 random words (slack 11..16, letters −2..4). Also N_y ∩ Z = ∅ for every type
of the runs below. So N_y is the right lower bound for the omission, for all letters.

**(b) Letters ≤ 2: N_y is (almost) everything.** Largest family Z(s, y, p) closed under blocks (nonzero letters)* 0 over ALL
words with letters ≤ 2 and slacks ≤ B (so Z ⊆ F(x) for each of them), B = 18, slacks 13..18:

| p | y | J* ∖ Z |
|---|---|---|
| any | 0 | ∅ (Z = J* on old prefixes, as in REPORT3) |
| −1 | 1..4 | N_y exactly (6, 20, 50, 110) |
| 0 | 2, 3 | N_y exactly; y = 1: N_1 + 2 states (s−3\|21, 21\|s−3) |
| 0 | 4, 5, 6 | N_y at odd s; at even s also 2–3, 8, 18 states (s−6,2,1\|21, 4211\|4211 at s = 16, 1\|s−7,3,2,1, …) |
| 1 | 1, 2, 3 | N_y + 2, 6, 6 states, all with d ≤ 5 (s−3\|21 or −\|s−3,2,1; s−4,1\|111, s−4,1\|3, −\|3 2 1^(s−5); −\|s−4,2,2, s−4\|22, …) |
| 1 | 4, 5, 6 | N_y + 8–14, 13–30, 20–24 states; but 42, 110, 290 states at s = 2y + 5, where the worst word is 1 1 2^(y+1) 1 0 (the excursion starts at the beginning of the word) |

The exact cores C(s, y, p) = ∩ F(x) agree with Z for 129 of 135 types at B = 16. So for letters ≤ 2 GRADED holds in the
tested range up to a sporadic set (at most ~30 states once s ≥ 2y + 6), which I could not fit (it contains the `E⁰`/k|k-like states
"long row + staircase 21" and depends on the parity of s). Recheck (12 s): `LET=-9,2 python3 young.py 16 14 show`
(`EXACT=1` for the cores; B = 18 takes a few minutes).

**(c) General letters: false.** Smallest prefix (smallest slack where J* is defined, smallest y, letters ≤ 3):

    x = 1 1 1 1 1 3 2 1 0 0     slack 11, y = 1:   J*(11, 0 0) ∖ F(x) = N_1 ∪ { −|65, −|83, 65|−, 83|− }      (10 states)
    x = 1 1 1 1 1 3 2 1 0       slack 11, y = 2:   38 states missing, |N_2| = 20; outside N_2: −|65 −|74 −|83 3|8 4|7 5|6 6|5 7|4 8|3 1^8|3 1^6|5 1^4|7 and transposes

The extra states are two-line states (two rows in one diagram, or one row in each: 3|11, 5|9, 7|7, 9|5, 11|3 at slack 14,
y = 1 after `1^8 3 2 1 0 0`), so their distance d to a one-line state is about s/2: no N of bounded thickness contains
them. They grow with the largest letter c and die only after about c zeros (`python3 zero.py "<word>"`, seconds):

| word | first zeros: y → missing (of which outside N_y) | exactly N_y from |
|---|---|---|
| 1^8 2 2 2 1 0 0 0 | 2 → 20 (0), 1 → 6 (0) | 1st zero |
| 1^5 3 2 1 0 0 | 2 → 38 (18), 1 → 10 (4) | y = 0 |
| 1^8 3 3 3 2 1 0^4 | 6 → 710 (300), 5 → 336 (114), 4 → 127 (17), 3 → 50 (0) | 4th zero |
| 1^5 4 3 2 1 0^6 | 5 → 458 (240), 4 → 192 (82), 3 → 62 (12), 2 → 20 (0) | 4th zero |
| 1^7 5 4 3 2 1 0^9 (slack 22) | 9 → 5971 (3737), 8 → 3009 (1645), 7 → 1186 (412), 6 → 488 (64), 5 → 227 (5), 4 → 110 (0) | 6th zero |

All words with slacks ≤ 16 (`python3 young.py 16 14`, 1 min): J* ∖ Z = N_y only for (p = −1, y = 1); otherwise N_y plus
2 (p = −1, y = 2), 8 (p = 0, y = 1, d up to 7), 33–39 (p = 1, y = 2), 115–138 (p = 1, y = 4), 350–490 (p = 1, y = 5).

**(d) Levels** (level = max(c, 1 − c)). The omission after a 0 is not "low levels only": after `1^5 4 3 2 1 0 0` the
missing/all counts are L1 148/2478, L2 38/1148, L3 6/210; one zero later L1 36, L2 26, L3 0; after `1^7 5 4 3 2 1 0 0 0`
L1 746/29566, L2 411/15268, L3 29/3728. The top level heals first, but levels 1
and 2 are damaged in the same proportion, and N_y itself meets both. I found no level-graded description of the extra states.

## 2. Closing rule Z (sets on every prefix ending in 0; type = slack, min(y, cap), p)

- **Exists for every cap.** `CLOSE=0 CLAMP=-1,1 YCAP=c ./types B YL1`: no empty set and no bad 1|0 pair for c = 0, 1, 2, 3
  through B = 16, and for c = 0 and c = ∞ through B = 18. With c = 0 the type is (slack, p): 3 sets per slack.
- **Equals the formula only without a cap.** With y exact, Z = J* on all old types and J* ∖ Z is §1b/§1c on young ones.
  With cap c every type with y ≥ c gets the set of the youngest prefixes, and this leaks into the old types: at B = 14,
  s = 13, type (p = 0, y = 0): |Z| = 984, 1170, 1478, 1618 for c = 0, 1, 2, 3 against |J*| = 1730. So no finite cap gives
  an explicit family in this range; y ≤ s, so the uncapped rule has O(s) types per slack.
- **Blocks.** With letters ≤ 2 a block is (1 | 2 | negative)* 0 and the set after it is J* ∖ N_y up to §1b. With larger
  letters the family still exists, but its sets are not thin-complements (§1c), so I have no formula to prove.

## 3. Blocks that are not monotone-sign runs

A letter is ≥ its predecessor − 1, so a word cannot go from a positive letter to a negative one without a 0. Hence with
closing at 0 the only mixed blocks are **(negative letters)⁺ (positive letters)⁺ 0**: a rise from a negative letter straight
to a positive one. Closing also at the prefixes ending in a negative letter (`CLOSE=n`; one set per (slack, y, p) for all
negative last letters) removes them by definition: every block is then one negative letter, or (letters ≥ 1)* 0.

- It costs nothing: the family exists (B = 14 all letters, B = 16 letters ≤ 2), and the sets on the 0-ending types are
  IDENTICAL to those of `CLOSE=0` (134 of 134 types at B = 14; 131 of 131 at B = 16, letters ≤ 2).
  Recheck (9 s): `NEG=1 python3 young.py 14 12`.
- The sets Z⁻ on negative-ending prefixes, against G⁻(s) of `../l2sets`: for old types (y = 0) G⁻ ∖ Z⁻ is 4 states
  (two with d = 0, two with d = 1) at s = 13 and Z⁻ is larger than G⁻ by 510 states (other classes). For young types
  G⁻ ∖ Z⁻ has 16, 42, 122, 142 states for y = 1, 2, 3, 4 (s = 13, all letters), not confined to small d (46 of the 122 have d ≥ 5).

## 4. Statement the data supports

For words with letters ≤ 2, sets on every prefix ending in a letter ≤ 0, every block a single negative letter or
(1 | 2)* 0:  F(x) ⊇ J*(s, τ) ∖ (N_y(s) ∪ S), S sporadic (§1b) and not fitted. For letters ≥ 3 the same
statement is false after the first 0; what survives is "after about c consecutive zeros (c = largest letter of the
excursion) the omission is exactly N_y", which is not a one-block statement. A uniform version would need a second
counter (zeros since the excursion, or the largest letter still "young") next to y; not attempted.
