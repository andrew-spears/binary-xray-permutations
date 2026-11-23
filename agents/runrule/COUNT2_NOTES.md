# COUNT2 working notes (branch devin/1795450551-del0-slack2, base devin/1795444188-two-marks; PR #8 merged)
Task (parent, 3 items): prove DEL0 N(x0y) >= N(xy) at slack-2 cuts; (1) explicit 3x3 forms + cone at slack 2;
(2) 'transpose one side' injection at slack 2 tested to n=10; (3) general slack: refinement by number of row holes
+ shift vs shift+transpose, mechanism behind 'row holes + col holes' at left cut for ZERO.  Deliver COUNT2_REPORT.md
(HIT = proof at slack 2 or precise finite statement giving it; else NOTHING), new PR into devin/1795444188-two-marks.

## Slack 2 algebra (derived from the folded matrices of gram/fold run, classes ((),(1,1)), ((),(2,)), ((1,),(1,)) in cone.part labels)
Per-state values: alpha = L(class ((),(1,1))) (each of its 2 states), beta = L(class ((),(2,))), gamma = L((1),(1)).
z = L_x, z' = L_{y*} (y* = y reversed and negated).  J swaps the classes alpha <-> beta, fixes gamma.
  N(x y)   = 2 alpha beta' + 2 beta alpha' + gamma gamma'
  N(x 0 y) = 2 alpha alpha' + 2 beta beta' + 2 beta gamma' + 2 gamma beta'
  D = N(x0y) - N(xy) = 2 p p' + 4 beta beta' - q q',   p = alpha - beta,  q = gamma - 2 beta      (Lorentz form, signature ++-)
SUFFICIENT for DEL0 at slack 2:  for every legal x at slack 2 with last letter <= 1:
  (i) alpha >= beta   (ii) 0 <= gamma <= 4 beta   [then p p' >= 0 and |q| <= 2 beta so q q' <= 4 beta beta'].
Known rays (alpha,beta,gamma): (1,1,0) x=(1,1); (3,1,2) x=(1,1,0,0); (3,1,4) x=(2,1,0,0,-1,0) [tight in (ii)]; (11,3,10).
x=(2) gives (0,1,1): violates (i) but is excluded (0 cannot follow 2).
TODO: test (i),(ii) on all prefixes (slack <= 10, length <= 12, last letter <= 1) with count_rule.cstep; identify which
concrete state is alpha/beta (rows used); by the slack-1 lemma the direction of L_x depends only on the tail since the last slack <= 1.
