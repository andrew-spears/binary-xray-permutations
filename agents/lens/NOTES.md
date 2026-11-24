# lens: three quick probes (parent session, working notes)

1. **Two tournaments instead of two permutations: NOTHING.** Rows a and columns b = a + d of a solution are two vertices
   of the permutohedron P_n. Relaxation: a, b score vectors of tournaments (lattice points of P_n). A solution is a
   point of P_n ∩ (P_n − d) where |a|² + |b|² is maximal (= 2 Σ i²). Hill climbing by unit exchanges
   a → a + e_i − e_j gets stuck at non-solutions: 3 of 9 sets at n = 5, 13 of 22 at n = 6 (`lens.py n`). With moves of
   up to r exchanges (`lens2.py n r`): r = 2 stuck at n = 6 (5 of 22), r = 3 stuck at n = 7 (3 of 59). The radius grows.
   Stuck points typically have one side a permutation (e.g. d = −6 −3 −2 1 2 3 5, a = 6 4 5 2 3 0 1).
   Same identity mod 2: Σ_solutions ∏ u_k^{row k} ≡ Σ over pairs of tournaments (T1, T2) with score(T2) − score(T1) = d
   of ∏ u_k^{score_T1(k)} (pairs with a non-transitive side cancel within each (a, b)); this is the F_4 formula of
   `../thirds/REPORT.md` before specialising u.

2. **What is left** (`left.py n`; words without tight cut, middle not covered by Theorems 0′, H). n = 13: 11,244 of 19,715.
   By (max, min) letter of the middle: (3,−3) 2719, (2,−3) 2430, (3,−2) 2430, (2,−2) 1498, (3,−4) 653, (4,−3) 653,
   (4,−4) 376, (2,−4) 164, (4,−2) 164. A theorem "all letters ≤ 2 ⟹ solvable" (and its mirror) would take 6,686 = 59%.
   All but 54 have a single block of high letters.

3. **Zeros heal; what stays missing is next to a hook** (`restore.py s0 "letters" ...`, `restore_show.py`). Start from
   G(s0), apply a block W of letters 1, 2, then zeros; count the states of G(s) not reached.
   - s0 = 1: `2 2 2 1 0 0 0 0` → 4 12 40 43 22 6 2 0; `2 2 2 2 1 0^6` → … 96 44 18 6 2 0 0;
     `2 2 2 1 1 1 0 0 0 0` → … 34 18 6 2 0; `2 1 2 1 2 1 0 0 0 0` → … 46 18 6 2 0. The tail 18, 6, 2, 0 does not depend on W.
   - The 2 states: (s|−), (−|s). The 6: also (−|1^s), (1^s|−), (s−1,1|−), (−|s−1,1). The 22 at slack 8 after `2 2 2 1 0`:
     a row ≥ s − 2 in either diagram, plus 1111|22, 211|22, 22|1111, 22|211, 2111111|−, −|2111111.
   - Before the first 0 the missing set is NOT near the hooks: s0 = 8, `2` → 88 missing at slack 10 (22|33, 33|4, 2|53 …:
     the tight states of `../onehigh` Lemma A), `2 1` → 40, `2 1 0` → 2, `2 1 0 0` → 0.
   - Zeros alone cannot heal everything: s0 = 2, `2 2 2 1 0^5` stays at 2 (21|321, 321|21 at slack 9), `2^4 1 0^6` at 8.
     A letter −1 heals faster: `2 2 2 1 0 −1 0` → 22 4 0.
   - Hypothesis (DAMAGE): for a block W of letters ≥ 1 and j ≥ 1, G(s) ∖ step_{W 0^j}(G(s0)) ⊆ N_r(s) = {a row or column
     of length ≥ s − r in λ or μ} ∪ (few), r = max(0, 3 − j) for letters ≤ 2. Not tested beyond the lines above.

4. **Combs.** After a staircase h, h−1, …, 1 the classes reached completely are the extreme ones (2-core a staircase):
   `prof.py 2 "4 3 2 1 0 0"`: at slack 12 the classes (c, K) = (−2, ±2) are reached 4/4, the others about half.
   Board meaning: stones on consecutive diagonals fill consecutive rows and every other column.

5. **Levels: a big letter pushes the fully reached classes outward, a zero pulls them back** (`levels.py`, `grid.py`).
   level(u) = max(c, 1 − c) (central = level 1). In board terms (a, b) count the stones on even rows minus odd rows, and the
   same for columns; an odd letter puts a stone on a cell with row ≡ column mod 2, an even letter on the other colour.
   - Counts (Lemma G of `../l2sets` with its shifts, table in `../onehigh/REPORT.md`): under a letter 2 a state of level ℓ ≥ 2
     has ≥ ℓ − 1 predecessors of level ℓ − 1; under a letter 0 it has ≥ ℓ of level ℓ − 1, and a level-1 state has ≥ 1 of
     level 1. Predecessors one level UP are not guaranteed: they are missing exactly for the tight states of Lemma A.
     Odd letters keep the level. Checked on all states of slack ≤ 12 (`predcount.py 12`): under a letter 2f a state of
     level ℓ ≥ f + 1 has ≥ ℓ − f predecessors of level ℓ − 1, for f = −2, …, 3 (so −2 gives ≥ ℓ + 1, 4 gives ≥ ℓ − 2);
     under −1 and −3 every state has ≥ 2 and ≥ 4 predecessors of its own level, under 1, 3, 5 possibly none.
   - Data, from a true old prefix (levels 1, 2 complete): `levels.py -1 "1 1 1 1 1 0 1 2 2 2 1 0 0 0"`:
     after 2: L1 118/133, L2 48/48, L3 4/4; after 2 2: L1 292/332, L2 126/133, L3 16/16; after 2 2 2: L1 700/784,
     L2 320/332, L3 48/48, L4 1/1; then 1 0 0 0: L1 1138, 1158, 1170, 1174 of 1176, L2 506, 508, 510, 512 of 512.
     After a 4 (from levels 1, 2 complete at slack 5): L3 8/8, L2 56/80, L1 116/212.
   - The states missing at level 1 after `x 2` are the same 15 (slack 8) for x = 1 1 1 1 1 0 1 and x = 1 1 1 1 0 0 1 1, and
     the same 40 after `x 2 2`: with the start family "levels 1 and 2" the sets after a 2 look local again
     (`levels.py -1 "..." show`). REPORT3 §1 found them non-local when only Central is used as the start.
   - `grid.py "1 1 1 0 1 0 1 4 3 2 1 0 0 0" 7`: per cell (a, b), after 4 3 2 the outer cells are complete and the inner
     ones 60–85 % reached; the zeros fill the cells from the outside in.
   - Reading: y of REPORT3 is an upper bound for how many levels the bottom of the complete window has been pushed up.
     Candidate invariant for young prefixes: "levels ≥ b(x) complete, lower levels complete minus an explicit set",
     b going up by one at a 2 and down by one at a 0.

6. **No residue tower: NOTHING** (`tower.py`). The damaged part of a cell is not a union of finer cells (stones per residue
   class of rows and of columns mod 4 or 8): after `1 1 1 0 1 0 1 4 3 2` (slack 14, 1864 of 2665 reached) 2292 states lie in
   mod-4 cells that are partly reached; mod 8 the cells are too small to say anything (1690 cells).

7. **Theorem D of `../damage/REPORT.md` against exact reachable sets, every level, every letter** (`../damage/dall.py 9 9 -3 4`).
   A(x) = states not violating Theorem D for x; F(x) ⊆ A(x). Summed over all legal prefixes from the empty word with
   length ≤ 9, slack ≤ 9, letters −3..4: after a letter ≤ 0 (8,629 prefixes) 1,555 of 507,103 states of A are not reached
   (last letter ≤ −2: none; −1: 17 of 94,726; 0: 1,538 of 403,051); after a positive letter 512,133 of 2,579,257.
   So after a letter ≤ 0 Theorem D is close to exact in every class, not only in levels 1–2; after a positive letter the
   odd-even classes matter. Every word without a tight cut has a letter ≤ 0 followed by a letter ≥ 0 (a cut that is clean on
   both sides, by the mirror), unless it is (positive letters) 0 (negative letters).
   The 8 states of G(11) missing after 1^7 2 0 0 2 0 0 0 (Proposition C there) have imbalances (2, −1), difference 3, so
   they are outside J*(11, 0 0) of REPORT3: no conflict with OLD.

8. **Theorem D explains most of the two-line damage of REPORT4 §1c, not all** (`../damage/dword.py`).
   1^5 3 2 1 0 (slack 11): 40 of 752 unreached, 34 violate D, rest 1^8|3, 1^6|5, 1^4|7 and swaps; next zero: 12 unreached,
   8 violate D, rest −|65, −|83 and swaps. 1^5 4 3 2 1 0 0 0 (slack 15): unreached 468, 194, 64; not violating D 46, 40, 12
   (the 12: −|10.5, −|87, 10.1|4, 10|41, 61|8, 6|81 and swaps = the 12 "outside N_y" of REPORT4).
   1^8 3 3 3 2 1 0 0 (slack 20): not violating D 200, 56. The residue has two long lines with a parity pattern
   (65, 83, 87, 10.5: both rows odd/even mixed); candidate: a mod-2 refinement of Theorem D (count stones by the parity
   of their bead, as in the card "Counting rows, columns and sums modulo m"). Not tried.

9. **Statement S of `../damage/REPORT.md` is false: NOTHING for 'Theorem D is exact after a letter ≤ 0'** (`../damage/sword.py s0 "word"`;
   found by the automatic review of PR #19). Letters ≤ 2, start Lev₂(s₀). After 2 2 2 2 1 0 (ŷ = 4): missing 56, violators 52;
   the other four are (−|R 2 2), (R|2 2) and swaps with R = s − ŷ (s₀ = 5, 6, 7, 9), back after one more 0, not after a −1 instead of the 0.
   After 2^5 1 0: (R 2 1|2 1), R = s − 6. Staircase pairs (Prop. C of damage and neighbours: 321|4321; 21|54321, 4321|521,
   321|6321, 32111|4321, 321|432111 and swaps at slack 18 from s₀ = 7) stay missing through four zeros and are back after a −1.
   Shape of the first kind = one row of the largest length Theorem D allows + a small state that is exceptional at small slack
   (the 2 × 2 square; 21|21). Same shape as the residue for letters ≥ 3 in item 8. Reading: take away the stone that made the long row
   (rows above a new bead lose one box per later stone, so a row of length s − r was made r' steps ago with r' fixed by r); what is left is a
   reachability question at slack about ŷ for a shorter word, and there the small-slack exceptions (T, squares) bite. Not checked further.
