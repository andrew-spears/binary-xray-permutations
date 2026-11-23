# A description uniform in the slack? — REPORT

**NOTHING** for a proof of S2 and for a description uniform in the slack: the natural uniform statement (polygon
inequalities, §3) is exact at slack 2 and 3, still true at slack 4, and false at slack 5; the cone at slack 4 is
already not simple. **HIT (tested)** for the two smaller questions: every return to slack 2 is a nonnegative
integer matrix in (u, v, w) and maps the whole triangle cone into the pentagon of S2 (§1); at slack 3 the cone of
all count vectors has 6 explicit generators and 6 facets, two triangles (§2). **Proved (sketch):** the parity that
makes u, v, w integers, at every slack (§3).

Notation as in COUNT2_REPORT.md. A *formal* word is any sequence of letters with slacks ≥ 0 (repeated or decreasing
diagonals allowed, stones placed in the given order); the interface machine counts its placements the same way.
J is the half-turn. All runs below take under a minute.

## 1. Slack 2: returns in the basis U, V, W
U = (2|−) + (1|1) + (−|2), V = (11|−) + (1|1) + (−|11), W = (2|−) + (11|−) + (−|2) + (−|11), so that
(α, β, γ) = uU + vV + wW. What they are: U is the count vector of the word (2) (the three positions of one stone);
V = JU is the set of states from which one stone (letter −2) finishes; W is the count vector of (1, 1) and W = JW.
V is also half the count vector of the formal word (2, 0).

`python3 returns2.py 8 9` (`out_returns2_8_9.txt`): the excursions above slack 2 of length ≤ 9 with slacks ≤ 8 give
263 distinct 3×3 matrices in the basis U, V, W.
- All entries are nonnegative integers. Examples: (1,0,−1): columns (1,1,1), (1,1,1), (2,2,0); (1,0,0,−1): columns
  (2,0,2), (0,2,2), (2,2,2).
- Every column (789) satisfies u ≤ 2v + w and v ≤ 3u + 4w, i.e. lies in the pentagon of S2; one column is on its
  boundary, the image of U under (1,0,0,−1) (the beginning (2,1,0,0,−1)).
- The number of distinct matrices grows with the length (31 for length ≤ 7); I see no sign that the monoid is
  finitely generated, e.g. the excursions (1, 0^k, −1) are one new matrix for each k.

The same for formal words, as cones (`python3 uniform.py 2 5 6 9`, `out_uniform_2_5.txt`): the cone spanned at slack
2 by the count vectors of all formal words with slacks ≤ 5 is exactly the cone on U, V, W, and it is already spanned
by words that stay at slack ≤ 2.

**What remains for S2.** S2 for all beginnings follows from
- (R1) every excursion above slack 2 acts on (u, v, w) by a nonnegative matrix (the triangle part);
- (R2) each column of that matrix satisfies u ≤ 2v + w and v ≤ 3u + 4w;
- (R3) the beginnings that reach slack 2 for the first time from above (from slack 0 or 1 over the top) lie in the
  pentagon,
because a beginning at slack 2 with last letter ≤ 1 is either (…, 1) arriving from slack 1, i.e. W; or a letter 0
after such a beginning (S2 is preserved by 0, proved); or the end of an excursion, which started at slack 2 in the
triangle cone (after a last letter 2 the vector is U) or below slack 2. All three are tested, none
proved: a proof needs the cones above slack 2, see §2–3.

## 2. Slack 3 (dimension 5)
Coordinates: per-state counts of the classes (111|−), (21|−), (3|−), (11|1), (2|1) (and mirror images).
`python3 uniform.py 3 5 7 10` (`out_uniform_3_5.txt`): the cone K₃ spanned by the count vectors of all formal words
with slacks ≤ 5 ending at slack 3 (the same for slacks ≤ 4) has 6 extreme rays, all 0/1 vectors:

| generator (set of classes) | formal word |
|---|---|
| (3|−), (2|1) | (3) |
| (21|−), (11|1), (2|1) | (2, 1) |
| (21|−), (3|−), (11|1) | (1, 2) |
| (111|−), (11|1) | (3, 1, −1) |
| (111|−), (21|−), (2|1) | (1, 2, 0) |
| (111|−), (21|−), (3|−) | (2, 0, 1) |

- K₃ is not a simplicial cone (6 rays in dimension 5), so there is no basis; the right object is the cone. Its 6
  facets are two triangles:  none of L(111|−), L(21|−), L(11|1) exceeds the sum of the other two, and the same
  for L(21|−), L(3|−), L(2|1).
- All 6,239 legal beginnings at slack 3 (slacks ≤ 7, length ≤ 10) lie in K₃. The set of generators is invariant
  under J (rows 1 ↔ 4, 3 ↔ 5, 2 and 6 fixed).
- DEL0 on K₃: of the 36 values N(g 0 g') − N(g g') on pairs of generators, 4 are negative (−2): the pairs
  {(3), (3,1,−1)} and {(1,2), (1,2,0)}, which are the pairs (g, Jg) with g ≠ Jg. At slack 2 the picture is the same:
  one negative pair, (U, V) = (U, JU). So the form is negative only between a generator and its half-turn, and an
  analogue of the two extra inequalities of S2 has to control exactly these two products.
- Words that stay at slack ≤ 3 are not enough (`uniform.py 3 3 6 9`): their cone has 7 rays and misses 49 of the
  376 directions of legal beginnings, e.g. (1,2,1,0,−1). One step higher (slack 4) is enough at slack 3.

## 3. Uniform statements
**Parity (proved, sketch; tested).** For a beginning x of slack s and diagrams (ν|μ) with |ν| + |μ| = s − 1, let
Add(ν|μ) be the states obtained by adding one box to ν or to μ. Then Σ_{κ ∈ Add(ν|μ)} L_x(κ) is even. At s = 2 this
is α + β + γ even, which makes u, v, w integers. Sketch: count placements with the sign of the permutation; adding
a row acts on the row diagram as a Bernstein operator B_ρ (up to exactly that sign), so the signed vector is
𝔅_{e_k}⋯𝔅_{e_1}·1 with 𝔅_n = Σ_{i+j=n} B_i(X)B_j(Y). The derivation D = ∂/∂p₁(X) + ∂/∂p₁(Y) satisfies
D𝔅_n = 𝔅_n D + 2𝔅_{n−1}, so D of the signed vector is twice an integer vector, and the coefficient of (ν|μ) in D z
is the sum of z over Add(ν|μ). Signed and unsigned counts agree mod 2. Test: `python3 polygon.py 6 9`: 0 odd sums
in 270,577 tests (slack 1..6), and 0 in 1.4 million for formal words (`polygon.py 5 7 formal`).

**Polygon inequalities P (tested: true for s ≤ 4, false at s = 5).** P: among the numbers L_x(κ), κ ∈ Add(ν|μ), none
exceeds the sum of the others (equivalently none exceeds half the even sum).
- s = 1: L(1|−) = L(−|1), the transposition symmetry. s = 2: the triangle inequalities. s = 3: exactly the facets
  of K₃. So P is the uniform statement that the data at slack ≤ 3 suggest.
- s = 4: 0 failures in 27,730 tests on legal beginnings (slacks ≤ 6, length ≤ 9) and in 377,810 on formal words.
- s = 5: fails, first for x = (1,1,2,1) and (ν|μ) = (−|22): L(1|22), L(−|32), L(−|221) = 0, 2, 0 (checked by hand: the
  two placements are rows (1,4,3,2) and (2,3,1,4)). 386 failures of 71,340 at slack 5, all for (−|22) and its mirror;
  at slack 6 for (2|111), (11|3) and mirrors (`out_polygon_6_9.txt`).

**The cone at slack 4** (`uniform.py 4 5 6 9`, 10 seconds): formal words with slacks ≤ 4 give 28 extreme rays at
slack 4, with slacks ≤ 5 already 51, no longer 0/1 vectors and no longer J-invariant, with generating words such as
(2,2,1,−1,1,−1,1,−1,0). So "finitely many explicit generators" stops at slack 3 as far as I can see.

**Staircase arrivals (item 3).** At slack 2: yes, every count vector is a nonnegative integer combination of
U, V, W, which come from (2), (2,0), (1,1). At slack 3: no for words staying ≤ 3, yes with the six words of the
table (one of them, (3,1,−1), goes to slack 4). At slack 4: no small family found.

## Conclusion
The inequalities that DEL0 needs at slack 2 and 3 are polygon inequalities between states differing by one box,
plus a bound on the products (g, Jg). They are consequences of the dynamics above (returns), and the description
of what lies above stops being simple at slack 4–5. So this route gives DEL0 at slack 2 only together with a
separate argument for (R1)–(R3); I do not have one. If one wants to continue here, the sharpest small target is
(R1) alone: the triangle inequalities α ≤ β + γ, β ≤ α + γ, γ ≤ α + β at slack 2 for all formal words, equivalently
a + c ≤ 2b ≤ 4·min(a, c) for the three ways to finish by two stones.
