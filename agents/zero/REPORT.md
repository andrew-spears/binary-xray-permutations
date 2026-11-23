# zero: the rule ZERO — REPORT

**HIT** (proved counterexamples, §1) and **NOTHING** for a true replacement (§2, tested only).

Notation as in `../interface/SHORTEN_BRIEF.md`: stone j of a prefix x has row + column = 2j + e_j, F(x) = set of
(rows used, columns used), states of words of different lengths are compared after Sh(A) = (A + 1) ∪ {1}.
Overlap: `../fshape` and `../runrule` (sibling sessions) found the residue-count lemma and the table of failing
RUN rules independently; what is new here is §1(b), §1(c) and the system of §2.

## 1. ZERO is false, also with two zeros (proved)

**(a) x = (2,3,3,2,2,1,1,0), slack 14** (sums 4, 7, 9, 10, 12, 13, 15, 16; the parent's case, 8 stones).
t = rows {1,2,3,4,6,7,9,10,12}, columns {1,…,7,9,12} is in F(x −1): stones (1,3) (2,5) (7,2) (6,4) (3,9) (12,1)
(9,6) (4,12) (10,7), sums 4 … 16, 17. Sh(t) = rows {1,2,3,4,5,7,8,10,11,13}, columns {1,…,8,10,13} is not in
F(x 0 −1), sums 4 … 16, 18, 19:
no sum is ≡ 2 (mod 3), so a row ≡ 1 never meets a column ≡ 1. The five rows ≡ 1 (1,4,7,10,13) therefore use all
five columns ≢ 1 (3,6 | 2,5,8), three of them a column ≡ 2 (sum ≡ 0). The five columns ≡ 1 then take the rows
2,5,8,11 (sum ≡ 0) and 3. That is 3 + 4 = 7 stones with sum ≡ 0, but only 9, 12, 15, 18 exist. ∎
*What goes wrong:* after its first letter x is the staircase 3 3 2 2 1 1 0, whose sums are ≡ 0 or 1 (mod 3). The
letter −1 gives the only sum ≡ 2 (17), and t needs that stone; 0 −1 gives 18, 19, again ≡ 0, 1. All 7 ways to seat
18 and 19 in Sh(t) leave a board outside F(x) that passes the sum (Landau) test (`cex.py`).

**(b) x = (2,5,4,3,2,1,0), slack 17** (sums 4, 9, …, 14; 7 stones, a shortest failing prefix:
none of the 276 legal prefixes of length ≤ 6 that −1 can follow fails, `./bylen 6 30 "-1:0,-1"`).
t = rows {1,3,4,5,6,7,8,13}, columns {1,…,7,13} is in F(x −1): (3,1) (5,4) (4,6) (8,3) (7,5) (6,7) (1,13) (13,2),
sums 4, 9 … 14, 15. Sh(t) = rows {1,2,4,…,9,14}, columns {1,…,8,14} is not in F(x 0 −1), sums 4, 9 … 14, 16, 17:
column 14 needs a row d − 14 ≤ 3, row 3 is absent, so it holds (2,14) with d = 16; row 14 needs d ≥ 15, so it holds
(14,3) with d = 17; the sum 4 needs (1,3), (2,2) or (3,1), and column 3, row 2 are used, row 3 is absent. ∎

**(c) Two zeros: x = (2,6,5,4,3,2,1,0,0), slack 23.** The same three stones: t = rows {1,3,…,10,17},
columns {1,…,9,17} is in F(x −1) ((3,1) (6,4) (5,6) (4,8) (10,3) (9,5) (8,7) (7,9) (1,17) (17,2)); Sh(t) = rows
{1,2,4,…,11,18}, columns {1,…,10,18}, sums 4, 10 … 16, 18, 20, 21, forces (2,18), (18,3) and blocks the sum 4. ∎
So F(x 0 0 −1) ⊄ F(x 0 0 0 −1) for x = (2,6,5,4,3,2,1): asking for two zeros before the −1 does not repair ZERO.

*What goes wrong in (b), (c):* t has one far row and one far column, served by the two top sums (2k, 2k+1) through
rows/columns 1 and 2. In the longer word the top sums are 2k+2, 2k+3 with 2k+1 skipped, the far pair needs
rows/columns 2 and 3, and these are exactly what the lowest stone (sum 4) needs. The extra 0 moves the frontier
by one but leaves the low sums of x where they were. These are **not** small-modulus obstructions: the residue
count (`../fshape`, `modcount.py`) excludes the target of (b) only for m = 13, 16 and that of (c) for no m ≤ 16,
so "residue counts explain every failure" is false. (Both targets also fail the linear relaxation.)

## 2. Replacement: NOTHING (tested)

The word-level step can use an inclusion on the prefix side **or on the suffix side** (mirror word: reverse and
negate). This gives a complete system (`system.py`, docstring) that needs only I1: (0,0,−1) → (0,0,0,−1),
I2(a,b): urun → a…1 0 0 −1…−b, I3(a,b) = RUN(a,b) for a ≤ b only, I4: (0,0) → (0,1,0,−1), I5: (0,−1) → (1,0,−1,−1);
it avoids ZERO after a single 0, PEAK in general, and RUN(a,b) with a > b (all the failures known at bound 14).
- Bound 14, all lengths (as requested): every needed inclusion holds (0 failures; a, b ≤ 4 occur), and all 69,443
  valid nonzero words of length ≤ 13 with slacks ≤ 14 reduce to the zero word by these steps.
- Beyond 14 it dies like the old rules (`by_7_24.txt`: prefixes of length ≤ 7, slacks ≤ 24; `by_8_20.txt`: length
  ≤ 8, slacks ≤ 20): I1 fails after (2,6,5,4,3,2,1) (slack 23, §1(c)), I2(3,1) after (3,4,3,4,3) (17), I3(1,2)
  after (5,4,3,2,1,2,1) (18), I3(2,2) after (5,4,3,2,2) (16), I4 after (3,2,4,3,3,2,1) (18). No failure in these
  ranges: I2(a,b) for a ≤ 2, b ≤ 3 and (3,2), I3(1,3), I3(2,3), I3(3,3), I5.

So I have no true set-level statement that carries "x (−1) y solvable ⇒ x 0 (−1) y solvable": more zeros, more
context and the mirror side each only raise the slack at which the inclusion fails (14 → 16–23). The mechanism of
§1(b) needs nothing but a steep prefix, so I expect the survivors to fail too. This agrees with `../runrule`.

## Recheck (under 4 minutes)
```
cd agents/zero && g++ -O2 -o rule rule.cpp && g++ -O2 -o bylen bylen.cpp
python3 cex.py        # 2 s: §1(a), the 16 placements of t, the 7 seatings of 18 and 19
python3 far.py        # 1 s: §1(b), (c) by brute force, placements, residue counts
python3 system.py 14 13   # 2.5 min: the system of §2 at bound 14
./bylen 5 24 "1,0,0,-1:2,1,0,-1,-2" "2,2,1,0:3,2,1,0,0,-1"   # 7 s: I3(2,2), I2(3,1) fail
./bylen 7 20 "0,0:0,1,0,-1" "0,-1,-1:1,0,-1,-2"              # 10 s: I4, I3(1,2) fail
```
Files: `lib.py` order-free model; `rule.cpp` interface machine at a slack bound (reproduces ZERO 1 of 904 at 14);
`bylen.cpp` all prefixes up to a length, 128-bit states; `modcount.py` residue counts.
