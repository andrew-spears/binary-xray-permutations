# interface: witnesses as walks on pairs of Young diagrams (Devin round 3, 2026-11-23)

## Model (checked against brute force, `check_walks.py`, all valid D, n <= 8: walk count = W(D))
- Flip rows, r' = n+1-r.  Stone k (k-th smallest diagonal) gets a cell (r', c) with
  r' + c = b_k = d_k + n + 1 = 2k + e_k, where e_k = s_k - (k-1) ("excess score").
- So: **conjecture <=> every strictly increasing b majorized by (2,4,...,2n) is a sum of two
  permutation vectors, b = rho + gamma** (rho(k) = r', gamma(k) = c of stone k).
- Landau slack sigma_k = sum_{i<=k} e_i.  Valid words e_1..e_n: e_{k+1} >= e_k - 1 (d increasing),
  sigma_k >= 0 (>= 1 inside: no tight cut), sigma_n = 0.  Second difference of sigma >= -1.
  P_n is the unique word with all inner slacks 1: e = (1,0,...,0,-1).
- After k stones, used rows R' and used columns C are k-subsets of [n] with
  excess(R') + excess(C) = sigma_k, excess(X) = sum(X) - k(k+1)/2.  A k-subset with excess j is a
  partition of j (parts x_(i) - i).  **Interface state = pair of partitions (lambda, mu),
  |lambda| + |mu| = sigma_k.**  A witness = a walk (0,0) -> ... -> (0,0); step k+1 adds row
  k+1+u and column k+1+v with u + v = e_{k+1}.  Translation invariant in k, independent of n.
- 3-cycles: t(D) = sum_k sigma_k - (1/2) sum_k e_k^2.

## Bounded-slack automaton (`slack_dfa.py`, `slack_dfa.cpp`)
With all sigma_k <= B the walk lives in a finite automaton; determinizing it over all valid words
decides the conjecture for ALL n at once on {D : max slack <= B}.
Result: ALL ACCEPTED for B = 1..15 (B=15: 14218 DFA states, largest reachable set 3956 =
all pairs of partitions of 15; 5 s, 410 MB).  DFA sizes B=1..: 3,7,15,32,60,113,?,389,?,1183,?,3368,?,8974,14218.
Observation: the DFA is tiny and the reachable sets are huge; after enough history the reachable
set is ALL pairs of partitions of size sigma (B=4 table in `inspect_dfa.py 4`).
