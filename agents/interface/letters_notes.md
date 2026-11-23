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
