# onehigh: one high stone (a single letter 2) — REPORT

**Item 1: HIT** — rule for what is missing after a letter 2 (tested, slack ≤ 14); the permanent part (hooks) is proved.
**Item 2: NOTHING** — no proof. Proved only: the theorem follows from one repair statement (X); (X) holds in every test.
**Item 3: HIT** — smallest obstruction (proved); the level-2 states as the sub-family with a margin (counts proved, family tested).

Setting and notation: `../l1sets/REPORT.md`, `../l2sets/REPORT.md` (state u = (M, B), class c = a + b, G, G⁻, T, Lemma G).
level(u) = max(c, 1 − c): central = level 1; level 2 = class 2 (even slack) or −1 (odd slack).
Words: x has letters ≤ 1 and slack s₀. After a letter 2 the next letter is ≥ 1, and the first negative letter is a −1
that follows a 0. So with one letter 2 the letters after it are **1^j 0 e …**, j ≥ 1, e ∈ {−1, 0, 1}.

Recheck: `cd agents/onehigh && sh runs.sh` (25 s; output `out_runs.txt`; no line with FAIL or NO CHAIN).

## 1. What is missing after one letter 2 (item 1)

**Rule (tested).** Sets computed from G(s₀) ⊆ F(x); s₀ ≤ 10 and slack ≤ 14 for rows 1–2 (`exit.py ones 14`), s₀ ≤ 8, at
most 7 letters 1^j 0 y, slack ≤ 13 for rows 3–4 (`exit.py all 8 7 13`: 1,882 words with e ∈ {0, 1}, 537 with e = −1).

| prefix | part of G(s) (G⁻(s) in row 4) that is not reached |
|---|---|
| x 2 1^j, j ≥ 1 | the four hooks (s\|−), (−\|s), (1^s\|−), (−\|1^s), plus up to 42 more states; only the hooks for j ≥ 4, s₀ ≥ 1 |
| x 2 1^j 0 | (s\|−), (−\|s), plus at most 2 more states; only these two for j ≥ 3, s₀ ≥ 1 |
| x 2 1^j 0 y e, y ∈ {0,1}*, e ∈ {0, 1} | nothing, for s₀ ≥ 1 |
| x 2 1^j 0 −1 and x 2 1^j 0 y 0 −1 | nothing, for every s₀ |

A letter 1 keeps the four hooks out and shrinks the rest; the first 0 brings back the column hooks and leaves at most
two states besides the row hooks; one more letter of any kind brings back everything.
Only for s₀ = 0, six words 0 1 0 1 … leave one or two states out (2|2, 11|11, 1|22, −|311, −|52 and mirrors); a −1 repairs them.

**Not a function of (slack, letters since the 2).** The hooks are missing for every x (Lemma C). The rest depends on x:
it is smaller when F(x) has non-central states (x with a 0 or a negative letter). Example with s₀ = 3: after x 2 1,
12 states of G(6) are missing for x = 1 1 1 and only the 4 hooks for x = 1 1 1 0 (`exit.py true 12`: 9 prefixes x,
11 continuations z, 28 of 99 differ from the set computed from G(s₀)). One letter after the first 0 there is no
difference in the 36 cases.

**Why (proved).** 2-quotient: M₀ = {k/2 : k ∈ M even}, M₁ = {(k − 1)/2 : k ∈ M odd}, same for B; charges a, −a, b, −b.
The e-predecessors t_k of u with k = 2i and k = 2i + 1 are indexed by the i in

| e | k even | k odd | class of t_k |
|---|---|---|---|
| 1 | M₀ ∖ B₀ | M₁ ∖ B₁ | 1 − c |
| −1 | M₀ ∖ (B₀ − 1) | M₁ ∖ (B₁ − 1) | 1 − c |
| 0 | M₀ ∖ B₁ | M₁ ∖ (B₀ − 1) | 2 − c (k even), −c (k odd) |
| 2 | M₀ ∖ (B₁ + 1) | M₁ ∖ B₀ | 2 − c (k even), −c (k odd) |

and |X ∖ Y| = ch X − ch Y + |Y ∖ X|. This is Lemma G of l2sets together with its equality cases:

- **Lemma A (tight states).** A central state has no central 2-predecessor iff M₁ = B₀ (c = 0), M₀ = B₁ + 1 (c = 1).
  It has no level-2 0-predecessor ("L-tight") iff M₀ = B₁ (c = 0), M₁ = B₀ − 1 (c = 1). It has no level-2
  2-predecessor iff M₀ ⊆ B₁ + 1 (c = 0), M₁ ⊆ B₀ (c = 1).
- **Lemma B (level 2 has a margin).** A level-2 state has ≥ 1 central 2-predecessor and ≥ 2 central 0-predecessors;
  its predecessors under ±1 are of level 2, and it has a 1-predecessor unless M = B, i.e. the state is (λ|λ′).
- **Lemma C (hooks).** (−|1^m) has no 2-predecessor and its only 1-predecessor is (−|1^{m−1}); the only 1-predecessor
  of (s|−) is (−|1^{s−1}) and its only 0-predecessor is (−|1^s). (M = ℤ_{<0}, B = {m − 1} ∪ ℤ_{<−1}; resp.
  M = {s − 1} ∪ ℤ_{<−1}, B = ℤ_{<0}.) Hence **for every prefix p, whatever its letters**: (−|1^s), (1^s|−) ∉ F(p 2 1^j)
  for j ≥ 0, and (s|−), (−|s) ∉ F(p 2 1^j), ∉ F(p 2 1^j 0) for j ≥ 1.
- **Lemma D (the two routes at j = 1).** After x 2 1^j 0 a central state u₁ is reached through a level-2 0-predecessor
  (route L) or a central one (route C). If u₁ is L-tight, every central 0-predecessor u₂ of u₁ has no central
  2-predecessor (c = 0, k = 2i + 1: u₂ has quotient ((M₁ ∖ i) + 1, M₀; B₁, (B₀ − 1) ∪ i) and M₀ = B₁; c = 1 alike).
  If moreover the common diagram (M₀ = B₁, resp. M₁ = B₀ − 1) is not a half-line, every 1-predecessor of every such
  u₂ has a central 2-predecessor (tightness would need (M₀ ∖ m) + 1 = M₀ or M₀ + 1 = M₀ ∪ m). The first
  statement says route C would fail with no 1 between the 2 and the 0; the second gives the 2-predecessor for
  j = 1 (still open there: that it lies in G, and that u₂ has a 1-predecessor).

Lemmas A–D and the table are checked on all 3,132 states of slack ≤ 12 (`tight.py 12`).

## 2. One letter 2: reduction to (X), no proof (item 2)

**(X)** For j ≥ 1 and y ∈ {0, 1}*:
(X1) G⁻(s) ⊆ step_{2 1^j 0 −1}(G(s₀)) for s₀ ≥ 0; (X2) G(s) ⊆ step_{2 1^j 0 e}(G(s₀)) for s₀ ≥ 1, e ∈ {0, 1};
(X3) G⁻(s) ⊆ step_{2 1^j 0 y 0 −1}(G(0)).

**Proved: (X) ⟹ every valid word with exactly one letter ≥ 2 has a permutation.** More generally: letters ≤ 2, and
before the next letter 2 each letter 2 is followed by 1^j 0 and one more letter (if it stands at slack ≥ 1), or by a
negative letter (if it stands at slack 0). *Proof.* Carry the invariant of Theorem 0 (G after 0, 1; G⁻ after a
negative letter; G ⊆ G⁻). It holds up to a letter 2. By (X2) it holds again one letter after the first 0 if that
letter is 0 or 1; by (X1), (X3) it holds at the first negative letter otherwise. In between nothing is claimed.
The word ends at slack 0, so a negative letter follows the last 2. With one letter ≥ 2 that letter is 2, because a
letter h ≥ 3 is followed by a letter ≥ 2. ∎

**(X) tested, no failure:** s₀ ≤ 8, at most 7 letters 1^j 0 y, slack ≤ 13 (§1; the only failures of the G-statement
are the six words at s₀ = 0); every target with ≤ 1 and ≤ 2 part sizes at slack 23, 24, words 2 1^j 0 e, j = 1, 2, 4
(68,970 pairs, backward search); 400 random targets at slack 34–96, s₀ ≥ 3.

**How far a Theorem-0-style proof gets (tested, slack ≤ 14, `fam.py 14`).** Families that depend on the slack only:
L0 / K0 = level-2 / central states with a 2-predecessor in G; Lam, Kap = the largest families inside them closed
backwards under 1 (so inside F(x 2 1^j) for every j); C1 = central states with a 0-predecessor in Lam ∪ Kap, C1L in Lam.

| type | family | what it is |
|---|---|---|
| x 2 | L0 | Level2(s) minus 4, 2, 2, 4 states at s = 6, 7, 10, 14 |
| x 2 1^j | Lam | Level2(s) ∖ {(λ\|λ′)}; at s = 7 four more states are missing |
| x 2 1^j | Kap | G(s) minus 41–64 states for s ≥ 11: no description |
| x 2 1^j 0 | C1 | G(s) ∖ {(s\|−), (−\|s)}, and (s/2, s/2\|−), (−\|s/2, s/2) at s = 10, 14 (s ≥ 9) |
| x 2 1^j 0 | C1L | G(s) minus 16–26% of it for s ≥ 9 (284 of 1,744 at s = 14) |

- exit −1: G⁻(s − 1) ⊆ step_{−1}(C1(s)) for all s ≤ 14, so (X1) has a slack-only proof shape. C1L alone gives
  G(s − 1) but not G⁻(s − 1) (missing −|44 at slack 8; −|66, 22|2222 at slack 12, and mirrors), and G alone does not
  carry a following −2 (2, 2, 4 states at s = 4, 8, 12). So route C is needed, for the states of G⁻ ∖ G.
- exit 1: G(s) ⊆ step_1(C1(s − 1)) for 9 ≤ s ≤ 14.
- exit 0: exactly two states of G(s) have no 0-predecessor in C1(s), 9 ≤ s ≤ 14: (s−1, 1|−), (−|s−1, 1) for s even,
  (s−1|1), (1|s−1) for s odd. They are reached (X2 holds), by states that depend on j.

**Why there is no proof.** (i) Kap has no description, and route L alone loses 16–26% of G at the 0 (the L-tight
states, Lemma A); Lemma D covers j = 1 and only 125 of the 494 L-tight states of slack ≤ 12. (ii) For the exit 0 the
family after x 2 1^j 0 must depend on j. (iii) Lam = Level2 ∖ {(λ|λ′)} is itself unproved: it needs the level-2
states all of whose central 2-predecessors lie in T (1|531, 1|751, 311|32211, …), i.e. Lemmas 1–5 of l1sets redone at level 2.

**Height and separation (tested only, `exit.py block 13`, s₀ ≥ 3, slack ≤ 13).** After 2 2 or 2 1 2 and then 1^j, the
family is back after 0 0 e and after 0 −1 e (200 of 200), never after 0 e or 0 1 e (≤ 8 states missing). After 3 2 it
is back after 0 −1 e (45 of 45), not after 0 0 e. After 4 3 2 and 3 2 1 2 it is not back two letters after the first
0 (4 cases). So "a 0 and one more letter" is the separation for single letters 2 only; I have no statement for blocks.

## 3. Smallest obstruction and a weaker target (item 3)

- **Obstruction (proved, Lemma C).** For every x and j ≥ 1: (s|−) ∉ F(x 2 1^j 0), and the four hooks ∉ F(x 2 1^j). No
  family containing G(s) serves these two types at any slack ≥ 3, and the bridging state (s|−) of Theorem 0′ is one of
  the missing ones. Smallest case: x empty, (3|−) ∉ F(2 1) and (3|−) ∉ F(2 1 0).
- **Weaker target with a margin: level 2.** Proved (Lemma B): every level-2 state has a central 2-predecessor, two
  central 0-predecessors, and a level-2 1-predecessor unless it is (λ|λ′). Tested (slack ≤ 14): Level2 ∖ {(λ|λ′)} is
  inside F(x 2 1^j) for all j ≥ 1 and s ≠ 7. So the letters 2 and 1 carry this family; it is lost at the next 0,
  where a central state needs a level-2 0-predecessor and the count of Lemma G is ≥ 0, not ≥ 1.
- **Central sub-families do not work.** The patterns of level 1 are not closed backwards under 2 (Lemma A: the tight
  ones, 17–20% of G(s) for s ≥ 11, column |G−K0|), and after x 2 1^j for all j at once 41–64 states of G are lost
  (column |G−Kap|). A single slack-only family for all types after the first 0 is empty (column |G−Q|); it is not
  needed, since by (X2) the family G is back one letter after the first 0.
