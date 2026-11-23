# Bounded letters (working notes, Devin 2026-11-23, second session)

Class L_c: valid words with every |e_k| <= c, i.e. scores s_k within c of the transitive scores k-1
(b_k = 2k + e_k). Slack is unbounded in L_c (e.g. +^a 0 -^a has slack a), so this is not covered by slack <= 16.

Findings so far (all small computations, scripts letters*.py):
- c = 1: the summary (sigma, last letter) carries an inductive family for every B tried (B <= 9, letters.py 1 9 1);
  for c = 2 and c = 3 a window of 1 or 2 letters fails from B = 5 (so the cap on letters alone does not help for c >= 2).
- c = 1: the determinised automaton has only about 7 new states per extra letter (letters_dfa.py 1 12): reachable
  sets are almost all pairs of partitions; after a letter -1 every pair is reachable for sigma <= 5.
- c = 1: there is a family F(sigma) depending on the slack ALONE with F(sigma+e) inside step_e(F(sigma)) for
  every letter e in {-1,0,1} in any order (letters_sigma.py 1 8: sizes 2,4,8,12,24,48,80,126 of 2,5,10,20,36,65,110,185).
  If F can be described and the backward step proved by hand, this proves the conjecture for L_1 (unbounded slack).
  Backward step = remove a row r' and column c of the state with r' + c = 2k + e; must land in F(sigma - e).
- Hand transitions (time k, rows R' and columns C as sets; (1^p) = one hole at depth p, (q) = one far stone at k+q):
  ((1^p),(q)) -0-> ((1^(p+1)),(q-1));  ((1^p),0) -e-> (0,(p+e));  ((1^p),0) -(+1)-> ((1^(p+1)),0);
  (0,(q)) -(-1)-> (0,(q-1)).  The witness of +^a 0 -^a is two cycles: rho = (1 2 ... a+1), gamma = (a+1 2a+1 2a ... a+2).
- F(sigma) in arm|leg form (letters_F.py 1 9 6): no simple description found yet. The number of advanced lines
  (rows + columns ahead of k) needed inside F grows with the slack: at most 2 works only up to slack 6, at most 3 up to
  slack >= 10 (letters_Fclass.py 1 10). So a hand description must be a family whose complexity grows with sigma.
- F(sigma) = states reachable after EVERY prefix of slack sigma = boards (R', C) that are solvable for every
  b_1..b_k with b_j in {2j-1, 2j, 2j+1}. It contains the one-hole boards ((1^p), 0) and one-far-stone boards ((p), 0):
  that part is the G1 claim (one deleted column) restricted to L_1, where G1's extra condition
  sigma_j >= j+1-h holds automatically because letters are <= 1.
- Idea not yet tested: build witnesses of + M - (M a Motzkin word) from a witness of 0 M 0 (direct sum with two
  corner stones (1,1), (n,n)) by a zigzag chain: the stone that is one short is moved up one row or right one column,
  pushing the stone there down/left, until the shortage reaches stone n. For + 0^m - this gives P_n's two witnesses.
  The deterministic alternating chain is injective on (stone, parity), so it cannot cycle in the static picture;
  the open point is stones visited in both parities.
- Chord picture (pair sums): points 1..2n, stone k is a chord {g-h, g+1+h} centred on the gap g = b_k - 1.
  Conjecture = for every Landau set of n gaps there is a perfect matching of the points whose chords are centred on
  exactly those gaps. L_1: stone k uses gap 2k-2 (-), 2k-1 (0, inside the home pair {2k-1,2k}) or 2k (+).
  A chord that no other chord crosses can be deleted: chords inside or spanning it shift their centre by 1,
  chords to the right by 2. Insertion at a gap is the reverse; which chords span the gap depends on the witness,
  so this gives an induction only with control over spanning chords (not found).
- Ansatz that fails: rho(k) = k+1 on every +, gamma(k) = k-1 on every -, zeros absorb the rest (z-m, z+m).
  It reduces to matching zeros z with a +run start t and a -run end t' with t + t' = 2z; fails for + 0 0 - (P_4),
  whose witnesses alternate the side that moves (dominoes). The side must be chosen per letter.
- For c >= 2 the letter cap alone does not help: (sigma, last 1 or 2 letters) fails from slack 5 (letters.py 2 9 1 2).
  L_1 is special because every order of letters is legal there (it sits inside 'each diagonal at most twice').
- letters_ansatz.py 11 (all L_1 words, any letter order, n <= 11; every one is solvable):
  * ansatz A (+ stones at (k+1,k)/(k,k+1), - stones at (k,k-1)/(k-1,k), zeros free) fails first at + + - - and
    for most words from n = 9 on: stones must leave their home cell by more than 1.
  * smallest m such that some witness keeps every stone within m of its home cell (k,k) in both coordinates:
    m <= 1 for exactly 2^(n-1) words (n <= 11), m = 3 first needed at n = 8 (1 word), 248 words at n = 11.
    Fixed m gives a regular language (finite window), so m must grow with the height of the word.
NEXT (not done): put an 'L_1' card on the map (open; lead: slack-only family F, order-free), characterise the
2^(n-1) words solvable with displacement <= 1, look for the rule that says how far a stone must move (height of the
word at k?), and test the zigzag-chain induction + M - from 0 M 0.

## LEAD: zigzag-chain induction for L_1 (letters_zigzag.py 10)
w = + M - (length n; M any word in -1,0,+1 with prefix sums >= 0 and total 0, tight cuts allowed).
Take ANY witness of M on rows/columns 2..n-1 and add corner stones (1,1), (n,n). Run the alternating chain
(row, column, row, ... or column, row, column, ...): the stone that is 1 short moves up one row / right one column
and pushes the stone there down / left; stop when the pushed stone is stone n.
Result: for n <= 9 the chain ends on stone n (so gives a witness of + M -) from EVERY witness of every M (with one of
the two starts); n = 10: from every witness for 322 of 323 words, and from some witness for all 323.
Since every L_1 word is a concatenation of blocks + M - and zeros at height 0 (direct sums), a proof that the chain
always ends on stone n (for a suitable class of witnesses closed under the chain) proves the conjecture for L_1
by induction on n. Static argument so far: the chain map on (stone, parity) is injective and the start has no
preimage, so it cannot cycle as long as no stone is visited in both parities; it can only stop in row n or column n.
TODO: find the n = 10 exception (which witness, why), and the class of witnesses that is closed.

## Follow-up on the zigzag chain (same session)
- The n = 10 exception: M = + 0 - + + 0 - -, 4 of its 8 witnesses. From them the chain returns to its start (a true cycle of
  28 moves, leapfrog.py); it never gets stuck at the border.
- Closed class K (direct sums + chain results only, letters_closed.py 13): NON-EMPTY for every word with n <= 13
  (41,835 words at n = 13); the chain closes into a cycle in 1,096 of about 200,000 runs, never for all members of K.
  (A first run reported K empty at n = 11; that run stopped the chain as soon as a stone was marked twice in the same
  mode, which is not a cycle. Corrected.)  So 'use the witnesses the induction built' survives as an induction.
- Static version (letters_static.py 11): in the picture of one witness, follow row-neighbour / column-neighbour edges
  alternately from stone 1; this walk always ends at stone n, and if it visits no stone twice it gives a witness of + M -.
  For every M with n <= 11 SOME witness of M has such a simple walk; no extremal witness (least displacement, fewest
  inversions, lexicographic) always does.
- Witnesses of small L_1 words are mostly products of rotations of intervals in rho and gamma (letters_wit.py).
  Chains 'gamma rotates [p,q] forward, rho rotates [q,r] backward, ...' only give words whose valleys at height h hold
  exactly h zeros, so the general construction must nest.
- Smallest slack-only family (letters_min.py 7, integer program): 1, 2, 4, 8, 10, 16, 32 states for slack 0..6; it is
  forced up to slack 3 and has no visible pattern. A hand description of F looks out of reach.

## Leapfrog graph (proved; leapfrog_check.py, leapfrog_cycles.py)
State: a permutation matrix on [n]^2 (coordinates r' = n+1-r and c) with one marked stone.  R: swap the marked stone's
row with the next row, the mark stays in its row (so it passes to the other stone).  C: same with columns.
R and C are involutions (where defined) and keep the multiset {r'+c, with the marked stone counted as r'+c+1}.
So for a multiset b* of n targets with total n(n+1)+1, the states with that multiset form a graph X(b*) of
alternating paths and cycles.  R is undefined iff the mark is in the last row, C iff it is in the last column.
LEMMA. Let D be valid of size N = n+1 with largest diagonal N-2 (last letter -1) and b* its other n targets.
Witnesses of D <-> states with the mark in the last row or column (put stone N at (n, n+1) or (n+1, n) and pull the
stone of row n+1 / column n+1 back by one).  Hence W(D) = 2 * (number of path components of X(b*)), and
D is solvable iff X(b*) has a component that is not a cycle.  Checked N <= 8.
X(b*) is the union over j of the witnesses of b* - delta_j (one stone one diagonal lower), so by induction it is
non-empty; what is missing is that not every component is a cycle.
- 'X(b*) has no cycles' is FALSE: none for N <= 9 (2031 paths at N = 9), 8 cycles against 12216 paths at N = 10
  (4 words, first + + 0 - + + 0 - - -).  The zigzag chain above is this walk started from 0 M 0.
- Parity: the reflection r' <-> c maps X to itself, swapping R and C, with no fixed edge; so an odd number of symmetric
  states forces a path.  With distinct diagonals symmetric states need every stone on the reflection line, so this only
  proves the P_n-like words 0..0 + 0..0 -.  With repeated diagonals the count is a Langford-type matching count.
- Signs: every move flips the sign of the permutation, so a path between two last-row ends has odd length and its two
  witnesses have opposite signs (this is how the signed count can vanish).

## Chirality of the chain (letters_chir.py, letters_canon.py, letters_pos.py)
Each block + M - is built by a chain whose first move is R or C (the two directions of one leapfrog path, so both work
or both loop).  Whether the NEXT chain loops depends on these choices in a clean way in small cases:
  + (+0-)(++0--) - : loops iff the two inner blocks have the SAME outer choice (4 of 8);
  + (+0-) 0 (++0--) - : loops iff they have DIFFERENT outer choices; inner choices never matter;
  + (++0--)(+0-) -, + (+0-)(+0-)(+0-) -, + (+0-)(+++0---) -, + (+00-)(++0--) - : never loops.
One fixed rule for all blocks fails: always R (first failure n = 10), alternate by nesting depth (10), by parity of the
block's start position (11), end position (12), length (10).  So the induction needs a choice that looks at the
neighbouring blocks; the class K of all choices is non-empty for every word with n <= 13.
NEXT: find the rule (which pairs of blocks interact, and with what parity) and prove 'half of the choices work'.

## Parity does not help (one-off count, n <= 9)
W(D) is even for every D except the evenly spaced one (reflection r' <-> c has no fixed witness), and is usually
divisible by a high power of 2: at n = 9 the 2-adic valuation of W over no-tight-cut D ranges from 1 to 7.
So 'the number of paths is odd' is false in general, and no parity count of ends can prove a path exists.
The high powers of 2 fit the chirality picture: independent binary choices per block.

## Transfer graph, general D (transfer.py, lastrow.py)
The leapfrog graph X(c) is defined for any multiset c of n targets with total n(n+1)+1, and it is the disjoint union
over k of the witnesses of c - delta_k (mark on stone k).  So for a minimal move D -> D' = D + delta_i - delta_j the
witnesses of D (mark i) and of D' (mark j) are vertices of the same graph X(D + delta_i).
- 'Every component of X(c) meets every solvable c - delta_k' is FALSE from n = 5 (transfer.py 5 -v:
  c = (4,5,7,7,8) has four paths, none of which sees all four labels).  So a walk from a given witness of D need not
  reach a witness of D'; only the corner case of the zigzag chain (mark must end on the top stone) is automatic.
- Ends of X(c) are the states with the marked stone in the last row or column.  So with T(D) = set of stones that sit in
  the last row in some witness:  for w = u - (last letter -1),  T(w) minus the top stone = { k : k in T(u - delta_k) }.
  T(D) is always a top segment of the stones and contains the top stone (lastrow.py, n <= 8).  This is the existing
  card G1 (one missing column) seen from the walk: 'k in T(D)' is 'the other stones fit the board without row n and
  column b_k - n', and G1 says the sum test decides that.  The recursion above is G1's corner peel, nothing more.
  (I re-ran one-gap boards before finding G1 / edgepeel / sum2 in state.md: same answers, nothing new.)

## Rounds lemma (proved) and scattering (letters_pass.py, letters_trace.py, letters_scatter.py)
M = U_1 ... U_k (units: a single 0 or a block + M' -), ANY witness of each unit, direct sum between corner stones
U_0, U_{k+1}; I_i = rows = columns of U_i.
Invariant: below the marked unit, each boundary has exactly one pair of neighbouring lines exchanged (the two rows
or the two columns at the boundary); above it nothing has moved.  So a move is internal, or goes up (exchanging the
two lines at a boundary), or goes down (undoing that exchange, hence by the same kind of move as the last way up).
Retracing: when the mark comes down into U_{j-1}, nothing in U_{j-1} or below has moved since the mark left.  The
stone that receives it is the one that passed it up, back in its earlier place; its next move is of the kind by which
it first received the mark; that move is an involution, so it undoes the earlier one; and so on down to stone 0.
=> a run is a sequence of ROUNDS, started alternately by R and C at stone 0.  In a round the mark climbs unit by
   unit; a unit either transmits (hands the mark up, by R or C) or reflects (sends it back; then everything below
   is restored, the unit itself has changed, and the next round starts).  Reflection on a given entering move is an
   involution on the unit's positions.  The run loops iff the rounds return to the starting position.
Scattering table of a unit between two corner stones, entry R / entry C  (T = through, with the move handed on):
  0: TC/TR     + -: TC/TR     + 0 - (rows first): TC/TC, (columns first): TR/TR     + 0 0 -: TR/TC
  + + 0 - - (rows first): TC/F or TR/F, (columns first): F/TC or F/TR      (letters_scatter.py 7 -v for the rest)
This explains every loop seen: e.g. (+0-)(++0--) loops iff both blocks have the same first move.
- No simple algebra: for + 0^k - the entering mark visits every third stone (k = 9: stones 2, 5, 8, 11 or 1, 4, 7, 10 of the block),
  so the behaviour depends on k mod 3 and on parities; a block's behaviour is 'a second mark crossing the trail of
  the first', and deeper nesting means more trails.
- Witnesses in K that reflect both moves exist from block length 10 (914 of 200,391 up to length 13).
- PASSING CLAIM (open, true for all 9,360 blocks of length <= 13): every block has, for each entering move, a witness
  in K that transmits it.  (By the transpose symmetry of K: some witness transmits some move.)  With the rounds
  lemma: choose the units bottom-up so that each transmits what reaches it; round 1 succeeds; so K is never empty.
- RED: 'a loop is cured by replacing one block witness by its sibling (same inside, other first move)': true for
  n <= 14, false at n = 15, M = (+0-)(++0--)(++0--), all rows-first, for one of the two insides of the second block
  (letters_flip.py 16: 138 of 42,052 loops).
