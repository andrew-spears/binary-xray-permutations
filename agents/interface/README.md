# interface: witnesses as walks on pairs of Young diagrams (Devin round 3, 2026-11-23)

All scripts in this folder; every number below was produced by the named script.

## 1. Model (exact; `check_walks.py 8`: walk count = W(D) for all valid D, n <= 8)
- Flip rows, r' = n+1-r.  Stone k (k-th smallest diagonal) gets a cell (r', c) with
  r' + c = b_k = d_k + n + 1 = 2k + e_k, where e_k = s_k - (k-1) ("excess score").
- **Conjecture <=> every strictly increasing b majorized by (2,4,...,2n) is a sum of two
  permutation vectors, b = rho + gamma** (rho(k) = r', gamma(k) = c of stone k).
  Same thing: [2n] splits into pairs with the prescribed odd sums 2b_k - 1 (odd element 2r'-1, even 2c).
  Same thing: m_b appears in m_delta^2 (monomial symmetric functions, delta = (n,...,1)); the signed
  count is the coefficient of z^b in the squared Vandermonde.  Landau = dominance ("squeezing").
- Landau slack sigma_k = sum_{i<=k} e_i.  Valid words e_1..e_n: e_1 >= 0, e_{k+1} >= e_k - 1 (d increasing),
  sigma_k >= 0 (>= 1 inside: no tight cut), sigma_n = 0.  (`check_words.py 10`: this rule generates
  exactly the no-tight-cut valid D, n <= 10.)  P_n is the unique word with all inner slacks 1: e = (1,0,...,0,-1).
  Max slack of any D of size n is <= n^2/8.
- After k stones, used rows R' and used columns C are k-subsets of [n] with
  excess(R') + excess(C) = sigma_k, excess(X) = sum(X) - k(k+1)/2 >= 0.  A k-subset with excess j is a
  partition of j (parts x_(i) - i).  **Interface state = pair of partitions (lambda, mu),
  |lambda| + |mu| = sigma_k.**  A witness = a walk (0,0) -> ... -> (0,0); step k+1 adds row
  k+1+u and column k+1+v with u + v = e_{k+1}.  Translation invariant in k, independent of n.
  Adding a bead at offset u: remove 1 from each of the m largest parts, insert a part u+m.
- 3-cycles: t(D) = sum_k sigma_k - (1/2) sum_k e_k^2.

## 2. HIT: bounded-slack automaton (`slack_dfa.cpp`, `slack_dfa.py`, `slack_dfa2.cpp B 1`)
If all sigma_k <= B then every hole/extra row or column is within B of k (a hole at position <= k-B
forces excess > B), so the walk lives in a finite automaton that does not depend on n.
Determinizing it over all valid words decides the conjecture for ALL n on {D : max slack <= B}.
**Result: every valid D of any size with all Landau slacks <= 16 has a witness.**
(B = 16: 22358 DFA states, largest reachable set 5822 = all pairs of partitions of 16; 11 s, 0.94 GB.
B = 17 runs out of the 7 GB of this VM.)  Recheck: `g++ -O2 -o slack_dfa slack_dfa.cpp && ./slack_dfa 16`.
Three implementations agree on ALL ACCEPTED (python B <= 8, two C++ versions B <= 12).
Covers every D with n <= 11 (n^2/8 <= 16) and, for larger n, everything within slack 16 of the start.

## 3. NOTHING: no online rule (`online_game.py`, `online_fixed_n.py`, `online_cex.py`)
Game: diagonals are revealed in increasing order, the stone must be placed at once.
Placer wins for n <= 7 and LOSES for n = 8, 9, 10, 11 (fixed n known to Placer; exhaustive game search).
On the automaton: Placer wins for B <= 2, loses for B >= 3.  No single pair of D's does it for n <= 8
(`online_cex.py 8`: any two valid D with a common prefix share a prefix placement), the adversary needs
a tree.  So any proof in diagonal order needs lookahead.

## 4. NOTHING: short summaries of the prefix do not carry an invariant (`invariant.py`, `invariant_other.py`)
Greatest family I(summary) with I(s.e) inside step_e(I(s)).  Summary (sigma, last L letters) suffices
inside slack <= B only for B <= 2 (L = 0, 1), B <= 4 (L = 2), B <= 8 (L = 3), B <= 13 (L = 4)
(`invariant.cpp`): thresholds fit L(L+1)/2 + L - 1, the window must hold a whole rise of the slack.
(sigma, e_last, capped length / max slack / sum of slacks / max letter / steps since last rise): all fail from B = 4.
What the DFA shows (`structure.py`, `inspect_dfa.py`): the reachable set becomes ALL pairs of partitions
of sigma after a few flat letters, and the DFA state is the suffix since the last "everything reachable" point.

## 5. LEAD: repeated diagonals, at most twice (`nonstrict.py`, `twice.cpp`, `slack_dfa2.cpp`)
b nondecreasing, majorized by (2,4,...,2n) (same Landau sums), every value used at most M times.
- **M = 2: always a sum of two permutations.**  Exhaustive n <= 15 (174,292,169 multisets at n = 15, 0 failures, 7 min;
  `./twice n 2`), and for ALL n when max slack <= 12 (`./slack_dfa2 12 2`, 207,436 DFA states).
- M = 3 fails at n = 6: b = (5,5,5,9,9,9), i.e. diagonals {-2,-2,-2,2,2,2}.  Failures by max multiplicity
  for n = 6..10: 1, 6, 32, 145, 634, none with max multiplicity <= 2.
- For arbitrary multiplicities the LP (fractional placement) is exact for n <= 11 and first fails at n = 12 on
  (5,6,10^5,14,20^3,21) and its mirror (`lp_fails.py 12`) = the known saturation gap in docs/state.md §"Saturation".
  This answers that entry's side question "gaps with multiplicities <= 2?": none for n <= 15.
- In words: e_{k+1} >= e_k - 2 and no three letters in a row dropping by exactly 2.

## 6. NOTHING: pair sums with mixed parity (`pairsum.cpp`)
"[2m] splits into pairs with prescribed distinct sums c_1<...<c_m whenever the j smallest sum to >= j(2j+1)"
is the conjecture when all c_i are odd (counts of sum-sets 1,2,4,9,22,59,167 = valid D, 0 failures m <= 8).
With even sums allowed it fails at m = 4: c = (4,8,10,14); 6/198 fail at m = 5, 1026/50944 at m = 8.
