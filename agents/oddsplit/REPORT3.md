# HIT: relative splits (free ends + chains) proved as a criterion, and one new infinite family (Theorem D); NOTHING for the open class of REPORT2. Also a correction to REPORT / REPORT2.

Words e_k = d_k − 2k as in REPORT.md. G(s), "central", "thin", Theorem 0 and Lemma H are those of `../l2sets/REPORT.md`; states are
(λ|γ) = (row diagram | column diagram), rows r_i = λ_i + i.

## 0. Correction to REPORT.md and REPORT2.md (found while doing this task)
The word enumerators of `ext.py`, `esplit.cpp`, `isplit.cpp`, `hsplit.cpp` pruned with a wrong bound (slack > r(r+1)/2 + r·max(e, 0) instead of
r(r+1)/2 − r·e, r = letters left) and so skipped valid words that end steeply, e.g. 2 1 0 −1 −2. They listed 5, 13, 35, 97, 285, 862, 2668
words without a tight cut for n = 6..12; the true numbers are 7, 21, 61, 184, 573, 1835, 5969. Fixed on this branch. Proofs are not affected;
`thm_b.py`, `thm_c.py`, `x2.py` have their own (correct) enumerators. Re-run with the fix:
- **RR-split for every valid word without a tight cut: still true for n ≤ 13** (19,715 words at n = 13; `esplit`). n = 14 was started and had not finished when this was written. The old "n ≤ 14, 27,225 words" covered about half of the words.
- **I-splits (interleaved pairing) fail earlier than reported**: 182 of 184 at n = 9, 565 of 573 at n = 10, 1789 of 1835 at n = 11,
  5780 of 5969 at n = 12; unimodal n = 13: 14,600 of 15,353. REPORT2's "works for n ≤ 10, fails first at n = 11" is wrong.
- Not re-run: the least-|S| table, `two.py`, `rules2.py`, `fixedrows.py`, `few.py`, `transfer.py` numbers of REPORT/REPORT2 (they used `ext.words`;
  their counts are for the smaller word list). The same `max(x, 0)` pattern occurs in `agents/interface/{lookahead_game,online_game,slack_dfa}.py`,
  `invariant.cpp`, `slack_dfa.cpp`; I did not check whether it is a bug there.

## 1. The criterion (proved)
**Lemma R′ (Lemma R without a board).** Let D = {d_1 < … < d_k}, R = {r_1 < … < r_k}, C = {c_1 < … < c_k} be sets of integers. If the multisets
{r_i + c_i − 2i} and {d_i − 2i} are equal, the number of bijections R → C with sums D is odd. Call such (D; R, C) a **chain**.
*Proof.* Lemma R of REPORT.md with λ_i = r_i − i, γ_i = c_i − i, u_i = d_i − 2i after a translation making λ_1 = γ_1 = 0 (the count and the
condition are translation invariant). The condition is also invariant under the half-turn, which is why both parts of an RR-split satisfy it. ∎

**Theorem M (mixed split).** Let the stones of D be partitioned into parts P_1, …, P_j and the rows and the columns of the board into sets
R_1, …, R_j and C_1, …, C_j with |R_i| = |C_i| = |P_i|. D has a permutation if every part is of one of two kinds:
- *chain*: (P_i; R_i, C_i) is a chain;
- *free*: for some translation (α, β) the word d − (α + β) − 2·(index in P_i) of the part is a legal prefix with all letters ≤ 1 and the
  translated (R_i, C_i) is a state of G(slack); or the same after a half-turn.
*Proof.* Each part has a placement on its own rows and columns (Lemma R′; Theorem 0), and placements of different parts do not interact. ∎
An RR-split is two chains. No joint parity is needed: every part only has to be nonempty.

**Relative split of w = x m y** (x a prefix with letters ≤ 1, slack s; y a suffix with letters ≥ −1; S ⊔ T = stones of m): parts X, S, T, Y with
S, T chains, (R_X, C_X) ∈ G(s), half-turn of (R_Y, C_Y) ∈ G(slack of −reverse(y)). In arithmetic form: for a row ρ not used by x let a(ρ) be the
number of rows of x above it, a′ the same for columns (two weakly decreasing sequences; λ_X, γ_X are their conjugates; Σa + Σa′ = s); b, b′
likewise for y (rows of y below). Then the chain condition for a part P of m is
 **{e_k + 2·#(other stones of m before k)}_{k ∈ P} = {#(other rows of m below r_i) + #(other columns of m below c_i) − a_i − a′_i + b_i + b′_i}_i**
as multisets. The only conditions on the ends are: Σa + Σa′ = s (automatic from the sums), and the state is central and not thin, i.e. the
2-core charges of λ_X and γ_X′ add up to s mod 2 ∈ {0, 1}, and the state is not in T(s) (only for 4 | s or s = 4m² + 1). Free parts are in
practice only prefixes and suffixes: a stone skipped before a stone of a free part raises its letter by 2.

**Compression (corollary of Theorem 0).** x z is solvable if for some word x̃ with the same slack (any length) x̃ z has a solution whose state
after x̃ is in G(s). For 4 ∤ s, s ≠ 4m² + 1: 1^s z solvable ⇒ x z solvable for every x with letters ≤ 1 and slack s.

## 2. One stone of m (proved): what the free end buys
Let y be empty, S = {κ}, τ = the letters of T: e_k before κ, e_k + 2 after κ, sorted τ_(1) ≤ τ_(2) ≤ …; let κ have j_r rows and j_c columns of T
below it. **The split is a relative split iff A_i := [i > j_r] + [i > j_c] − τ_(i) is ≥ 0 and weakly decreasing, A = a + a′ with a, a′ weakly
decreasing, a_κ + a′_κ = j_r + j_c − e_κ − 2·#(T before κ) fits between its neighbours in a and a′, and the state (conj a | conj a′) is in G(s).**
(Proof: the displayed condition of §1 for T and for the single stone κ; a sum of two weakly decreasing sequences is weakly decreasing.)
So a letter −h after κ, which in an RR-split needs ⌈h/2⌉ stones of S before it, here only needs h − 2 units of the slack of x above one row or
column: **a gentle prefix with enough slack absorbs depth.** Example: 1^5 2 2 1 0 −1 −2 −3 −4 has 20 one-stone relative splits (`rel.py`), no
one-stone RR-split.

## 3. Item 2: is it easier than a full RR-split?
- **Not for the smallest open case in general.** A word of that class can have no gentle end at all: 2^7 1 0 −1 −2 −3 −4 −5 (n = 14) has x and
  y empty, so a relative split is a split into chains only. (This word has no I-split with 3 or 4 stones.)
- **Yes when the gentle prefix has slack (tested on single words).** 1^5 2 1^8 0 −1 −2 −3 −4 −5 (n = 20): the target 6 of Theorem C is jumped by
  the letter 2 and the I-splits need a third stone inside the falling side ({1, 6, 17}, …). It has a two-stone relative split with
  S = {6, 14} = {the letter 2 that jumps, the last positive letter} and x in the state (−|5): the jump is repaired inside the rising side. It
  has no one-stone relative split. 1^6 2 2 1 0 −1 … −5 (n = 15) has none with ≤ 2 stones.
- All valid words with a nonempty middle, tight cuts included (1, 3, 12, 51, 197 words for n = 5..9, the counts of `../l2sets`): each has a
  relative split with at most 2 stones of m in S; one stone is enough for 11 of 12 (n = 7), 43 of 51 (n = 8), 154 of 197 (n = 9); S = ∅ never
  works. Two are needed e.g. for 3 2 1 0 −1 −2 −3 and 2 2 1 1 0 −1 −2 −3 (no gentle end).
- I have no rule for S and the state beyond Theorem D, and no proof that jumps separated by gentle stretches can always be repaired.

## 4. Theorem D (proved, explicit rule)
**Theorem D.** Let w = x m be valid, x a prefix with all letters ≤ 1 (any depth) and slack s ≥ 1, and κ a stone of m such that the letters of m
before κ are in {0, 1, 2} and those after κ in {0, −1, −2}. Let z_0, z_1 be the numbers of τ equal to 0, 1 (τ = e_k before κ, e_k + 2 after:
z_0 = #(0 before κ) + #(−2 after κ)). If z_0 ≤ s and (s, z_0) ≠ (5, 3), then w has a permutation with κ on the cell
(p − s + z_0 + 1, p + z_0 + z_1 + 1), p = |x|, and x in the state
 H = ((z_0 + 1, 1^{s − z_0 − 1}) | −) if z_0 ≤ s − 1 and (s even or z_0 even), P = ((1^{s − z_0}) | (z_0)) otherwise.
By the mirror the same holds for w = m y. x may be non-unimodal and may contain letters below −2, so this is not in Theorem A, and m has a
2 before a −2, so not in Theorem 0′. Example: x = 1^4, m = 2 1 0 −1 −1 −1 −2 −2, κ = the letter 1.

*Proof.* The sum of m is −s, which gives 2z_0 + z_1 − s = 2β + e_κ, β = #(stones of m before κ) (∗).
State H: the columns of x are 1..p; the rows not used by x are ρ_0 < ρ_1 < …, ρ_0 = p − s + z_0 + 1, with s − z_0 rows of x above ρ_0, one
above each of ρ_1..ρ_{z_0}, none above the others. κ takes (ρ_0, p + z_0 + z_1 + 1): its diagonal is 2p + 2z_0 + z_1 − s + 2 = 2(p + β + 1) + e_κ
by (∗). T takes ρ_i and the i-th other column: r_i − i = p + 1 − [i ≤ z_0], c_i − i = p + [i > z_0 + z_1], so r_i + c_i − 2i − 2p is
0 (z_0 times), 1 (z_1 times), 2 (the rest), which is the multiset of τ = d_k − 2·(index in T) − 2p. So T is a chain.
State P: the rows not used by x are ρ_0 = p − s + z_0 + 1 and p + 2, p + 3, …; the columns of x are 1..p − 1 and p + z_0. κ takes the same
cell. For T: r_i − i = p + 1, c_i − i = p − 1 + [i > z_0] + [i > z_0 + z_1]: the same multiset.
Both states have at most s ≤ p rows and fit the board. They are in G(s): with the 2-core charge c0 of `../l1sets` (even beads ≥ 0 minus even
holes < 0 of {λ_i − i}), c0((1^j)) = [j odd] and c0((g + 1, 1^j)) = [g even] − [j odd]; so H has class s mod 2 iff s or z_0 is even, and P has
class [s − z_0 odd] + [z_0 odd] = s mod 2 iff not both are odd, which holds whenever P is used. They are not self-conjugate pairs and not built
from 2 × 2 blocks (SC, E⁰). For s = 4m² + 1 the four states of A(s) must be avoided: P = ((1,1)|(3)) ∈ A(5) is the excluded case; that no other
H or P is in A(s) I checked by machine for s ≤ 80 and did not prove for larger s (Lemma 4 of `../l1sets` builds A from a doubled staircase).
By Theorem 0 x reaches the state, by Lemma R′ T has an odd number of placements. ∎

**Tested (`thm_d.py`, brute force of both counts).** n ≤ 10: 6,816 pairs (x, κ) in 755 words at n = 10 (2,461 in 286 at n = 9), 0 failures
(states H/P at n = 10: 4175/2641); without the exclusion the single failure for n ≤ 9 is 1^5 0 −1 −2 −2 with κ = the −1.

## 5. Not checked
- Theorem D for s = 4m² + 1 > 80 rests on the unproved "not in A(s)" above. Nobody else has read the proofs. The dominance lemma behind
  Lemma R is still cited from memory (REPORT.md).
- Relative splits with ≥ 3 stones, with both ends nonempty beyond the enumeration of §3, free parts in the middle, and any rule for two stones.
- No comparison with the HYBRID enumeration of the other session; `rel.py` is a slow Python search meant for single words.

## Recheck (under 10 minutes)
```
cd agents/oddsplit
python3 thm_d.py 10                                  # Theorem D, brute force (a few minutes; 9 is under a minute)
python3 rel.py "1 1 1 1 1 2 2 1 0 -1 -2 -3 -4" 1     # one-stone relative splits of the example
g++ -O2 -o /tmp/esplit esplit.cpp && for n in 9 10 11 12; do /tmp/esplit $n; done     # corrected RR table
g++ -O2 -o /tmp/isplit isplit.cpp && for n in 9 10 11; do /tmp/isplit $n; done        # corrected I-split numbers
python3 -c "from ext import words; print([len(words(n, False)) for n in range(2, 11)])"   # 1 2 4 9 22 59 167 490 1486
```
Suggested cards (I did not edit `map/build.py`): green child of `rrsplit`/`upone`: "mixed split" (Theorem M) and Theorem D; a correction on
`rrsplit` (tested n ≤ 13 on the full word list; I-splits fail from n = 9).
