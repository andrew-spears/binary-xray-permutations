# referee: the two hand proofs marked proved (cards `l1`, `upone`, `nocross`) — REPORT

**HIT: both proofs hold.** I read `agents/l1sets/REPORT.md` §1–§2 and `agents/l2sets/REPORT.md` §1–§2 line by line and
re-derived every step. No gap. One sentence in Lemma 4 needs a repair (it overlooks a case that the lemma's
hypothesis already excludes), and one remark in l2sets §2 is false but is not used. Every lemma was also re-checked on
all states of slack ≤ 17 by a script written from `universal/maya.py` alone (`check.py`, no code of the two authors).

Recheck: `cd agents/referee && python3 check.py 17` (30 s; output in `out_check_17.txt`, every line `ok`).

## 1. `agents/l1sets/REPORT.md` §1–§2 (letters −1, 0, 1)

| item | verdict | what I checked by hand |
|---|---|---|
| §1 step / predecessor formulas | correct | derived from `universal/maya.py`: row offset u = k + 1, and B = −1 − (complement of M(μ)) turns "add column offset v = e − u" into B′ = (B + 1) ∖ {k + 1 − e} |
| §1 class facts (c₀(μ′) = c₀(μ); s ≡ a + b mod 2; central SC only for 4 \| s; E⁰ has class 0, slack ≡ 0 mod 4) | correct | charge-0 bead counts; 2-core of charge a has a(2a − 1) boxes |
| Lemma 1 (counts and classes) | correct | window counts incl. the two boundary beads; ε(S ± 1) = 1 − ε(S) holds for any S containing all far-negative integers (needed, since M ∖ k has charge −1) |
| (∗) | correct | shifts of the three conditions |
| Lemma 2 (a), (b), (c) | correct | all four sub-arguments; the "loner" count in both sub-cases j ≠ k + 2, j = k + 2 |
| Lemma 3 (a), (b), converse | correct | (b) does not use the last condition of (∗) |
| Lemma 4 | **correct after a repair** (one sentence, see below) | SC branch gives slack 1; pair-index equation; charge(Q) = 2·charge(Q°) − 1; count ≤ 4 |
| Lemma 5 (a), (b), (c) | correct | (a) incl. "the exchanged state is in A" (same unique 1-predecessor); (b), (c) the k-term is disjoint from the Q-terms |
| Proof of the Theorem (case split) | correct | T(s) ≠ ∅ only for 4 \| s > 0 and s = 4m² + 1, m ≥ 1; three letters each; s = 0 and e = 1, u ∈ SC handled |
| Corollary 1 (abstract machine = boards) | correct | slack(t) ≤ n − 1 gives ≤ n − 1 parts in both diagrams, so the removed bead k is a real row/column |
| finite sub-cases (`local.py 8`) | correct, re-run | O4 for m ≤ 3 is needed (12, 20, 28 successors), O6 for m ≤ 5; the script does m ≤ 8 and its assertions are the statements the proof uses |

**Repair in Lemma 4** (*Slack* paragraph). "Adding i₀ changes α − β by ±2, so the two diagrams are δ_j and δ_{j±1}" is
false in one case: for a charge-0 2-core diagram α − β = (−1)^{j+1}(2j + 1), so for j = 0 (α − β = −1) the choice
i₀ = α + 2 gives α − β = +1, again δ₀. Then t = (∅|∅) and u has slack 1 = 4·0² + 1. Smallest instance: Q = ℤ_{<0}
(Q° = ℤ_{<0}), i₀ = 0, pair {−1, 0}: u = (1|−) or (−|1). The lemma assumes slack ≥ 5, so nothing breaks; the sentence
should read "δ_j and δ_{j±1}, or j = 0 twice, which is slack 1 and excluded". With that, m ≥ 1 and the count is as stated.

Remarks that are not gaps:
- ∅|∅ satisfies the definition of E⁰ literally (M = B = ℤ_{<0} = (B − 2) ⊔ {−2, −1}); it is the only state in SC ∩ E⁰
  (a union of eo-pairs with B° = (B° − 1) ⊔ {i} is a half-line). T(0) = ∅ is set by hand, so this is harmless.
- T(s) for 4 | s contains non-central SC states (e.g. 321|321, slack 12, class 4); harmless since G = Central ∖ T.
- Lemma 4 is used in the case "4 | s, e = 1" only through "no such u at slacks other than 4m² + 1"; there the slack is
  ≥ 5, as the lemma requires.
- Slack 3 (not covered by "≥ 5" in Lemma 4, not needed): T(2) = ∅, so the case never arises.

## 2. `agents/l2sets/REPORT.md` §1–§2 (letters ≤ 1; no letter ≥ 2 before a letter ≤ −2)

| item | verdict | what I checked by hand |
|---|---|---|
| Lemma G (i), (ii) | correct | shifted-window counts for f ≥ 0 and f < 0 separately (B gains f beads below or loses \|f\|); classes from Lemma 1 |
| Lemma G (iii), (iv) | correct | (iii) is the "two in E⁰" argument of Lemma 2, which does not use e |
| Consequences, negative letters | correct | e = −2j: ≥ j + 1 central predecessors; e = −(2j − 1): ≥ 2j, all central |
| Family G⁻, U(4m²) | correct, **one false remark** (below) | U = (−1)-successors of A: two states, in E⁰, by Lemma 5(a) |
| Theorem 0 (a), (b) with the equality, (c) | correct | (b): the three cases T(s + 1) = ∅, 4 \| s + 1, s + 1 = 4m² + 1; (c): U ⊆ E⁰ and Lemma G (iii) |
| Corollary (induction) | correct | a letter −k, k ≥ 2, follows a negative letter (legal prefix), so its source type is G⁻; after 1 −1 the source is G(s + 1), covered by (b) |
| Lemma H | correct | charges of (s) and (1^s); not SC, not E⁰ (the pair {−2, −1}, resp. {0, 1}, is broken), not A (s boxes apart) |
| A(y) = conj F(−reverse(y)), conj = conjugate both partitions | correct | half-turn (r, c) ↦ (n + 1 − r, n + 1 − c): the letter of stone n + 1 − j is −w_j, and the offsets of the free rows 1..n turn into −1 − (complement of M(λ)) = M(λ′); rows and columns are not exchanged |
| conj(1^s \| −) = (s \| −) | correct | repo convention: `universal/REPORT.md` line 4, `universal/load.py` |
| Theorem 0′ | correct | −reverse(y) is a legal prefix with letters ≤ 1 and slack s (partial sums, and z_{i+1} ≥ z_i − 1); the two half-boards are complementary because λ₁ ≤ n − N; s = 0 is ∅\|∅ |

**False remark, not used** (§2, Family): "G(s) ⊆ G⁻(s), and they differ only for 4 | s". They also differ at
s = 4m² + 1, where U(s) = ∅ and so G⁻(s) = Central(s) contains the four states of A. Smallest instance: 2|111 ∈ G⁻(5) ∖ G(5).
The proofs of (b) and (c) treat G⁻(s) = Central(s) ∖ U(s) for every s, so nothing depends on the remark; the script
confirms (b) and (c) with G⁻(5) = Central(5), G⁻(17) = Central(17). The inclusion G ⊆ G⁻, which is used, is true.

Remarks that are not gaps:
- Lemma H is stated for s ≥ 1; Theorem 0′ at s = 0 needs ∅|∅ ∈ G(0), which is the definition.
- §1 "that predecessor is one level lower" holds for the letters 2f with f ≥ 1 (for f = 0, c = 1 the level stays 1). Not used.
- §2 "No other pair (s, k) fails" is a tested remark, not part of the proof; confirmed for slack ≤ 17 (only k = 2, 4 | s).
- The cards `l1`, `upone`, `nocross` state exactly what is proved.

## 3. By hand / by script

- **By hand:** every row of the two tables, including the case split of the L1 Theorem, the edge cases s = 0, 1, 3,
  4, 5, the derivation of the step formula from `maya.py`, and the mirror identity for A(y).
- **By script (`check.py 17`, independent code, 25,815 states, letters −5..2):** predecessor formula; Lemma 1 and
  Lemma G (i)–(iv); Lemma 2; Lemma 3 with converse; the definitional A (non-empty only at slack 1, 5, 17; 4 states at
  5 and 17); Lemma 5 and both finite sub-cases for m = 1, 2; the L1 Theorem; Theorem 0 (b) with equality and (c) for
  k = 2..5; U(4) and U(16); Lemma H; A(y) = conj F(−reverse(y)) on all 2,216 cuts of valid words of length ≤ 8.
- **Authors' scripts re-run:** `l1sets/check.py 18 12` and `l1sets/local.py 8` reproduce their stored outputs;
  `local.py` asserts the two statements the proof needs (m ≤ 3 and m ≤ 5 are needed, m ≤ 8 is run).
- **Not checked by script beyond m = 2:** Lemma 4 and Lemma 5 for large m rest on the hand proof (and on `local.py`
  for m ≤ 8, which builds A from the proof's own description).
