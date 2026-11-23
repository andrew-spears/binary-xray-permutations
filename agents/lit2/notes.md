# lit2 notes (2026-11-22): literature on the integer analogue of Hall, rainbow matchings, and the Skolem side

## Q1: an integer (non-wrapping) Hall 1952
I found no integer theorem that says which sets or multisets of displacements π(i) − i of permutations of [n] occur. Everything Hall-like I found works modulo n or in other groups:
- Hall 1952: cyclic and abelian groups.
- Kohen–Sadofschi Costa, arXiv:1603.06625: pairings of Z_{2n} with prescribed unit differences (Adamaszek's conjecture). They use Hall as a lemma.
- Preissmann–Mischler: Z_p.
- Zabokritskiy, arXiv:2607.08630: F_2^s (the Balister–Győri–Schelp "two-hole" problem), done with a coefficient (Nullstellensatz-type) method on a group circulant. A possible template; see the notes on the permanent below.
- Aliabadi, arXiv:2605.16478: a nonabelian version. Its Thm 3.4 is a "cycle-tiling criterion".
- Ullman–Velleman, "Differences of bijections", Amer. Math. Monthly 126 (2019) 199–216: an exposition covering infinite abelian groups. These are bijections of all of Z, not of [n].
- Cruz–Ramos–Rubio slides (2021): a block decomposition of Hall solutions in Z_n into zero-sum irreducible blocks plus shifted partial sums.
- Del Lungo, TCS 281 (2002): reconstructing a permutation from its diagonal sums takes polynomial time "on a cylinder" (wraparound). Non-binary and non-wrapping is NP-complete (Yu 1996; Nordh, DAM 158 (2010) "hardness of Skolem-type sequences"; Brunetti–Del Lungo–Gritzmann–de Vries, TCS 406 (2008)).
- Brualdi–Dahl, arXiv:1908.03739: they characterize the discrete derivatives π(i+1) − π(i) (Prop 2.5). That is a different statistic, not π(i) − i.
- OEIS A099152: W summed over all D, i.e. the number of permutations with distinct π(i) − i. It equals the number of transversals of the integer table i + j (Cavenagh–Wanless, DAM 158 (2010)). Counting only.
- Arsovski/Snevily and Alon (Z_p, sumsets): these do not transfer, because in Z the "distinct sums" version is trivial.
- Spearman footrule and excedance-set literature: about distributions, not existence. Nothing relevant.

## Q2: rainbow matchings
All the general theorems (Aharoni–Berger, Drisko, Dirac-type and locally bounded colourings, Ryser–Brualdi–Stein) need colour classes of size at least n, or dense host graphs. Our colour classes are diagonals of size n − |d| in a sparse host graph, so none of them applies. Searches for "Toeplitz", "circulant" or "prescribed symbols" transversals turned up nothing specific.

## Q3: Skolem side
Nordh 2008 (Discrete Math. 308, 1653–1664). MaRDI/zbMATH lists 7 citing items:
1. **Brualdi–Fritscher, "Hankel and Toeplitz X-rays of permutations", Lin. Alg. Appl. 449 (2014) 350–380.** Not in state.md. It links Toeplitz/Hankel x-rays, tournaments, transversals of partial Latin squares, and Skolem sequences. It has existence theorems for binary, palindromic, skew-palindromic and equal Hankel/Toeplitz x-rays, constructions, open problems and data. Thm 1.3 (as quoted by Davis–Schroeder): characteristic sequences of permutations of Z_n ⊆ score sequences of 2-tournaments; they conjectured equality, and Nordh refuted it. They restate the conjecture as: a_1 < … < a_n < 2n is a Toeplitz characteristic iff Σ_{i≤k} a_i ≥ k², with equality at n. I could not get the full text (Elsevier).
2. Nordh, "A note on the hardness of Skolem-type sequences", DAM 158 (2010) 964–966: NP-completeness for the non-binary or multi versions.
3. "NP-completeness of generalized multi-Skolem sequences".
4. Francetić–Mendelsohn, "A survey of Skolem-type sequences and Rosa's use of them", Math. Slovaca 59 (2009).
5. Linek–Mor, "On partitions of {1,…,2m+1}∖{k} into differences d,…,d+m−1: extended Langford sequences of large defect".
6. "Strong Skolem starters".
7. "Disjoint Skolem sequences and related disjoint structures".

Also in this cluster: Nordh 2017 (arXiv:1707.03928, already known), Davis–Schroeder 2026, Li–Liu–Yao 2026, the Li–Yao MIT UROP+ 2025 report, and the Polymath Jr 2024 (Mneimneh) projects on infinite and n-copy Skolem sequences. None of them proves a new case of the set conjecture.

### Which Skolem-type families have no tight cut (my own computation)
For n = 2m and D = ±L with L = {d, …, d+m−1}:
- Scores: s_k = m − d for k ≤ m, and s_k = m + d − 1 for k > m. Symmetric D always gives s_k + s_{n+1−k} = n − 1.
- Landau holds iff m ≥ 2d − 1. This is exactly the Simpson/Langford existence bound.
- At m = 2d − 1 ("perfect Langford") the cut at k = m is tight.
- For m ≥ 2d there are no tight cuts.

So Langford sequences (parity m ≡ 0,1 mod 4 for d odd, m ≡ 0,3 mod 4 for d even) give involution witnesses for a whole no-tight-cut family. The complementary parity classes are covered by hooked or extended Langford (Linek–Mor, Linek–Jiang), with a fixed point (0 ∈ D) and n = 2m + 1. Skolem itself is the case d = 1, with scores (m−1)^m m^m (near-regular).

Near-Skolem (Shalaby; (1,m)-near-Skolem, Gu–Zhang–Cao, AJC 87 (2023)) gives ±({1..k}∖{m}). That is Nordh's F2, already in state.md.
