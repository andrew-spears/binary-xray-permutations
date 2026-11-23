# HIT: unimodal words with all letters in [−2, 2] — proved for all slacks; and a purely combinatorial statement (RR) that implies the conjecture, tested for n ≤ 14

Sub-task of `NOTES.md` (odd splits). Builds on the parity theorem of `../unimodal/REPORT.md` (card `paritylr`).

**Proved (by hand, §1–§3):**
1. *Lemma R (extreme states).* For a part-word w ≥ 0 with skew diagram θ(w), row lengths ρ and column lengths κ, the state
   (λ|γ) has an odd number of partial placements whenever λ + γ = ρ, and whenever λ′ + γ′ = κ. In both cases the parity
   number ⟨s_θ, s_λ s_γ⟩ is exactly 1.
2. *Theorem E (E-splits).* If for some set S of stones both part-words are ≥ 0 and some (λ|γ) is extreme for S and its
   conjugate is extreme for S^c, then D has an odd split, so D is solvable. The simplest case, **RR**: the positive letters
   of the two part-words, sorted, are λ + γ and λ′ + γ′ for some pair of partitions λ, γ.
3. *Theorem A (one stone).* **Every valid unimodal word with all letters in {−2, …, 2} has a permutation**, at every slack.
   Precisely: if e_i ∈ {0, 1, 2} for i < k and e_i ∈ {0, −1, −2} for i > k, then the number of solutions with stone k on
   the cell (p + q + 1, p + 1) is odd, where p = #{i < k: e_i = 0} + #{i > k: e_i = −2} and
   q = #{i < k: e_i = 1} + #{i > k: e_i = −1}. This contains {0, 1}*{0, −1}* (the previous family).
4. *Converse.* S = {k} is an odd split **only** for such k: the number of solutions with stone k on a given cell is, mod 2,
   a number of two-letter tableaux, which is 0 as soon as another stone has a letter outside the ranges above.

**Tested only (§4):**
- **RR**: every valid word without a tight cut has an RR-split, for all n ≤ 14 (27,225 words at n = 14), and for all
  unimodal words with n ≤ 15 (60,570 at n = 15). If RR is true for all n, the conjecture follows (tight cuts split the word).
- Fixed shapes of S fail: S in the first |S| columns (γ = ∅) fails for 1 of 251 unimodal words at n = 10; both part-words in
  {0, 1} exists only for the old family; a given S survives a shortening step in only 74–84% of the cases.

**Not proved:** full UNIMODAL; RR for all n; any rule that names S. **NOTHING** on an induction on n (§6).

Notation as in `NOTES.md`: d_k = 2k + e_k; a state of m stones is (R, C) = (λ|γ), λ_j = r_j − j, γ_j = c_j − j.

## 1. Part-words and Lemma R
For S = {k_1 < … < k_m} put a_k = #{i ∉ S: i < k} and b_k = #{i ∈ S: i > k}.
- **S-word** u_j = d_{k_j} − 2j = e_{k_j} + 2a_{k_j}. L_S(R, C) is the partial-placement count of the prefix u.
- **S^c-word** v: the letters 2b_k − e_k, k ∉ S, read from right to left. The half-turn r ↦ n + 1 − r sends the placements
  of S^c on (R^c, C^c) to the placements of the prefix v in the state (λ′|γ′) (complement and reverse = conjugate).
- Σu = Σv. An odd state needs u ≥ 0 and v ≥ 0 ("admissible" in `NOTES.md`).
- θ(w): rows of lengths w_1, …, w_m from bottom to top, row j starting in column j. ρ(w) = the positive letters sorted;
  κ(w) = the column lengths sorted.

By the parity theorem, L_S(R, C) ≡ P_u(λ|γ) := ⟨s_θ(u), s_λ s_γ⟩ = Σ_ν c^θ_ν · c^ν_{λγ}, and
L_{S^c}(R^c, C^c) ≡ P_v(λ′|γ′).

**Lemma R.** Let w ≥ 0. If λ + γ = ρ(w), or if λ′ + γ′ = κ(w), then P_w(λ|γ) = 1.

*Proof.* Two standard facts about dominance order ⊴.
- (i) If c^θ_ν ≠ 0 then ρ ⊴ ν ⊴ κ′, and c^θ_ρ = c^θ_{κ′} = 1. (In a semistandard filling of θ the entries ≤ i occupy at
  most min(i, length) cells of each column, so ν ⊴ κ′; equality forces 1, 2, 3, … down every column, which is a
  Littlewood–Richardson filling. Apply ω for the other end. This is the "rows(A) ≼ λ ≼ cols(A)ᵗ" lemma of McNamara,
  *Necessary conditions for Schur-positivity*, J. Algebraic Combin. 2008; cited from memory, not re-read.)
- (ii) If c^ν_{λγ} ≠ 0 then λ ∪ γ ⊴ ν ⊴ λ + γ, and both ends have coefficient 1. (s_λ s_γ has leading monomial
  x^{λ+γ}; apply ω for the other end, since (λ′ + γ′)′ = λ ∪ γ.)

If λ + γ = ρ, a nonzero term needs ρ ⊴ ν ⊴ λ + γ = ρ, so only ν = ρ remains, with value 1 · 1. If λ′ + γ′ = κ, then
λ ∪ γ = κ′ and a nonzero term needs κ′ = λ ∪ γ ⊴ ν ⊴ κ′. ∎

For a 0/1 word this gives only (1^s|−), (−|1^s), ((s)|−), (−|(s)), in agreement with C(s,|λ|) f^λ f^γ.
The earlier criterion PAR of the unimodal report used ρ of one side against κ of the other; splitting ρ between rows and
columns (γ ≠ ∅) is what is new, and it is what makes non-prefix S work.

## 2. Theorem E
**Theorem E.** Let S be a nonempty proper set of stones with u, v ≥ 0, and write ρ_1, κ_1 for u and ρ_2, κ_2 for v.
D has an odd split (hence a permutation) if there are partitions λ, γ with
 [λ + γ = ρ_1 or λ′ + γ′ = κ_1] and [λ′ + γ′ = ρ_2 or λ + γ = κ_2].
Both parity numbers are then exactly 1.

| type | condition |
|---|---|
| RR | ρ_1 = λ + γ and ρ_2 = λ′ + γ′ |
| CC | κ_1 = λ′ + γ′ and κ_2 = λ + γ |
| RC | ρ_1 = κ_2 |
| CR | κ_1 = ρ_2 |

*Proof.* Lemma R for u in the state (λ|γ) and for v in the state (λ′|γ′). The state fits the board: λ and γ have at most
m parts (because ρ_1 has at most m parts, or because the parts of κ_1 = λ′ + γ′ are ≤ m), and their parts are ≤ n − m
(the same argument for v and λ′, γ′). ∎

RR is symmetric under the mirror D ~ −D, which exchanges S with S^c and (λ, γ) with (λ′, γ′).
**H-split** = RR with γ = ∅: ρ_1′ = ρ_2; the stones of S fill the first m columns.
A necessary condition for RR: every letter of v is ≤ 2m and every letter of u is ≤ 2(n − m). So every stone outside S
has |e_k| ≤ 2|S|, and every stone in S has |e_k| ≤ 2|S^c|.

## 3. One stone
**Theorem A.** Let e be a valid word and k a position with e_i ∈ {0, 1, 2} for all i < k and e_i ∈ {0, −1, −2} for all
i > k. Then S = {k} is an RR-split, and the number of solutions with stone k on (p + q + 1, p + 1) is odd; the same
holds for (p + 1, p + q + 1). Here p and q are the numbers of letters 2 and 1 in v, as in the summary.

*Proof.* v has the letters 2 − e_i (i < k) and −e_i (i > k), all in {0, 1, 2}, so ρ_2 = (2^p 1^q) and
Σv = 2p + q = u_1 = d_k − 2. Take λ = (p + q), γ = (p): λ + γ = (2p + q) = ρ_1 and λ′ + γ′ = (1^{p+q}) + (1^p) = ρ_2.
The state ((p + q)|(p)) of one stone is the cell (1 + p + q, 1 + p), where L_S = 1. By Lemma R the number of placements
of the other stones on the remaining rows and columns is odd. Swap λ and γ for the other cell. ∎

**Corollary.** Every valid unimodal word (letters ≥ 0, then letters ≤ 0) with all |e_k| ≤ 2 is solvable: take k = the
position just before the first negative letter. (Conversely the hypothesis of Theorem A forces e_k ∈ {−1, 0, 1}, so the family is exactly
this one.) The slack is unbounded, e.g. (2, 1)^a 0^b (−1, −2)^a for b ≥ 1. It is 221 of the 251 unimodal words
without a tight cut at n = 10, against 64 for {0, 1}*{0, −1}*.

**Proposition (converse and exact parity).** For any k, any valid e and any cell (1 + a, 1 + c) with a + c = d_k − 2, the
number of solutions with stone k on that cell is, mod 2, the number of semistandard fillings of the transposed diagram
θ(v)′ with a ones and c twos. It is 0 unless all letters of v are in {0, 1, 2}.

*Proof.* The count is L_{S^c} in the state ((a)|(c))′ = (1^a|1^c), so its parity is ⟨s_θ(v), e_a e_c⟩ = ⟨s_θ(v)′, h_a h_c⟩,
the number of semistandard fillings of θ(v)′ with content (a, c). The columns of θ(v)′ are the rows of θ(v); a column
longer than 2 has no strictly increasing filling by {1, 2}; a negative letter gives s_θ = 0. ∎

**Two stones.** For S = {k_1 < k_2}, RR holds exactly when all letters of v are ≤ 4 and max(u_1, u_2) ∈ {N_1 + N_2, N_1 + N_3},
N_t = #{letters of v that are ≥ t}. (Checked against the general test in 16,237 cases.) It is one linear condition, not
a family with a clean description.

## 4. Tested
All counts are over valid words **without a tight cut** (words with a tight cut can fail, e.g. 1 0 −1 1 0 −1 has no
E-split, but they split into shorter words).

| n | words | RR-split | H-split | unimodal | unimodal with H-split |
|---|---|---|---|---|---|
| 9 | 97 | 97 | 95 | 90 | 90 |
| 10 | 285 | 285 | 271 | 251 | 250 |
| 11 | 862 | 862 | 793 | 720 | 714 |
| 12 | 2,668 | 2,668 | 2,370 | 2,115 | 2,082 |
| 13 | 8,442 | 8,442 | 7,215 | 6,348 | 6,201 |
| 14 | 27,225 | 27,225 | 22,266 | 19,438 | 18,718 |

- **RR holds for every word tested**: all valid words without a tight cut, n ≤ 14.
- H-splits fail first at n = 9 (1 1 0 −1 0 1 0 −1 −1 and 2 1 0 −1 −1 1 0 −1 −1) and for unimodal words at n = 10
  (3 2 1 0 −1 0 −1 −2 −1 −1).
- The criteria are sound against brute force: all 14,703 pairs (word, S) of size 8 that satisfy RR, CC, RC or CR are
  odd splits (`check_e.py`); Lemma R: 854 words, 4,574 states, 0 even counts (`check_rows.py`); Theorem A and its
  converse: 0 mismatches over all words of size 8 and 9 (`check_one.py`), and the cell itself for n ≤ 9 (`check_cell.py`).
- **The test words 1^a 0 −1 −2 −3 …** (`./esplit w …`):

| word | n | S with RR, out of 2^n − 2 | an RR-split |
|---|---|---|---|
| 1^6 0 −1 −2 −3 | 10 | 50 | stones 1, 6 |
| 1^8 0 −1 −2 −3 −2 | 13 | 84 | stones 1, 8 |
| 1^9 0 −1 −2 −3 −3 | 14 | 84 | stones 2, 9 |
| 1^10 0 −1 −2 −3 −4 | 15 | 144 | stones 3, 10 |
| 1^15 0 −1 −2 −3 −4 −5 | 21 | 350 | stones 1, 6, 15 |

  Example: 1^6 0 −1 −2 −3, S = {1, 6}: u = (1, 9), v = (3, 2, 1, 0, 1, 1, 1, 1), λ = (7, 1), γ = (2):
  λ + γ = (9, 1), λ′ + γ′ = (2, 1^6) + (1, 1) = (3, 2, 1^5).

## 5. Item 2: a rule for S
- **Both LR numbers exactly 1:** yes in every E-split, so for every word without a tight cut with n ≤ 14.
- **How large S must be** (`./esplit m n`): least |S| of an RR-split against ⌈max|e_k| / 2⌉.

| | least = bound | least = bound + 1 |
|---|---|---|
| unimodal, n = 13 | 6,238 | 110 |
| all, n = 11 | 721 | 141 |

  It was never smaller than the bound and never larger than bound + 1. For unimodal words with max |e_k| ≤ 2 it is 1 (Theorem A); with max |e_k| ≤ 4 two
  stones suffice except for 2, 19, 110 words at n = 11, 12, 13 (first: 1 1 3 2 1 0 −1 −2 −3 −1 −1).
- **Fewest RR-splits** (`few.py`): at n = 10 the word 1^4 0 0 (−1)^4 with 38 of 1,022 sets; at n = 9, 1^4 0 (−1)^4 with 26
  of 510. (The word (1 0 −1)^3 of `NOTES.md` has tight cuts.) The most: 1 0 1 0 −1 1 0 −1 0 −1 with 224.
- **No rule found.** I do not have a rule that names S and (λ, γ) from the word. What a proof of RR needs is exactly that:
  a choice of S for which the two multisets of positive letters are λ + γ and λ′ + γ′. For unimodal words with small
  letters the smallest S is a few stones near the turn (Theorem A); for the test words above it is the last 1 together
  with one or two earlier ones.

## 6. Item 3: induction on n — NOTHING
`transfer.py`: for the steps x y → x 0 y and 0 → (1, 0, −1), **some** RR-split of the shorter word extends to the longer
one in every case (24, 71, 214 insertions and 11, 32, 94 PEAK steps for n = 6, 7, 8), but a given S extends in only
468 of 560, 1,876 of 2,394, 7,386 of 10,038 cases, with the new stone on either side. So an induction would need to
carry a describable subclass of splits, and I have none. RUN steps were not tested.

## 7. Ruled out
- S in the first |S| columns (H-splits): table in §4.
- S with both part-words in {0, 1} (the candidate in the task): such S exist for exactly the words of {0, 1}*{0, −1}*
  (64 of 285 at n = 10), so it gives nothing new (`zo.py`).
- θ(u) and θ(v)′ equal as shapes ("T-split"): fails for 1 of 5 unimodal words at n = 6 and 38 of 90 at n = 9 (`tsplit.py`).
- H-splits with both part-words weakly increasing (then the permutation is two increasing runs): 13 of 90 unimodal
  words at n = 9 (`mono.py`).

## 8. Not checked
- RR for n ≥ 15, except unimodal words at n = 15: all 60,570 have an RR-split (57,603 an H-split; `./esplit 15 uni`, 7 min).
- Odd j-splits with j ≥ 3 and the 2-quotient idea of `../twoadic/NOTES.md`.
- Non-extreme odd states (ν strictly between ρ and κ′): Theorem E uses only the two ends.
- RUN steps in §6.

## 9. Recheck (all in this directory; total under 6 minutes)
```
g++ -O2 -o esplit esplit.cpp
./esplit 13                 # 27 s: 8442 words, RR-split 8442, H-split 7215     (n = 14: 4 min)
./esplit 14 uni             # 46 s: unimodal 19438, RR-split 19438, H-split 18718
./esplit m 11 v             # least |S|
./esplit w 1 1 1 1 1 1 0 -1 -2 -3
python3 check_rows.py 6 7   # Lemma R by brute force, 20 s
g++ -O2 -o dump dump.cpp && ./dump 8 > /tmp/os_8.txt && ./dump 9 > /tmp/os_9.txt
python3 check_e.py /tmp/os_8.txt      # 2 min
python3 check_one.py /tmp/os_9.txt    # Theorem A and converse
python3 check_cell.py 9               # the cell of Theorem A
python3 zo.py 10; python3 transfer.py 7; python3 few.py 9; python3 tsplit.py 9 uni; python3 mono.py 9 uni
g++ -O2 -o hsplit hsplit.cpp && ./hsplit 10 uni v
```
`ext.py` is the slow reference version of the tests in `esplit.cpp` (all four types).

## 10. Suggested cards (I did not touch `map/build.py` or `docs/state.md`)
- green, child of `paritylr`: "unimodal words with all letters in [−2, 2] are solvable" (Theorem A).
- open, child of the odd-split card: "RR: every valid word without a tight cut has S, λ, γ with ρ(u) = λ + γ and
  ρ(v) = λ′ + γ′" (tested n ≤ 14), with the red child "γ = ∅ suffices" (fails at n = 9; unimodal n = 10).
