# thin: a small sub-machine of the interface machine — REPORT

**NOTHING** for a slack-independent thin family (every family tested dies on some valid word), with two **HIT** facts:
the right thinness parameter is the number of corners, and the corner families fail late, at explicit words (§2, §3).

Setting: `../universal/maya.py` (states (λ|μ), step `succ`). A family T *accepts* a valid word if some walk of the
word stays in T. #c(λ) = number of distinct part sizes of λ = corners of its Young diagram = blocks of stones above
the ground state in its Maya diagram.
**T(a,b)** = { (λ|μ) : #c(λ) ≤ a and #c(μ) ≤ b, or the same with λ, μ swapped }. It is closed under the mirror and has
polynomially many states per slack (`count.py`):

| slack | all pairs | T(1,2) | T(1,3) | T(2,2) |
|------:|----------:|-------:|-------:|-------:|
| 16 | 5,822 | 1,460 | 2,906 | 2,727 |
| 24 | 94,235 | 5,266 | 17,924 | 16,279 |
| 40 | 9,035,539 | 25,006 | 178,114 | 155,181 |

Everything below is computed, nothing is proved. Two programs agree on every rejection quoted (C++ `steep`/`words`,
Python `corners.py` on `maya.py`).

## 1. Data for small bounds — NOTHING

- Forced states (in every accepting family) at B = 4, 5: only (−|1) and (1|−) (`data.py`). Greedy-minimal families
  from nine deletion orders keep 27–31 of 38 states at B = 4 and 47–57 of 74 at B = 5, with no common shape.
- Exact minimum (MaxSAT, `minfam.py`): 14 of 18 states at B = 3, per slack 1, 2, 4, 7 of 1, 2, 5, 10.
- Lower bound from single cuts (forward set ∩ mirrored set must meet T, `hit.py`): 2 states per slack at B = 6, 8.
  So forced states give no thickness bound; small bounds say nothing about the shape of T.

## 2. Closed forms (`cand.py`, restricted subset construction, B ≤ 10) — all but corners fail early

| family | first rejected at slack bound |
|---|---|
| both ≤ k rows (or ≤ k columns), k = 1, 2, 3 | 2, 4, 7 |
| each of λ, μ has ≤ k rows or ≤ k columns, k = 1, 2 | 3, 8 (k = 3: none ≤ 10) |
| Durfee square ≤ 1; both hooks | 6; 6 |
| \|\|λ\| − \|μ\|\| ≤ c, c = 1, 2, 3 | 2, 3, 4 |
| λ = μ or λ = μ′ up to one box; both inside a staircase; distinct parts | 2 |
| 2-cores (both empty / ≤ 1 box each) | 3 |
| both rectangles = T(1,1) | 3: `2 1 0 0 -1 -2` |

Row, column and Durfee bounds grow with the pyramid j, j−1, …, −j, so they are not slack independent: for
j = 1..8 the smallest k is 1 1 2 2 3 3 4 4 for "each has ≤ k rows or ≤ k columns", 0 1 1 1 2 2 2 3 for "λ or μ has
≤ k rows or columns", 1 1 1 2 2 2 3 3 for Durfee ≤ k. The pyramids need only T(1,1) (checked to j = 7, slack 28):
corners are the parameter that steep words do not force. Not thin but alive to B = 10: "λ ⊆ μ or μ ⊆ λ", "λ or μ a rectangle / a hook".

## 3. The corner families — HIT (exact ranges), and they all die

| family | accepts every valid word with | first known rejected word |
|---|---|---|
| T(1,1) | ≤ 5 letters | 6 letters, slack 3 (shortest) |
| T(1,2) | slacks ≤ 16 (any length); ≤ 15 letters | 16 letters, slack 22 (shortest): `4 3 5 4 3 2 1 0 0 -1 -2 -3 -4 -5 -3 -4` |
| T(1,3) | slacks ≤ 16; ≤ 18 letters (slack up to 36) | 25 letters, slack 56: `5 4 3 8 8 7 6 5 4 3 2 1 0 -1 … -8 -8 -3 -4 -5` |
| T(2,2) | slacks ≤ 16; ≤ 18 letters (slack up to 36) | 44 letters, slack 74: x 0 0 x~, x = `10 9 … 1 3 2 2 1 2 2 2 1 2 1 1` |

- The last two words are locally minimal (`shrink.py`: no letter of x can be deleted, no run lowered), not known
  shortest. All four are in `killers.txt`; T(1,4) accepts all four; the T(1,3) word has a walk in T(2,2).
- The killers are mirror-symmetric steep words x 0ᶻ x~ with several descending runs in x: 1 run needs T(1,1),
  2 runs kill T(1,2), 3 runs kill T(1,3), 11 short runs after a pyramid kill T(2,2). I found no clean infinite
  family (m, m−1, …, 1 followed by k copies of `2 1`, mirrored, has walks in T(1,2) for m = 4, 6 and k ≤ 7, by `steep`), so "no T(a,b) works" is the
  expected answer but is not proved.
- Thinness is real while it lasts: along the T(1,2)-killer the T(2,2)-reachable sets have at most 1,754 states
  against 32,068 for the full machine, and 160 against 19,538 alive ones (`trace.py`).
- Word-dependent variant "corners(λ) + corners(μ) ≤ (descending runs of the prefix) + c": c = 1 rejects a 12-letter
  word, c = 2 accepts every word with ≤ 16 letters but is not thin (sets up to 115,289 states). NOTHING (`dyn.cpp`).

## 4. Verdict

No induction was attempted on F_T(x): the surviving T(a,b) are only alive below their killers, and the restricted
sets still have hundreds to thousands of states with no visible description.
What forces thickness, as far as the data goes: the number of corners needed grows with the number of descending
runs of a steep prefix, slowly (2, 3, 4 corners in total last to 5, 15, ≥ 18 letters). A family with
corners ≤ c·(runs) would have s^{O(runs)} states per slack; that is the smallest candidate left, and it is not a
fixed sub-machine.

## Recheck (all under 10 minutes together, except the last line)

```
cd agents/thin && g++ -O2 -o words words.cpp && g++ -O2 -o steep steep.cpp && g++ -O2 -o thin thin.cpp
./words 16 1 2              # 8 s: T(1,2) rejects the 16-letter word;  ./words 15 1 2 accepts
./words 16 2 2; ./words 16 1 3     # 25 s each: accept
for f in "1 1" "1 2" "1 3" "2 2" "1 4"; do ./steep $f - < killers.txt; done     # 12 s: 4, 3, 2, 1, 0 words without a walk
./thin 16 2 2; ./thin 16 1 3       # 30 s each: accept every valid word with slacks <= 16
python3 corners.py 5 4 3 8 8 7 6 5 4 3 2 1 0 -1 -2 -3 -4 -5 -6 -7 -8 -8 -3 -4 -5      # [(1, 4), (2, 2)]
python3 cand.py 8           # table of section 2 (3 s; cand.py 10 for the families alive to B = 10, about 5 minutes)
./words 18 2 2; ./words 18 1 3     # 8-11 minutes each
```
