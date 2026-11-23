# REPORT2 (draft; item verdicts filled in below)

Notation. After n stones a state is (R, C), R = used rows, C = used columns, |R| = |C| = n, R = {λ_i + n − i + 1},
C = {μ_i + n − i + 1}; R, C ⊂ [1, 2n] because |λ|, |μ| ≤ slack ≤ n is not needed: only λ_1, μ_1 ≤ n is used below and
holds whenever the slack is ≤ n. Put **X = 2n + 1 − C** (reflected columns). The last stone of a prefix x e of
length n sits at (r, c) with r + c = 2n + e, i.e. **r − x = e − 1** with x = 2n + 1 − c in X, and
(R, C) is in F(x e) iff for some such pair (R − r, C − c) is in F(x).   (LAST)
Removing the stone shifts the reflection: the reflected columns of the remainder are (X − {x}) − 2.

## 1. F(1^n) exactly (PROVED)
P_n = parity set = states of slack n with #odd(R) = #even(C) (equivalently #odd(R) = #odd(X)).
E_n = {(λ | λ′) : |λ| = n/2, 2-core of λ empty}; E_n is empty unless 4 | n, and |E_4m| = number of pairs of partitions
of total size m (2, 5, 10, 20, 36 for n = 4, .., 20).

**Theorem.** F(1^n) = P_n ∖ E_n for every n ≥ 1.

*Proof.* Induction on n; F(1) = P_1 (both states). Let n ≥ 2.
(a) F(1^n) ⊆ P_n: every stone has an odd sum, so it joins an odd row to an even column or conversely.
(b) By (LAST) with e = 1 the last stone uses r = x in R ∩ X. If (R, C) is in P_n and r is in R ∩ X then the remainder
    is in P_{n−1} (r and c = 2n + 1 − r have opposite parity; the slack drops by 1).
(c) R ∩ X = ∅ iff μ = λ′ and |λ| = n/2. Indeed slack n gives λ_1, μ_1 ≤ n, so R, X ⊆ [1, 2n]; two disjoint n-sets
    fill [1, 2n], and X = [1, 2n] ∖ R is exactly μ = λ′ (complement of beta-numbers); then |λ| = |λ′| = n/2. Such a
    state is in P_n iff R has as many odd as even elements iff the 2-core of λ is empty. So
    {(R, C) in P_n : R ∩ X ≠ ∅} = P_n ∖ E_n, and F(1^n) ⊆ P_n ∖ E_n.
(d) If 4 ∤ n − 1 then E_{n−1} = ∅, F(1^{n−1}) = P_{n−1}, and (b), (c) give F(1^n) = P_n ∖ E_n.
(e) Let n − 1 = 4m, m ≥ 1 (so E_n = ∅) and (R, C) in P_n. Put Y = X − 2, I = [1, 2n − 2]. The remainder after
    removing r in R ∩ X is in E_{n−1} only if (R − r) ⊔ (Y − (r − 2)) = I, i.e. R + Y = I + {r, r − 2} as multisets.
    The multiset R + Y determines r, so at most one r in R ∩ X is bad; by (c) R ∩ X ≠ ∅. So (R, C) is unreachable
    only if R ∩ X = {r} with r bad. Then:
    - r ∉ I (r ≥ 2n − 1): λ_1 ≥ n − 1, the remainder has |λ_0| = |λ| − λ_1 ≤ 1 < 2m. Not in E_{n−1}.
    - r − 2 ∉ I (r ≤ 2): the same with columns (μ_1 ≥ n − 1).
    - r, r − 2 in I: both lie in R ∩ Y, every other element of I lies in exactly one of R, Y. R ∩ (Y + 2) = {r}
      forces: r + 2 ∉ R; and for t in R, t ≠ r: t − 2 ∉ Y, hence t − 2 in R whenever t − 2 ≥ 1. So in each
      parity class R is an initial segment, in the class of r it ends at r. Then R − r is [1, n − 1] (the two
      segments have (n + 1)/2 and (n − 1)/2 elements by the parity condition #odd(R) = #odd(X)), i.e. λ_0 = ∅,
      but E_{n−1} needs |λ_0| = 2m > 0. Not in E_{n−1}.
    So every state of P_n is reachable. ∎

Check: `python3 fx.py ones 20` compares with the machine for n ≤ 20.

## NOTES (working, to be rewritten)
- fx.py ones 13: Theorem confirmed by direct enumeration n <= 13 (machine data w20: n <= 20, exceptions listed = E_n).
- fx.py zeros 8 2: F(1^a 0) = parity-count set (card paritycount, z = 1, p = a) for a <= 8 except a = 4: missing -|22, 22|-;
  a = 8: missing -|44, 44|-   (guess: 4 | a: missing (∅ | (a/2, a/2)) and its swap).  F(1^a 0 0) = parity-count set
  (z = 2), a <= 8, no exceptions; for a = 4, 5, 6(65), 7(110), 8(185) that is ALL states of slack a (a=6: 0^1 gives 64/65).
- Staircase k, k-1, .., 1 has sums k+2, .., 2k+1 (consecutive); with trailing 0: k+2 .. 2k+2.  In reflected
  coordinates differences r - x take consecutive values: a Langford/Skolem-type problem (Skolem: n = 0, 1 mod 4).
- TODO item 2: w(F(1^s)) for core2 weights = 1 - w(E_s) (E_s inside core2) -> not the minimiser; need staircases at s = 21, 28, 36
  by C++ (int128 masks), weights core2 dim, core2 dim^2.
- TODO item 3: letter-1 defect from P_{n-1}: exactly E_n (step (c)); in general (LAST): the states receiving nothing from a
  letter e are those with (R + 1 - e) ∩ X = ∅.
- fx.cpp (./fx e1 e2 ...: |F| and weights dim, core2 dim, core2 dim^2 after every letter; matches machine at s = 20).
  out2/staircase.txt: staircase k..1 (l=1) and k..1 0 (l=0), k = 3..8 (s = 6, 10, 15, 21, 28, 36):
  core2 dim^2: l=1: .881 .827 .760 .754 .766 .814; l=0: .937 .909 .913 .890 .892 .903  (sum 1.64-1.82, no decay)
  core2 dim:   l=1: .681 .647 .592 .565 .569 .599; l=0: .817 .782 .768 .735 .726 .725  (sum ~1.30-1.32 at k=6..8)
  dim:         l=1: .646 .591 .579 .588 .595 .603; l=0: .838 .785 .766 .752 .741 .732
  k = 9 (s = 45, 54 s, 0.9 GB): l=1: |F| 3,700,460  dim .6058  core2 dim .6063  core2 dim^2 .8301;
                               l=0: |F| 5,515,478  dim .7235  core2 dim .7182  core2 dim^2 .9010
- NEXT: (i) fx.py zeros 12 1 too slow in python -> check guess for 1^12 0 with ./fx sizes vs parity-count size;
  (ii) near-staircases (k k k-1 .. 1; minimisers at s = 16..24 from out/argmin_core2dim2_20.txt) at s ~ 30-40 via ./fx;
  (iii) item 3: defect sets via (LAST); letter-0 flow proof attempt (growth diagram) or NOTHING;
  (iv) rewrite REPORT2.md (verdict per item), add runs2.sh, PR into devin/1795444188-two-marks.
