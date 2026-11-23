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
