# REPORT (draft notes; rewrite at the end)
Task (parent, 01:30): family L1 = words with letters in {-1,0,1}, any slack. Branch devin/1795455019-l1sets off devin/1795444188-two-marks.
Deliverable: agents/l1sets/REPORT.md (HIT/NOTHING, exact statements, ranges, recheck < 10 min), push branch, tell branch name, NO PR,
do not touch map/build.py or docs/state.md. Final message: 2-3 sentences: proved / only tested / not checked.
Items: 1 F(x) exactly for x in {0,1}* ("D-class, K-class, containment minus explicit family"?), then legal x in {-1,0,1}*; else a subset
G(x) <= F(x) with G(x e) <= step_e(G(x)) nonempty and containing the empty state at the end of valid words (would prove L1).
2 cut form: F(x) n conj F(-reverse(y)) nonempty at a well-chosen cut (last return to slack 0, or the maximum of the slack).
3 if L1 falls: what breaks for letters in {-2..2}.
Read first: agents/unimodal/REPORT.md (Theorem 2: {0,1}*{0,-1}* proved; parity theorem L_x(lam|gam) = C(s,|lam|) f^lam f^gam mod 2 for x in {0,1}*),
cards l1, zigzag, rounds in map/build.py (text only).
Tools from agents/weights: maya.py (Maya(smax): states(s), succ(t, e), name, part; dval(Mo, t, n) -> (D, K)), REPORT2 (Theorems 1-3: F(1^a 0^b)),
REPORT3 (Lemma 2 matching criterion: constant letter e run <-> bijection I -> J with sums e, e+2, ..; K conserved by even letters, D by odd letters;
zo.py: F(x) for x in {0,1}* is NOT parity-count set in general, e.g. 1 0 1^8 misses 80 of 292).
## Notes
- unimodal/REPORT.md read: Theorem 2 proof = parity: for x in {0,1}^m with s ones the counts at (-|1^s) and (-|s) are odd (L_x(lam|gam) = C(s,|lam|) f^lam f^gam mod 2),
  glue two halves. Counts are EVEN as soon as x has a negative letter, so parity gives nothing for {-1,0,1} prefixes with a -1. O(x) = odd states <= F(x).
  For 0/1 words (tested s <= 20) one inclusion-minimal F set per (slack, last letter). Tools there: uplus.cpp, par.py.
- TODO next: read cards l1, zigzag, rounds (grep in map/build.py), then compute F(x) for x in {0,1}* vs {D-class, K-class, containment} with weights/maya.py.
- cards read. l1 (empirical): all words n <= 11 solvable; inside slack <= 10 there IS a family Fam(sigma) depending on slack only with Fam(sigma+e) <= step_e(Fam(sigma)),
  sizes 2,4,8,12,24,48,80 (sigma = 1..7) (same sizes as U+ for {0,1}|{0,-1} in unimodal §4), needs 3 advanced lines from slack 7; no description found.
  For {-2..2}: slack + last two letters fails at slack 5. zigzag (disproved at n = 10), rounds (proved, structure of the chain). Do not redo leapfrog chains.
- PLAN: (a) l1sets/fl1.py using ../weights/maya.py: for all x in {0,1}^n (n <= 12) compare F(x) with C(x) = {D in allowed set, K in allowed set, containment};
  look at the missing family (expect (lam|lam')-type after last letter 1, Theorem 1/2 families). (b) the common core of F(x) over all L1 prefixes of slack s
  (the slack-only family of card l1): describe via D, K, Maya diagrams; sizes 2,4,8,12,24,48,80. (c) cut at max slack: F(x) n conj F(x') nonempty.
- fam.py (bound 6, 8, 10): the largest slack-only family G(s) = I(s) (intersection of F over all L1 prefixes) = P(s) (intersection over 0/1 words), sizes 1,2,4,8,12,24,48,80,126,212,332.
  ONLY 37 distinct (F(x), slack) for all L1 prefixes inside slack <= 10 (34 for 0/1 words)!! sets.py: F(x) = parity set {|D| <= E} (E = #zeros) minus 0..7 states,
  BUT |D| <= E is too weak a bound (1 0 1^8 has F = F(1^9), zero forced).  Right coordinates: a = c_0(lam), b = c_0(mu) 2-core charges
  (c_0(M) = #{even beads >= 0} - #{even holes < 0}); the pair of 2-cores IS the parity class: D = [n odd] + (-1)^n (a + b), K = (-1)^n (a - b).
  Step: filling an even hole a -> -a, odd hole a -> 1 - a. So c = a + b: odd letter c -> 1 - c; zero c -> -c or 2 - c.
  CONJECTURE to test: F(x) = {t : (a, b)(t) in Pi(x)} minus a small explicit family, Pi(x) = reachable pairs of 2-cores (slack-bounded walk).
- cores.py / auto.py (bound 10): HIT-shaped data. Every F(x) for L1 prefixes = Sat(s, Gamma) minus Ex, Sat = all states of slack s with c = a + b in Gamma
  (ALL core pairs with these sums), Ex tiny: after '+' Ex = {(lam|lam')} in Sat (no 1-predecessor); 1^4 0, 1^8 0: -|22 22|-, -|44 44|- (E^0 of REPORT2);
  ++++0+ : 2|111 11|3 3|11 111|2; ++++0+0: 2|111 111|2; after that nothing. Node ++++0 <-> ++++0+ under + and - (Ex persists on that 2-cycle).
  Exact by definition: Ex(xe) = {u in Sat' : all e-predecessors of u inside Sat(Gamma) lie in Ex(x)} (+ SC for e = 1).
- predecessors of u = (lam|mu) under e  <->  pairs of beads k in M(lam), k' in M(mu), k + k' = e - 2 (remove beads k+1, k'+1 from the diagrams shifted up).
  Counts by parity (A_0, A_1, B_0, B_1 = 2-quotient Maya diagrams, charges a, -a, b, -b):
   e = 0: k even: N_even = c' + |B_0' \ A_0| >= c', predecessor class c = 2 - c';  k odd: N_odd = 1 - c' + |..| >= 1 - c', class c = -c'.
   e = 1: k even N = (a - b) + |..|, k odd N = (b - a) + |..|; none iff mu = lam'.   e = -1: k even >= a - b + 1, k odd >= b - a + 1 (so >= 2 if a = b).
  Odd letters: c -> 1 - c always (all predecessors in one class). Min slack for class c: m(m-1) or m(m-1)+1, m = |c - 1/2| + 1/2.
- NEXT: bigger bound (12-14) to see all Ex types; then prove "Forced_e(B) subset of B'" for an explicit thin family B containing SC, with empty|empty never in it.
- auto.py 16 (1 s; 70 nodes): same picture to slack 16. Gamma always contains the CENTRAL class (c = 0 for s even, c = 1 for s odd; |gamma| = 1/2, gamma = c - 1/2:
  odd letter gamma -> -gamma, zero gamma -> -gamma +- 1, feasible iff m(m-1) <= s, m = |gamma| + 1/2).
  KEY: slack-only invariant family G(s) = Central(s) minus T(s) with T(s) = SC(s) u E0(s) for 4 | s (SC = {(lam|lam')}, E0 = REPORT2 family: -|44 44|-; s = 12: -|66 22|2222 2222|22 66|-),
  T(4) = {2|11 11|2 -|22 22|-}, T(5) = {2|111 11|3 3|11 111|2}, else empty  (matches sizes 1,2,4,8,12,24,48,80,126,212,332 and card l1's family).
  If G(s+e) <= step_e(G(s)) is PROVED for all s, L1 follows.  Obligations (central predecessors always exist: N_odd >= 1 - c', N_even >= c'):
   (+) into 4|s: u not SC has a predecessor, T(s-1) empty: trivial.   (+) out of 4|s: u in Central(s+1) needs a 1-pred not in SC u E0.
   (-) out of 4|s: u in Central(s-1) needs a (-1)-pred not in E0 (SC has no -1 successor).  (-) into 4|s: trivial.
   (0) at 4|s: u in Central minus T needs an odd-type 0-pred outside SC u E0 (at most ONE 0-pred is SC: M(mu_u) = (M(lam_u') - 2) + {q, q-1}).
  Coordinates (M, B = M(mu')): forward step = shift M down 1, B up 1, then a bead jumps from position k + 1 - e of B to the hole k of M. SC: M = B.
- HAND PROOFS so far (Maya coordinates (M, B), B = M(mu'); e-preds: k in M, k+1-e not in B; pred = ((M\k)+1, (B u {k+1-e}) - 1); SC: M = B;
  E0: M, B unions of pairs {2i, 2i+1} and M = (B-2) + one pair):
  (O2) PROVED: every state has >= 2 (-1)-preds (|M \ (B-2)| >= 2), none is SC, at most one is in E0 (M\k and M\j cannot both be unions of oe-pairs {2i-1,2i}).
  (O1): at most ONE 1-pred is in SC u E0 (case analysis on pairs). So only u with a unique 1-pred matter (|M \ B| = 1):
     unique pred in SC  => lam, nu 2-cores with adjacent charges, central only at slack 1.
     unique pred in E0  => pred t = (2 delta_i 2 | 2 delta_{i+-1} 2), slack 4(i+1)^2 = 4, 16, 36..  => ANOMALY T(s) nonempty expected at s = 5, 17, 37, ...
     (s = 5 seen: 2|111 11|3 3|11 111|2). Bound 16 cannot see 17: run bound >= 18 and print T(s) = Central minus G.
- tset.py 18 (3 s): T(s) = Central minus G: s=4: SC + {-|22 22|-}; s=5: 2|111 11|3 3|11 111|2; s=8,12,16: SC + E0 (2,4,5 states); s=17: 422|33111 3311|522 522|3311 33111|422
  (predicted by hand before running!); T = empty at all other s <= 18.
## PROOF PLAN (believed complete modulo write-up + checks) : THEOREM  F(x) >= G(s) := Central(s) \ T(s) for every legal L1 prefix x  ==>  L1 CONJECTURE for all slacks.
 Definitions (Maya coordinates u = (M, B), M = M(lam), B = M(mu'), both charge 0):
   forward letter e: M' = (M - 1) u {k}, B' = (B + 1) \ {k + 1 - e}   (k not in M - 1, k + 1 - e in B + 1);
   e-preds of u: k in M with k + 1 - e not in B, t_k = ((M \ k) + 1, (B u {k + 1 - e}) - 1).  #preds: e=1: |M\B|; e=0: |M\(B-1)| >= 1; e=-1: |M\(B-2)| >= 2.
   class c = a + b (2-core charges of lam, mu); odd letters: c -> 1 - c; zero: pred via k even has c = 2 - c' (N_even >= c'), via k odd c = -c' (N_odd >= 1 - c').
   Central(s): c = s mod 2.   SC = {M = B} (central only if 4 | s).   E0(s) (4 | s) = {M, B unions of pairs {2i, 2i+1}, M = (B - 2) + one pair} = states whose only central 0-pred is SC.
   A(4m^2+1), m >= 1: 4 states (P u {kappa}, P u {y}): P = pairs(Q) for a 2-core Maya diagram Q (delta_{m-1} or delta_m), {y, kappa} = the pair at (a top of Q) + 2
     = states whose only 1-pred is in E0 (that pred = (2 delta_i 2 | 2 delta_{i+-1} 2), slack 4(i+1)^2).  In (lam, mu') form: the two diagrams differ by ONE box.
   T(0) = empty; T(s) = SC u E0 (4 | s, s >= 4); T(4m^2+1) = A; else empty.
 Steps needed: every u in G(s') has an e-pred in G(s' - e). Central preds always exist (counts above; central SC only when 4 | s').
   (O1) + out of 4|s: at most one 1-pred of u is in SC u E0 [E0,E0: M\k, M\j both oe-pair unions impossible; SC,SC: M = (B-2)+{k-2,k} fixes k; SC,E0: loners argument].
        unique pred in SC => (core|core) adjacent charges, central only slack 1 (u = 1|-, -|1, pred = empty: fine).  unique pred in E0 => u in A (by definition of A). DONE
   (O2) - out of 4|s: >= 2 preds, none SC (SC has no -1 successor), at most one in E0. DONE
   (O3) 0 at 4|s: at most one central 0-pred is bad (SC: M = (B-2)+{k-1,k}; E0: needs k+1 not in M, so two E0-bad impossible; SC+E0: loner j-2). Unique central pred: SC => u in E0;
        E0 => Q subset Q', Q 2-core, and then M = B, u in SC. DONE
   (O5) - out of 4m^2+1: each a in A has exactly ONE (-1)-successor u_a (k = y - 1), u_a = ((P u pair) - 1, P + 1) in E0 (or SC for m = 1); so nothing new. DONE
   (O4) + out of 4m^2+1 and (O6) 0 at 4m^2+1: a successor u of a in A has >= 1 + (2i - 1) 1-preds (i = m-1 or m), resp. >= i central 0-preds ((P-1)\P has i elements p - 1, p odd => even => central type),
        more than |A| = 4 for m large; small m by a LOCAL computation (successors of the 4 states of A and their preds; no enumeration of all states). TODO write local.py, m <= 8.
   (+ into 4|s, - into 4|s, + into 4m^2+1, - into 4m^2+1, all other steps): trivial (T of the source empty, or by definition of T).
   s = 0: by hand.  Finite n: preds have slack <= n - 1 parts, real rows: fine.
 TODO: (1) check.py: explicit T(s) (structural definitions) == Central minus gfp G for s <= 18 or 20; verify each "at most one bad pred" lemma by brute force for s <= 14.
       (2) local.py for A(4m^2+1), m <= 8.  (3) write REPORT.md cleanly (theorem, proofs, exact description data for F(x): Sat(Gamma) minus Ex, automaton), runs.sh, push, tell parent.
       (4) item 3: what breaks for letters {-2..2}: letter 2 changes c non-deterministically? (even letter: c -> -c or 2 - c like 0) and states with no 2-pred are M(mu) = M(lam')+1 + one bead: bigger defect family; card l1 says slack + last two letters fails at slack 5. Quick test: is there a slack-only family for {-2..2}? (expected no).
- check.py 18 12 (4 s): structural T(s) (l1.in_T) = Central minus gfp G for all s < 18; l1.py machine = maya.py; lemmas O1, O2, O3 on all states slack <= 12: ok.
  local.py 8: A(4m^2+1) = 4 states for m <= 8 (slack <= 257), O4, O5, O6 ok; least number of 1-preds of a successor = 2m, of central 0-preds = m (m >= 2).
  Proof of O4 / O6 by counting: successor u of a = (P u kappa, P u y) has >= 2i >= 2m - 2 1-preds (P \ (P+2) = pairs(Q \ (Q+1)), i beads of the staircase) and >= i >= m - 1 central 0-preds;
  |A| <= 4, so m >= 4 (O4), m >= 6 (O6) by counting, smaller m by local.py.
  Hand derivations re-checked: O1 (SC,E0) via "M has exactly one loner j"; O3 unique pred in E0 => Q subset Q', Q' = Q + {k,k+1}, B = M (SC).
  Finite n: pred t has l(lam_t) + l(mu_t) <= slack(t) <= n - 1 (slack <= number of + letters), so it is a state with n - 1 stones.  s = 0 by hand.
  NOTE: the theorem covers ALL words in {-1,0,1} with slack >= 0, including the factor "+ -" (repeated diagonal); the card l1 family (distinct marks) is the subfamily without "+ -".
- TODO: solve.py = the proof as an algorithm (backward: from empty, choose any e-pred in G) -> explicit permutation; test all valid words n <= 12 + random long words with large slack. Then write-up.
