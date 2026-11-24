# Chains, blocks and the two-chain machine (follow-up to agents/patterns/REPORT.md)

Convention as in agents/patterns: rows and columns 1-based, stone (i, c) on line i + c, lines = D + n + 1,
letter of the k-th smallest line = line − 2k. A chain is a set of stones increasing in row and column.

## 1. Three words

A solution with chains X ∈ {A, B, C} is three words of the same content: a (chain of each row), b (chain of each
column), c (chain of each stone in order of lines). The t-th X of a, of b and of c are the same stone, and

    letter of a stone = (place in a) + (place in b) − 2 (place in c).

Only requirement: the letters read along c never drop by 2 or more (lines distinct and in the order c).
For any solution: letter = (incomparable stones later in line order) − (incomparable stones earlier).

## 2. Two chains: PROVED description (machine checked against brute force for every word, n ≤ 9: m2.py check 9)

Draw a, b, c as lattice paths in a k × m box (A = east, B = north). A_j and B_t are incomparable exactly when the
cell (j, t) lies between the paths a and b. The path c runs between a and b, and

    letter of A_j = (height of a at east step j) + (height of b at east step j) − 2 (height of c at east step j),

the same with 'horizontal position' for north steps. So letter = twice the distance of c from the midpoint of a
and b: c is the midpath, and a word with letters in {−1, 0, 1} asks for c within half a step of the middle.

The slack after a prefix of c ending at the point p is the number of cells between a and b that lie up-left of p
or down-right of p. These two sets are Young diagrams ν (anchored at p, up-left) and κ (down-right).

**Two-chain machine.** State: two partitions (P, Q) = (ν, κ transposed), |P| + |Q| = slack. A stone with letter e is
- A: delete the first row of Q (length q₁); give P a new first column of height e + q₁ (needs e + q₁ ≥ rows of P);
- B: the same with P and Q exchanged.
A word has a two-chain solution iff some sequence of A/B steps leads from (∅, ∅) to (∅, ∅). Each step is forced
once A or B is chosen. (Proof: the up-left region gains the column of a new A-stone and loses one cell per
column when c goes north; see the derivation in the session log; the code m2.py is the statement.)

Heuristic: in a ribbon of vertical thickness δ and slope s the slack is about δ²/s. A two-chain solution exists
when the thickness can follow the slack, i.e. when the slack profile is smooth; a big letter changes the slack
faster than a ribbon can widen.

## 3. What two chains reach (computed)

- All words: without a two-chain solution 1 of 22 (n = 6), 29 of 167 (n = 8), 483 of 1,486 (n = 10).
- Letters in {−1, 0, 1}: every word up to n = 9 has a two-chain solution; FALSE at n = 10:
  1 1 0 0 1 0 −1 0 −1 −1 and its mirror; 8 of 978 at n = 11, 1,005 of 30,372 at n = 15 (pm1.py 15).

## 4. The third chain is short (computed, third.cpp)

Smallest number of stones outside two chains, over all solutions with at most three chains:
- every word: at most 1 for n ≤ 8, at most 2 for n ≤ 13 (n = 13: 22,833 words need 0, 24,443 need 1, 831 need 2);
- words with no high stone before a low stone (the proved family): at most 1 for n ≤ 13 (13,430 words at n = 13);
- staircase k, …, 1, 0, 0, −1, …, −k: exactly 1 for k = 2..7, with an explicit solution (k = 7: rows 1..8 to
  columns 8..11, 13..16; rows 9..12 to columns 1..4; row 13 to column 12; rows 14..16 to columns 5..7);
- staircases with j zeros: 2 for j = 3 (k = 3..6); 3 for k = 6, j = 4, 5, 6 (n = 16..18). So it is not bounded.

## 5. Blocks (computed, blocks.py)

A block = stones on neighbouring rows and neighbouring columns of one chain (lines going up by 2). Contracting
every block to a point gives a weighted problem (weights = block lengths), but blocks are not few:
1 0 … 0 −1 has only solutions with n blocks. Fewest blocks is always attained by a solution with ≤ 3 chains (n ≤ 9).

## 6. Where three chains bite (tight3.py)

Whenever some solution needs more than three chains, there are still at least 12 solutions with at most three
(n = 9, 10). Smallest share: 26 of 396 for 4 3 2 1 0 0 −1 −2 −3 −4. For staircases the number of three-chain
solutions stays small (6, 22, 26, 48 for k = 2..5 with two zeros) while the number of all solutions grows fast.

## Recheck
    python3 m2.py check 9        # machine = brute force, 1 minute
    python3 pm1.py 12            # letters in {-1,0,1}: first failures at n = 10
    g++ -O2 -o third third.cpp && ./third n 12     # third chain at most 2
