# intervals: drop "two-dimensional", keep "interval order" (parent session, working notes)

## The restatement (proved, elementary)
Rotate the board: stone k has a_k = n − 1 − row, b_k = column, c_k = a_k + b_k = d_k + n − 1. Order the stones by
"above and to the right" (a and b both larger). This is a poset P of dimension ≤ 2, and
  d_k = down(k) − up(k)   (number of stones below k minus number above k).
Conversely any 2-dimensional poset on n elements gives a permutation. For ANY poset d = down − up is strictly increasing
along the order, so if the values are distinct, sorting by d is a linear extension. With the stones in that order,
  letter e_k = (number of later stones incomparable to k) − (number of earlier stones incomparable to k),
  slack after k stones = number of incomparable pairs across the cut.
So: **D is solvable ⟺ D = {down − up} for a poset of dimension ≤ 2.**
Hierarchy: any graph of "incomparable" pairs (= Landau, trivial) ⊃ posets ⊃ interval orders, 2-dimensional posets.

## Interval orders (2 + 2-free posets)
Stone = interval; below = entirely to the left. Keep the unfinished stones (those that still owe incomparable later stones)
with label = number owed. Labels increase with the right endpoint automatically, so the state is a **partition of the
slack**. Step with letter e (`pm.py`): choose m = 0 or a corner of λ (λ_m > λ_{m+1}; m = ℓ(λ) allowed); the new stone is
incomparable to the m stones with the largest labels (each loses 1) and gets label y = e + m; needed: y ≥ λ_{m+1}, and
y = 0 only if m = ℓ(λ).
- `pm.py 13`: every legal word up to n = 13 (48,107 words at n = 13) has an interval order. TESTED, not proved, and NOT
  implied by the conjecture (a solution need not be an interval order).
- No greedy rule for m works (`rules.py`): smallest m, largest m, most parts, … all fail from n = 5 or n = 7.
- m = ℓ(λ) always (every stone incomparable to all unfinished ones; `iv.py`) is deterministic and fails first on
  2 1 1 0 −1 −1 −2.
- Semiorders (Dyck path, j-th up-step matched with j-th down-step; e_j = height after j-th down-step − height before
  j-th up-step; `semi.py`): the map Dyck path → word is injective on legal words but misses 1 of 22 at n = 6, 9,007 of
  14,805 at n = 12. First miss 1 1 0 0 −1 −1.
- Dyck form of an interval order: α_j = number of right endpoints before the j-th left endpoint, β_i = number of left
  endpoints before the i-th right endpoint, matching π with right endpoint after left endpoint; D + n = {α_j + β_π(j)}.
  So the interval-order version is an x-ray problem on a Ferrers board with two rulers α, β given by a Dyck path that
  one may choose.

## Interval AND 2-dimensional = solutions avoiding the pattern 2143 (vexillary)
On the board (σ(row) = column) a solution's order is 2 + 2-free exactly when σ avoids 2143.
- `iv2.py 9 2`, `pat4.py 9`, `pat4b.py 9`: for n ≤ 9 every valid arrangement has a solution avoiding 2143. The same holds
  for each of 1234 1243 1324 1342 1423 1432 2134 2314 3124 3214 separately (1234 = width ≤ 3 must fail later; 123 fails
  at n = 6), but for no pair of these patterns other than pairs with 1234. So these classes work because they are
  large, not because they are canonical.
- `vex.py n` (complete search): avoiding 2143 FAILS at n = 10 for 3 2 1 0 0 0 0 −1 −2 −3 and 3 3 2 1 0 0 −1 −2 −3 −3;
  10 of 4,639 at n = 11, 29 of 14,805 at n = 12 (out_vex.txt).
- Width 2 (avoid 123): 21 of 22 at n = 6, 1003 of 1486 at n = 10 (`classes.py`).

## Ideas not yet tried
1. Exact description of the reachable partitions F(x) in the partition machine (they look like "all partitions of the
   slack between two bounds"); a Gale–Ryser type criterion would prove the interval-order version.
2. A local condition on the partition machine that forces dimension 2; then the pair machine could be replaced by a
   one-partition machine with a little memory.
3. Necessary condition seen so far: the j largest labels sum to at least the sum of the last j letters.

## Cuts: a Gale–Ryser shape (`cut.py n`)
At a cut x | z, a left interval i overlaps a right interval j iff j starts before i ends, so the overlap pattern is a
Ferrers (nested) bipartite graph: the labels of the left intervals and the labels of the right intervals are CONJUGATE
partitions. Hence  x z has an interval order ⟺ F(x) ∩ conj F(z̄) ≠ ∅,  z̄ = z reversed and negated.
TESTED n ≤ 10 (11,567 cuts with slack > 0): F(x) and conj F(z̄) each have a least and a greatest element in dominance
order, in every case. The meet of the two greatest elements lies in both sets except in 32 cases, and so does the join
of the two least (32 exceptions). Exceptions are staircase-like: 3 2 1 | 0 0 −1 −2 −3 has the single common state (3, 2, 1),
while the join of the bottoms is (2, 2, 2) and the meet of the tops (after 3 2 1 0 0 | −1 −2 −3) is (3, 3).
F(x) is not always the whole dominance interval: after 2 2 2 it is {222, 321, 411, 42}, and 33 is missing.
Greatest element of F(x) = the run with m = ℓ(λ) always, when that run exists; least = m as small as possible (to check).
Plan for a proof of the interval-order version: (1) formulas for least and greatest element of F(x) from the word;
(2) F(x) ⊇ dominance interval minus a named thin family; (3) least(x) ⊴ conj least(z̄)-type inequalities from Landau.
