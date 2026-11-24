# REPORT2. Item 1: HIT (F(1^a 0^b) exactly, proved); staircases NOTHING. Item 2: dim has no chance, core2·dim² flat to s = 45 (tested). Item 3: defect of every letter (proved); letter-0 flow NOTHING.

Follow-up to `REPORT.md`. Everything marked PROVED is a short counting argument written out below; the rest is tested.

**Coordinates.** After n stones a state is (R, C) = (used rows, used columns), |R| = |C| = n,
R = {λ_i + n − i + 1}, C = {μ_i + n − i + 1}, slack s = |λ| + |μ|. Put **X = 2n + 1 − C**. Throughout n ≥ s, so
R, X ⊆ [1, 2n]. Stone n of a prefix with last letter e sits at (r, c), r + c = 2n + e, so with x = 2n + 1 − c:

**(LAST)** (R, C) ∈ F(x e) iff there is r ∈ R with r + 1 − e ∈ X such that (R − r, C − c) ∈ F(x).

D = #odd(R) − #even(C) = #odd(R) − #odd(X). A stone with odd sum does not change D, a stone with even sum changes
it by ±1 (odd row and column: +1). So D ≡ (number of even letters) mod 2 and |D| ≤ that number (card `paritycount`).

## 1. Exact reachable sets

### 1.1 Three theorems (PROVED; checked a ≤ 24 for 1.1–1.2, a ≤ 20, b ≤ 4 for 1.3)
- P_n = {slack n, D = 0}; Q_{a,b} = {slack a, n = a + b stones, |D| ≤ b}.
- E_n = {(λ | λ′) : |λ| = n/2, 2-core of λ empty}; empty unless 4 | n; sizes 2, 5, 10, 20, 36, 65 for n = 4, …, 24.
- E⁰_a = {(2ν2 | 2κ2) : |ν| + |κ| = a/4, β(ν) ∩ (a − β(κ)) is one point}, where 2ν2 = ν with every box replaced by
  a 2 × 2 block and β(ν) = {ν_i + a/2 − i + 1 : i ≤ a/2}; empty unless 4 | a; sizes 2, 2, 4, 5, 6, 10 for a = 4, …, 24
  (a = 12: −|66, 66|−, 22|2222, 2222|22).

**Theorem 1.** F(1^n) = P_n ∖ E_n.
**Theorem 2.** F(1^a 0) = Q_{a,1} ∖ E⁰_a.
**Theorem 3.** F(1^a 0^b) = Q_{a,b} for b ≥ 2. Q_{a,b} is every state of slack a once b is large enough (a ≤ 11:
b ≥ 2; a ≤ 19: b ≥ 3; a = 20: b ≥ 4), so **F(1^a 0^b) = all states** from there on.

*Proof of Theorem 1.* Induction on n. F ⊆ P_n by the parity count. By (LAST) the last stone uses r ∈ R ∩ X, and the
remainder of a state of P_n is in P_{n−1}.
(c) R ∩ X = ∅ iff R ⊔ X = [1, 2n] iff μ = λ′ (complement of beta-numbers), and then |λ| = n/2; D = 0 says R has n/2
odd elements, i.e. the 2-core of λ is empty. So {P_n, R ∩ X = ∅} = E_n and F(1^n) ⊆ P_n ∖ E_n.
(d) If 4 ∤ n − 1, F(1^{n−1}) = P_{n−1} and every state of P_n ∖ E_n has a last stone: equality.
(e) Let n − 1 = 4m ≥ 4 (so E_n = ∅), (R, C) ∈ P_n, Y = X − 2, I = [1, 2n − 2]. Removing r ∈ R ∩ X lands in
E_{n−1} iff R + Y = I + {r, r − 2} as multisets; that determines r, so at most one r is bad, and (R, C) is
unreachable only if R ∩ X = {r} with r bad. If r ∉ I then λ_1 ≥ n − 1 and the remainder has |λ_0| ≤ 1 < 2m; same
for r − 2 ∉ I with μ. Otherwise r, r − 2 ∈ R ∩ Y and every other element of I is in exactly one of R, Y. For t ∈ R,
t ≠ r: t ∉ X, so t − 2 ∉ Y, so t − 2 ∈ R; and r + 2 ∉ R. So R is an initial segment in each parity class, ending at
r in the class of r; D = 0 gives #odd(R) = (n − 1)/2 + [r odd], hence R − r = [1, n − 1], λ_0 = ∅, not in
E_{n−1}. So no state of P_n is unreachable. ∎

*Pigeonhole (used below).* Let b ≥ 1, slack a, n = a + b, so R ⊆ [1, 2n − b], X ⊆ [b + 1, 2n]. A last stone 0 is
r ∈ R with r + 1 ∈ X. Odd r: R_odd + 1 and X_even are sets of even numbers in [2, 2n] of total size n + D, so at
least D choices. Even r: R_even + 1 and X_odd are sets of odd numbers in [3, 2n − 1] of total size n − D, so at
least 1 − D choices. An odd r lowers D by 1, an even r raises it.

*Proof of Theorem 2.* n = a + 1, D = ±1, the remainder must be in P_a ∖ E_a, which forces odd r for D = 1 and even
r for D = −1; such r exist (pigeonhole: ≥ 1, resp. ≥ 2). As in (e) at most one r is bad (R + Y = I + {r, r − 1},
Y = X − 2, I = [1, 2a]). So D = −1 is always reachable, and D = 1 is unreachable iff (R_odd + 1) ∩ X_even = {r + 1}
with r bad. The cases r = 2n − 1, r = 1 give λ_0 = ∅ or |λ_0| = a. Otherwise r − 1, r ∈ R ∩ Y, every other element
of I in exactly one of them; uniqueness of r says: odd t ∈ R, t ≠ r ⇒ t − 1 ∈ R, and even u ∈ Y, u ≠ r − 1 ⇒
u + 1 ∈ Y. So each pair {2j, 2j + 1} (1 ≤ j ≤ a − 1) lies in R or in Y, the pair of r in both; counting odd and
even elements with D = 1 gives 1 ∈ R, 2a ∈ Y. Hence R = {1} ∪ pairs(A), C = 2n − 1 − Y = {1} ∪ pairs(B) with
|A| = |B| = a/2, A ∩ (a − B) = {q}; λ = 2ν2, μ = 2κ2 with β(ν) = A, β(κ) = B, and slack a means |ν| + |κ| = a/4.
Conversely such a state has the single last stone r = 2q + 1 and it is bad. ∎

*Proof of Theorem 3.* b ≥ 3 from b − 1: if D ≥ 1 remove an odd r, if D ≤ 0 an even r (pigeonhole); the remainder
has |D′| ≤ b − 1. b = 2: D = −2: even r, remainder has D′ = −1, no exception. D = 2: at least two odd r; if
R − r₁ and R − r₂ were both {1} ∪ pairs, then r₂ = 2j + 1 with 2j ∈ R (or r₂ = 1, then swap the roles) and
R − r₂ contains 2j without 2j + 1: contradiction; so one of them is not in E⁰_a. D = 0: an even r exists; if its
remainder is in E⁰_a (sets A, B as above) then A ∩ (a + 1 − B) ≠ ∅ (otherwise a − B is an up-set, so a − B =
[a/2, a − 1], A = [1, a/2], ν = κ = ∅), and j in it gives an odd last stone (2j + 1, 2(a + 1 − j) + 1) with D′ = −1. ∎

Check: `python3 ones0.py 24` (30 s), `python3 zeros.py 20 4` (20 s), `python3 fx.py ones 13` (independent brute force).

### 1.2 Other words in {0,1}* (tested, length ≤ 10: `zo.py 10`, `out2/zo_10.txt`)
F(x) is not "parity set minus a small family" in general. After a last letter 1 all (λ | λ′) are missing (§3), e.g.
the words of slack 6 with two zeros ending in 1 miss 111|3, 21|21, 3|111; words 1 0 1^j miss much more (1 0 1^8: 80 of 292).
Words starting with 1: 341 of 1,023 differ from the parity-count set.

### 1.3 Staircases: NOTHING
k, k−1, …, 1 has sums k+2, …, 2k+1: (R, C) is reachable iff R can be matched to X with **differences x − r equal to
0, 1, …, k − 1, each once**; with a trailing 0: differences 1, …, k + 1 (if R ⊔ X = [1, 2k + 2] this is a Skolem
sequence). `stair.py`, `stair6.py`:

| prefix | \|F\| | plain LP feasible (`agents/fshape/lp.py`) |
|---|---|---|
| k … 1, k ≤ 5 | 6, 27, 151, 982 | the same sets |
| k … 1 0, k ≤ 4 | 8, 40, 233 | the same sets |
| 5 4 3 2 1 0 | 1,542 | 1,546 (22\|4421, 33\|4311 and swaps) |
| 6 … 1 / 6 … 1 0 | 7,134 / 11,090 | 7,158 / 11,114 |

Of the 48 exceptions at k = 6 only 2 fail a residue count (mod 8; moduli 2..9 tested). No description found.

## 2. Which weight can work for all s
**dim cannot.** On the exact sets of §1 (`tail.cpp`, `out2/tail_60.txt`; s = 20 agrees with the machine):

| s | 20 | 32 | 40 | 48 | 60 |
|---|---|---|---|---|---|
| dim(F(1^s)) | 0.555 | 0.498 | 0.477 | 0.461 | 0.437 |
| dim(F(1^s 0)) | 0.874 | 0.832 | 0.805 | 0.779 | 0.757 |
| sum (≥ a(0) + a(1)) | 1.429 | 1.329 | 1.282 | 1.240 | 1.193 |

Reason: D = c(λ) + c(μ) up to a constant, c = charge of the 2-core, and under dim the 2-cores grow with s, so every
fixed value of D loses its weight. (Not proved here; the decay is slow: at the present rate the sum reaches 1
somewhere beyond s ≈ 110.)

**core2 weights ignore these prefixes**: core2 ⊆ P_s and ⊆ Q_{s,1}, so only E_s and E⁰_s are lost: core2·dim² of
F(1^s) is .950, .940, .975, .977 for s = 12, 16, 20, 24 and 1 otherwise; of F(1^s 0) it is ≥ .9994 from s = 12. Their
minimisers are the staircases (`fx.cpp`, direct enumeration, `out2/staircase.txt`):

| k (s) | 3 (6) | 4 (10) | 5 (15) | 6 (21) | 7 (28) | 8 (36) | 9 (45) |
|---|---|---|---|---|---|---|---|
| core2·dim², k…1 | .881 | .827 | .760 | .754 | .766 | .814 | .830 |
| core2·dim², k…1 0 | .937 | .909 | .913 | .890 | .892 | .903 | .901 |
| core2·dim, k…1 | .681 | .647 | .592 | .565 | .569 | .599 | .606 |
| core2·dim, k…1 0 | .817 | .782 | .768 | .735 | .726 | .725 | .718 |

So on staircases a(0) + a(1) is 1.64–1.73 for core2·dim² with no downward trend, and 1.29–1.33 for core2·dim
(the 0-side still falls slowly). Staircases with one letter lowered (s = 22..27, 29..35, 44) and double staircases
(s = 25, 30, 36) are all higher (`out2/near.txt`; lowest: .828 for 6 5 5 4 3 2 1, s = 26, and .918 for 8 8 7 6 5 4 3 2 1 0, s = 44).
**No monotonicity statement found**: for s ≤ 24 the minimiser is not always in these families (s = 16:
4 3 2 1 3 2 1), and I have no rule "changing a letter pair lowers the weight". Verdict: core2·dim² is the candidate;
bounded away from 1 on every family tried, minimum over all prefixes known only to s = 24.

## 3. Defects and flows
**Defect lemma (PROVED, from (LAST)).** A state with n stones has no predecessor under the letter e iff
(R + 1 − e) ∩ X = ∅. For e = 1 these are exactly the states **(λ | λ′)** (p(s/2) of them, s even); by the mirror
they are also exactly the states with no successor under −1 (this is the c = 0 at even s in `out/transport.txt`).
Inside the parity set P_n the defect of the letter 1 is E_n: that is Theorem 1.

**Letter 0 is onto (PROVED).** If n > s every state has at least max(D, 1 − D) ≥ 1 predecessors under a 0 (pigeonhole
above). This is the case S = everything of the flow statement.

**Letter-0 flow dim(N_0(S)) ≥ dim(S) for every S: NOTHING.** No bijection on standard fillings found. What I can say:
in (R, X) coordinates a letter 0 adds r to R and r + 1 to X (after shifting X by 2), i.e. the signless
Σ_p ψ*_p ⊗ ψ*_{p+1}; tensoring with a B_s-representation or restriction–induction gives flows for dim², not dim, and
for dim² the constant is far below 1 (0.34 at s = 11), so the statement is special to dim and to the letter 0.
Letters ±1 between normalised dim_s and dim_{s±1}: best constants 0.60 → 0.32 (letter 1, s = 2..13), 0.56 → 0.23
(letter −1, odd s), 0 for even s (the defect above).

## Recheck
`sh runs2.sh` (about 3 minutes, 0.2 GB; k = 9 staircase not included: `./fx 9 8 7 6 5 4 3 2 1 0`, 1 minute, 0.9 GB).
