# lie2: literature on ρ + wρ, why G_2 and F_4 fail, and type C as a board problem

Notation as in `../lie/REPORT.md`: "PRV" means W-conjugate to ρ + wρ; S(Φ) is the statement "every regular dominant
μ ≤ 2ρ of Φ is PRV". The conjecture is S(A_{n−1}) for all n. Weights are in fundamental-weight coordinates, node
numbering as in `../lie/prv_gen.py`. Working notes: `NOTES.md`.

| part | verdict |
|---|---|
| A literature | **NOTHING** for regular μ (one named class is covered, but its only regular member is 2ρ) |
| B G_2, F_4 | **HIT** (proved + tested): the non-simply-laced statements are "symmetric weights have symmetric witnesses" for A/D/E; the four failing weights are PRV in D_4 and E_6 |
| C type C board | **NOTHING** (no easy proof; and proved: any proof of type C_n contains type A_{n−1}) |

## A. Literature — NOTHING

Read in full text (theorem numbers are from the texts):

- **Chirivì–Kumar–Maffei, Components of V(ρ)⊗V(ρ), Transform. Groups 22 (2017) 645–650.**
  Theorem 3: if λ ≤ 2ρ is dominant and d is a saturation factor then V(dλ) ⊂ V(dρ)⊗V(dρ) (d = 1 for sl_n).
  Lemma 8 / Proposition 9: every dominant λ ≤ 2ρ is ρ + β with β a weight of V(ρ) (β need not be extremal, i.e. need
  not be in Wρ; the proof writes the vertices 2ρ − Σ_{Φ_J^+} α as ρ + w_0^J ρ and takes convex combinations).
  Remark 4: Berenstein–Zelevinsky proved Kostant's conjecture for sl_{n+1} (their Theorem 6).
  Remark 7: Kostant's conjecture checked with LiE for G_2, F_4 (the authors) and E_6, E_7, E_8 (Papi). So the four
  failing weights of part B are components of V(ρ)⊗V(ρ) that are not PRV.
- **A. Boysal, On Kostant's conjecture for components of V(ρ)⊗V(ρ), arXiv:2309.06890** (this is the paper behind the
  arXiv number in the task; it is by Boysal, not CKM). Proposition 2.3 (attributed to Kostant): the vertices of the
  dominant polytope P(2ρ) are exactly ρ + w_J ρ, w_J the longest element of the parabolic subgroup W_J, J ⊂ simple
  roots. Theorem 1.3: for every simple g each vertex occurs in V(ρ)⊗V(ρ) with multiplicity one. Theorem 1.4 = CKM
  Theorem 3 by a different proof. Introduction: for sl_{r+1}, V(λ) has multiplicity one iff λ is a vertex of P(2ρ)
  (quoted as Berenstein–Zelevinsky Theorem 14); "only if" fails outside type A (B_2, λ = 2ω_2).
  **This is the named class: {ρ + w_J ρ} = vertices of P(2ρ) are PRV in every type.** But ρ + w_J ρ is orthogonal
  to the simple roots in J, so the only regular one is 2ρ (J = ∅): in board terms the class is the tight-cut
  decomposition into blocks P_k, i.e. nothing new.
- **Dimitrov–Roth, Cup products of line bundles on homogeneous varieties and generalized PRV components of
  multiplicity one, Algebra Number Theory 11 (2017) 767–815** (introduction and statements read; proofs not).
  Theorem I: the cup product H^{d_1}(L_{λ_1}) ⊗ H^{d_2}(L_{λ_2}) → H^d(L_λ) is surjective iff the inversion set of w
  is the disjoint union of those of w_1, w_2. Theorem II: a "cohomological component" is a generalised PRV component
  of stable multiplicity one, and conversely if one weight is strictly dominant or G is classical; the Remark after it:
  in type A, cohomological ⇔ PRV of multiplicity one. With the multiplicity-one statement above: for sl_n the cohomological components of V(ρ)⊗V(ρ) are among the vertices, so
  this machinery reaches no regular μ other than 2ρ.

Abstract or secondary quotation only (not read): Berenstein–Zelevinsky, J. Algebraic Combin. 1 (1992) 7–22 (paywalled;
its Theorems 6 and 14 are quoted above from CKM and Boysal; the abstract says multiplicities are counted as integer
points of a cone and the conjecture is proved by linear programming — I could not check whether the proof exhibits
extremal weights for regular μ); Montagard–Pasquier–Ressayre,
arXiv:1004.2119 and 1110.4621 (abstracts: further components that occur "for the same reason" as PRV ones; not checked
whether they say anything for V(ρ)⊗V(ρ)); Jeralds–Kumar 2025 (affine analogue of CKM); Kostant's Λg papers,
Suter math/0210463, Panyushev, Bazlov math/0012244 (abelian ideals of the Borel and graded multiplicities in Λg; abstracts and
introductions only, no statement about inversion sets or regular weights seen); OEIS A362968 (comment: sums
of two permutations are all integer points of twice the permutohedron only for n ≤ 5).

I found no statement anywhere about which regular dominant weights are conjugate to ρ + wρ. Search time about 40
minutes.

## B. G_2 and F_4 — HIT

**The failing weights.** (`python3 fail.py G 2`, `python3 fail.py F 4`, a few seconds.)

| type | regular dominant μ ≤ 2ρ | not PRV | 2ρ − μ in simple roots | (μ, μ), long roots of norm 2 |
|---|---|---|---|---|
| G_2 (α_1 long) | 5 | (1,2) | 2α_1 + 3α_2 = highest root | 26/3 |
| | | (2,1) | α_1 + 2α_2 = highest short root | 38/3 |
| F_4 (α_1, α_2 long) | 58 | (2,1,3,1) | (2,4,5,3) | 119 |
| | | (3,2,1,1) | (1,3,5,3) | 127 |

**Which simple necessary condition do they violate?**
- G_2: the norm. (μ, μ) must equal 2(ρ,ρ) + 2(ρ, wρ) for some w; 26/3 and 38/3 are not among the 12 values
  (proved by listing; `python3 norm.py G 2`).
- F_4: none that I could find. Both norms are attained (`norm.py F 4`); 2ρ − μ lies in the lattice spanned by the
  2ρ − μ′ of the 56 PRV weights (that lattice is the whole root lattice); each failing weight is the midpoint of two
  regular PRV weights (`python3 sep.py F 4`). So no condition of the form "convex set + lattice coset" separates
  them, and replacing "≤ 2ρ" by "in the hull of W·2ρ plus a coset" cannot repair the statement (in G_2 the PRV
  lattice has index 2, but (1,2) is still the midpoint of (1,1) and (1,3)).
- The norm condition is never violated in A_5, A_6, B_5, B_6, C_5, C_6, D_5, D_6, E_6 (`norm.out`), so it is vacuous
  in the classical types in tests.
- ρ + wρ^∨-type mixtures (a = ρ_long + sρ_short, b = ρ_long + tρ_short, "regular μ ≤ a + b is conjugate to a + wb"):
  (s,t) = (1,1) is the only pair with no misses in B_2…B_4, C_3, C_4; (1,2) misses 4/20 in C_3, 18/111 in C_4,
  2/8 in G_2, 24/157 in F_4 (`python3 mix.py TYPE rank`). No repair.

**What is going on: folding (proved).** Let X be simply laced, s a diagram automorphism whose orbits of simple roots
are mutually orthogonal, Y the folded type (simple roots = orbit sums: D_4 → G_2, E_6 → F_4, A_{2n−1} → B_n,
D_{n+1} → C_n). Then
1. weights of Y = s-symmetric weights of X (same fundamental coordinates on each orbit), ρ_Y = ρ_X, W(Y) = the
   centraliser W(X)^s, and the root order of Y is the root order of X restricted to symmetric weights (the symmetric
   part of the positive root cone of X is spanned by the orbit sums);
2. for w ∈ W(X): ρ + wρ is symmetric iff w ∈ W(X)^s (ρ is regular, so s(w)ρ = wρ forces s(w) = w).

Hence **S(Y) ⇔ every s-symmetric regular dominant μ ≤ 2ρ of X has an s-symmetric witness w.** The non-simply-laced
statements are symmetric refinements of the simply-laced ones, and:

| folding | symmetric regular μ ≤ 2ρ | without any witness in W(X) | with a witness but no symmetric one |
|---|---|---|---|
| D_4 → G_2 (triality) | 5 | 0 | 2: (1,2,1,1), (2,1,2,2) (6 witnesses each) |
| E_6 → F_4 | 58 | 0 | 2: (2,1,3,1,2,1) (24 witnesses), (3,2,1,2,3,1) (12) |
| A_3, A_5, A_7 → B_2, B_3, B_4 | 2, 6, 19 | 0 | 0 |
| D_4 … D_7 → C_3 … C_6 | 8, 26, 81, 277 | 0 | 0 |

(`python3 fold.py`, 15 seconds; it also checks 1 and 2 on these cases.)

**Corrected uniform statement.** "Every regular dominant μ ≤ 2ρ is conjugate to ρ + wρ with w in the Weyl group of
the simply-laced unfolding" — equivalently, **S(Φ) for simply-laced Φ only**. It survives every type tested:
A (the conjecture, n ≤ 22), D_4…D_6, E_6, E_7 (`../lie`), and G_2, F_4, B_n, C_n as above (E_8 still not run). The
G_2 and F_4 failures are failures of *symmetry of the witness*, not of existence.

**What a uniform proof must use.** It must break under folding: any argument that produces a witness from μ by a rule
commuting with diagram automorphisms would prove S(G_2) and S(F_4), which are false. In type A the automorphism is the
mirror D ↦ −D (board rotated by 180°), W^s = centrosymmetric permutations, and the same remark already bites:
- even board 2n: S(B_n) = "every symmetric valid D has a centrosymmetric witness" (true in tests, card in state.md §3);
- odd board 2n+1: the orbit {α_n, α_{n+1}} is not orthogonal; the symmetric weights with a centrosymmetric witness
  are those with Σ_{d ∈ D, d > 0} d even (the witness reads |i ± σ(i)|, and Σ (i ± σ(i)) is even), and on these the
  statement is exactly S(C_n). So half of the symmetric D on odd boards (280 of 557 at size 13, as the sympair
  agent counted) have no centrosymmetric witness for a parity reason, and the rest have one for n ≤ 7 (size ≤ 15;
  `ctype.py`). No canonical mirror-equivariant construction of witnesses exists in type A.

Not explained: why symmetric witnesses always exist for the order-2 foldings of A and D and not for E_6 or triality.

## C. Type C_n as a board problem — NOTHING

Setting (`ctype.py`): ρ = (n, …, 1); a target is m_1 > … > m_n ≥ 1 with even sum and m_1 + … + m_k ≤ k(2n − k + 1);
a solution is a permutation σ and signs with {|i ± σ(i)|} = {m}. Deficiency δ = (n(n+1) − Σ m)/2 ≥ 0.

- **All targets are solvable for n ≤ 7** (2, 8, 26, 81, 277, 996 targets for n = 2…7; `ctype7.out`; this extends the C_n test from rank 6 to 7).
- **Proved: type C_n contains type A_{n−1}.** If δ = 0 then Σ |i ± σ(i)| = Σ (i + σ(i)) forces every sign to be +, and
  the conditions on m are Landau's conditions for the sums i + σ(i). So the δ = 0 targets of C_n are exactly the valid
  D of size n (59 of the 996 at n = 7), with the same solutions, and there is no sign freedom there. The same holds
  for B_n and D_n, and in general S(Φ) implies S of every sub-diagram (Levi heredity, `NOTES.md`). So an easy proof of
  type C cannot exist unless it is a proof of the conjecture; the question "which step breaks with all signs +" has
  the answer "the proof would have to handle that case itself".
- So the only way sign freedom could help is an **induction on δ** down to type A. The natural step — a target with
  δ > 0 has a solution in which some minus row can be flipped to + keeping the values distinct, i.e. it comes from a
  solved target of smaller deficiency by one sign flip — fails: 1 of 6 targets at n = 3 ((6,3,1)), 5 of 22 at n = 4,
  11 of 72 at n = 5, 27 of 255 at n = 6 (`python3 c_def.py 6`, 20 seconds). Requiring a solution with exactly one
  minus row fails for 75 of 255 at n = 6.
- **Greedy** (rows n, n−1, …, each takes the largest readable remaining value) fails from n = 4, first at (7,5,4,2);
  608 of 996 targets at n = 7.
- **Remove the last row and column** (row n reads some m_j with value v, the row holding value n reads another m_k,
  re-close to a target of C_{n−1}): valid reductions that do not lift exist from n = 4 (32 of 102; 3042 of 12148 at
  n = 7), and from n = 4 there are prime targets (no tight cut) where no reduction lifts at all:
  (7,5,4,2), (8,7,5,3,1), (11,9,8,7,3,2), (13,11,10,9,6,3,2) (`c_ind.out`; `python3 c_ind.py 6`, under a minute).

Nothing here is easier than in type A; the positive-deficiency targets just have more solutions (least number of
solutions of a prime target at n = 7: 2, 4, 4, 12, 12, 20 for δ = 1…6).

## Recheck (all under 10 minutes together, run in this directory)

    python3 fold.py                       # B: folding table
    python3 fail.py G 2; python3 fail.py F 4; python3 norm.py G 2; python3 norm.py F 4; python3 sep.py F 4
    python3 ctype.py 6; python3 c_def.py 6; python3 c_ind.py 6       # C
