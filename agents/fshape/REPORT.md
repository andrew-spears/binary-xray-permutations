# HIT (a disproof and a diagnosis); NOTHING on an exact description of F(x)

Notation as in `agents/interface/SHORTEN_BRIEF.md`: stone j of a prefix x has row + column = 2j + e_j; F(x) = set of
(rows used, columns used); states of words of different lengths are compared after the shift Sh(A) = (A + 1) ∪ {1}.

## 1. PEAK is false as a set inclusion (proved; slack 16)
**Claim.** For x = (3, 4, 3, 3, 2, 1): F(x 0) ⊄ F(x 1 0 −1). Three of the 3,426 states of F(x 0) are missing.
One of them: rows = columns = {1, 2, 3, 4, 7, 8, 11}.

**Proof.** (a) It is reachable for x 0 (sums 5, 8, 9, 11, 12, 13, 14): stones (1,4) (2,7) (3,11) (4,8) (7,1) (8,3)
(11,2). (b) Shifted twice it is rows = columns = {1, 2, 3, 4, 5, 6, 9, 10, 13}, to be filled with the sums
5, 8, 9, 11, 12, 13, 15, 16, 17 of x 1 0 −1. No sum is ≡ 2 (mod 4), so a row ≡ 1 never meets a column ≡ 1. The four
rows ≡ 1 (1, 5, 9, 13) must use columns ≡ 0, 2 or 3; there is one column ≡ 0 (4) and one ≡ 3 (3), so at least two of
these stones sit in columns ≡ 2 and have sum ≡ 3. By symmetry at least two stones in columns ≡ 1 sit in rows ≡ 2 and
have sum ≡ 3. That is four stones with sum ≡ 3 (mod 4), but only 11 and 15 are available. ∎

**Why it matters.** With the parent's slack-14 failures of ZERO and RUN(2,1), none of the three shortening rules is a
set inclusion of reachable sets. The missed states are not dead ends (`alive.py`): e.g. rows {1,2,3,4,5,7,11}, columns {1,3,4,5,7,8,11} extends to
a permutation of size 13 with word x 0 y, y = (−1, −2, −3, −4, −3, −3) (printed by `peak16.py`). The longer word x 1 0 −1 y is still
solvable, through a different state at the cut. So an induction by shortening must let the state at the cut depend
on the continuation; restricting the inclusion to completable states does not rescue it.

**Range.** Every legal prefix of length ≤ 7 with letters ≤ 4 and last letter ≤ 1, no slack bound (2,656 prefixes,
slack up to 28): PEAK fails after exactly two words up to leading zeros, x above and (3, 4, 3, 2, 3, 2, 1) (slack 18,
1 of 8,281 states). Letters ≤ 3, length ≤ 7 (2,332 prefixes, slack up to 21): no failure. ZERO did not fail on these
short prefixes (999 tests).

**Recheck.** `cd agents/fshape; python3 peak16.py` (2 seconds: brute force, the placements, and the window machine
of `agents/interface/rewrite.py` at bound 17); `python3 peak_short.py 6 4` (5 seconds, finds it);
`python3 peak_short.py 7 4` (1 minute, the range above).

## 2. Why the inclusions break: residue counts (proved necessary condition)
**Lemma (residue counts mod m).** If (A, B) is in F(x), then for every m ≥ 2 there are integers n(i, j) ≥ 0
(i, j mod m) with Σ_j n(i, j) = #{rows ≡ i}, Σ_i n(i, j) = #{columns ≡ j}, Σ_{i+j≡s} n(i, j) = #{sums ≡ s}.
Proof: n(i, j) = number of stones in a row ≡ i and a column ≡ j. m = 2 is card `paritycount`.

**Every missed state found so far violates it (and so has no fractional placement either), each time because the
sums of the longer word avoid a residue class:**

| rule | x | slack | modulus | class with no sum |
|---|---|---|---|---|
| ZERO | (2, 3, 3, 2, 2, 1, 1, 0) | 14 | 3 | 2 |
| RUN(2,1) | (4, 3, 2, 1) | 10 → 14 | 7 | 3, 4 |
| RUN(2,1) | (4, 3, 2, 1, 0) | 10 → 14 | 8 | 3, 4, 5 |
| PEAK | (3, 4, 3, 3, 2, 1) (all three missed states) | 16 | 4 | 2 |
| PEAK | (3, 4, 3, 2, 3, 2, 1) | 18 | 9 | 2, 3, 7 |

Mechanism in the first PEAK case (k = length of x): the short word has one stone with sum 2k + 2; the long word
replaces it by 2k + 3, 2k + 4, 2k + 5, none ≡ 2k + 2 (mod 4), and the shift by 2 preserves row + column mod 4. No sum
of x is ≡ 2k + 2 (mod 4), so a pairing of residue classes that the short word used once is forbidden in the long word.
So the obstruction is not 2-adic: moduli 3, 7 and 9 occur. Recheck: `python3 counts.py` (1 second), `python3 zero14.py`.

## 3. NOTHING: no exact description of F(x)
Tested on every legal prefix of length ≤ K with slacks ≤ B, against every state of the right slack:
- **Plain LP** (fractional placement): exact for K = 5, B = 11 (0 exceptions). Not exact: K = B = 7 has 114
  unreachable LP-feasible pairs of 69,089 unreachable (158,680 pairs); first x = (2, 1, 1, 1, 1, 0), rows
  {1,2,3,4,5,8}, columns {1,2,4,5,6,7} (slack 6).
- **Parity test** (card `parity`: choose the row parity of every sum, then LP): exact for K = B = 7. Not exact for
  K = B = 8: first x = (1, 1, 1, 0, 1, 2, 2), rows {1,2,3,4,5,6,8}, columns {1,2,3,4,7,8,10} (slack 8). The rows
  have a hole, so the statement of card `parity` (rows 1…m) is not contradicted; its extension to row holes is false.
- **Mod-3 test** (same with the row residue mod 3 of every sum): no exception for K = B = 8 (914,233 pairs, 411,395
  unreachable, 1,055 of them LP-feasible, 8 pass the parity test, 0 pass the mod-3 test). The mod-4 test also rejects
  the 8. Given how depth 0 and depth 1 failed, I expect the mod-3 test to fail at larger slack; not a conjecture.
- **LP + integer residue counts mod 2, 3, 4, 5, 6, 8**: not exact (all 114 pairs above pass).
The 2-adic recursion is trivially exact once 2^j exceeds the board; the data say only that each fixed depth fails
at some slack (depth 0 at 6, depth 1 at 8). No closure property of F(x) beyond row/column swap was found.
Recheck: `python3 survivor.py` (2 seconds); `python3 exact2.py 7 7` (70 seconds); `python3 exact2.py 8 8` (11 minutes).

## 4. On the common core (parent's question, `agents/majority/`)
- No closed form found. For slack s ≤ 7 the core C(s, l) = ∩ F(x) (last letter l ∈ {0, 1}) is cut out by about s
  short prefixes (descending runs and near-constant words), not by one or two: `python3 core_gen.py 9 7` (3 seconds).
- The forcing argument for s = 1 does not extend: it needs a suffix whose set A(y) is one state and its mirror. By
  reversing the board A(y) is an F of the reversed word, and the smallest F at slack 2, 3, 4 with last letter ≤ 1
  has 4, 6, 13 states (prefixes of length ≤ 8, slacks ≤ 6).

## Proved / only tested
Proved: section 1 (explicit placement + counting argument), the lemma of section 2. Only tested: every "exact for"
statement, the counts of failures, the ranges. Files: `core.py` (F by brute force), `lp.py`, `counts.py`, `cert.py`
(weight certificates of LP infeasibility), `alive.py`, `find_fail.py` (words for the slack-14 failures, slow; output in `fail14.log`), `anyT.py` (random boards).
