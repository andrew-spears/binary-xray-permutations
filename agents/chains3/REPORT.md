# Three chains: a machine, the extra stone, failed rules

Convention (as in `agents/patterns/`): rows and columns 0-based, a stone at (i, c) is on the line i + c, chains are
increasing, the word e of D lists the sorted lines as e_j + 2j (j = 0..n−1). "Stone j" = the stone on the j-th line.
Slack of the cut t = e_0 + … + e_{t−1}. Known and used (state.md, 'Orders instead of boards'): in any solution
e_j = (stones incomparable to stone j on later lines) − (those on earlier lines), and the slack of a cut is the
number of incomparable pairs across it.

Summary

| | result | status |
|---|---|---|
| 1 | Exact machine for solutions with at most w chains (any w, so w = 3): state = two words, one step rule | **HIT, proved**; checked w = 2, 3, 4 |
| 2 | Lead "no high stone before a low stone ⟹ two chains + one stone" | **false at n = 14** (9 words), true n ≤ 13 |
| 3 | Letters in {−1, 0, 1} ⟹ two chains + one stone | tested n ≤ 16, LEAD |
| 4 | Rules that place the extra stone | all fail; smallest counterexamples listed |
| 5 | Canonical three-chain solution (lex extreme, corner block, one-block third level, few places, online colouring) | all fail; smallest counterexamples listed |
| 6 | Small proved facts: tight cuts, peak zero, two staircase families; one correction to `agents/patterns/REPORT.md` | proved |

No proof of 3C and no rule naming the three words was found.

## 1. HIT (proved): the chain machine

**Machine M_w.** Letters: `•` (a stone already read) and 1, …, w (a stone of that chain not read yet, "owed").
A state is a pair of words (α, β) with the same number m of `•`. Start: both empty.
Step with the letter e: choose a chain X. In α: if α contains a letter X, the first X becomes `•`; otherwise α is
replaced by α u `•` with any word u in the letters ≠ X (possibly empty). Let p_α = number of letters before the new
`•`. The same in β, giving p_β (with its own word u′). The step is allowed iff

    e = p_α + p_β − 2m.

Afterwards delete from the front of both words the same number d of `•`, d as large as possible.
The word is accepted iff after the last letter both words are empty.

**Theorem 1.** A valid word e has a solution with at most w chains iff M_w accepts e. The accepting runs correspond
one to one to the pairs (solution, labelling of its stones by 1..w with every label class increasing).

Meaning: α and β are the parts of the row word a and the column word b (blocks NOTES §1) that the unread stones can
still see; the step condition is "letter = place in a + place in b − 2 · place in c" inside this window.

**Proof.** (⟹) Take a solution with its stones labelled by chains. For j = 0..n let T_j be the stones on the j
lowest lines. Write the stones in row order, `•` for a stone of T_j and the chain label otherwise, and cut the word
after its last `•`; do the same in column order. Both words have j letters `•`. Let d_j be the largest d such that
both begin with d letters `•`; delete these. Call the result (α_j, β_j). The leading run of `•` only grows with j,
so the deletions of the machine give the same words. Let s be stone j, of chain X. A chain increases in rows and in
columns, hence in lines, so in row order s stands after the stones of X in T_j and before all other unread stones of X.
So if some `•` stands after s, then s is the first X of α_j; if not, the letters between the last `•` and s are
unread stones of other chains: this is u. In both cases the row of s is d_j + p_α; likewise its column is d_j + p_β.
With m = j − d_j: e_j + 2j = row + column = 2d_j + p_α + p_β, i.e. e_j = p_α + p_β − 2m. At j = n both words consist
of `•` only and are deleted.

(⟸) Replay an accepting run without the deletions and with names: words Â, B̂ whose letters are the stones read so
far (named 0, 1, …) and owed letters. They differ from α, β only by the d deleted named stones at the front, so the
run can be replayed, and at the end no owed letter is left: Â and B̂ are orderings of the stones 0..n−1. Put stone j
in the row given by its place in Â and the column given by its place in B̂. Later steps only replace an owed letter
in place or append at the end, so the number of letters before stone j never changes: its row is d + p_α and its
column d + p_β with d = j − m, and row + column = 2(j − m) + e_j + 2m = e_j + 2j. So the stones are on the lines of D
(distinct, as e is valid): a solution. Give stone j the chain X chosen at step j. Owed letters X are created only
in a block u in front of a stone appended at the end, so they stand after every named stone of X; a new stone of X
takes the first owed X, or goes to the end when there is none. Hence the stones of X appear in Â and in B̂ in the
order of their names: X is increasing in rows and columns. The two constructions are inverse to each other. ∎

**Checked** (`m3.py`): for every valid word the set of permutations rebuilt from all accepting runs equals the set
of all solutions with at most w chains from the complete search `sol3.cpp`: w = 2, n ≤ 10 (1,486 words at n = 10);
w = 3, n ≤ 9 (490 words, 8,439 solutions at n = 9); w = 4, n ≤ 8. No disagreement. (The program also names chains in
order of first appearance and bounds the owed stones by the stones left; neither changes what is accepted.)

For w = 2 this accepts the same words as the two-partition machine of `agents/blocks/m2.py` (both are exact; m2.py is
checked for n ≤ 9; `two.py` is that machine written with the numbers owed, `two_check.py` checks it for n ≤ 10).

**Tight cuts (proved).** At a cut of slack 0 no pair is incomparable across the cut, so every solution is a direct
sum there and the least number of chains of a word is the largest over its tight-cut pieces. 3C needs a proof only
for words with no tight cut.

## 2. The lead "two chains + one stone" is false at n = 14

G = valid words with no letter ≥ 2 before a letter ≤ −2.

**Claim tested.** Every word of G has a solution that is two chains plus one stone.
**Result.** True for n ≤ 13 (as in blocks NOTES §4). **False at n = 14**: of 35,543 words of G, 28,090 have two
chains, 7,444 need exactly one extra stone, and 9 need two:

    1 1 0 0 1 1 0 −1 1 0 −1 0 −1 −2        1 1 1 1 0 −1 −2 1 0 0 1 0 −1 −2      1 1 1 1 0 −1 −2 1 1 1 0 −1 −2 −1
    1 1 1 1 0 −1 −2 2 1 0 −1 −1 −1 −1      1 1 1 1 0 −1 1 0 −1 1 0 −1 −2 −1     1 2 1 0 −1 −1 −1 2 1 0 −1 −1 −1 −1
    1 2 1 0 −1 1 0 −1 1 0 −1 −1 −1 −1      2 1 0 −1 0 0 −1 2 1 0 −1 −1 −1 −1    2 1 0 1 0 −1 1 0 −1 −1 0 0 −1 −1

None has a tight cut. Each has two or three separate local peaks of the slack, of heights 3 or 4.
Independent check: `agents/blocks/third.cpp` gives "smallest third chain 2" for the first word.
So one extra stone is not enough on G. Guess (not tested): the number needed grows with the number of peaks.

**LEAD (tested).** Every valid word with letters in {−1, 0, 1} has a solution that is two chains plus one stone:
complete for n ≤ 16 (n = 15: 30,372 words, 1,005 without two chains, all 1,005 with one extra stone; n = 16: 72,832
words, 2,996 without two chains, all 2,996 with one extra stone, `out_one_16_pm1.txt`). n = 17 was started and
stopped unfinished at the ten-minute limit: not checked. The 9 words above all contain a letter ±2.

## 3. Rules for the extra stone: all fail

F = words of G with no two-chain solution (4, 22, 80, 262, 821, 2,496, 7,453 words for n = 8..14). For a solution
that is two chains plus a stone x: x has k stones incomparable to it on earlier lines and k + (letter of x) on later
lines, and deleting x leaves a two-chain solution of the word obtained by deleting the letter of x, lowering the
earlier ones by 1 and raising the later ones by 1 (`extra.py` prints all of these for one word).

**Peak zero (proved).** In every valid word the letter after the first cut of greatest slack is 0. (At that cut t
the next letter is ≤ 0; if t > 0 the letter before is > 0 and letters drop by at most 1; if t = 0 the first letter is ≥ 0.)

| rule: the extra stone can be chosen as … | holds | smallest counterexample |
|---|---|---|
| the stone on the first or last line | no | n = 8: 1 1 0 0 1 0 −1 −2 |
| the first largest letter | no | n = 8: 1 1 0 0 1 0 −1 −2 |
| a stone next to a cut of least slack (cuts 1..n−1) | no | n = 8: 1 1 1 1 0 −1 −2 −1 |
| a stone with at most 2 incomparable stones | no | n = 8: 1 1 1 1 0 −1 −2 −1 |
| a stone with at most 3 incomparable stones | n ≤ 10 | n = 11: 1 1 1 1 1 1 0 −1 −2 −1 −2 |
| a stone next to a cut of greatest slack | n ≤ 12 (not run further) | |
| Z1: the first zero between two cuts of greatest slack | n ≤ 9 | n = 10: 2 1 0 −1 1 0 −1 0 −1 −1 |
| Z3: the last such zero | n ≤ 9 | n = 10: 1 1 0 1 0 −1 1 0 −1 −2 |
| Z2: some zero between two cuts of greatest slack | n ≤ 12 | n = 13: 1 1 1 1 1 0 −1 −1 1 0 −1 −2 −1 (2 of 2,496 fail; there the zero at the second, lower peak works) |
| Z4: Z2 with the incomparable stones = nearest neighbours in line order | n ≤ 10 | n = 11: 1 1 0 1 0 0 1 0 −1 −2 −1 |
| Z5: some zero at a local peak of the slack | n ≤ 13 | n = 14: 21 of 7,453 fail (9 of them have no single extra stone at all) |
| Z6: some stone with letter 0 | n ≤ 13 | n = 14: 13 of 7,453 fail (same 9, and 4 more) |

So up to n = 13 the extra stone can always be a zero at a local peak of the slack (it then has equally many
incomparable stones before and after), and this is the best rule found; it has no proof and dies at n = 14.

## 4. Canonical three-chain solutions: failed rules

| rule | smallest counterexample |
|---|---|
| R1: the lexicographically smallest solution (row by row) has ≤ 3 chains | n = 8: 1 0 2 1 0 −1 −2 −1 |
| R2: the lexicographically largest solution has ≤ 3 chains | n = 7: 2 2 1 0 −1 −2 −2 |
| R4: corner rule: some solution is (two-chain solution) + (a block of c neighbouring rows in a corner), i.e. D minus the c central lines n−c, n−c+2, …, n+c−2 has two chains | n = 6: 2 1 0 0 −1 −2 |
| R5: some three-chain solution whose third level (stones with an antichain of two up-left of them) is one block | n = 9: 3 2 1 0 0 0 −1 −2 −3 |
| R6: some three-chain solution with stones in at most three places (values of column − row) | n = 4: 1 0 0 −1 |
| online colouring for two chains: the chain of a stone is a function of the letters read so far | 1 1 0 −1 −1 needs the first two stones in the same chain (runs AABAA, BBABB only); 1 1 0 0 −1 −1 needs them in different chains (ABAABA, ABABAB, BABABA, BABBAB only) |

R3 (some solution with the fewest blocks has ≤ 3 chains) holds for n ≤ 9, as in blocks NOTES §5; no rule comes from it
(for the staircases with k = 2 the fewest-blocks solutions have 2, 5, 5, 5, 5, 7 blocks for j = 1..6).

**Staircases S(k, j) = k … 1 0^j −1 … −k** (`stair2.py`, k ≤ 8, j ≤ 12; two chains decided by the machine `two.py`,
which agrees with the complete search `sol3` on the 54 pairs with n ≤ 16). Two chains exist exactly for:
k = 1: every j; k = 2: j = 1, 4, 5, 7..12; k = 3: j = 1, 6, 8, 10, 11; k = 4: j = 1, 8; k = 5: j = 1, 9; k = 6: j = 1, 11;
k = 7: j = 1, 12; k = 8: j = 1. For 45 of the 96 pairs no corner size works (R4 fails).
Correction to `agents/patterns/REPORT.md` ("j ∈ {2, 3, 5}: never two"): false for k = 1 and for (k, j) = (2, 5),
solved with two chains by 3 4 5 | 1 | 7 8 9 | 2 | 6; true for 3 ≤ k ≤ 8 and for (2, 2), (2, 3).

**Two explicit families (proved; `fam.py` checks k ≤ 25).**
- S(k, 1): rows 0..k to columns k..2k, rows k+1..2k to columns 0..k−1. Lines k, k+2, …, 3k and k+1, k+3, …, 3k−1:
  exactly the lines k + j of the word. Two blocks, two chains.
- S(k, (k+1)/2) for odd k = 2b+1 (n = 5b + 3, c = b + 1): five blocks
  rows 0..b → columns c+b.., rows b+1..2b → columns c.., rows k..k+b → columns c+k+b.., rows k+b+1..2k−1 → columns c+k..,
  rows 2k..2k+b → columns 0... Their lines are k, k+2, …, 2k−1; k+1, …, 2k−2; 3k, 3k+2, …, 4k−1; 3k+1, …, 4k−2;
  2k, 2k+2, …, 2k+2b: the lines of the word. Blocks 1, 3 form a chain, blocks 2, 4 a chain, block 5 a chain.
  For k = 5 this is the picture 6 7 8 | 4 5 | 11 12 13 | 9 10 | 1 2 3.
These are isolated families; no formula for general (k, j) was found (the corner sizes that work are irregular).

## What is still open

- A description of the words accepted by M_2 (item 2 of the task): not obtained. The peak zeros of §3 and the 9 words
  of §2 suggest that the obstruction sits at the peaks of the slack, one extra stone per bad peak.
- A proof for letters in {−1, 0, 1} (two chains + one stone, §2 LEAD).
- Any rule for the words α, β of M_3; the machine is exact but nondeterministic (choice of X, u, u′).

## Recheck (each under 10 minutes; run in `agents/chains3/`)

    g++ -O2 -o sol3 sol3.cpp
    python3 m3.py check 3 9          # Theorem 1, w = 3: 1.5 min
    python3 m3.py check 2 10         # w = 2: 6 s
    python3 m3.py check 4 8          # w = 4: 2.5 min
    python3 two_check.py 10          # two-chain machine in owed-number form: 6 s
    python3 one.py 14                # §2: the 9 words, 1.5 min
    python3 one.py 15 pm1            # §2 LEAD at n = 15: 20 s;   python3 one.py 16 pm1: 2 min (out_one_16_pm1.txt)
    python3 extra_rules.py 12        # §3 first five rows: 5 s
    python3 peak.py 13               # §3 Z1..Z6: 25 s;   python3 peak.py 14 14: 1.5 min (out_peak_14.txt)
    python3 extra.py 1 1 1 1 1 0 -1 -1 1 0 -1 -2 -1     # every 'two chains + one stone' solution of one word
    python3 rules.py 9               # §4 R1..R6
    python3 stair2.py 8 12           # staircases: corner sizes (0 = two chains)
    python3 fam.py 25                # the two explicit families
