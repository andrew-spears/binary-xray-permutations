# hybrid working notes
Task (parent 02:53): HYBRID = BRIDGE with parity in the middle. w = x m y (m from first letter >= 2 to last letter <= -2, slacks s1, s2).
(HYBRID) exist u in G(s1), v in conj G(s2) with an ODD number of m-walks u -> v.  (HYBRID-RR) same with (lam, gam) extreme (LR = 1), or a few stones of m on chosen cells + rest extreme.
Items: 1. test on all words n <= 12 not covered by Theorem 0' (modify l2sets/bridge.py, count mod 2); which (R, C) work, extreme enough?, rule naming (R, C) from m alone; given (R, C) when do u, v exist.
2. prove new infinite family: x letters <= 1, y letters >= -1, m pyramid-like in {0,1,2}*{0,-1,-2}* (one stone on explicit cell, uni2, board with holes); then m of Theorem B type.
3. if HYBRID fails: smallest word + replacement.   Report agents/hybrid/REPORT.md, HIT/NOTHING, recheck; branch devin/1795460030-hybrid off two-marks; push, no PR; no map/build.py, docs/state.md edits.
Read: cards upone, nocross, bridge, rrsplit, uni2, uni4, paritylr; agents/oddsplit/REPORT.md (Lemma R, Theorem E, Theorem A), REPORT2.md (I-splits, Theorems B, C).

## Setup facts (derived, to be used in the report)
- Coordinates relative to N = |x|: rows used by u: {k + 1 : k in M_u}; after the k stones of m rows used by v: {kap + k + 1 : kap in M_v}. Unused columns of u: {-y : y in B_u}; of v: {k - y : y in B_v}  (B = M(nu), nu = mu').
  The number of m-walks u -> v = number of placements of the stones of m (diagonals 2j + m_j) on R x C, R = R_v minus R_u, C = C_v minus C_u; independent of N.
- Lemma R, first case, restated: lam + gam = rho  <=>  sorted rows and sorted columns paired in order have sums 2i + (m sorted ascending)_i.
  I.e. (R, C) = rows and columns of an INCREASING placement of the sorted word. Invariant under translations of rows / columns and half-turn. Then count is odd.
  Second case lam u gam = kappa' depends on the translation (finite board).
- u = (s|-): free rows rel {0, 1, 2, ..} minus {s}, free columns {1, 2, ..}: same as a first stone with letter s on cell (s + 1, 1). v = (1^s|-): one row hole at depth s: same as a last stone with letter -s in the last column.
  So w is solvable if the word (s1) m (-s2) has a solution with first stone in column 1 (or row 1) and last stone in the last column (or row): 16 corner variants "H0" (all four states (s|-), (-|s), (1^s|-), (-|1^s) are in G(s) and in conj G(s)).
  Then with one more stone of m (the turn) on a cell: 3 fixed stones, Theorem E / Lemma R for the rest: arithmetic like Theorem A. PLAN for item 2.

## Results so far (session 2)
- hybrid.py 12 (12 s): plain HYBRID FAILS for almost all words: n = 5..12: 1, 3, 12, 51, 197, 733, 2686 of 2687, 9694 of 9703 fail. Smallest 2 1 0 -1 -2 (6 solutions; s1 = s2 = 0).
  Reason (paritylr): odd count needs sorted letters >= 0 in the frame (min R, min C) = (1, 1): needs min m >= -(depth of deepest row hole + column hole of u) >= -s1, and max m <= s2.
- hybrid1.py (one stone of m fixed on a cell, others odd): n <= 9: fails 1, 8, 42 words at n = 7, 8, 9 (first 3 2 1 0 -1 -2 -3). For m in {0,1,2}*{0,-1,-2}* never fails n <= 11 (5 s);
  with the others row-extreme (chain) it fails 1, 7, 34 at n = 9, 10, 11 (first 1 2 2 1 0 -1 -2 -2 -1).
- KEY IDEA (proved, write up): TRANSFER. Normal word w0 = 1^s1 m (-1)^s2. If w0 has an odd split (S; R, C) with S inside m, then x m y is solvable for all x (letters <= 1, slack s1), y (letters >= -1).
  Proof: N_{S^c}(R^c, C^c) = sum_{u, v} L_{1^s1}(u) W(u, v) L_{(-1)^s2}(v) odd => some u, v with L(u), L(v) odd and W >= 1. Lemma O: O(s) = {u: L_{1^s}(u) odd} inside G(s):
  class = s mod 2 (letter 1 sends class c to 1 - c); SC has no 1-predecessor; A(4m^2+1) states have their only 1-predecessor in E0; E0: L = C(s,|lam|) f^lam f^nu mod 2 (paritylr, theta(1^s) = s single boxes, s_theta = p_1^s)
  and f of a 2x2-blow-up of alpha (|alpha| = a >= 1) has v_2 = a - v_2(a!) + 2 v_2(f^alpha) >= 1 (hooks of a block: 2h+1, 2h, 2h, 2h-1).
  With Theorem A (S = {turn stone}, inside m): THEOREM H: every valid x a b y, x <= 1, a in {0,1,2}*, b in {0,-1,-2}*, y >= -1 is solvable.
- normal.py 11 (1 s): extreme split of w0 inside m exists for all but 0,0,0,0,1,5,22 words at n = 5..11 (first 1 1 1 2 1 0 -1 -2 -3: s1 = 3 >= T = 1, Theorem B's k_1 falls into 1^s1).
TODO: normal.py 12/13; exact parity for failures (hybrid1 restricted to O x conj O); check Lemma O numerically (O(s) in G(s), s <= 20); Theorem B transfer condition (s1 < T); count coverage; REPORT.

## Session 2, later
- lemmao.py 24 (0.2 s): O(s) inside G(s) for s <= 24 (|O| = 1,2,4,8,8,16,32,64,16,...); odd path counts of 1^s are exactly O(s) for s <= 9. (Exact count is NOT C f f, only the parity.)
- normal.py 12 (30 s), 13 (3 min, out/normal13.txt): extreme split of w0 inside m: n = 9..12 fails 1, 5, 22, 96 words (of 197, 733, 2687, 9703); least |S| 1 (= Theorem H: 140, 454, 1434, 4424), 2, few 3, 4.
- fails.py 11: the 8 failing (s1, m) at n <= 11: (1; 3 2 1 0 -1 -2), (3; 2 1 0 -1 -2 -3) [21 words], (4; 2 1 0 -1 -2 -3), (1; 3 2 1 0 -1 -1 -2), (2; 3 2 1 0 -1 -2 -3), (3; 2 1 1 0 -1 -2 -3),
  (4; 2 1 0 -1 -1 -2 -3), (3; 3 2 1 0 -1 -2 -3 -3). One-stone direct hybrid (u in G, v in conj G, odd): P > 0 for all but the last; one-stone transfer Q = 0 for all (expected, depth 3).
- Theorem B through transfer: k_1 inside m iff s1 < T = sum over letters <= -3 of (|e| - 2); k_2 in {t+1, t+2} always inside m. => THEOREM H2: m in {0,1,2}*{0..-4}*, s1 < T (mirror: {0..4}*{0,-1,-2}*, s2 < T').
- GENERAL NORMAL FORMS (oddz.py 6 7): any prefix z (letters >= 0) with slack s1 and Odd(z) inside G(s1) can replace 1^s1 (same proof). 114 of 728 prefixes with a letter >= 2 qualify, e.g. (3), (5), (7), 3 3, 1 5, 2 1 2 1.
TODO: normal2.py = transfer with normal forms z, z' for the failing (s1, m); then REPORT. Possibly: two fixed stones direct for (3; 3 2 1 0 -1 -2 -3 -3).
- normal.py 13: 34297 of 34677 (least |S| 1: 13403, 2: 20282, 3: 587, 4: 21, 5: 2, 7: 2), none 380. n <= 12 total none: 124 words = 21 pairs (s1, m).
- normal2.py 11 5 (5 s): with normal z, z' (length <= 5): 24 of the 28 words at n <= 11 get a split (z = 3 for (3; 2 1 0 -1 -2 -3)); normal2.py 12 5: 85 of 124, 39 words (13 pairs) left. out/normal2_12.txt
- Lemma N (why plain HYBRID fails): odd number of m-walks u -> v forces -(l(lam_u) + l(mu_u)) <= m_i <= lam_1(v) + mu_1(v), so min m >= -s1, max m <= s2.
- Theorem H cell, relative to the start of m (row/col N + .): stone kap = last letter of m before its first negative letter; p = #0 before kap + #(-2) after, q = s1 + s2 + #1 before + #(-1) after; cell (p + q + 1 - s1, p + 1 - s1).
NEXT: thmh.py check, hybrid1.py 11 totals, fails.py 12 (out/fails12.txt), REPORT.md, runs.sh, commit explicit files, push devin/1795460030-hybrid, final message (no PR).
- thmh.py 11 (5 s): 2084 words, 535 pairs (s1, m): the number of odd (u, v) in O x conj O at the named cell is odd for all. Theorem H confirmed through its proof.
- hybrid1.py 11 (all m, direct one stone, u in G, v in conj G): fails 1, 8, 42, 199, 895 words at n = 7..11 (depth 3 middles); row-extreme version 1, 8, 43, 206, 931.
- fails.py 12 (out/fails12.txt): of the 21 pairs without extreme split inside m (z = 1^s), direct one-stone P = 0 for 4 pairs (9 words): (3; 3 2 1 0 -1 -2 -3 -3), (4; 3 2 1 0 -1 -2 -3 -4), (1; 4 3 2 1 0 -1 -2 -3 -3), (2; 3 3 2 1 0 -1 -2 -3 -4).
- hybrid.py 12 v: the ONLY (s1, m) with an odd full pair at n <= 12 are (3; 2 1 0 -1 -2) and (3; 2 1 0 0 -1 -2), s2 = 3 (10 words, 16 odd pairs each). "Lemma N" is NOT sharp/proved: do not state it; state only: w = m = 2 1 0 -1 -2 has 6 solutions, G(0) one state.
- Proof checks done: F(1^s) in Central(s) (L1 Lemma 1: letter 1 sends class c to 1 - c); E0 = both diagrams doubled (M, B unions of pairs) => f even; A: only 1-predecessor in E0. Lemma O OK.
- thmh2.py 13 (1 s): Theorem H2: 6996 (word, orientation) with B-type middle and s1 < T: Theorem B's two stones are an RR-split inside m, 0 failures.
- normal2.py 11 7 running -> out/normal2_11_7.txt (LZ = 7 gives nothing new for the first rows).
- Totals n <= 12: 13387 uncovered words; transfer with z = 1^s: 13263; with normal z, z' (len <= 5): 13348; left 39 words (13 pairs).
NEXT: write REPORT.md + runs.sh, git add agents/hybrid (no __pycache__), commit, push, final message with branch name.
