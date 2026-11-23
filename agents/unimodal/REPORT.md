# HIT: letters in {0, 1} followed by letters in {0, −1} — proved for all slacks; and a parity theorem behind it

**Proved (by hand, §1–§2):**
1. *Parity theorem.* For every prefix x and every interface state (λ|γ), the number L_x(λ|γ) of partial placements is,
   modulo 2, the coefficient of s_λ(X)·s_γ(Y) in s_θ(X ∪ Y), where θ = θ(x) is the skew diagram whose rows, from bottom
   to top, have lengths x_1, …, x_m, each row starting one column to the right of the row below (s_θ = 0 if some letter
   is negative). So the parities are Littlewood–Richardson numbers.
2. *A new infinite family with unbounded slack.* Every word x y with all letters of x in {0, 1}, all letters of y in
   {0, −1} and letter sum 0 has a permutation. (Slack at the cut = number of ones, unbounded; the cyclic shift and
   Nordh's F1 are the members 1^a 0 (−1)^a and their neighbours.)
3. *Criterion PAR.* A word x y, cut anywhere, is solvable if s_θ(x)(X ∪ Y) and s_θ(x′)′(X ∪ Y), x′ = −reverse(y), θ′ = transposed
   diagram, share a term s_λ(X) s_γ(Y) with odd coefficients. In particular (§3) whenever the positive letters of x,
   sorted, are the column lengths of θ(x′), sorted.

**Tested only:** PAR holds for every unimodal cut of slack ≤ 7 and fails for 4 of 64 (slack 8) and 2 of 144 (slack 9)
pairs of parity patterns, e.g. x = 1^9, x′ = (3,3,2,1,0). So parity alone does **not** prove UNIMODAL (§3).
**NOTHING** on a closed form for the universal states of all unimodal words (§4).

Notation: d_k = 2k + x_k (sums row + column, rows and columns numbered from 1); a state after m stones is the pair
(R, C) of used rows and columns, written (λ|γ) with λ_i = r_i − i, γ_i = c_i − i (r_1 < … < r_m); slack = |λ| + |γ|.
`conj` = conjugate both diagrams. This is the machine of `../universal/cores.cpp`.

## 1. The parity theorem
Let D = {d_1 < … < d_m} be distinct positive integers and L(R, C) the number of bijections σ: R → C with
{r + σ(r)} = D.

**Theorem 1.** L(R, C) ≡ [s_λ(R)(X) s_γ(C)(Y)] Φ_D(X ∪ Y) (mod 2), where
Φ_D = Σ_β ∏_{i=1..m} h_{β(i) − 2i}, the sum over bijections β: {1..m} → D with β(i) ≥ 2i for all i.

*Proof.* Take indeterminates y_j and the Hankel matrix H = (y_{i+c}), i ≤ m + q, c ≤ m + r, with q, r large.
L(R, C) is the coefficient of the squarefree monomial y^D = ∏_{d ∈ D} y_d in the permanent of H_{R,C}, hence, mod 2,
in det H_{R,C}. Work over F_2.
- *Border.* Let B = [[H, W], [T, 0]] with T_{j,c} = u_j^{c−1} (r rows) and W_{i,j} = w_j^{i−1} (q columns). Expanding
  along the borders, det B = Σ_{R,C} det W_{R^c} · det T_{C^c} · det H_{R,C}, and det T_K = V(u)·s_ν(K)(u), ν(K)_i = k_i − i
  (V = Vandermonde; R^c, C^c = complements).
- *Clear the borders.* Replace column r + c (c = m, …, 1) by Σ_{k=0..r} e_{r−k}(u)·column(c + k). The entry in row j of T
  becomes u_j^{c−1} ∏_i (u_j + u_i) = 0. Do the same with rows and w. These operations do not change det B, and the
  entry in new row q + i, new column r + c is z_{i+c}, with z_j = Σ_p e_{q+r−p}(u, w)·y_{j+p}. So
  det B = V(u) V(w) · det (z_{i+c})_{i,c ≤ m}.
- *Symmetry.* (z_{i+c}) is symmetric, so the terms of σ and σ^{−1} cancel mod 2 and only involutions remain:
  det = Σ_τ ∏_{fixed i} z_{2i} ∏_{pairs {i,j}} z_{i+j}². Modulo the squares y_j² we have z_j² = 0, so only τ = identity
  remains: det (z_{i+c}) ≡ ∏_{i ≤ m} z_{2i}.
- *Read off.* Comparing coefficients of y^D:
  Σ_{R,C} s_ν(R^c)(w) s_ν(C^c)(u) L(R, C) ≡ Σ_β ∏_i e_{q+r−(β(i)−2i)}(u, w).
  With ū = 1/u: e_{r−k}(u) = e_r(u) e_k(ū) and s_ν(C^c)(u) = e_r(u)^m s_γ(C)′(ū) (complement in the r × m rectangle).
  Dividing by e_r(u)^m e_q(w)^m and applying ω (e ↔ h, s_μ′ ↔ s_μ) gives the statement; the products s_λ(X) s_γ(Y) are
  linearly independent mod 2. ∎

**Corollary 1 (skew shape).** Φ_D is the permanent of (h_{d_k − 2i}), ≡ det (h_{d_k − 2i}) = s_θ(x) by Jacobi–Trudi:
θ(x) = α/δ with δ = (m−1, …, 1, 0) and α_a = (m − a) + x_{m+1−a}. The condition x_{k+1} ≥ x_k − 1 (distinct diagonals)
is exactly "α is a partition"; a negative letter gives α ⊉ δ and s_θ = 0.
- Every count L_x(t) is even as soon as x has a negative letter. (At the end of a word: N(D) is even unless D is the main diagonal.)
- Zeros only separate rows: x and x with zeros inserted/removed have the same parities when the shape is unchanged.
- x ∈ {0,1}^m with s ones: θ = s separate cells, Φ = h_1^s, so **L_x(λ|γ) ≡ C(s, |λ|)·f^λ·f^γ** (f = number of standard
  tableaux) — the weight `dim` of `../weights/REPORT.md` mod 2, for every such x.
- Staircase x = (k, …, 1): θ = δ_k rotated, **L_x(λ|γ) ≡ c^{δ_k}_{λγ}** (Littlewood–Richardson coefficient).
- For every x ≥ 0 the state (−|γ) with γ = letters of x sorted has an odd count, and so has γ = conjugate of the sorted
  column lengths of θ(x) (the two extreme terms of a skew Schur function have coefficient 1).

Test (`parity.py`): all 394 prefixes with letters ≥ 0, length ≤ 6, slack ≤ 5 (5,703 states with a placement, plus all
states without one), and 192 prefixes with letters of both signs (length ≤ 5, slack ≤ 4): 0 parity mismatches; negative
letters add no odd count. `g1parity.py 7`: with rows 1..m and columns {1..m+1} minus c, the sets D with an odd number
of placements are exactly the C(m, c−1) words in {0,1}^m with m + 1 − c ones.

## 2. Theorem: {0, 1} then {0, −1}
**Theorem 2.** Let x ∈ {0,1}^m and y ∈ {0,−1}^{m′} have s ones and s minus-ones. Then x y has a permutation.

*Proof.* Let x′ = −reverse(y) ∈ {0,1}^{m′}, n = m + m′. By Corollary 1 the counts at (−|1^s) and (−|s) are ≡ f = 1, so
- there is σ_1: {1..m} → {1..m+1} ∖ {m+1−s} with sums {2k + x_k} (state (−|1^s));
- there is σ_2: {1..m′} → {1..m′−1} ∪ {m′+s} with sums {2k + x′_k} (state (−|s)).
Put σ = σ_1 on rows 1..m and σ(n+1−i) = n+1−σ_2(i) on rows m+1..n. The columns of the second part are
{m+2..n} ∪ {m+1−s}, the complement of the first; its sums are 2n + 2 − (2k′ + x′_{k′}) = 2k + y_{k−m} for k = n+1−k′. ∎

Nothing here uses the last letters of x, x′, so the theorem also holds with a repeated diagonal at the junction
(x ends in 1, y starts with −1). Directly, without symmetric functions: the number of σ_1 is the squarefree part of
the coefficient of t^s in det[[H], [t^m … t 1]] = det (y_{i+c} + t·y_{i+c+1}) ≡ ∏_k (y_{2k} + t·y_{2k+1}).
The proof is not constructive: `a2count.py 13` — the number of σ_1 is odd for every word (1 for m − 1 words of each length m, e.g. 1 0^a 1^b 0 at m = 5; up to 249 at m = 13).
No explicit rule found; the "near-diagonal" skeleton fails (`../l1form`).

## 3. What parity gives for all unimodal words (item 3)
O(x) = states with an odd count ⊆ F(x). **PAR:** O(x) ∩ conj O(x′) ≠ ∅ ⇒ x y solvable (x′ = −reverse y).
- *Proved family.* If the positive letters of x, sorted, equal the sorted column lengths of θ(x′) (column j has
  #{k : k ≤ j < k + x′_k} cells), then x y is solvable: (−|γ) is an extreme term on both sides. Contains Theorem 2
  (all ones), the staircases (k, …, 1, 0^j, −1, …, −k) for every j ≥ 1 (j = 1 is the cyclic shift, j = 2 Nordh's F1) and
  e.g. (2^a, 1, 0^j, −1, (−2)^a). Extreme terms tested by `extreme.py 6 6`.
- *Tested, `par.py 9` (4 s), exact for the slack:* every pair (x ≥ 0 ending 1, x′ ≥ 0 ending 0) at slack ≤ 7 has a
  common odd state; failures: 4 of 64 pairs of distinct odd sets at slack 8 (e.g. x = 1^8 against (1,0,1,0,3,2,1,0) and (2,3,2,1,0)), 2 of 144 at slack 9 (x = 1^9 against (3,3,2,1,0) and the mirror). No single state is odd for all x from slack 5 on.
- So UNIMODAL is reduced, for most cuts, to: s_{α/δ} and s_{α*/δ}′ share an odd term in X ∪ Y — a question about skew
  Schur functions over a staircase mod 2 — but a second idea is needed for cuts like 1^9 | 0 −1 −2 −3 −3. Possible
  next steps: cut somewhere else (PAR may be applied at any cut whose left part has no negative letter), or refine mod 4.

## 4. Items 1 and 2 of the brief
- **F(x) for nonnegative x (item 1).** No exact description. New lower bound, proved: F(x) ⊇ O(x) = odd terms of
  s_θ(x)(X ∪ Y); for x ∈ {0,1}* this is {C(s,|λ|) f^λ f^γ odd}, inside the parity set of card `paritycount`.
  For 0/1 words, tested s ≤ 20 (`./uplus 20 1`): there is a single inclusion-minimal F set per (slack, last letter)
  (except two at s = 5, 17 for last letter 1), so one prefix per slack is binding.
- **U⁺(s) (item 2), `./uplus 20`:** sizes 2, 4, 4, 6, 6, 2, 6, 12, 8, 14, 12, 22, 26, 40, 40, 78, 136, 184, 270, 348 for
  s = 1..20 — almost the unrestricted numbers of `../universal/REPORT.md` (the binding prefixes were already nonnegative),
  and (−|s), (−|1^s) are not in U⁺(s) at s = 4, 5, 8, 12, 16, 17, 20 (the ones looked at). No closed form. For letters in {0,1} | {0,−1}: |U⁺| = 2, 4, 8, 12, 24, 48, 80,
  126, 212, 332, …, 15,254 (s = 20), containing (−|s) and (−|1^s) at every s — this is what led to Theorem 2.

## Recheck (each under 1 minute)
    cd agents/unimodal
    python3 parity.py 6 5; python3 parity.py 5 4 neg      # Theorem 1, brute force       (out_parity_6_5.txt)
    python3 g1parity.py 7                                  # odd counts = 0/1 words        (out_g1parity_7.txt)
    python3 a2count.py 11                                  # sigma_1 exists, odd count     (out_a2count_11.txt)
    python3 extreme.py 6 6                                 # extreme states are odd
    python3 par.py 9                                       # PAR on unimodal cuts          (out_par_9.txt)
    g++ -O2 -o uplus uplus.cpp && ./uplus 20 > /dev/null && ./uplus 20 1 > /dev/null   # U+(s)  (out_uplus_20.txt, out_uplus01_20.txt)
    python3 look.py 1 1 0 0 -1 -1                          # solutions of one word

Suggested card (not added; `map/build.py` untouched): "parity of placement counts = LR numbers (proved); {0,1}|{0,−1} proved".
