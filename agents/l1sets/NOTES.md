# Reachable sets for letters −1, 0, +1 (working notes; nothing here is on the map as a claim)

All(s) = every interface state of slack s = every pair of diagrams with s boxes (1, 2, 5, 10, 20, 36, 65, 110, 185).

1. Few sets, mostly everything (sets.py 9, classes.py, full.py 9 12). For slack ≤ 8 there are at most 7 distinct
   F(x) per slack. Zeros at height ≤ 1 change nothing. At slack 5 only the tails +++++ (28 of 36), ++++0+ (32),
   ++++0+0 (34) fall short of All(5). At slack 4 every prefix ending in + falls short (at most 18 of 20), at
   slack 8 at most 180 of 185. The number of zeros needed for All(s) grows with s (card paritycount).
2. The odd/even count with z = number of zeros is not exact (par.py 9 16): zeros at height ≤ 1 do not count, and
   pure + words miss more at slack 4 and 8 (14 of 16, 128 of 133 count-feasible states): a mod 4 effect.
3. Why no simple description is expected. After + … + (k letters) every stone has an odd sum, so odd rows pair
   with even columns and even rows with odd columns. In half coordinates the two sub-boards are boards with holes
   whose sum sets U1, U2 are ANY partition of {2, …, k+1}. So F(+^k) is described by the reachable sets of
   arbitrary sum sets of half the size: letters −1, 0, +1 are not simpler than the general problem.
   Same remark as a count identity (a diagonal used twice): N(+^a −^a) = Σ N(U1) · N(U2) over all ways to split
   the multiset {2, …, 2a} ∪ {a+1} into two sets of size a.
4. Predecessors (proved, pigeonhole; stable range k ≥ slack). Rows R and columns C after k stones. For e ≤ 0 there
   are always r in R, c in C with r + c = 2k + e: the sets {u : k+u in R} and {u : k+e−u in C} have M+1 and at
   least M+1 elements in the window [−M, M] of size 2M+1. So every hole pattern has a predecessor under every
   letter ≤ 0. For e = +1 the count is M + (M+1): a predecessor exists unless the two sets are complementary, which
   happens for exactly p(m) states of slack 2m (1, 2, 3, 5 for m = 1…4; full.py).
