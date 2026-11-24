# intervals2: the interval-order version (report)

**Overall: NOTHING on the full statement.** The interval-order version is neither proved nor refuted, and I have no
reduction to a smaller statement that I can prove equivalent. What is below: two HITs (one computer-assisted result
for every n, one hand-proved obstruction) and seven failed attempts with their counterexamples.

Notation. D = (d_1 < … < d_n) valid; letters e_i = d_i − (2i − n − 1) (so e_1 ≥ 0, e_{i+1} ≥ e_i − 1); slack
f(j) = e_1 + … + e_j ≥ 0, f(n) = 0. Machine = `agents/intervals/pm.py` (form (b) of the task). F(x) = set of states
the machine can be in after reading the prefix x. List form (form (a)): a list v_1 … v_n (an ordering of D, the order
of right endpoints) is *realizable* iff the peel "remove the last entry k, need 0 ≤ k ≤ (length − 1), add 1 to the
first k entries" runs to the empty list (`lib.py: decode`); it is deterministic, so the only freedom is the order.

Recheck everything: `sh agents/intervals2/recheck.sh` (under 1 minute, 3.5 GB of memory; output in `out.txt`).

---

## HIT 1 — bounded slack, every n (computer-assisted, not a hand proof)

**Claim.** For every n and every valid D whose slack satisfies f(j) ≤ 22 for all j, there is an interval order with
values D. In particular the interval-order version holds for every valid D with n ≤ 14 (n ≤ 13 was known from
`pm.py`; n = 14 is new).

**Range.** B = 22 run once (238,070 pairs (F, last letter), none empty, 39 s, 5.8 GB). The recheck runs B = 21
(158,341 pairs, 22 s, 3.5 GB), which is what n ≤ 14 needs.

**Why the finite computation covers every n (hand proof).**
1. F(x e) = ⋃_{λ ∈ F(x)} succ(λ, e): by definition of the machine.
2. A letter e′ may follow a prefix with last letter e and slack s only if e′ ≥ e − 1 and s + e′ ≥ 0 (first letter:
   e′ ≥ 0). These conditions depend only on (s, e), and s = |λ| for any λ ∈ F(x).
3. So the pair (F(x e′), e′) is a function of the pair (F(x), e) and e′. `bounded.py B` starts from ({∅}, no letter)
   and closes under all e′ allowed by 2 with s + e′ ≤ B. Every prefix of every valid word whose slack stays ≤ B is
   reached (induction on its length), whatever n is. The set of pairs is finite (partitions of at most B; letters
   between −B and B).
4. If no reached pair has F = ∅, then F(w) ≠ ∅ for every such complete word w, and a run of the machine is an interval
   order with values D (NOTES.md, section 'Interval orders').
5. Slack bound: for a valid word of length n = a + b, f(a) ≤ ab/2 ≤ n²/8. Proof: put e = e_a. Earlier letters satisfy
   e_i ≤ e + (a − i), so f(a) ≤ a e + a(a − 1)/2. Later letters satisfy e_i ≥ e − (i − a) and sum to −f(a), so
   f(a) ≤ −b e + b(b + 1)/2. Multiply the first by b, the second by a, add: (a + b) f(a) ≤ ab(a + b)/2. With e an
   integer, the smaller of the two bounds, maximised over a and e, is 21 for n = 13 and 14 and 28 for n = 15
   (`maxslack.py 16 11` prints this table, and the true maximum by enumeration for n ≤ 11, which is equal to it).

**Why it matters / status.** A complete finite search, so as trustworthy as `bounded.py` and `pm.py: succ`; steps 1–5 are checkable by
hand. It is the interval-order analogue of the existing 'Bounded slack, all n' result for permutations (docs/state.md,
agents/interface/slack_dfa.cpp, B ≤ 16). It says nothing about unbounded slack.

**Numbers that may help.** Number of distinct sets F(x) of slack s = 0..7: 1, 1, 2, 5, 9, 17, 38, 57 (the same in
the runs B = 10, 12, 21; for s ≥ 8 the count still grows with B: 125, 127, 127). The number of pairs grows by a
factor of 1.5 to 1.65 per unit of B (2,392 at B = 12; 17,311 at 16; 103,065 at 20; 238,070 at 22). I did not find
what information about x determines F(x).

## HIT 2 — no online rule (hand proof)

**Claim.** There is no rule that chooses m at each step from the letters read so far (with unlimited memory of the
past, but no knowledge of later letters) and solves every valid word. Witness: prefix x = 3 2 1 0 −1 with the two
endings z1 = −2 −3 (n = 7, D = −3..3) and z2 = −2 −1 −2 (n = 8).

**Proof** (forwards only; the rule is: m = 0 or a corner, m ≥ −e, top m parts lose 1, new part y = e + m ≥ λ_{m+1},
y = 0 only if m = ℓ(λ)).
States after x, letter by letter:
- 3: ∅ → (3).
- 2: from (3): m = 0 has y = 2 < 3, no; m = 1: y = 3 → (3, 2).
- 1: from (3, 2): m = 0: y = 1 < 3, no; m = 1: y = 2 → (2, 2, 2); m = 2: y = 3 → (3, 2, 1).
- 0: from (2, 2, 2) (corner 3 only): m = 0: y = 0 with m < ℓ, no; m = 3 → (3, 1, 1, 1).
  From (3, 2, 1): m = 0, no; m = 1: y = 1 < λ_2 = 2, no; m = 2: y = 2 → (2, 2, 1, 1); m = 3: y = 3 → (3, 2, 1).
- −1 (m ≥ 1): from (3, 1, 1, 1) (corners 1, 4): m = 1: y = 0, no; m = 4 → (3, 2).
  From (2, 2, 1, 1) (corners 2, 4): m = 2: y = 1 → (1, 1, 1, 1, 1); m = 4 → (3, 1, 1).
  From (3, 2, 1): m = 1: y = 0, no; m = 2: y = 1 → (2, 1, 1, 1); m = 3: y = 2 → (2, 2, 1).
So F(x) = {(3, 2), (3, 1, 1), (2, 2, 1), (2, 1, 1, 1), (1, 1, 1, 1, 1)}.
Next letter −2 (m ≥ 2), common to both endings; each state has one legal move:
(3, 2): m = 2, y = 0 → (2, 1). (3, 1, 1): corners 1, 3; m = 3, y = 1 → (2, 1). (2, 1, 1, 1): corners 1, 4; m = 4,
y = 2 → (2, 1). (2, 2, 1): m = 2 has y = 0 with m < ℓ, no; m = 3, y = 1 → (1, 1, 1). (1⁵): m = 5, y = 3 → (3).
A last letter −c ends in ∅ only from the state (1^c): every part must vanish, so all parts are 1, m = ℓ, and the
new part m − c is 0.
- z1 = −2 −3: after −2 the state must be (1, 1, 1). Only (2, 2, 1) gives it.
- z2 = −2 −1 −2: after −2 −1 the state must be (1, 1). Letter −1 from (1, 1, 1): only m = 3, y = 2 → (2), no.
  From (3): m = 1, y = 0 → (2), no. From (2, 1): m = 1 has y = 0 with m < ℓ, no; m = 2, y = 1 → (1, 1), yes.
  So exactly (3, 2), (3, 1, 1), (2, 1, 1, 1) work.
The state after x must be (2, 2, 1) for z1 and must not be (2, 2, 1) for z2. A rule that sees only x is in one state
after x, so it fails on x z1 or on x z2. Both words are valid (partial sums 3 5 6 6 5 3 0 and 3 5 6 6 5 3 2 0;
D = (−3, …, 3) and (−4, −3, −2, −1, 0, 1, 4, 5)). ∎
`online.py 4 8` finds the same witness and the same two sets of states, and finds no witness of smaller total length
among words of length ≤ 8. (The same sets come out of the cut form: conj F(3 2) = {(2, 2, 1)} and
conj F(2 1 2) = {(3, 2), (3, 1, 1), (2, 1, 1, 1)}.)

**Why it matters.** `rules.py` showed that seven greedy rules fail; this shows that every rule of that kind fails. A
proof through the machine in order of diagonals cannot build one run letter by letter; it has to be a statement
about the sets F(x), or about both sides of a cut.

---

## Failed attempts (each is a precise statement that is FALSE; candidates for red children of `intervalorder`)

All in list form. Counts are exhaustive over all valid D of the stated n.

1. **Right endpoints in order of value** (list = D sorted).
   False first at n = 7, only for (−4, −3, −1, 0, 1, 3, 4) = word 2 1 1 0 −1 −1 −2. By hand: peel 4 →
   (−3, −2, 0, 1, 1, 3); peel 3 → (−2, −1, 1, 1, 1); peel 1 → (−1, −1, 1, 1); peel 1 → (0, −1, 1); peel 1 → (1, −1);
   last entry −1 < 0. (After three peels the list is −1 −1 1 1, the multiset of `subex.py`.) Failures:
   n = 7: 1 of 59; 8: 7 of 167; 9: 32 of 490; 10: 132 of 1,486; 11: 526 of 4,639; 12: 2,030 of 14,805 (`sorted.py 12 0`).
2. **Right endpoints or left endpoints in order of value** (list sorted, or the same for −D). Fails for both at once:
   n = 7: 1; 8: 6; 9: 22; 10: 75; 11: 262; 12: 914 (`sorted.py`). The n = 7 set is the one in 1 (it equals −D).
3. **Always peel a current maximum** (some order of D such that every peeled entry is a largest entry of the current
   list; this is the peel of the any-poset theorem with 'the k smallest' replaced by 'the first k of the list'). False at n = 6 for
   (−4, −2, −1, 1, 2, 4) = word 1 1 0 0 −1 −1 (all 720 orders tried); 8 of 59 at n = 7, 40 of 167 at n = 8
   (`classA.py 8 max`). The sorted list does work for this set: (−4, −2, −1, 1, 2, 4) → (−3, −1, 0, 2, 2) → (−2, 0, 0, 2) →
   (−1, 1, 0) → (−1, 1) → (0) → ∅. The third peel has a tie across its cut (0 | 0) and the fourth peels 0 while 1 is
   present. So a tie across the cut does not by itself block an interval order, and peeling non-maxima is necessary.
4. **Peel a current maximum or an entry equal to 0** (an isolated element): false at n = 7 for (−6, −3, −1, 0, 2, 3, 5)
   and (−5, −4, −1, 0, 2, 3, 5); 13 of 167 at n = 8 (`classA.py 8 A`).
5. **Stay inside distinct sets** (some order of D whose peel has distinct entries at every stage, so that the
   induction could stay inside the conjecture's own class): false at n = 4 for (−2, −1, 1, 2); 4 of 9 at n = 5,
   11 of 22 at n = 6 (`hd.py`). Lists with repeated entries are unavoidable, and realizability of a multiset depends
   on its order (−1 −1 1 1 has none), so the induction hypothesis has to be about lists.
6. **Extreme run from the left, extreme run from the right, meeting at some cut** (m always largest / always smallest
   legal on x, the same on z̄, some cut where the two states are conjugate; four combinations). All four false at
   n = 7 on 2 1 1 0 −1 −1 −2; at n = 8 they miss 33, 4, 4, 6 of 167 (`twophase.py 8`). So the
   two extreme runs are not enough.
7. **A monotone fixed point.** For the sorted list the up-numbers solve u_t = #{i > t : d_i + u_i ≥ t}, and the map
   is monotone, but the solution is unique (computed from t = n down) and the content is 0 ≤ d_t + u_t ≤ t − 1, which
   monotonicity does not give. No use.

Tested only, no proof: every valid D with n ≤ 9 has a realizable list with at most 2 inversions relative to the
sorted list (n = 9: 458 with 0, 31 with 1, 1 with 2; `inversions.py 9 0`). I found no rule for which pair to swap.

Repeats: (−1, −1, 1, 1) is the only M-multiset of size 4 with no interval order (1 of 16; `multi.py 4 5`), as in
`subex.py`.

---

## Does any of this survive 'insert at position k + 1' (the real conjecture)?

- **HIT 1 (finite closure for bounded slack).** Survives, and is already there: it does not use the recursion at
  all, only that the object can be built in order of diagonals with a state bounded by the slack. For permutations
  this is the automaton A_B of agents/interface (B ≤ 16). It breaks at the same place in both problems: the number of
  states grows exponentially in B and nothing is said for unbounded slack.
- **HIT 2 (no online rule).** This is an obstruction, proved here only for the interval machine. I did not test the
  permutation interface machine for the same statement; the argument (two endings whose sets of good states after a
  common prefix are disjoint) is a finite search there too.
- **The list peels (attempts 1–5)** are the ones written in the language of the recursion, and all of them already
  fail for 'insert at the end', so there is no technique to carry over. What carries over is negative: an induction
  on this recursion cannot keep the list sorted by value, cannot keep the values distinct, and cannot peel only
  maxima. For 'insert at position k + 1' one peels any entry whose value equals the number of entries before it
  (instead of the last entry, whatever its position); I did not run the corresponding tests.

## What I would try next (not done)
The closure in HIT 1 keeps about 1.6^B sets F(x). Find the invariant of x that determines F(x) (the counts
1, 1, 2, 5, 9, 17, 38, 57 by slack are the place to start), then prove F(x) ≠ ∅ from it. HIT 2 says this, not a rule
for one run, is the shape a proof through the machine must have.

## Files
`lib.py` (valid sets, values of a triangle k, peel), `bounded.py`, `maxslack.py` (HIT 1), `online.py` (HIT 2),
`sorted.py`, `classA.py`, `hd.py`, `twophase.py`, `inversions.py`, `multi.py` (failed attempts), `recheck.sh`, `out.txt`.
