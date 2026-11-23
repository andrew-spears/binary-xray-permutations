# HIT (Task 0): every valid word with all letters ≤ 1 is solvable, and so is every valid word in which no letter ≥ 2 comes before a letter ≤ −2 (proved). NOTHING on a proof for c = 2.

Words are x = (x_1, …, x_n), x_k = d_k − 2k for the occupied diagonals d_1 < d_2 < … (so x_{k+1} ≥ x_k − 1: a letter −k
follows a letter ≤ −k + 1), valid = partial sums ≥ 0, sum 0. Notation, G(s), T(s), SC, E⁰, A and Lemmas 1–5 are those of
`../l1sets/REPORT.md`.

**Proved (hand proof on top of the L1 Theorem; no new finite checks).**
- **Theorem 0.** Every valid word with all letters ≤ 1 has a permutation (negative letters of any depth). By the mirror,
  the same for all letters ≥ −1.
- **Theorem 0′.** Every valid word that can be cut as x | y with all letters of x ≤ 1 and all letters of y ≥ −1 has a
  permutation. That is every valid word in which no letter ≥ 2 comes before a letter ≤ −2 (any letters, any slack).
  It contains L1, the unimodal words of `../unimodal/`, and Theorem 0.
- **Lemma G (count for any letter).** For every letter e and every state: the number and the parity classes of the
  e-predecessors (§1). A letter −k is *easier* than −1: a central state has at least 2 central predecessors under every
  negative letter, and for every letter at most one predecessor lies in E⁰. Positive letters are the hard ones: a
  letter 2f needs "level" ≥ f + 1, a letter 2f + 1 needs |a − b| ≥ f + 1.

**Tested only.**
- The two theorems as algorithms (`neg0.py`): all 9,397 valid words of length 13 with letters ≤ 1; 150 random ones of
  length ≥ 250 (slack to 181, letters down to −12); all valid words of length ≤ 14 with no letter ≥ 2 before a letter ≤ −2
  (35,543 at n = 14); 100 random ones of length ≥ 240 (slack to 361, letters −4..5). All solved.
- **(BRIDGE)**, the statement that would finish every letter bound (§3): it holds for all 48,064 valid words of length
  ≤ 13 that Theorem 0′ does not cover (at n = 13 that is 34,677 of the 48,107 valid words), and for 200 random words with letters in [−2, 2], length ≥ 30, slack ≤ 9.

**NOTHING for c = 2 (§3, §4).** What is left for c = 2 is exactly the words with a 2 before a −2. The L1 method does
not carry over, for three stated reasons, and the 13 block sets have no description I could find.

**Not checked.** Nobody else has read the proofs. Words with repeated diagonals (x_{k+1} = x_k − 2) are covered only
for the factor 1 −1 (L1); the step 0 → −2 is not (§2, remark).

## 1. Lemma G: predecessors under any letter

State u = (M, B) with 2-core charges a, b, class c = a + b. The e-predecessors are t_k, k ∈ M, k + 1 − e ∉ B.

**Lemma G.** (i) e = 2f: the predecessors with k even have class 2 − c and there are at least c − f of them; those with
k odd have class −c and there are at least 1 − c − f.
(ii) e = 2f + 1: every predecessor has class 1 − c; at least a − b − f have k even and at least b − a − f have k odd.
(iii) For every e at most one predecessor is in E⁰.
(iv) No predecessor at all iff M ⊆ B + e − 1 (REPORT2 of `../weights`, §3).

*Proof.* Window [−2L, 2L), L large: M has L + a even and L − a odd beads; below the window B is full and above it empty.
(i) k even, y = k + 1 − 2f odd: y runs over the odd numbers of the window shifted by −2f, where B has L − b + f beads:
at least (L + a) − (L − b + f) such k have y ∉ B. k odd, y even: y runs over the even numbers of [−2L + 2 − 2f, 2L + 2 − 2f),
where B has L + b − 1 + f beads: at least (L − a) − (L + b − 1 + f).
(ii) k even, y = k − 2f even: B has L + b + f even beads in the shifted window: at least a − b − f. k odd: B has
L − b + f odd ones: at least b − a − f.
Classes: as in Lemma 1 of L1 (a_t = 1 − a for k even, −a for k odd; b_t = −b for y even, 1 − b for y odd); the
parities of k and y are equal for odd e and opposite for even e.
(iii) If t_k ∈ E⁰ then M ∖ k is a union of pairs {2i − 1, 2i}. If also t_j ∈ E⁰, j ≠ k: j has a partner in M ∖ k, and
this partner is in M ∖ j without j. ∎

**Consequences.**
- *Negative letters.* u central (c ∈ {0, 1}), e = −2j: at least j + 1 central predecessors (c = 0: k odd; c = 1: k even).
  e = −(2j − 1): at least 2j predecessors, all central. So ≥ 2 central predecessors for every e ≤ −1, ≥ 4 for e = −3.
- *Positive letters.* Put level(u) = max(c, 1 − c) (central = level 1; level m needs slack ≥ m(m − 1)). Under the
  letter 2f a predecessor is guaranteed iff level ≥ f + 1, and that predecessor is one level lower. Under 2f + 1 iff
  |a − b| ≥ f + 1. So backwards a letter 2 uses up one level; a run 2^r is guaranteed only from level r + 1, slack ≥ r(r + 1).
  For a central state the existence of a central 2-predecessor is a condition on the next 2-adic digit
  (c = 0: some odd k ∈ M with k − 1 ∉ B); it fails on large sets, not on a thin family.

## 2. Theorem 0 and Theorem 0′

**Family.** Type of a prefix = (slack, sign of the last letter).
- last letter 0 or 1, or empty prefix: G(s) = Central(s) ∖ T(s), the L1 family;
- last letter negative: **G⁻(s) = Central(s) ∖ U(s)**, where U(4m²) = the (−1)-successors of the four states A(4m² + 1)
  (two states, inside E⁰, by Lemma 5(a) of L1), m ≥ 1, and U(s) = ∅ otherwise. G(s) ⊆ G⁻(s); they differ for 4 | s and for s = 4m² + 1 (where G⁻(s) = Central(s) contains the four states of A, e.g. 2|111 at s = 5). Nothing below uses where they differ (corrected after the referee read, `../referee/REPORT.md`).

**Theorem 0 (step).** (a) e ∈ {0, 1}: every u ∈ G(s) has an e-predecessor in G(s − e) ⊆ G⁻(s − e).
(b) Every u ∈ G⁻(s) has a (−1)-predecessor in G(s + 1); in fact G⁻(s) = Central(s) ∩ step_{−1}(G(s + 1)).
(c) k ≥ 2: every u ∈ Central(s) has a (−k)-predecessor in G⁻(s + k).

*Proof.* (a) is the L1 Theorem. (b) u has at least 2 predecessors, all central (Lemma G). If T(s + 1) = ∅, done.
If 4 | s + 1: none is in SC and at most one in E⁰ (Lemma 2(a) of L1). If s + 1 = 4m² + 1: T = A, and all predecessors
of u are in A only if u is a (−1)-successor of A, i.e. u ∈ U(s). Conversely a state of U has its two predecessors in A
(Lemma 5(a)). (c) u has at least 2 central predecessors, at most one is in E⁰ ⊇ U(s + k) (Lemma G). ∎

**Corollary (Theorem 0).** If x is a prefix with all letters ≤ 1 and slack s, then G(s) ⊆ F(x), and G⁻(s) ⊆ F(x) if x
ends in a negative letter. *Proof.* Induction on the length, as Corollary 1 of L1: before a letter −k, k ≥ 2, the letter
is negative, so the source type is G⁻ and (c) applies; before −1 the source contains G(s + 1); before 0, 1 it contains
G(s − e). The slack is at most the number of letters 1, so every state used is a state with that many stones. ∎
With G(0) = {∅|∅} this is Theorem 0.

*A letter −k is no harder than −2.* (c) needs nothing about u beyond "central", and its margin grows with k. The only
reason the family has to remember the sign of the last letter is the step −2 out of a slack divisible by 4: from G(s),
4 | s, some states of slack s − 2 have all their central (−2)-predecessors in T(s) = SC ∪ E⁰ (2, 2, 4 states at
s = 4, 8, 12, `neg0.py check`); G⁻(s) keeps SC and all of E⁰ except at most two states, so they are available after a
negative letter. No other pair (s, k) fails.

*Remark (repeated diagonals).* If two stones may share a diagonal, 0 may be followed by −2, from the type G(s), and
that step fails at those 2, 2, 4 states. Not treated.

**Lemma H.** For s ≥ 1 the states (s | −) and (1^s | −) are in G(s).
*Proof.* M((s)) = {s − 1} ∪ {−2, −3, …}: charge [s odd]; M((1^s)) has its only hole below 0 at −s: charge 1 − [s even].
So both are central. They are not (λ|λ′), not built from 2 × 2 blocks (E⁰), and the two diagrams do not differ by one
box unless s = 1 (A has slack ≥ 5). ∎

**Theorem 0′.** Let w = x y be valid, all letters of x ≤ 1, all letters of y ≥ −1, s = slack(x). Then
(s | −) ∈ F(x) ∩ A(y), so w has a permutation.
*Proof.* (s | −) ∈ G(s) ⊆ F(x). The word −reverse(y) is a legal prefix with letters ≤ 1 and slack s, so (1^s | −) ∈
F(−reverse(y)), and A(y) = conj F(−reverse(y)) contains conj(1^s | −) = (s | −). ∎
The permutation is built by the backward algorithm on x and on the mirror of y (`neg0.py split`).

## 3. c = 2 and all letters: what is left, and (BRIDGE)

A valid word not covered by Theorem 0′ is w = x m y, where m starts at the first letter ≥ 2 and ends at the last
letter ≤ −2; x has letters ≤ 1, y has letters ≥ −1. Then G(s₁) ⊆ F(x) and conj G(s₂) ⊆ A(y), so w is solvable if

**(BRIDGE)  step_m(G(s₁)) ∩ conj G(s₂) ≠ ∅**  (s₁, s₂ the slacks before and after m).

This is a statement about the middle only, with explicit sets at both ends; proved for all m it is the conjecture.
Tested (`bridge.py`): no failure among the valid words of length ≤ 13 (1, 3, 12, 51, 197, 733, 2,687, 9,703, 34,677 words for
n = 5..13, all letters; `bridge.py 13`, 3 minutes), nor for 200 random words with letters in [−2, 2], length ≥ 30, slack ≤ 9, middle up to 45
letters. The intersection can be a single state (0^j 2 1 0 −1 −2), so there is no room for a count.

The same with the parent's cut: after the last letter ≤ −2 the suffix accepts conj G(s), so for c = 2 it is enough that
F(x) meets conj G(s) for every legal prefix x with letters ≤ 2 ending in −2. `inter2.py 2 10`: the intersection of all
such F(x) is everything for slack ≤ 5 and 63 of 65, 108 of 110 states at slack 6, 7; but after a last letter 1 or 2
the intersection is small (4, 4, 8, 6, 12, 16, 34, 48, 118 and 3, 6, 6, 6, 6, 10, 12, 24, 54 states for slack 2..10), and
(s | −) is not in it from slack 5 on.

**Why the L1 proof does not extend to the letter 2** (all computed, slack ≤ 9..11):
1. *No central family.* A central state can have no central 2-predecessor, or none at all (11|−, −|11; 2, 4, 5, 6, 10,
   12, 15, 20 central-or-not states without 2-predecessor at slack 2..9). A block family whose block ends lie in the
   central class dies: `blocks.py 2 10 3 central` (first empty type: slack 5 after the block 1, from slack 4).
2. *No exact description by classes.* For letters in [−2, 2] there are 500 distinct sets F(x) at slack ≤ 10 (L1: 44 at
   slack ≤ 12), and F(x) is not a function of (slack, set of classes present, last 5 letters): 335 keys are ambiguous,
   up to 6 sets per key (`keys.py 2 10`; at slack ≤ 9: 344 sets, 202 ambiguous keys). After 2 2 2 2 the set is far from class-saturated and zeros repair it slowly.
3. *The 13 block sets per slack are not class sets.* They are not unions of 2-core classes (164 of 435 (type, class)
   pairs split) nor of 4-core classes (268 of 2,271), and not "4-core classes minus a thin family" either (`fine.py`).
   Compared with "the last block applied to all states" they agree at small slack and are much smaller later
   (type 2 1: 30 of 58 at slack 6, 116 of 296 at slack 9; `model.py`). The binding prefixes are steep (2^r 1, 2 1 2 1 …),
   where F(x) is a Skolem-type matching set (REPORT2 of `../weights`, staircases), not a parity set.

So item 1 of the task (describe the 13 sets, prove the blocks 2^r 1) is NOTHING. Negative runs are done (Theorem 0(c)).

## 4. c = 3 and a uniform statement

- Negative letters cost nothing: Lemma G(i)–(iii) and Theorem 0(c) hold for every −k with the same proof. This is the
  parent's observation that the memory depends only on the largest positive letter.
- By Lemma G, backwards a letter 2f or 2f + 1 is guaranteed only at level, resp. |a − b|, ≥ f + 1, and each use lowers
  it. So a type for letters ≤ c must at least record how much of this has been used by the final run of letters ≥ 2;
  that is consistent with the parent's window c + 1, but I have no description of the sets, already for c = 2.
- What a uniform proof needs, stated on the middle: for every legal m that starts with a letter ≥ 2 and ends with a
  letter ≤ −2, (BRIDGE). Equivalently a family of sets J(type) for prefixes that contain a letter ≥ 2, started from
  G(s₁), and shown to meet conj G at every later letter ≤ −2. I did not test c = 3 separately beyond `bridge.py 13`
  (all letters).

## 5. L1 proof re-read (item 3)

Changes in `../l1sets/REPORT.md` (no change of statements):
- E⁰: added why its states have class 0 and slack ≡ 0 mod 4.
- Lemma 4: the slack 4m², the form of Q° and the count "at most 4" are now derived step by step.
- Lemma 5(a): added that the successor is in E⁰ and that its two (−1)-predecessors are both in A (used in Theorem 0(b) here).
- Theorem, case 4 | s, e = 1: the reference to Lemma 4 is spelled out.
Still by script only: the two finite sub-cases on A(4m² + 1) (m ≤ 3 and m ≤ 5).

## 6. Recheck

`cd agents/l2sets && sh runs.sh` (about 90 seconds; output in `out_runs.txt`).

| command | what | result |
|---|---|---|
| `neg0.py check 12` | Lemma G on 6,597 (state, letter) pairs, letters −6..2, slack ≤ 9; Theorem 0(b), (c) on all states of slack ≤ 12 | ok; G alone fails only for −2 at s = 4, 8, 12 |
| `neg0.py all 13`, `random 150 250` | Theorem 0 as an algorithm | all solved |
| `neg0.py hooks 300` | Lemma H, s ≤ 300 | ok |
| `neg0.py split 12`, `splitrandom 100 120` | Theorem 0′ as an algorithm | all solved |
| `bridge.py 12`, `bridge.py random 60 30 9 2` | (BRIDGE) | no failure |
| `keys.py 2 9`, `blocks.py 2 10 3 central` | §3, reasons 2 and 1 | as stated |

Other scripts (`fx2.py`, `fine.py`, `model.py`, `inter2.py`) are exploratory; usage in their first lines. `NOTES.md` is the working log.
