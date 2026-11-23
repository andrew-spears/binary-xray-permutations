# onehigh: one high stone (a single letter 2) — REPORT

**Item 1: HIT** (exact rule for what is missing after a letter 2, tested; the permanent part proved).
**Item 2: NOTHING** as a proof; the theorem is reduced to one repair statement (X), which holds in every test.
**Item 3: HIT** (the smallest obstruction, proved, and a sub-family that is closed backwards under 2, proved).

Setting and notation: `../l1sets/REPORT.md`, `../l2sets/REPORT.md` (state u = (M, B), class c = a + b, G, G⁻, T, Lemma G).
level(u) = max(c, 1 − c): central = level 1; level 2 = class 2 (even slack) or −1 (odd slack).
Words: x has letters ≤ 1 and slack s₀; after a letter 2 the next letter is 1, and the first negative letter is a −1
that follows a 0. So the letters after the 2 are **1^j 0 e …** with j ≥ 1 and e ∈ {−1, 0, 1}.

Recheck: `cd agents/onehigh && sh runs.sh` (40 s, output `out_runs.txt`; no line FAIL or NO CHAIN).

## 1. What is missing after one letter 2 (item 1)

**Rule (tested: s₀ ≤ 10, slack ≤ 14, `exit.py ones 14`, `exit.py all 8 7 13`).** Start from G(s₀) ⊆ F(x).
| prefix | part of G(s) that is not reached |
|---|---|
| x 2 1^j, j ≥ 1 | the four hooks (s\|−), (−\|s), (1^s\|−), (−\|1^s), plus a transient set (up to 42 states for j = 1), empty for j ≥ 4 when s₀ ≥ 1 |
| x 2 1^j 0 | (s\|−), (−\|s), plus at most 2 more states when j ≤ 2; nothing more for j ≥ 3 |
| x 2 1^j 0 e …, e ∈ {0, 1} | nothing: all of G(s) (s₀ ≥ 1) |
| x 2 1^j 0 … 0 −1 | nothing: all of G⁻(s) (every s₀) |

So a letter 1 keeps the hooks out and shrinks the transient part; the first 0 brings back the two column hooks and
ends the transient part; one more letter of any kind after that 0 brings back everything.
At s₀ = 0 only, a few states stay out longer along 0 1 0 1 … (2|2, 11|11, ±311, ±52: 6 words of 720); a −1 repairs them.

**Not a function of (slack, letters since the 2).** The hooks are missing for every x (Lemma C). The transient part
depends on x: it is what G(s₀) alone gives, and it is smaller when F(x) has non-central states (x containing a 0 or a
negative letter). Example: after x 2 1 with s₀ = 3, 12 states of G(6) are missing for x = 1 1 1 and 4 (the hooks) for
x = 1 1 1 0 (`exit.py true 12`: 28 of 99 prefixes differ). After the first 0 the difference is gone in all 99.

**Why (proved).** Write M₀ = {k/2 : k ∈ M even}, M₁ = {(k − 1)/2 : k ∈ M odd}, same for B (2-quotient; charges
a, −a, b, −b). The e-predecessors with k even / odd are the elements of
e = 1: M₀ ∖ B₀, M₁ ∖ B₁; e = 0: M₀ ∖ B₁, M₁ ∖ (B₀ − 1); e = 2: M₀ ∖ (B₁ + 1), M₁ ∖ B₀; e = −1: M₀ ∖ (B₀ − 1), M₁ ∖ (B₁ − 1).
For diagrams X, Y of charges p, q: |X ∖ Y| = p − q + |Y ∖ X|. This is Lemma G, with the equality cases:

- **Lemma A (tight states).** A central state has no central 2-predecessor iff M₁ = B₀ (c = 0), M₀ = B₁ + 1 (c = 1).
  It has no level-2 0-predecessor iff M₀ = B₁ (c = 0), M₁ = B₀ − 1 (c = 1). It has no level-2 2-predecessor iff
  M₀ ⊆ B₁ + 1 (c = 0), M₁ ⊆ B₀ (c = 1).
- **Lemma B (level 2 is robust).** A level-2 state has ≥ 1 central 2-predecessor and ≥ 2 central 0-predecessors, and
  its predecessors under ±1 are level 2 (Lemma G with |c − ½| = 3/2).
- **Lemma C (hooks).** (−|1^m) has no 2-predecessor and its only 1-predecessor is (−|1^{m−1}); the only 1-predecessor
  of (s|−) is (−|1^{s−1}) and its only 0-predecessor is (−|1^s). (M = ℤ_{<0}, B = {m − 1} ∪ ℤ_{<−1}; M = {s − 1} ∪ ℤ_{<−1},
  B = ℤ_{<0}.) Hence, **for every prefix p whatever its letters**: (−|1^s), (1^s|−) ∉ F(p 2 1^j) for j ≥ 0, and
  (s|−), (−|s) ∉ F(p 2 1^j) and ∉ F(p 2 1^j 0) for j ≥ 1.
- **Lemma D (the two routes exclude each other at j = 0).** After x 2 1^j 0 a central state u₁ is reached through a
  level-2 0-predecessor (route L) or through a central one (route C). If u₁ has no level-2 0-predecessor, every central
  0-predecessor u₂ of u₁ has no central 2-predecessor: for c = 0 and k = 2i + 1, u₂ has quotient
  ((M₁ ∖ i) + 1, M₀; M₀, (B₀ − 1) ∪ i), whose second and third diagrams are equal. If moreover the common diagram
  (M₀ = B₁, resp. M₁ = B₀ − 1) is not a half-line, every 1-predecessor of every such u₂ has a central 2-predecessor
  (it would need (M₀ ∖ m) + 1 = M₀ or M₀ + 1 = M₀ ∪ m). So the 1 after the 2 is what makes route C work.

Sizes (`fam.py 13`, slack-only over j): route L alone misses 15–20% of G(s) after the first 0 (the L-tight states:
208 of 1,176 at slack 13); route C alone misses the transient part; together they miss the two hooks and ≤ 6 states.
Lemmas A–D are checked on all 3,132 states of slack ≤ 12 (`tight.py`).

## 2. One letter 2: reduction, no proof (item 2)

**(X)** For s₀ ≥ 0, j ≥ 1, y ∈ {0, 1}*: G⁻(s) ⊆ step_{2 1^j 0 y 0 −1}(G(s₀)) (also with y 0 dropped), and for s₀ ≥ 1,
e ∈ {0, 1}: G(s) ⊆ step_{2 1^j 0 e}(G(s₀)).

**Proved: (X) ⟹** every valid word whose letters are ≤ 2, with a 0 and one more letter after it between any two
letters 2, has a permutation; in particular every valid word with exactly one letter ≥ 2. *Proof.* Invariant of
Theorem 0 (G after 0, 1; G⁻ after a negative letter), which holds up to each 2 and, by (X), again one letter after the
first 0 that follows it; in between nothing is claimed. The word ends at slack 0, so the last 2 is followed by 1^j 0 … 0 −1. ∎
(With exactly one letter ≥ 2 that letter is 2: a letter h ≥ 3 is followed by a letter ≥ 2.)

**(X) tested, no failure:** all s₀ ≤ 8 and all words 2 1^j 0 y e with ≤ 8 letters after the 2, slack ≤ 13 (1,522 words
with s₀ ≥ 1, 537 exits); every target with ≤ 1 and ≤ 2 part sizes at slack 23, 24 (68,970 pairs, by backward search);
400 random targets at slack 34..96.

**Why there is no proof.** The Theorem 0 pattern needs explicit families for the two types "x 2 1^j" and "x 2 1^j 0".
The second is G(s) minus two hooks and ≤ 2 states, but its proof needs the first, and the first is not thin: the
central part depends on j and on x (§1), and neither route has a margin: route L fails on the L-tight states and
route C on the 2-tight ones (Lemma A), 15–20% of G each. What is missing is a description of the central states
reached after x 2 1^j from G(s₀) that is exact enough to show the two failure sets meet only in the hooks; Lemma D is
the first step (j = 1, non-half-line case; 125 of the 494 L-tight states of slack ≤ 12).

**Height and separation (tested only, `exit.py block 13`, s₀ ≥ 3).** After the blocks 2 2 and 2 1 2 followed by 1^j,
G is back after 0 0 and one more letter (35 of 35), not after one 0. After 3 2 it is not back after 0 0 0 (2 states
missing), after 4 3 2 not after 0 0 −1 (30 missing). So the number of zeros needed grows with the level the block
reaches (one per letter 2 in a row; more for odd high letters), and "separated" means: a 0 and one more letter
after each single 2.

## 3. Smallest obstruction and a weaker target (item 3)

- **Obstruction (proved, Lemma C).** For every x and j ≥ 1, (s|−) ∉ F(x 2 1^j 0) and four hooks ∉ F(x 2 1^j): no family
  that contains G(s) can serve these two types, at any slack, and the bridging state (s|−) of Theorem 0′ is one of the
  missing ones. A proof of (X) must carry "G minus hooks minus a j-dependent set" through the 1's.
- **Sub-family closed backwards under 2 (proved, Lemma B + Lemma G).** Level-2 states: every one has a central
  2-predecessor, and at most one of them in E⁰, so Level2(s) ∖ Θ(s) ⊆ F(x 2), where Θ(s) = level-2 states all of whose
  central 2-predecessors are in T(s − 2) (4, 2, 2 states at s = 6, 7, 10; none at the other s ≤ 13). Level 2 is closed
  under the letter 1 except for (λ|λ′) and what Θ kills (largest slack-only family: Level2 minus 2, 4, 5 states at
  s = 6, 7, 10, `fam.py`). So after x 2 1^j almost all of level 2 is reached, with a margin; the loss is at the next 0,
  where a central state needs a level-2 0-predecessor (count ≥ 0).
- **Weaker targets that fail.** A sub-family of the central class alone cannot be closed under 0 after the first zero
  (the largest one inside the central states reached after 2 1^j 0 is empty at every slack ≤ 13: the central
  0-predecessor is often unique, so removing the hooks removes everything). The exit step with route L alone gives
  G(s) but not G⁻(s) (2 and 4 states of E⁰ ∪ SC missing at slack 8, 12), which is not enough for a following −2.
