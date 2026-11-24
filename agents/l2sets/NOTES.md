# l2sets working notes (in order of discovery)
Task (parent, 02:12): same kind of proof as agents/l1sets/REPORT.md for letters in {-2..2}, and a statement uniform in the letter bound c.
Branch devin/1795457539-l2sets off devin/1795444188-two-marks. Report agents/l2sets/REPORT.md (HIT/NOTHING), do not touch map/build.py, docs/state.md.
Parent's finding: agents/universal/types.cpp with LET=lo,hi; blocks (run of letters outside {0,1} + closing letter 0 or 1 = one step),
type = (slack, last letter, final non-increasing run of <= c+1 letters): family exists for [-2,2] with window 3 (bounds 12..28; 13 types per slack),
for [-3,3] with window 4 (bounds 12,16,20). Windows one shorter fail. `LET=-2,2 KLO=0 ./types 20 A2K` (4 s), `LET=-3,3 KLO=0 ./types 16 A3K`, add `sizes` or `dump`.
Items: 1. c = 2: describe the 13 sets per slack (class conditions + what the last run forbids, e.g. M subset B+1 after a 2), prove step relations incl. blocks 2^a 1
and negative runs; smaller describable family fine; or exact F(x) description like L1 §4 (better route).  2. c = 3, uniform in c; what must a general type remember.
3. Re-read L1 proof; fix steps needing more detail in agents/l1sets/REPORT.md.  Small computations. Stop when proof for c = 2 or clear statement of what blocks it.
Tools: agents/l1sets/l1.py (machine on (lam, nu = mu'), M = M(lam), B = M(nu); e-preds: k in M, k+1-e not in B; t_k = ((M\k)+1, (B u {k+1-e})-1); classes c = a+b),
agents/weights/maya.py (bitmask machine), agents/l1sets/fam.py (gfp, step on bitsets).
- General letter e, state u = (M, B) of class c = a + b (as l1sets): e-preds k in M, k+1-e not in B.
  e = 2f even: preds with k even have class 2 - c, at least c - f of them; k odd: class -c, at least 1 - c - f.   (e = 2: c - 1 and -c;  e = -2: c + 1 and 2 - c)
  e = 2f+1 odd: all preds class 1 - c; k even at least a - b - f, k odd at least b - a - f.
  Forward: even letters act on classes like 0 (c -> -c or 2 - c), odd letters c -> 1 - c.  No 2-pred iff M subset B + 1.
  Central states with no CENTRAL 2-pred: c = 0: M_odd - 1 = B_even (2-quotient condition, a big set); so no slack-only central family.
- fx2.py C S J (first version): "F(x'w) = step_w(Sat(Gamma(x')))" (saturation j letters back) holds for L1 (110 of 114 nodes at j = 1), but for L2 only 508 of 819 nodes at j = 3
  (bound 9): after 2 2 2 2 the set is far from class-saturated and zeros heal slowly (0 0 0 after 2 2 2 2 1: defect 10 at slack 9). So NO description of the L1 §4 kind (class set + last few letters).
- keys.py 2 10: 500 distinct (F, slack) for L2 at slack <= 10 (L1: 44 at slack <= 12); F(x) is NOT a function of (slack, Gamma, last 5 letters) (335 ambiguous keys), nor of the last 6 letters.
  So the exact-description route of L1 §4 is closed for c = 2; only a sub-family indexed by types can work (parent's 13 types, block form).
- parent's gfp sets (LET=-2,2 KLO=0 ./types 16 A2K dump) are not class sets (e.g. J(2 1) at slack 3 = -|21 11|1 1|11 1|2 21|- 2|1 has classes 1 and -1).
- PLAN: own block-gfp in Python (blocks.py) with a restriction mask, to look for a DESCRIBABLE sub-family: (i) unrestricted (reproduce parent sizes), (ii) block ends inside Central,
  (iii) Central minus T, ... then read the sets in (M, B) / 2-quotient coordinates.  A direct family (empty state in J at slack 0; w solvable iff w 0 solvable) instead of the pair test.
- blocks.py 2 S WIN MASK (own block-gfp, reproduces parent's 13 sets; bound-independent): mask central -> family dies (first empty: slack 5 run (1) from slack 4 run (1 0));
  mask m2 (classes c in {-1,0,1,2}) works to 10 but sets stay complicated. fine.py: J sets are not unions of 2-core classes (164 of 435 split) nor 4-core (268 of 2271), 8-core nearly (11 of 5358, trivial).
  model.py: J(run) vs P(run) = run applied to ALL states: equal for small slack, then J much smaller (2 1: 30/58 at slack 6, 116/296 at 9). Binding prefixes are steep (2^a 1, 2 1 2 1 ..): Skolem-type sets.
- PARENT 02:19: TASK 0 FIRST. Memory depends only on the largest POSITIVE letter. Words with all letters <= 1 (negative letters of any depth, falling one at a time: a letter -k may only follow a letter <= -k+1):
  type (slack, last letter) carries a step-closed family (LET=-99,1 ./types 14 L0 WORKS; blocks: LET=-99,1 KLO=0 ./types 24 K, two sets per slack).
  Sets almost G(s): intersection over last letter has sizes of G; J(s, last = 1) = 2,4,8,14,24,48,80,128,212,332,512,774 (differs from G only at 4|s); J(s, last = 0) nearly everything.
  agents/l1sets/neg.py 13: G(s-k) inside step_{-k}(G(s)) for every k >= 3, s <= 13; for k = 2 except when 4 | s (2, 2, 4 states missing at s = 4, 8, 12).
  TASK 0: prove every valid word with all letters <= 1 is solvable; find G(s, l) = Central(s) minus exceptional set depending on last letter l <= 1 (or slack-only for steps <= -3 + repair for -2 at 4|s);
  extend Lemmas 1-5 to letters -k; say whether general -k is no harder than -2. Then continue c = 2.  ("letters in [-c, c]" should read "letters <= c".)
- (neg.py is not on origin/devin/1795444188-two-marks at 02:25; wrote own checks.)
- TASK 0 SOLVED (proof, short, on top of the L1 Theorem).  General count (window argument): letter e, u of class c = a + b:
    e = 2f: preds with k even: class 2 - c, >= c - f;  k odd: class -c, >= 1 - c - f.   e = 2f + 1: all class 1 - c; k even >= a - b - f, k odd >= b - a - f.  Total = 1 - e + |(B+e-1) \ M|.
  So a CENTRAL u has >= j + 1 central preds under -2j and >= 2j under -(2j-1): at least 2 for every letter <= -1.  And for every letter at most ONE pred is in E0
  (t_k in E0 => M \ k is a union of oe-pairs; two such k impossible).
  Family: after a last letter 0 / 1 (or the empty word): G(s) = Central \ T (L1).  After a negative last letter: G-(s) = Central(s) \ U(s), U(4m^2) = the (-1)-successors of A(4m^2+1)
  (<= 2 states, in E0; Lemma 5(a) of l1sets), U = empty otherwise.   G subset G-.
    letters 0, 1 from any type: L1 Theorem (source family contains G).
    letter -1 from any type: u central: >= 2 preds, all central; source G(s+1): 4 | s+1: none in SC, <= 1 in E0;  s+1 = 4m^2+1: all preds in A => u in U;  else T empty.
    letter -k, k >= 2 (previous letter is negative, source G-(s+k) = Central \ U, U subset E0): >= 2 central preds, at most one in E0.
  Uses "a letter -k, k >= 2, follows a negative letter" (true for distinct diagonals).  General -k is EASIER than -2.  Finite n: slack <= number of + letters still.
  TODO: neg0.py check (bitsets, bound 13) + solver for words with letters <= 1; then write §1 of REPORT.md; then L1 re-read (item 3); then c = 2 summary.
- neg0.py: check 12 ok (G-(s) = Central n step_-1(G(s+1)); G- step-closed under -k, k >= 2; G alone fails only for k = 2 at s = 4, 8, 12: 2, 2, 4 states = parent's numbers; counts for letters -6..2 ok);
  all 13: every valid word with letters <= 1 (distinct diagonals) of length <= 13 solved (9397 at n = 13); random 150 words length >= 250, slack to 181, letters down to -12: solved.
  (l1.preds needs more depth for letters <= -6: neg0 sets l1.depth deeper.)
- NEW COROLLARY (cut + mirror): (s|-) is in G(s) and (1^s|-) is in G(s) for every s >= 1 (central: c_0((s)) = [s odd]; not SC, not E0, not A). So for w = x y with all letters of x <= 1 and all letters
  of y >= -1: F(x) contains (s|-), A(y) = conj F(-rev y) contains conj(1^s|-) = (s|-).  ==> EVERY VALID WORD IN WHICH NO LETTER >= 2 PRECEDES A LETTER <= -2 IS SOLVABLE (any letters, any slack).
  Constructive (two half-solvers, mirror the second). TODO verify: in_G((s),()) and ((1^s),()) for s <= 300; brute force all such words n <= 10; random.
- So for c = 2 what remains: words with a 2 before a -2.  Cut after the last -2: y has letters >= -1, A(y) contains conj G(s) (large). Needed: (P2) every L2 prefix x ending in -2 has F(x) meeting
  Central(s) minus conj T(s).  Data (l1sets/out_l2_9.txt): intersection of F(x) over L2 prefixes ending in -2 is nearly everything (20/20, 36/36, 63/65 at slack 4, 5, 6).
- inter2.py 2 10: intersection of F(x) over L2 prefixes by last letter: after -2 everything (slack <= 5; 63/65, 108/110 at 6, 7 inside bound 10); after -1: 18/20 .. 274/300; after 0: ~70%;
  after 1: 4, 4, 8, 6, 12, 16, 34, 48, 118 states (slack 2..10); after 2: 3, 6, 6, 6, 6, 10, 12, 24, 54.  (s|-) is NOT in the intersections from slack 5-8 on.
- LEVELS (from the general count). gamma = c - 1/2, level m = max(c, 1 - c) = |gamma| + 1/2 (central = level 1), K = a - b.
  letter 2f: u has >= gamma + 1/2 - f preds of class 2 - c and >= 1/2 - gamma - f of class -c: guaranteed iff level >= f + 1, and then the pred is one level LOWER.
  letter 2f+1: >= K - f (k even) and >= -K - f (k odd) preds, same class: guaranteed iff |K| >= f + 1.
  So backward, a positive even letter consumes level, a positive odd letter consumes |K|; negative letters are free; level m needs slack >= m(m-1).
  A run 2^a backward would need level a + 1: impossible for long runs => the fragile predecessors decide, and their existence is a condition on the 2-QUOTIENTS (c = 0: some odd k in M with k - 1 not in B),
  i.e. on the next 2-adic level (4-cores).  Guess: letters <= 1 <-> 2-cores (L1 proof), letters <= 3 <-> 4-cores, letters <= 7 <-> 8-cores ("2-adic tower").
  TEST next: are the gfp sets J(type) for c = 2 "unions of 4-core classes minus thin"? (fine.py: histogram of the fraction of each 4-core class inside J.)
- fine.py histogram: gfp J(type) for c = 2 are NOT "4-core classes minus thin" (classes of size >= 4: 190 full, 178 miss 1-2, 264 middle, 38 has 1-2, 18 empty). The 2-adic-tower guess is not confirmed at the level of the gfp sets.
- neg0.py modes added: hooks S ((s|-), (1^s|-) in G(s): ok to 300); split N (all valid words, any letters, with no letter >= 2 before a letter <= -2: solved by two half-solvers, n <= 12: 5102 at n = 12;
  counts 19, 47, 116, 293, 753, 1952, 5102, 13430 of all 22, 59, 167, 490, 1486, 4639, 14805, 48107 valid words for n = 6..13; first word with both kinds of letters at n = 12);
  splitrandom 100 120 (letters -4..5, slack to 361: solved).
- WRITE-UP PLAN (REPORT.md): §0 general predecessor count (levels); §1 Task 0 theorem (letters <= 1) + corollary (no letter >= 2 before a letter <= -2) [HIT, proved];
  §2 c = 2: what remains = words with a 2 before a -2; (P2) at the cut after the last -2; data; why L1 route fails (keys.py, blocks.py central, fine.py, model.py); levels; [NOTHING on a proof]
  §3 c = 3 / uniform: what a type must remember; §4 L1 re-read: fixes made in agents/l1sets/REPORT.md.  runs.sh.  Then push + message parent.
