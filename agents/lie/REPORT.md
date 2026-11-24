# lie: the conjecture as a statement about weights of sl_n, and the same statement for other root systems

**HIT (proved, a restatement).** Write ρ = (n−1, n−2, …, 0) and, for a valid D with scores s_1 ≤ … ≤ s_n, λ = (s_n, …, s_1).
- D valid ⇔ λ is a partition majorised by ρ ⇔ λ is a dominant weight with λ ≤ ρ in the root order of sl_n
  (Landau's inequalities are the majorisation inequalities).
- With rows reflected, a stone in row i and column j (both counted from 0) has sum i + j = d + n − 1, so the sorted
  sums are s_k + k − 1, i.e. the vector λ + ρ. A permutation matrix is a pair of orderings of 0…n−1, so
  **D is solvable ⇔ λ + ρ = wρ + w′ρ for two permutations w, w′ ⇔ λ + ρ is conjugate to ρ + wρ for some w**, and the
  number of solutions is N(D) = #{w : ρ + wρ is a rearrangement of λ + ρ}.
- Distinct diagonals ⇔ λ + ρ has distinct coordinates ⇔ it is a regular weight. Every regular dominant weight is
  λ + ρ with λ dominant, and λ + ρ ≤ 2ρ ⇔ λ ≤ ρ.

So the conjecture is: **every regular dominant weight μ ≤ 2ρ of sl_n is conjugate to ρ + wρ for some permutation w.**
The weights conjugate to ρ + wρ are the "generalised PRV weights" of V(ρ) ⊗ V(ρ): by the PRV conjecture (a theorem
of Kumar and Mathieu) the representation V(μ) occurs in V(ρ) ⊗ V(ρ) for each of them. Kostant's conjecture (in
Berenstein–Zelevinsky 1992, who prove it for sl_n; other proofs by Chirivì–Kumar–Maffei and arXiv:2309.06890) says
V(μ) occurs in V(ρ) ⊗ V(ρ) for EVERY dominant μ ≤ 2ρ. The x-ray conjecture is the sharper statement that for regular
μ the occurrence is already explained by an extremal weight. Also ρ + wρ = 2ρ − (sum of the inversion roots of w⁻¹).
Without regularity it is false (repeated diagonals: card `thrice`), in agreement with 1105 of 1111 at n = 7 below.
Literature statements are paraphrased from abstracts found by web search; I did not find this question
("which components of V(ρ) ⊗ V(ρ) are PRV components") treated anywhere. Not checked in depth.

**HIT (tested): the same statement in the other root systems.** For a root system with Weyl group W and half-sum ρ:
is every regular dominant μ ≤ 2ρ (μ − 2ρ in the root lattice) of the form w′(ρ + wρ)?

| type | dominant μ ≤ 2ρ | of the form ρ + wρ | regular | regular and NOT of that form |
|---|---|---|---|---|
| A_2, A_4, A_6 | 5, 59, 1111 | 5, 59, 1105 | 2, 9, 59 | 0 (and n ≤ 22 by the known exhaustive check) |
| B_2 … B_6 | 8, 39, 210, 1192, 6996 | 7, 32, 174, 1024, 6273 | 2, 6, 19, 64, 223 | 0 |
| C_2 … C_6 | 8, 35, 185, 1021, 5941 | 7, 30, 159, 917, 5499 | 2, 8, 26, 81, 277 | 0 |
| D_4, D_5, D_6 | 89, 497, 2987 | 86, 477, 2891 | 14, 44, 147 | 0 |
| E_6 | 4679 | 4543 | 226 | 0 |
| E_7 | 54573 | 53801 | 1464 | 0 |
| G_2 | 14 | 10 | 5 | **2**: μ = ρ + ω_1, ρ + ω_2 |
| F_4 | 451 | 383 | 58 | **2**: μ = (2,1,3,1), (3,2,1,1) in fundamental weights |

So the statement is not a general fact about root systems (it fails in G_2 and F_4), but it holds in every classical
type and in E_6, E_7 as far as tested. In coordinates the classical cases are board problems of the same kind:
- type C_n: a permutation σ of 1…n and a sign for each i; the stone of row i reads i + σ(i) or |i − σ(i)|. Claim: every
  set of n distinct positive integers m_1 > … > m_n with even sum and m_1 + … + m_k ≤ k(2n − k + 1) for all k is
  read by some choice. (All signs + is the x-ray problem itself, read along anti-diagonals.)
- type B_n: the same with half-integers ρ_i = i − ½; type D_n: ρ_i = i − 1 and an even number of minus signs.

**Recheck** (each under 20 seconds except E 7, 4 minutes): `python3 prv.py B 5`, `python3 prv_gen.py F 4`,
`python3 prv_gen.py G 2`, `python3 prv_gen.py E 6`. `prv.py` (coordinates) and `prv_gen.py` (Cartan matrix) are
independent and agree on B_3, C_4, D_5, A_4.

**What it might be good for.** (1) A second family of true instances (types B, C, D) to test any proposed mechanism
against, with more freedom (signs). (2) The failures in G_2 and F_4 say a proof cannot use only general properties
of Weyl groups. (3) The representation-theoretic tools for PRV components (Demazure modules, Littelmann paths) give
existence of V(μ) but not of an extremal weight; I have no argument from them.
