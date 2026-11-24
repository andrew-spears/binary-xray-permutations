# oddbridge: two smaller forms of BRIDGE, both false

Setting: `../l2sets/REPORT.md` (G, BRIDGE), `../hybrid/REPORT.md` (Theorem T). A middle is (s₁, m, s₂): m starts with a
letter ≥ 2, ends with a letter ≤ −2, s₁ and s₂ are the slacks before and after. Odd(1^s) = states reached by 1^s in an odd
number of ways; Odd′(s) = states from which (−1)^s finishes in an odd number of ways.

**HIT (disproof). BRIDGE-ODD is false.** Statement: step_m(Odd(1^{s₁})) ∩ Odd′(s₂) ≠ ∅ for every middle.
- Why it matters: every count of the padded word 1^{s₁} m (−1)^{s₂} with stones of m in fixed rows and columns is
  Σ_{u, walk, v} L(u) · L′(v) over the m-walks u → v allowed by the constraint. So an odd count exists iff BRIDGE-ODD holds
  for the middle. Where it fails, Theorem T with the padding 1^s cannot apply.
- Counterexamples: (0, 4 5 4 3 2 1 0 −1 −2, 16), n = 25 (smallest found); (0, 6 5 4 3 2 1 0 −1 −2, 18);
  (1, 6 5 4 3 2 1 0 −1 −2, 19); (1, 5 4 4 3 2 1 0 −1 −2, 19). BRIDGE itself holds in all four (2,543; 4,550; 7,478; 4,134
  states of conj G(s₂) reached).
- Range where it holds: all 4,605 middles from valid words of length ≤ 12; the 13 pairs of `hybrid/REPORT.md` §5;
  all 721 middles with ≤ 8 letters, |letter| ≤ 5, s₁ ≤ 4, slacks ≤ 16, n ≤ 28. Not shown: n = 25 is the least failure.
- Recheck: `python3 bridgeat.py 0 "4 5 4 3 2 1 0 -1 -2"` (2 minutes; prints BRIDGE 2543, BRIDGE-ODD 0, LINE 0);
  `python3 bridgerand.py one 1 "5 4 4 3 2 1 0 -1 -2"` (2 s, BRIDGE only); `python3 oddbridge.py 11` (20 s, 1,344 middles, no
  failure; `12`: 4 minutes); `python3 oddmin.py 8 4 16 5 28` (4 minutes).

**HIT (disproof). LINE is false.** Statement: m carries one of (s₁|−), (−|s₁), (1^{s₁}|−), (−|1^{s₁}) to one of the four
such states of slack s₂.
- Why it matters: these four states are in G(s) (checked s < 400) and (s|−) is the bridging state of Theorem 0′; a
  4 × 4 table per middle would have been the smallest possible invariant.
- Counterexamples: (3, 3 3 2 1 0 −1 −2, 9), n = 19; (4, 2 3 2 1 0 −1 −2, 9) and (4, 3 2 2 1 0 −1 −2, 9), n = 20.
  BRIDGE holds there (208, 210 states). Reason: `../onehigh/REPORT.md` Lemma C (line states have no predecessors after a 2).
- Range where it holds: all 4,605 middles from valid words of length ≤ 12 (`rows_12.txt`).
- Recheck: `python3 linemin.py 7 5 12 3` (1 minute: 199 middles, 3 failures); `python3 rows.py 10` (4 s).

**Tested only, kept.** Odd(1^s) = the states obtained an odd number of times by adding to either diagram rim hooks of
sizes 2^j, j running over the binary digits of s in increasing order (s ≤ 13, `stats.py 10`, 20 s). |Odd(1^s)| for
s = 0..19: 1 2 4 8 8 16 32 64 16 32 64 128 128 256 512 1024 32 64 128 256; at slack 16 the class has 3,730 states.

**Remark (class profile, `cls.py s1 "m"`).** Along a middle the reached share of each class falls on the rising letters
(about 10% at the top of 4 5 4 3) and returns to 70–100% on the falling ones; the odd states are too few to be hit, G is not.

Other scripts: `oddrand.py`, `linerand.py` (random and structured middles, meet in the middle), `bridgerand.py` (BRIDGE on
the same random middles; `one s1 "m"` for one middle without listing G(s₂)).
