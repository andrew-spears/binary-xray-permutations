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
- Starting from the one solution of the evenly spaced arrangement and using only successful repairs reaches some
  solution of every valid D for n ≤ 9 (reach.py), but I have no description of the solutions reached.

## Recheck

    python3 refl.py 10        # about 8 seconds; asserts Claims 1 and 2 on every solution, prints Claim 3 counts
    python3 refl.py 11        # about 40 seconds
    python3 near.py 9 1       # Claim 4, a few seconds; near.py 8 0 shows s = n + 1 alone is not enough
    python3 one.py 8 1 rows   # one kept solution per arrangement is not enough
    python3 cyc.py 9          # loop reflections do not connect

hw.py, hw2.py, reach.py are the first experiments, written with lines r + c (columns reversed).
