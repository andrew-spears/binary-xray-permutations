# Three chains (task: which restricted classes of solutions always contain one)

**HIT (computation, not a proof).**

**Claim (3C).** Every valid D has a solution whose stones split into three chains, a chain being a sequence of
stones each higher up and further right than the one before. Equivalently: a solution σ (σ(row) = column, rows
numbered from the top) with no four stones pairwise incomparable, i.e. avoiding the pattern 1234.

Convention in the programs here: rows and columns 0-based, a stone at (i, c) is on the line i + c (the board
flipped top to bottom), so chains are increasing sequences and the avoided pattern is 4321.

**Why it matters.** It is the first restriction on solutions that survives every test, and it is a strong one: a
solution of this kind is given by two words a, b in three letters with the same content (row i belongs to chain
a_i, column c to chain b_c; the t-th row of a chain is matched with its t-th column), and
D + n + 1 = { (place of the t-th letter j in a) + (place of the t-th letter j in b) }. Two chains are not enough,
and for interval orders no bounded number is.

**Evidence.**
- Complete search, every valid arrangement: n ≤ 15 (531,469 arrangements at n = 15), no failure (`width.cpp`).
- Random arrangements (scores of random tournaments, three biases), complete search with a cap of 3,000,000 nodes:
  n = 16, 18, 20, 2,666 arrangements, no failure, 2 searches at n = 20 cut off (`wrand.cpp`).
- Words k, k−1, …, 1, 0^j, −1, …, −k for k ≤ 8 and j ∈ {2, 3, 5} (n ≤ 21): three chains, never two (`width1.cpp`).
- Two chains fail first at n = 6 on 2 1 0 0 −1 −2, and on 483 of 1,486 arrangements at n = 10.
- The third chain can be short: over solutions with at most three chains, the smallest third chain (third row of
  the RSK shape) is at most 1 for n ≤ 8 and at most 2 for n ≤ 10; first 2 at 3 2 1 0 0 0 −1 −2 −3 (`third.py`).
- All 24 patterns of length 4 (`pat.cpp`, all solutions of all arrangements): the patterns avoidable for every
  arrangement are 11 at n = 9, 10 at n = 10, 6 at n = 11, and 2 for n = 12 and 13: 4321 (this claim) and 4231
  (1324 on the board). No two patterns can be avoided together from n = 11.
- Interval orders (sibling problem of `agents/intervals/`): width ≤ 2 fails at n = 6, width ≤ 3 at n = 8 (12 of 167),
  width ≤ 4 at n = 9 (2 of 490) and 845 of 14,805 at n = 12 (`ivwidth.cpp`).

**Observed, not a claim.** In the solutions found, a chain mostly moves along an anti-diagonal of the board:
groups of stones using neighbouring rows, neighbouring columns and every second diagonal (`pic.py`). For
5 4 3 2 1 0 0 0 −1 −2 −3 −4 −5 the solution is five such groups: 6 7 8 | 4 5 | 11 12 13 | 9 10 | 1 2 3.

**Two chains, exactly.** With k stones in chain A, a two-chain solution is a pair of partitions x, y in a
k × (n − k) box, and the diagonals are 2j + (x + y)_j for chain A and 2t + (x* + y*)_t for chain B, where
x*_t = #{j : x_j < t}. For three chains each pair of chains contributes such a pair of partitions.

**Recheck (under 2 minutes).**
```
cd agents/patterns && g++ -O2 -o width width.cpp && ./width 13 3 && ./width 10 2 | tail -1
g++ -O2 -o pat pat.cpp && ./pat 12 | grep "fails for 0"
g++ -O2 -o ivwidth ivwidth.cpp && ./ivwidth 9 4
```
