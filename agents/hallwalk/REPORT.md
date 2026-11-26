# HIT (small): repairing a solution after a minimal move by reflecting a chain of stones

Board language: a stone is (row r, column c), its diagonal is d = c − r. D is valid. A minimal move takes the stones
X on x and Y on y (x < y) to x + 1 and y − 1.

## Claim 1 (proved): reflecting a chain

For an integer s, reflect a stone in the anti-diagonal r + c = s: (r, c) → (s − c, s − r). The stone stays on its
diagonal. In a solution, let ψ_s(r) be the row of the stone in column s − r (undefined when s − r is off the board).
ψ_s is a one-to-one partial map on the rows, so its orbits are closed loops and open paths, and there are exactly
|s − (n + 1)| open paths.

(a) Reflecting all stones of a closed loop gives another solution of the same D. (s = n + 1, every loop: the usual
    reflection of the whole board.)
(b) Reflecting the stones in rows r_1 → r_2 → … → r_m of a chain (r_{j+1} = ψ_s(r_j)), all except the first, frees
    row r_m and column s − r_1, and uses row r_1 and column s − r_m instead. Nothing else changes.

Proof. The stone in row r_{j+1} has column s − r_j; its mirror image is (r_j, s − r_{j+1}). So the reflected stones
use rows r_1 … r_{m−1} and columns s − r_2 … s − r_m, where before they used rows r_2 … r_m and columns
s − r_1 … s − r_{m−1}. For a closed loop the two lists are the same.

## Claim 2 (proved): when the repair works

Put s1 = r_X + c_Y − 1 and s2 = r_Y + c_X + 1. For s = s1: take X and Y off. Put Y back one column to the left,
at (r_Y, c_Y − 1). That column is s1 − r_X. If it is taken, follow r_X → ψ(r_X) → … until the column s1 − r is one
of the two free columns c_X, c_Y, and reflect the stones met on the way; by (b) this frees the column s1 − r_X that
Y needs and uses a free one. X goes in the row and column left over, and lands on x + 1 because the sum of all
diagonals is unchanged. The same works starting from r_Y, with Y placed in row r_X. The chain from a row stops at a
free column exactly when it comes back to the row of X or Y before leaving the board. So

    for s = s1 (or s2), no repair exists  ⇔  the rows of X and Y lie on two different open paths of ψ_s.

Corollary. If some solution of D has s1 or s2 in {n, n + 1, n + 2}, the moved arrangement is solvable (there is at
most one open path). In words: the corner (r_X, c_Y) of the rectangle spanned by the two stones lies on the main
anti-diagonal of the board shifted by 0, 1 or 2 cells; or the same for the other corner, mirrored.

The case s = n + 1 is not new: there the repair is "reflect one closed loop, then swap two stones in adjacent rows
or columns", so it works exactly when D has a solution with X and Y in the right adjacent rows or columns (the
plain swap of card goodwitness). The cases s = n and s = n + 2 use the single open path and are new.

These four repairs (s1 or s2, start at X or Y) are the eight walks of M. Hall's exchange argument for sums of two
permutations in an abelian group (1952), which come in equal pairs. In a group the walk cannot leave the board;
here leaving the board is the only way to fail.

## Claim 3 (tested only): a solution near the anti-diagonal always exists

For every minimal move of every valid D with n ≤ 11 (12,913 moves at n = 11), some solution has s1 or s2 in
{n, n + 1, n + 2}. For about 8% of the moves at n = 11 (1,083) no solution has s = n + 1, so the plain swap is not
enough and the open path is needed. If Claim 3 holds for every n, the conjecture follows.

## Claim 4 (tested only): the induction closes on the solutions it builds

Start from the one solution of the evenly spaced arrangement and use only repairs with s in {n, n + 1, n + 2}.
For n ≤ 9 this reaches a solution of every valid D, and for every minimal move one of the solutions reached has
s1 or s2 in {n, n + 1, n + 2} (near.py). With s = n + 1 alone it stops at the first move. The solutions reached are
about two thirds of all solutions (8,465 of 12,657 at n = 9), but for single arrangements as few as 0.8%. Neither the
largest distance of a stone from the middle anti-diagonal nor the number of chains separates reached from unreached
solutions (nearstat.py), so I have no description of the class yet.

Equivalent form of Claim 3: some solution has r_X + r_Y in {n+1−y, n+2−y, n+3−y} or in {n−1−x, n−x, n+1−x}.

Claim 3 split in two (tested only, n ≤ 10, spread.py). Let t = r + c − (n + 1) be the offset of a stone from the
middle anti-diagonal, T = t_X + t_Y and g = y − x. Claim 3 says |T| ∈ {g − 4, g − 2, g} for some solution, and
reflecting the whole board changes the sign of T. Over all solutions of D:
- (A) the largest T is at least g − 4 (it can be larger than g: up to g + 10 at n = 10);
- (B) two neighbouring values of T differ by 2 or 4, except when the only values are −4 and 4.
(A) and (B) give Claim 3, because a step of 4 cannot jump over three consecutive values. (A) alone is weaker than
Claim 3 and reads: some solution has r_X + r_Y ≥ n − 1 − x.

## Claim 5 (tested only): the path that always opens the first run keeps a solution

Undoing a minimal move means opening a maximal run of two or more consecutive diagonals a+1, …, b−1 of D′: its two
end stones go to a and b. Call the result a parent of D′ if it is valid. Fix a rule that picks one parent for each
D′; then each D′ has one path of minimal moves from the evenly spaced arrangement. Let A(evenly spaced) be its one
solution and A(D′) the set of solutions got from A(parent) by any of the four repairs of Claim 2 (s1 or s2, chain
started at X or at Y).

For each of eight rules (first run, last run, longest, shortest, run nearest the middle, run furthest from the
middle, run at the greatest slack, run at the least slack) A(D′) is non-empty for every valid D′ with n ≤ 12
(14,805 arrangements at n = 12; tree.py). The sets are small: at most 2,924 solutions at n = 12. If this holds for
every n for one rule, the conjecture follows. The claim is stated for the rule "first run" (the lowest run whose
opening is valid); the other seven are further evidence that many rules work. Not every rule works: a minimal move
lowers the sum of squares, so every path of moves is the path of some rule, and one path at n = 7 fails (below).

Limits of Claim 5, all computed:
- It needs a fixed path. Following every path of moves from the start, with A defined the same way, A becomes empty
  at n = 7: after the eleven moves (−6,−2), (−3,0), (−1,2), (1,4), (−2,2), (−4,−1), (3,6), (1,4), (−5,0), (−1,2),
  (1,5) the set A has two solutions of −4, −3, −2, 0, 2, 3, 4, and neither can be repaired for the move (−2, 2)
  (allpaths.py). That is the only such state at n = 7.
- It needs all four repairs. With mirror lines next to the middle only, every one of the eight rules leaves some
  arrangement empty by n = 7 or 8 (tree.py N near).
- The sets are not thin and have no description yet. For the rule "first run", A(D′) is a median half of all
  solutions of D′ (smallest share 1/8 at n = 9), and for a single move as little as half of A(parent) can be
  repaired (a quarter for the rule "shortest run"), n = 9. The sets for the eight rules have no solution in common for 118 of the 490 arrangements at n = 9
  (treeshape.py). The sign of the permutation is not constant on A(D′).
- Without any rule: let U(D′) be all solutions got by a repair from U(D) over every parent D. Then U is 82% of
  all solutions at n = 9 (10,371 of 12,657), all of them for 181 of 490 arrangements, and at least a quarter for
  each (union.py 9). The solutions never reached include 25314 and 41352 for −3, −1, 0, 1, 3 and 2413 ⊕ 1, 3142 ⊕ 1,
  1 ⊕ 2413, 1 ⊕ 3142 for −2, …, 2 (written as columns by row), although 2413 itself is reached at n = 4.
- Loops do not fill the gaps. U is not a union of loop-reflection classes (Claim 1 (a), any s): at n = 8, 74 of
  the 324 classes are split by U and 44 are missed entirely (loops.py 8). Closing U under loop reflections as well
  as repairs still misses 6 of the 23 solutions at n = 5 and 118 of 2,113 at n = 8.
- Why U misses solutions: in the repair graph (every solution of every valid D, an edge for each repair along a
  minimal move) some solutions other than the evenly spaced one have no incoming edge, so no un-move can be
  un-repaired. There are 1, 3, 11, 49, 195 of these sources for n = 4 … 8 (sources.py 8). The smallest are 25314
  and 41352 for −3, −1, 0, 1, 3; most of those at n = 6 are an n = 5 source with one extra stone in a corner, for
  example 364251. A proof that U(D′) ≠ ∅ has to show that no arrangement has all its solutions downstream of
  sources other than the start.
- It needs sets. Keeping one solution per arrangement, namely the first repair that works in a fixed order of the
  four, fails by n = 10 for all 8 × 24 combinations of rule and order; the best five (all with the rule "run
  furthest from the middle") work up to n = 9 (tree1.py).

## What does not work

- Repair from every solution: the share of solutions of D that can be repaired falls with n (1, 0.83, 0.83, 0.69,
  0.69, 0.53 for n = 6 … 11), lowest for the last move into the most central arrangement.
- Loop reflections do not connect all solutions of D: 2 classes already for diagonals −3, −1, 0, 1, 3 (n = 5),
  10 classes for one set at n = 9 (cyc.py, written with lines r + c instead of diagonals).
- Keeping one solution per arrangement, chosen by a fixed order, and using only repairs with s in {n, n+1, n+2}:
  some arrangement is left with no solution from n = 7 for the two orders tried (smallest rows first, largest rows
  first: 1, 3, 17 arrangements at n = 7, 8, 9) and for six random orders at n = 8 (3 to 28 arrangements). Keeping
  three per arrangement still leaves 2 at n = 8 (one.py). So the class of Claim 4 cannot be cut down to a single
  canonical solution this simply. "The solution nearest the middle anti-diagonal" is not a rule: the sum of
  (r + c − n − 1)² over the stones is the same for every solution of D.
- A helper block cannot join two open paths (proved, a few lines). Put D next to another solvable arrangement B
  across a tight cut, so that every solution is a block sum, and use a mirror line of the large board. The line has
  the same distance k from the middle in each block. The k open paths of B's block end in its k lowest rows, and the
  next column on each is one of the k leftmost columns of D's block, where D's open paths begin. So each open path
  of D is only made longer by one open path of B (and likewise at its other end by a block on the other side); two
  different open paths of D stay different, and the repair fails exactly when it failed without the helper.
- Starting from the one solution of the evenly spaced arrangement and using only successful repairs reaches some
  solution of every valid D for n ≤ 9 (reach.py), but I have no description of the solutions reached.

## Recheck

    python3 refl.py 10        # about 8 seconds; asserts Claims 1 and 2 on every solution, prints Claim 3 counts
    python3 refl.py 11        # about 40 seconds
    python3 near.py 9 1       # Claim 4, a few seconds; near.py 8 0 shows s = n + 1 alone is not enough
    python3 one.py 8 1 rows   # one kept solution per arrangement is not enough
    python3 cyc.py 9          # loop reflections do not connect
    python3 tree.py 10        # Claim 5 for n ≤ 10, 5 seconds (n = 12: about 4 minutes per rule); "tree.py 9 near" for the near-middle version
    python3 treesub.py 9      # which of the four repairs are needed (4 minutes); treeshape.py 9: sizes of the sets
    (run from agents/hallwalk/ or with the path in front; the scripts find refl.py beside themselves)
    python3 loops.py 8        # loop classes split or missed by U (1 minute); sources.py 8: sources of the repair graph
    python3 allpaths.py 7     # every path instead of one: A becomes empty
    python3 tree1.py 10 "run furthest from the middle"   # one solution per arrangement fails at n = 10

hw.py, hw2.py, reach.py are the first experiments, written with lines r + c (columns reversed).
