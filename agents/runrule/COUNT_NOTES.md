# COUNT follow-up: working notes (branch devin/1795449449-countshape)

## 1. Class-by-class refinement (refine.py, brute force, canonical steps, n <= 10: 623 PEAK, 862 RUN, 746 ZERO)
Cuts: left = state after x, right = state before y, left-1 / right+1 = one letter further out.
Number of steps with a violating class (out_refine_10.txt):
- PEAK: 0 for every statistic except the full state (6 at left and at right, 0 at left-1 and right+1).
  In particular the ROW SIDE ALONE (lambda) works at all four cuts, and so do (|lam|,|mu|), hole counts, top extras, lowest holes.
- RUN: (|lam|,|mu|) and '#row holes only' work at all four cuts; (#row holes, #col holes) fails once at left/right;
  row side only fails (7); full state fails (21).
- ZERO: left cut: only '#row holes + #col holes' works. (|lam|,|mu|) fails at left-1 (1), left (6), right (10), works at right+1.
  '#row holes only' works at left-1, right, right+1 (fails 17 at left). Full state fails everywhere.
- n <= 9: first full-state failure of PEAK is (3,2,1,1,0,-1,-1,-2,-3) <- (3,2,1,0,-1,-2,-3).

## 2. Equality cases (equal.py, n <= 9; rerun at 10 for the report)
- DEL0 with slack 0 at the deleted 0 (tight cut): ratio 1 always (828/828) -- product structure.
- DEL0 with slack 1 at the 0: ratio EXACTLY 1 always (577/577).  PROOF: the slack-1 states are A = (box, empty),
  B = (empty, box).  From A (rows: hole at m, extra at m+1; columns 1..m, coordinates of the board, m stones placed)
  the only 0-stone (r + c = 2m+2) is (m, m+2), leading to B; symmetric from B.  So T_0 swaps A and B, L_x is
  transposition-symmetric, hence N(x0y) = N(xy).  Bijection: keep the stones of x, add (m, m+2), shift the stones
  of y by (+1,+1) and transpose them (reflect in the main diagonal).  [check the transposed-continuation step]
- DEL0 slack 2: ratio >= 4/3, never 1.  Slack 3: 24 of 216 have ratio 1, e.g. (2,1,0,0,-1,-2) <- (2,1,0,-1,-2). Slack >= 4: > 1.
- canonical ZERO: slack before v = 1: always 1 (79/79); 2: >= 4/3; 3: 11 of 72 equal 1.
- canonical PEAK: ratio exactly 2 iff slack before v <= 2 (78+85+29 of 192, all); slack >= 3: >= 2.57.
- RUN ratio 1.5 only for RUN(1,2), RUN(2,1) (10 of 74, 11 of 81), e.g. (1,1,0,1,0,-1,-2) <- (1,1,0,0,-1,-1).

## 3. Idea being tested: finite matrices per slack level
States of slack s = pairs of partitions of total size s (finite: 1,2,5,10,20,36,65).  T_0 and T_(1,0,-1) restricted to
slack s are finite matrices M_s, P_s.  With the mirror J (180 degree rotation, R_y(t) = L_{y*}(Jt)):
N(xvy) - N(xuy) = L_x^T G_s L_{y*},  G_s = (T_v - T_u) J.   COUNT <=> G_s >= 0 on the cone of reachable vectors.
Test: is G_s symmetric / PSD / low rank / a nonnegative combination of products of nonnegative functionals?
RESULT (gram.py 5): G_s is SYMMETRIC for DEL0 and PEAK at every s <= 5, indefinite (about half the eigenvalues
negative), full or nearly full rank -> no PSD / low-rank argument.  But G_s is entrywise >= 0 except for a FEW
entries equal to -1: DEL0: exactly dim(s) of them (1,2,5,10,20,36 -> the entries of -J not covered by T_0 J);
PEAK: 0, 0, 2 of 25, 8 of 100, 29 of 400, 60 of 1296.
PROOF SHAPE to test next: COUNT <=> sum_{t,t'} L(t) G_s(t,t') L'(t') >= 0 on reachable L = L_x, L' = L_{y*}.
Match every -1 entry (t,t') to +entries (a,b) and prove domination inequalities between counts,
L_x(t) <= L_x(a) (or sums), i.e. an order on states that the COUNT VECTORS respect (not the sets).
TODO: print G_2 (dim 5) for DEL0 and G_2, G_3 for PEAK with partition labels; list which inequalities
L_x(t) <= L_x(a) would suffice; test them over all prefixes x (slack <= 10, length <= 12) with count_rule.cstep.
Remaining plan: task 3 (formula side) only if time; then write COUNT_REPORT.md, commit agents/runrule/{countlib,refine,equal,gram}.py,
out_refine_10.txt, notes; PR into devin/1795444188-two-marks (new PR; PR #4 already merged).
