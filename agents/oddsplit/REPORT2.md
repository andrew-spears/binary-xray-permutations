# HIT: unimodal words with letters in {0, 1} on one side and ANY depth on the other — proved, with an explicit S; RR itself is not proved

Continues `REPORT.md` (Lemma R, Theorem E, RR-splits, Theorem A). Notation as there: e_k = d_k − 2k; for a set
S = {k_1 < … < k_m} of stones, u_j = e_{k_j} + 2·#(S^c before k_j) = d_{k_j} − 2j, and for k ∉ S,
v_k = −e_k + 2·#(S after k); N_i = #{k ∉ S : v_k ≥ i}. S is an RR-split if all u, v ≥ 0 and there are partitions with
λ + γ = sort(u), λ ∪ γ = N; then the number of solutions with the stones of S in the rows {λ_{m+1−j} + j} and the columns
{γ_{m+1−j} + j} is odd (Theorem E). "Unimodal": x (letters ≥ 0) followed by y (letters ≤ 0); t = the last stone of x;
always e_t = 0 and e_{t+1} = −1, because e_{k+1} ≥ e_k − 1.

**Proved (by hand, §1–§3):**
- **Theorem C.** Every valid unimodal word with x ∈ {0, 1}* and y arbitrary (any depth) is solvable, by an explicit
  RR-split: with m = ⌈max|y| / 2⌉, S = the ones of x number c_1 < … < c_m, c_j = Σ_{k > t} max(|e_k| − 2(m − j), 0).
  By the mirror, also x arbitrary and y ∈ {0, −1}*. This contains the old family {0,1}*{0,−1}* and all the test words
  1^a 0 −1 −2 −3 … (for 1^6 0 −1 −2 −3 it gives S = {1, 6}; for 1^15 0 −1 … −5, S = {1, 6, 15}).
- **Theorem B.** Every valid unimodal word with x ∈ {0, 1, 2}* and y ∈ {0, −1, −2, −3, −4}* is solvable (and the mirror
  class), by an explicit one- or two-stone RR-split.
- **Balance form (§1).** For the interleaved pairing λ = (N_1, N_3, …), γ = (N_2, N_4, …) the RR condition is one
  equation per stone of S: what the stone sees on its left equals what it sees on its right, where each stone of S in
  between hides 2 units. The state is that of a permutation made of cycles on disjoint intervals.

**Tested only (§4–§6):** the interleaved pairing alone ("I-split") works for every valid word without a tight cut with
n ≤ 10, and fails first at n = 11 (2 of 862 words); the least size of an RR-split equals an elementary lower bound W(e)
for every word with n ≤ 10 and is W + 1 for 2 words at n = 11; two-stone RR-splits always straddle the turn.

**NOTHING:** RR for all words is not proved; §7 says what blocks it. RR-splits with a fixed row set (every third row)
do not exist (§6), so card `thirds` is not explained by extreme terms.

## 1. The balance form of an RR-split

**Lemma I (interleaved pairing).** If 0 ≤ v_k ≤ 2m for all k ∉ S, all u_j ≥ 0, and the i-th largest of the u_j equals
N_{2i−1} + N_{2i} = Σ_{k ∉ S} clamp(v_k − 2(i − 1), 0, 2) for i = 1..m, then S is an RR-split, with λ = (N_1, N_3, …,
N_{2m−1}) and γ = (N_2, N_4, …, N_{2m}). (Immediate from the definition; clamp(a, 0, 2) = max(0, min(2, a)).) Call
such an S an **I-split**.

**Proposition 1 (balance).** S is an I-split with u_1 ≤ … ≤ u_m if and only if
- (window) every k ∉ S has −2·#(S before k) ≤ e_k ≤ 2·#(S after k), and
- (balance) for every κ ∈ S:
  e_κ + Σ_{k < κ, k ∉ S} clamp(e_k − 2σ, 0, 2) = Σ_{k > κ, k ∉ S} clamp(−e_k − 2σ, 0, 2),
  where σ = the number of stones of S strictly between k and κ.

*Proof.* The window is 0 ≤ v_k ≤ 2m. For κ = k_j the i-th largest u is u_j with i = m + 1 − j, and
u_j = e_κ + 2·#{k ∉ S, k < κ}. A stone k < κ outside S has #(S after k) = σ + m − j + 1, so
clamp(v_k − 2(m − j), 0, 2) = 2 − clamp(e_k − 2σ, 0, 2); a stone k > κ has #(S after k) = m − j − σ, so the term is
clamp(−e_k − 2σ, 0, 2). Subtract 2·#{k ∉ S, k < κ} from both sides. ∎

For m = 1 the caps never act and the balance is Σ e = 0: this is Theorem A. Without caps and screens the balance is
always the identity Σ e = 0; the equations say that capping and screening do not change it.

**Proposition 2 (cycle picture).** In an I-split with u increasing, put r_j = N_{2m−2j+1} + j and c_j = N_{2m−2j+2} + j
(the rows and columns of S). Then c_1 ≤ r_1 < c_2 ≤ r_2 < … < c_m ≤ r_m and r_j + c_j = d_{k_j}. So (R, C) is the state
of the permutation π that is the cycle i → i + 1 → … → r_j → c_j on each interval [c_j, r_j] and fixes every other
point: the stones of S are the closing stones (r_j, c_j) of the cycles, the others sit on the main diagonal (outside
the intervals) or one step above it (inside). D has an I-split with u increasing iff for some S the diagonals of S are
those of the closing stones and the other diagonals differ from those of π only by a rearrangement of the values
d − 2·(index among the stones outside S).

*Proof.* N_{2i−1} ≥ N_{2i} ≥ N_{2i+1} gives the interlacing; r_j + c_j = u_j + 2j. ∎

In general (any pairing, any order of u) an RR-split is the same statement for a permutation that is a union of two
increasing sequences (rows of R to columns of C in order, and the rest in order): |e_k| ≤ 2|S| outside S is the
statement that the second sequence stays within |S| steps of the main diagonal.

Checked for all 97 words without a tight cut at n = 9 and all 49,470 pairs (word, S): Propositions 1 and 2 agree with
the definition (640 I-splits), `balance.py 9`.

## 2. Theorem C: letters in {0, 1} on one side, any depth on the other

**Theorem C.** Let e be a valid unimodal word with x ∈ {0, 1}*, y ≠ 0, and let h = max |e_k|, m = ⌈h / 2⌉,
Y_i = #{k > t : |e_k| ≥ i}, c_j = Σ_{i > 2(m − j)} Y_i = Σ_{k > t} max(|e_k| − 2(m − j), 0) for j = 1..m.
Let k_j be the position of the c_j-th one of x. Then S = {k_1, …, k_m} is an I-split with u increasing. Hence the
number of solutions with the stones of S in rows r_j = N_{2m−2j+1} + j and columns c_j = N_{2m−2j+2} + j is odd, and e is
solvable.

*Proof.* c_1 = Y_{2m−1} + Y_{2m} ≥ 1 because h ≥ 2m − 1; c_{j+1} − c_j = Y_{2(m−j)−1} + Y_{2(m−j)} ≥ 2 for 1 ≤ j < m
because 2(m − j) < h; c_m = Σ|y| = the number of ones of x. So the k_j exist, are distinct, and k_m is the last one of
x. Call zone j the stones of x strictly between k_j and k_{j+1} (zone 0 before k_1, zone m after k_m); it has
o_j = c_{j+1} − c_j − 1 ones (c_0 = 0; o_m = 0) and z_j zeros. Put G_j = Σ_{i ≤ j} (o_i + z_i).
A stone of zone j has v = 2(m − j) − e ∈ [0, 2m]; a stone of y has v = |e| ≤ h ≤ 2m. Counting,
N_{2i−1} = Y_{2i−1} + G_{m−i} and N_{2i} = Y_{2i} + G_{m−i} − o_{m−i}, so with j = m − i
N_{2i−1} + N_{2i} = (c_{j+1} − c_j) − o_j + 2G_j = 1 + 2G_j = e_{k_{j+1}} + 2·#(S^c before k_{j+1}) = u_{j+1}.
The u_j increase with j, so u_{j+1} is the i-th largest. Lemma I. ∎

In the balance form: the stone k_{j+1} sees on its left the ones of x back to k_j (the zeros count 0, the stones before
k_j are hidden: 1 − 2 < 0), and on its right the part of each letter of y between depth 2(m − j − 1) and 2(m − j).
The proof needs only that the partial sums of x take every value: x has steps of size 1.

Checked (`thm_c.py 22 11`): the arithmetic for all words of the class with n ≤ 22 (6,436,781 words at n = 22, m up
to 3), 0 failures; the two placement counts by brute force for all words with n ≤ 11 (871 at n = 11), 0 even.

## 3. Theorem B: x ∈ {0, 1, 2}*, y ∈ {0, …, −4}*

**Theorem B.** Let e be a valid unimodal word with x ∈ {0, 1, 2}* and y ∈ {0, −1, −2, −3, −4}*. If y ∈ {0, −1, −2}*,
Theorem A applies. Otherwise let T = Σ_{k > t} max(|e_k| − 2, 0), P(k) = e_1 + … + e_k, k_1 = the first k with
P(k) ≥ T, and k_2 = t + 1 if P(k_1) = T, k_2 = t + 2 if P(k_1) = T + 1. Then S = {k_1, k_2} is an I-split, so the number
of solutions with the two stones in rows {N_3 + 1, N_1 + 2} and columns {N_4 + 1, N_2 + 2} is odd.

*Proof.* T ≥ 1, and P has steps ≤ 2, so P(k_1) ∈ {T, T + 1}. Σ|y| − T = Σ_y min(|e|, 2) ≥ 1 + 2 + 2 (y starts with −1
and passes −2 before its first letter ≤ −3). So the letters of x after k_1 have sum ≥ 4; they are ≤ 2, the last is 0 and
the one before is ≤ 1, so there are at least 4 of them, and u_2 − u_1 = e_{k_2} − e_{k_1} + 2(k_2 − k_1 − 1) > 0.
The values v: 4 − e ∈ {2, 3, 4} before k_1; 2 − e ∈ {0, 1, 2} for x after k_1; 3 for the stone t + 1 if k_2 = t + 2;
|e| ≤ 4 after k_2. So N_3 + N_4 = Σ clamp(v − 2, 0, 2) = 2(k_1 − 1) − P(k_1 − 1) + [k_2 = t + 2] + T, and
u_1 = e_{k_1} + 2(k_1 − 1). They are equal because P(k_1) = T + [k_2 = t + 2]. The other equation u_2 = N_1 + N_2 follows
from Σu = Σv. Lemma I. ∎

Here a letter 2 of x can jump over the target T; the repair is to move k_2 one step into y, which uncovers the first
letter −1 for the stone k_1 and raises its target by 1. Checked (`thm_b.py 14 10`): all words of the class with n ≤ 14
(15,400 at n = 14), 0 failures; brute force for n ≤ 10 (84 words), 0 even.

## 4. Two stones, exactly (item 1)

- **Criterion.** S = {k_1 < k_2} is an RR-split iff all v ∈ [0, 4], u ≥ 0 and min(u_1, u_2) ∈ {N_3 + N_4, N_2 + N_4}
  (the pairings {(N_1,N_3), (N_2,N_4)} and {(N_1,N_2), (N_3,N_4)}; the third gives the same sums). Checked against the
  general test for all pairs at n ≤ 9 (`balance.py 9`).
- **The variables separate.** For a unimodal word and k_1 ≤ t < k_2 with u_1 ≤ u_2, the first case reads
  e_{k_1} + Σ_{i < k_1} min(e_i, 2) = Σ_{t < i < k_2} |e_i| + Σ_{i > k_2} max(|e_i| − 2, 0):
  the left side depends on k_1 only, the right side on k_2 only (letters of x after k_1 must be ≤ 2, letters of y before
  k_2 must be ≥ −2). So a two-stone split exists when two explicit sets of integers meet. Both sides are monotone
  with steps ≤ 2 while the stone moves over letters ≤ 2 in absolute value; a step is 2 exactly at a letter ±2 (and
  larger after a letter ≥ 3). A discrete intermediate-value argument works when one side has steps ≤ 1 (Theorem C) or
  when the other side offers two consecutive values (Theorem B: T and T + 1).
- **Which words** (`two.py n`; valid words without a tight cut with max |e| ∈ {3, 4}, where one stone is impossible):

| n | words | with a two-stone RR-split | with one with k_1 ≤ t < k_2 |
|---|---|---|---|
| 8 | 1 | 1 | 1 |
| 9 | 5 | 5 | 5 |
| 10 | 30 | 30 | 30 |
| 11 | 145 | 143 | 143 |
| 12 | 629 | 607 | 607 |

  Whenever a two-stone split exists there is one that straddles the turn. The words without one all contain
  3 2 1 0 −1 −2 −3 with more weight on one side: at n = 11 they are 1 1 3 2 1 0 −1 −2 −3 −1 −1 and
  3 3 2 1 0 −1 −2 −3 −1 −1 −1. For the second: the left side takes the values 5, 6, 7 and the right side 1, 2, 3.
- For m stones: u_j depends on k_j only and every N_i is a sum of one function of each k_j, so RR is m − 1 equations of
  this separable kind in m unknowns. I found no monotone structure that gives a solution for m ≥ 3 beyond Theorem C.

## 5. Least size of S and the "+1" cases (item 2)

**Window bound.** W(e) = the least |S| such that every k ∉ S has at least ⌈−e_k / 2⌉ stones of S before it and at least
⌈e_k / 2⌉ after it. It is necessary for RR (it is 0 ≤ v ≤ 2|S|), and W ≥ ⌈max|e| / 2⌉. For a word that is not unimodal
W ≥ 2: a negative letter needs a stone of S before it and a later positive letter needs one after it.

Tested (`least.py n`, words without a tight cut):

| n | words | least RR size = W | = W + 1 | least I-split size = W | = W + 1 | no I-split |
|---|---|---|---|---|---|---|
| 9 | 97 | 97 | 0 | 97 | 0 | 0 |
| 10 | 285 | 285 | 0 | 282 | 3 | 0 |
| 11 | 862 | 860 | 2 | 841 | 19 | 2 |

So the "+1" of `REPORT.md` §4 against ⌈max|e| / 2⌉ is, for n ≤ 10, entirely the window bound: the 34 words at n = 10
with max|e| ≤ 2 and least size 2 are the non-unimodal ones. The first words above W are the two words of §4 at n = 11
(W = 2, least size 3).

Where S sits: by the window, S contains or straddles everything between the first negative and the last positive
letter. No fixed rule gives an RR-split or even an E-split (`rules2.py 9`, 97 words): S = {e_k > 0}: RR for 7 words,
E for 35; {e_k ≥ 0}: 8, 35; the prefix up to the turn: 1, 53; odd diagonals: 5, 5. So the fixed rules that are odd
splits for every n ≤ 9 are odd through terms that are not extreme. The least span (last − first + 1) of an RR-split
is at most 5 at n = 9 (worst word 3 2 1 0 −1 −1 −1 −2 −1).

## 6. Other criteria and the fixed row set (items 3 and 4)

- **I-splits** (`isplit.cpp`): every valid word without a tight cut with n ≤ 10 has one; n = 11: 860 of 862 (missing
  4 3 2 1 0 −1 −2 −3 −2 −1 −1 and 4 3 2 1 0 −1 −2 −3 −1 −2 −1); n = 12: 2,657 of 2,668; unimodal n = 13: 6,297 of 6,348.
  In every case an I-split exists iff one with u increasing exists (the two counts agree for n ≤ 12 and unimodal 13).
  The word 4 3 2 1 0 −1 −2 −3 −2 −1 −1 has the RR-split S = {2, 8}, u = (5, 9), λ = (7, 4), γ = (2, 1): the other
  pairing. So the second pairing is needed, from n = 11 on.
- **Item 3.** RR already covers every word tested (n ≤ 14), so CC/RC/CR add nothing there; I did not find a wider
  criterion with a canonical S (see the fixed rules in §5).
- **Item 4: no.** RR-splits whose stones sit in the rows r ≡ 1 (mod 3) (`fixedrows.py n 100`) exist for 1 of 5 words
  at n = 6, 0 of 13 at n = 7, 9 of 35 at n = 8, 9 of 97 at n = 9, 0 of 285 at n = 10; not even for (1, 0, …, 0, −1).
  Rows ≡ 2: 39 of 97 at n = 9; rows ≡ 0: 13; odd rows: 43. The reason is Proposition 2 and its general form: the rows
  of an RR-split are far from evenly spread (for an I-split they are the ends of disjoint intervals placed where the
  word is nonzero). So `thirds` is a statement about non-extreme terms.

## 7. What blocks a proof of RR

1. The balance equations are solved by moving one stone of S at a time, and each side moves in steps of 1 only over
   letters 0, ±1. Over a letter ±2 it moves by 2, so a target can be jumped. Theorem C is exactly the case without
   jumps; Theorem B repairs one jump with one stone of S placed in y.
2. For m ≥ 3 stones one needs m − 1 targets at once. A repair for target j (uncover a letter −1, or a letter −3 behind
   one stone, …) moves the later stones into y and changes their equations. I have no argument that the repairs can
   be made simultaneously; for x ∈ {0, 1, 2}* and y of any depth an I-split of size ⌈max|y| / 2⌉ exists for every word
   with n ≤ 12 (`x2.py`; 1,282 words at n = 12, all with two stones, so this tests Theorem B only).
3. The interleaved pairing is not enough from n = 11 on, and the least size is not always W. So a proof of RR must
   choose the pairing and sometimes one more stone; the first words where this happens are the lopsided
   3 2 1 0 −1 −2 −3 words of §4.

The smallest open statement on this line: **every valid unimodal word with x ∈ {0, 1, 2}* has an I-split** (y of any
depth). It contains Theorems A (one side), B and C, and by 1–2 it needs one new idea: a simultaneous repair of the
jumps.

## 8. Not checked

- Theorem C and B are checked by brute force only for n ≤ 11 and n ≤ 10; beyond that only the arithmetic of the rule.
- The open statement of §7 for three or more stones (it needs n ≥ 21 or so for a deep y with twos in x).
- I-splits for n ≥ 13 (non-unimodal) and n ≥ 14; whether "I-split ⟺ I-split with u increasing" has a proof.
- The second pairing in general (only m = 2 was written out); an analogue of Proposition 1 for it.
- Rows ≡ 1 mod 3 was tested for RR-splits only, not for E-splits of the other types.
- Lemma R of `REPORT.md` still rests on the dominance lemma cited there.

## 9. Recheck (under 10 minutes in total)

```
cd agents/oddsplit
python3 thm_c.py 18 10      # Theorem C: rule fails 0, even counts 0
python3 thm_b.py 14 10      # Theorem B: rule fails 0, even counts 0
python3 balance.py 9        # Propositions 1, 2 and the two-stone criterion: 0, 0, 0
python3 two.py 12           # table of §4
python3 least.py 10         # table of §5 (n = 11: 6 min)
python3 rules2.py 9         # fixed rules
g++ -O2 -o isplit isplit.cpp && ./isplit 11 v && ./isplit 12
python3 fixedrows.py 9 100; python3 fixedrows.py 10 100
python3 x2.py 12
```

## 10. Suggested cards (I did not edit `map/build.py` or `docs/state.md`)

- green, under `rrsplit`: **uni01** — "a valid unimodal word with letters in {0, 1} before the turn (or in {0, −1}
  after it) is solvable": Theorem C, with the explicit S.
- green: **uni24** — Theorem B.
- open: **isplit** — "every valid unimodal word with x ∈ {0, 1, 2}* has an I-split".
- red child of `rrsplit`: "the interleaved pairing always works" — false at n = 11 for 4 3 2 1 0 −1 −2 −3 −2 −1 −1.
- red child of `thirds`: "an RR-split with S in every third row" — false already for (1, 0, 0, 0, 0, −1).
