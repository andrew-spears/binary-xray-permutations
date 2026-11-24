# Chains, blocks and the two-chain machine (follow-up to agents/patterns/REPORT.md)

Convention as in agents/patterns: rows and columns 1-based, stone (i, c) on line i + c, lines = D + n + 1,
letter of the k-th smallest line = line − 2k. A chain is a set of stones increasing in row and column.

## 1. Three words

A solution with chains X ∈ {A, B, C} is three words of the same content: a (chain of each row), b (chain of each
column), c (chain of each stone in order of lines). The t-th X of a, of b and of c are the same stone, and

    letter of a stone = (place in a) + (place in b) − 2 (place in c).

Only requirement: the letters read along c never drop by 2 or more (lines distinct and in the order c).
For any solution: letter = (incomparable stones later in line order) − (incomparable stones earlier).

## 2. Two chains: PROVED description (also machine checked against brute force for every word, n ≤ 9: m2.py check 9)

Draw a, b, c as lattice paths in a k × m box (A = east, B = north). A_j and B_t are incomparable exactly when the
cell (j, t) lies between the paths a and b. The path c runs between a and b, and

    letter of A_j = (height of a at east step j) + (height of b at east step j) − 2 (height of c at east step j),

the same with 'horizontal position' for north steps. So letter = twice the distance of c from the midpoint of a
and b: c is the midpath, and a word with letters in {−1, 0, 1} asks for c within half a step of the middle.

The slack after a prefix of c ending at the point p is the number of cells between a and b that lie up-left of p
or down-right of p. These two sets are Young diagrams ν (anchored at p, up-left) and κ (down-right).

**Two-chain machine.** State: two partitions (P, Q), |P| + |Q| = slack. A stone with letter e is
- A: delete the first row of Q (length q₁); give P a new first column of height e + q₁ (needs e + q₁ ≥ rows of P);
- B: the same with P and Q exchanged.
A word has a two-chain solution iff some sequence of A/B steps leads from (∅, ∅) to (∅, ∅). Each step is forced
once A or B is chosen.

*Proof.* Write w(j) for the number of B's before the j-th A in a word w, and lo(j) = min(a(j), b(j)),
hi(j) = max(a(j), b(j)); both are nondecreasing in j. A_j is below B_t iff t > hi(j), above iff t ≤ lo(j), and
incomparable iff lo(j) < t ≤ hi(j). Lines increase along the order, so lo(j) ≤ c(j) ≤ hi(j), and
letter(A_j) = (j + a(j)) + (j + b(j)) − 2(j + c(j)) = (hi(j) − c(j)) − (c(j) − lo(j)).
After a prefix of c with i A's and t B's let P be the set of incomparable pairs (A_j placed, B_t' unplaced) and
Q the set of incomparable pairs (A_j unplaced, B_t' placed). P has one column per placed A_j, of height
hi(j) − t (longest for j = i), and one row per unplaced B; Q has one row per unplaced A_j, of length t − lo(j)
(longest for j = i + 1). Placing A_{i+1} deletes its row of Q, of length q₁ = t − lo(i+1) = c(i+1) − lo(i+1), and
gives P the column of height h = hi(i+1) − t ≥ hi(i) − t = rows of P; the letter is h − q₁. Placing B_{t+1}
deletes its row of P (the p₁ placed A's incomparable to it) and adds one cell to the row of every unplaced A_j
with lo(j) ≤ t: a first column of height r ≥ rows of Q; the letter is (later incomparable) − (earlier) = r − p₁.
Conversely, from a run define hi(j) = t + h and lo(j) = t − q₁ at the step that places A_j. A row of Q, once
nonempty, grows at every B step, so its cells are the last B's placed, and both sequences are nondecreasing. Take
a = the word with a(j) = lo(j) and b = the word with b(j) = hi(j). The letters of the A's are right by
construction; for B_t placed after i A's, (place in a) + (place in b) − 2(place in c) =
#{j : lo(j) < t} + #{j : hi(j) < t} − 2i = #{j > i : lo(j) < t} − #{j ≤ i : hi(j) ≥ t} = r − p₁. ∎

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

## 7. Two chains plus extra stones

An extra stone C is a point u on the path a, a point v on the path b and a point p on the path c, with p in the
box spanned by u and v. Its letter is |u| + |v| − 2|p| (steps along the paths). It adds +1 to the letter of every
stone of A and of B that is incomparable to it and earlier in line order (the last few A's and B's before p),
and −1 to those incomparable and later. So 'two chains plus t stones' = a run of the two-chain machine whose
letters are corrected by ±1 near t marked points. For the proved family (no high stone before a low stone) one
marked point is enough up to n = 13.

## 8. More than two chains

For any number of chains, letter of a stone = sum over the other chains of its two-chain letter against that
chain. The exact machine is the general interface machine (hole patterns of rows and of columns) with one
pointer per chain in the rows and one in the columns: a stone of chain X goes into a hole after X's pointers,
the pointers move there, and no hole may be left behind all pointers. Not yet coded.
