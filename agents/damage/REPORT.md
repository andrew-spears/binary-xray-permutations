# damage: what a block of letters 1, 2 destroys and what the next letters repair — REPORT

**Item 1 (the exact statement): HIT.** The family is explicit and its necessity is proved for every word (Theorem D,
Corollary N); that nothing else is missing is tested only, and only for the start family "levels 1 and 2", not for G.
**Item 2 (proof of the block step): NOTHING.** No proof, not even for W = 2 1^j (statement (X) of onehigh).
**Item 3 (Theorem L2): NOTHING.** Two proved obstructions to the plan as stated (Propositions C and E).

Setting: `../l1sets/REPORT.md`, `../l2sets/REPORT.md`, `../onehigh/REPORT.md` (state u = (λ|μ) = (M, B), class, G, G⁻, T,
level(u) = max(c, 1 − c)). s = slack of u. Young excess (`../universal/REPORT3.md`): y′ = max(0, y + e − 1) along the word.
For a prefix x: **y** = excess of x, **ŷ** = excess of x without its last letter.
Recheck: `cd agents/damage && sh runs.sh` (3 minutes; writes `out_runs.txt`).

## 1. Proved

**Stones.** By the predecessor formula of l1sets §1, a backward chain of L steps from u = (M, B) through the letters
e_1 (last letter of the word), e_2, …, e_L is the same as L stones: distinct beads m_i ∈ M and distinct holes n_i ∉ B with
n_i − m_i = δ_i := 2i − 1 − e_i. Legality (e_i ≥ e_{i+1} − 1) gives δ_1 < δ_2 < …. The state reached is
((M ∖ {m_i}) + L, (B ∪ {n_i}) − L). So "u has a backward chain through w" is a board problem of the same kind as the conjecture.

**Theorem D (any letters).** Let u = (λ|μ) ∈ F(x), or more generally u ∈ step_w(any set of states). For all p, q ≥ 0, k ≥ 1
with t = p + q and t + k ≤ length:

  (sum of the k letters that come before the last t letters) ≤ k t + Σ_{i ≤ k} (λ_{p+i} + μ_{q+i}).

*Proof.* Beads of M in decreasing order are b_i = λ_i − i, holes of B in increasing order are h_i = i − 1 − μ_i. Take the
stones 1, …, j = t + k. At most p of them sit on b_1, …, b_p and at most q on h_1, …, h_q; choose k of the others. Their
beads are distinct and ≤ b_{p+1}, their holes distinct and ≥ h_{q+1}, so their δ sum to at least
Σ_{i ≤ k} (h_{q+i} − b_{p+i}) = k t + k² − Σ_{i ≤ k} (λ_{p+i} + μ_{q+i}). The δ are increasing, so the sum is at most
δ_{t+1} + … + δ_j = k² + 2 k t − (e_{t+1} + … + e_j). ∎

**Corollary N (the family N).** For a prefix x of slack s put
N(x) = { (λ|μ) : max(λ_1, μ_1) > s − ŷ  or  max(ℓ(λ), ℓ(μ)) > s − y }  (a row longer than s − ŷ or a column longer than s − y).
(a) For every legal prefix x, with any letters: F(x) ∩ N(x) = ∅.
(b) If all letters are ≤ 2 and the last one is ≤ 0, N(x) is exactly the set of states violating Theorem D.

*Proof.* Rows, (p, q) = (1, 0): f(k) = (sum of the k letters before the last) − k has maximum ŷ. If λ_1 > s − ŷ take k with
f(k) = ŷ: the right side is ≤ k + s − λ_1 < k + ŷ. Conversely (letters ≤ 2, so f(k) ≤ k): a violation needs
Σ_{i≤k}(λ_{1+i} + μ_i) < f(k) ≤ k, so neither λ minus its first row nor μ has k parts, the sum is s − λ_1, and s − λ_1 < ŷ.
Columns, t = 0: with c = ℓ(λ) and k ≤ c, k + min(k, s − c) ≤ Σ_{i≤k}(λ_i + μ_i) ≤ k + s − c; for k > max(ℓ(λ), ℓ(μ)) the sum is s ≥ E_k.
If c > s − y take k with E_k − k = y (then k ≤ s − y < c): violated. Conversely, last letter ≤ 0 gives E_k − k ≤ k − 2,
so a violation at k ≤ c needs E_k − k > s − c, i.e. y > s − c. For t ≥ 2 and letters ≤ 2 the left side is ≤ 2k ≤ kt. ∎

So the grading asked for is the pair (ŷ, y): rows are graded by ŷ and columns by y = max(0, ŷ + e − 1), e the last letter.
A 0 lowers both by one, a −k lowers the column grade by k + 1; this is why a −1 heals faster than a 0.
It reproduces the counts 2, 8, 22, 52 (last letter 0, ŷ = 1..4) and the 18, 6, 2, 0 of lens item 3 (inside G).
(`small.py` asserts (a) and (b) on all states: 7,214 prefixes ending in a letter ≤ 0, length ≤ 9, slack ≤ 10, letters −3..2.)

**Proposition C (states that zeros never repair).** Let d_a = (a, a − 1, …, 1). The states (d_a|d_{a+1}) and (d_{a+1}|d_a),
slack (a + 1)², central, are each other's only 0-predecessor and have no 2-predecessor.
*Proof.* M = {a−1, a−3, …, 1−a} ∪ {≤ −a−1}, B = {a, a−2, …, −a} ∪ {≤ −a−2}: k + 1 ∉ B only for k = −a − 2 and k − 1 ∈ B
for every k ∈ M; the same for the swapped pair with k = a. ∎ (`cores.py`, a ≤ 6.)
Consequences (computed, `cores.py`): after x 2 0^k with slack 9 both 21|321 and 321|21 ∈ G(9) are missing for every k.
The two old prefixes 1^7 2 0 0 2 0 0 0 and 1^9 2 0 0 0 (slack 11, ŷ = y = 0, same last four letters) miss 8 and 0 states of
G(11), and still do after three more zeros. So **no family depending on (slack, y, last letters) equals G minus the
damage, even on old prefixes ending in 0 0 0**; the thin part of J* in REPORT3 has to absorb such sets.

**Proposition E (Central alone cannot carry the induction).** For s ≥ 2 the only 0-predecessors of (s−1|1) are (s|−) and
(−|2 1^{s−2}) (M = {s−2} ∪ {≤ −2}, B = {0} ∪ {≤ −2}: k + 1 ∉ B only for k = s − 2, −2). (s|−) ∈ N whenever ŷ ≥ 1, and (−|2 1^{s−2}) has level 2 (`cores.py`, s = 3 and 11).
So after x 2 1^j 0 0 the central state (s−1|1) ∈ G(s) is reached only through a level-2 state: smallest case
(2|1) ∈ F(2 1 0 0) comes from (−|21) only. A family "(G or G⁻) minus N_r" has no predecessor for it.

## 2. Tested (item 1)

**Statement S.** Lev₂(s) = all states of level ≤ 2. For every s₀, every legal word w with letters ≤ 2 ending in a
letter ≤ 0: Lev₂(s) ∖ step_w(Lev₂(s₀)) = Lev₂(s) ∩ N(w) exactly.
- `lev.py 6 7 12 2 2 -3`: s₀ = 6, length ≤ 7, slack ≤ 12, letters −3..2: 706 words containing a 2, no exception
  (also s₀ = 5; also with target level 1).
- Closed under cutting (`CUT=1`: every level above 2 is thrown away at each prefix ending in a letter ≤ 0): still exact for s₀ = 6.
  For s₀ = 5, length ≤ 8, slack ≤ 11, 14 of 2,506 words fail; the printed ones first descend to slack 1 or 2, e.g. −|33 after −1 −1 −2 1 2 1 1 0.
- With the start G(s₀) instead (`landau.py 4 7 12 -3`): exact after every negative letter, but 36 of 510 words ending in 0
  have 2–4 more states missing (2|411 after 2 1 1 0; 11|522 after 2 2 2 1 0). This is the non-locality seen before; it
  comes from starting with Central only (Proposition E), not from the block.
- Exact F from the empty word (`small.py 11 11 -3 2`): (Lev₂ ∖ T) ∖ F(x) = N for all 35,939 prefixes ending in a
  letter ≤ 0 whose last two cuts (prefixes ending in a letter ≤ 0) have slack 3..8; 1,340 exceptions when one of them has
  slack ≤ 2 (up to 14 states) and 38 when it has slack 9 or 11 (the sets of Proposition C and their successors).
So in the form asked: Lev₂(s) ∖ step_{W 0}(Lev₂(s₀) ∖ N) ⊆ N with (ŷ, y) updated by the rule above, tested at slack 5–12;
with G in place of Lev₂ it is false (2|411).

## 3. Why there is no proof (items 2, 3)

- **The step that fails.** After the first backward step (the 0) the level-2 route of the task needs, at each 2, a
  predecessor one level down, which exists only from level ≥ 2. Through 2^a the guaranteed chain needs level a + 1 at
  the top, and a state of level m needs slack about m(m − 1): the slack s₀ + 2a hosts it only if a(a − 1) ≤ s₀. In the
  tests S holds far outside this (s₀ = 6, a = 4), so the chains that exist go up a level at some 2, where existence is
  not a count but the stone problem above with L = |W| + 1 stones. Theorem D is Landau's condition for that problem; its
  sufficiency is a statement of the same kind as the conjecture, and I found no argument for it, also not for W = 2 1^j.
- **Smallest examples.** Central-only families: (2|1) after 2 1 0 0 (Proposition E). Route through one level-2
  0-predecessor only: fails for 140 states of G at slack 13 (`routeL.py`, earlier run, not in `runs.sh`).
- **Theorem L2.** S would give it only above slack about 5 and away from the squares; from the empty word the exceptions
  at cuts of slack ≤ 2 and the zero-closed sets of Proposition C are not described. The largest closed system with types
  (slack, y, last two letters) is nonempty through bound 10 (`ty.py`, earlier run) but is not G minus a thin set (the type slack 8, y = 0,
  last letters 0 −1 lacks 19 states of G⁻(8)).

## 4. What to take from this

1. Use (ŷ, y) and N(x) of Corollary N as the damage family; it is forced (proved), so no smaller family can work.
2. Carry levels 1 and 2, not G: with Lev₂ the block step is exact and local in every test; with G it is neither.
3. The open statement is S (sufficiency of Theorem D inside Lev₂). The 0-closed sets of Proposition C must be excluded
   from any family on prefixes ending in zeros.
