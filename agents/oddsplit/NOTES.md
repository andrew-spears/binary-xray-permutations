# oddsplit: HIT (tested) — every valid D with n ≤ 10 has an odd split

Builds on the parity theorem of `../unimodal/REPORT.md` (counts of partial placements are LR numbers mod 2).

**Definition.** D = {d_1 < … < d_n} (sums row + column). For a set S of stones, L_S(R, C) = number of bijections
R → C with sums {d_k : k ∈ S}. For every S: N(D) = Σ_{R,C} L_S(R, C) · L_{S^c}(R^c, C^c).
D has an **odd split** if for some S and some (R, C) both factors are odd. Then D is solvable.
The unimodal report tested only S = a prefix (its criterion PAR), which needs all letters of the prefix ≥ 0.
A general S needs only: the j-th smallest sum of S is ≥ 2j, and the j-th largest sum of S^c is ≤ 2n + 2 − 2j
("admissible"), which leaves many S for every word.

**Tested (`oddsplit.cpp`).** Every valid D has an odd split for n ≤ 10 (1, 2, 4, 9, 22, 59, 167, 490, 1486 sets).
With S a prefix only: 21/22, 54/59, 146/167, 410/490, 1186/1486.
For n ≤ 9 the fixed rules S = {e_k > 0} and S = {e_k ≥ 0} always work (`rules.py`), and 55–100% of the admissible S
are odd (mean 91%). These fixed rules do not work for ever: for 1^9 0 −1 −2 −3 −3 (n = 14, the PAR failure of the
unimodal report) both give no odd state, but 29 of 30 random admissible S are odd splits (`single.cpp`).

**In symmetric functions.** L_S(R, C) ≡ c(α; δ_m, λ, γ) mod 2, the coefficient of s_α in s_δ s_λ s_γ, where the
partitions are given by their beta-sets: α ↔ {d − 2 : d ∈ D_S}, δ_m ↔ {0, 2, …, 2m − 2}, λ ↔ R − 1, γ ↔ C − 1.
So the odd-split statement is: for some S there are λ, γ in the m × (n − m) box with c(α_S; δ_m, λ, γ) and
c(α′_S; δ_{n−m}, λ^c′, γ^c′) both odd.

**Ruled out.**
- "LR number positive ⇒ state reachable" is false (`lrpos.py 5 5`: x = 0 0 0 1 1, state (1|1): c = 2, L = 0;
  558 of 2,979 positive states are unreachable). Only the parity carries over.
- Odd splits in which the stones of S fill the first |S| rows: missing for 1 of 22 (n = 6), 5 of 59, 19 of 167,
  68 of 490 (`rowsplit.cpp`), e.g. 1 0 −1 1 0 −1.

Recheck: `g++ -O2 -o oddsplit oddsplit.cpp && ./oddsplit 9 v` (2 s; n = 10: 50 s);
`g++ -O2 -o dump dump.cpp && ./dump 9 > /tmp/os_9.txt && python3 rules.py /tmp/os_9.txt`;
`g++ -O2 -o single single.cpp && ./single 30 1 1 1 1 1 1 1 1 1 0 -1 -2 -3 -3` (10 s, 0.1 GB).
