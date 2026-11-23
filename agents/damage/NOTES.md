# damage working notes
- Branch devin/1795465445-damage off two-marks. REPORT3 (young excess y) is only on origin/devin/1795458080-uniform-exc:agents/universal/REPORT3.md.
- oh.py copied from ../onehigh (G, Gm, preds, step, run, nm). d1.py SMAX "s0:W" : missing after W + tails, by deficiency d = s - longest row/column. d2.py prints the sets.
- Board picture of a backward chain: u = (M, B); going back through letters e_1 (last), e_2, ...: choose distinct beads m_i in M and distinct holes n_i of B
  with n_i - m_i = delta_i = 2i - 1 - e_i (increasing in i); the state i steps back is ((M - {m_j}) + i, (B + {n_j}) - i).
- Data (G(s0) start, W in {1,2}* ending in 1 with a twos, r = a - 1 = y after the first 0), counts by d: after W 0:
  r=0: d0:2 [(s|-),(-|s)];  r=1: d0:4 d1:2 [+ (1^s|-), (s-1,1|-), mirrors];  r=2: d0:4 d1:4 d2:10 (18 states, s0=5 W=2221, slack 12);
  r=3: d0:4 d1:4 d2:20 d3:10 d4:4 (42 states, s0=3 W=22221 slack 12, includes 822|-, 8|22).  Same counts for W = 2 1 2 1, 2 2 1 1 1.
  Sporadic extras at small s0 (s0=1,4 W=2221: 4 more; s0=0 W=22221: 21|321 survives zeros).
  after W 0 0: r drops by one. after W 0 1: r=0: 4 hooks; r=1: 8; r=2: 28.  after W 0 -1 (G-): y drops by 2: r=2 -> 4 states (s|-),(s-1|1),mirrors; r=3 -> 16.
- d3/d4: damage D = G(s) - step_{W0}(G(s0)) equals Loc = G(s) - step_{W0}(ALL states of slack s0) (no backward chain from any state), plus a few
  "parity extras" (chains exist but none ends central): 1|83, 1|8111 (s=12), 51|7, 3|91, 111|91 (13), -|77, 1|10.3 (14) for W = 2 1 2 2 1; none for 2 2 2 1.
  Loc for a = 4 depends on W (38 or 42 states).
- KEY PICTURE: backward chain of L letters from u = (M,B) = L non-attacking stones: beads m_i in M, holes n_i of B, n_i - m_i = delta_i = 2i - 1 - e_i (e_1 = last letter).
  End class (L even): c_w = c_u + #{i: e_i even, m_i odd} - #{i: e_i even, m_i even}.   For (s|-): one stone on the bead s-1, the others in the quadrant x >= 2, y >= 0, x + y = delta_i;
  Landau for the quadrant (drop stone 1) <=> every suffix of J letters of (prefix minus last letter) has sum <= J  <=> prefix minus last letter is OLD (REPORT3).  So y is the Landau excess of the corner problem.
- BUT y alone is not exact: a = 3: W 0 0 (y = 1) leaves 6, W 0 1 0 (y = 1) leaves 18.
- routeL.py: route L (level-2 0-predecessor) alone: fine for exit -1 (misses only -|44, -|66, 2222|22: 4 | s), but for exits 1 and 0 misses 56 and 140 states of G at slack 14/13 -> not a proof of (X).
- IDEA for theorem: cut at the last letter <= -2 (P2): need only F(x) meets conj G(s) there.
- CORRECTION: W 0 1 0 with three 2s leaves 6 (not 18; I misread the a = 4 line). (y, yhat, last) fits all counts so far (prof.py).
- THEOREM D (proved, any letters): u = (lam|mu) in F(p) => for all p_, q_ >= 0, k >= 1:  (sum of the k letters before the last t = p_+q_ letters) <= k t + sum_{i<=k} (lam_{p_+i} + mu_{q_+i}).
  Proof: j = t + k last stones; at most p_ of them on the top p_ beads of M, at most q_ on the lowest q_ holes of B; the other >= k stones have sum of delta >= sum_{i<=k}(h_{q_+i} - b_{p_+i}),
  b_i = lam_i - i, h_i = i - 1 - mu_i; the k largest deltas among the first j are those of stones t+1..j; sum = j^2 - t^2 - (E_j - E_t).
  Letters <= 2: only t = 0, 1 matter.  t = 1: violated iff lam_1 > s - yhat or mu_1 > s - yhat.  t = 0: near-columns, sum_{i<=k}(lam_i + mu_i) < E_k.
  Matches 2 / 6 / 18 exactly.
- landau.py (s0 = 4, len <= 8, slack <= 13, letters -3..2; s0 = 7 len <= 6): V = fam(s) n {violators of Theorem D for the suffix w} is ALWAYS inside D (as proved) and D = V for every word ending in a
  negative letter (all types) ; for words ending in 0, D = V except 0-12 extra states (2|411, -|55, 4|11111, 1|63, -|722, 21|521 ...).  Sizes |V| = 2, 6, 18, 38 for (yhat, last 0) = 1..4; 2, 4, 16 for last -1.
- PLAN: write REPORT: Theorem D + corollaries (proved), DAMAGE = V tested, block step / Theorem L2 NOTHING (route L misses 56/140 states; level families empty at low slack).
- ty.py: largest closed system by (s, y, last two letters), letters <= 2: nonempty at bound 10 but NOT G-minus-thin: y alone is too coarse.
- ind.py: induction "carry (G or G-) minus N_r" FAILS: (s-1|1) has only two 0-predecessors, (s|-) [never reached after x 2 1^j 0] and (-|2 1^{s-2}) (not central) -> families must contain level 2.
- lev.py (KEY): start = ALL states of level <= 2 at s0 (5, 6), letters -3..2, slack <= 12: Lev<=2(s) - step_w(Lev<=2(s0)) = V(w) EXACTLY for every word ending in a letter <= 0; also with CUT=1 (s0 = 6).
  Words ending in 1 or 2: many extras.  So the extras of landau.py come from starting at Central only.
- small.py: exact F from the empty word; extras only when a recent cut has slack <= 2, or at slack 9, 11: core pairs (d_a|d_{a+1}) are closed under 0-predecessors with no 2-predecessor (cores.py).
- d3.py, d4.py, routeL.py, ind.py, ty.py are exploratory and not in runs.sh.  Final statements: REPORT.md.
