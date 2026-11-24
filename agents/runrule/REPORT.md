# runrule: set-monotone shortening rules — REPORT

**NOTHING** for a complete set-monotone rule system: every candidate fails as a set inclusion by bound 22 (§1,
counterexamples). **LEAD**: the same rules hold at word level with multiplicity, including behind the prefixes where
the set inclusion fails (§2, tested only).

Nothing here is proved; everything is computation on the interface machine of `../interface/rewrite.py`, redone in
C++ (`rules.cpp`, bitsets, bound 22 in 2 minutes / 1.2 GB). `rules.cpp` reproduces the Python numbers at bound 14
exactly (ZERO 1 of 904, RUN(2,1) 2 of 1,344, PEAK 0 of 1,941) and the known PEAK failure after (3,4,3,3,2,1).

## 1. Which rules fail as set inclusions, bounds 14–22 (counterexamples)

Entries: failing situations / tested situations, "F(xu) ⊆ F(xv)", all legal prefixes x with slacks ≤ B.
A dash means no failure. RUN(a, b) for a, b ≤ 10; rows not shown have no failure through B = 22.

| rule | B=14 | 16 | 18 | 20 | 22 | shortest failing prefix x (slack) |
|---|---|---|---|---|---|---|
| ZERO | 1/904 | 1/1825 | 2/3550 | 8/6771 | 15/12559 | 2 3 3 2 2 1 1 0 (14) |
| PEAK | – | – | **1/8417** | 5/16477 | 6/31424 | 3 4 3 3 2 1 (16) |
| RUN(2,1) | 2/1344 | 7/3308 | 30/7365 | 103/15813 | 233/32301 | 4 3 2 1 (10) |
| RUN(3,1) | 7/388 | 19/1060 | 39/2764 | 78/6739 | 355/15333 | 1 3 3 (7) |
| RUN(4,1) | – | 1/140 | 5/425 | 19/1175 | 59/3155 | 2 1 1 1 (5) |
| RUN(5,1) | – | – | 1/34 | 6/88 | 25/257 | 2 1 (3) |
| RUN(1,3) | – | – | 1/8371 | 3/16430 | 5/31375 | 1^17 (17) |
| RUN(1,2) | – | – | – | 2/16463 | 3/31408 | 5 4 3 2 1 2 1 (18) |
| RUN(2,2) | – | – | – | 8/15813 | 10/32301 | 5 4 3 2 2 (16) |
| RUN(3,2) | – | – | – | 10/6739 | 15/15333 | 4 4 3 2 (13) |
| RUN(4,2) | – | – | – | 1/1175 | 5/3155 | 2 1 1 1 4 (9) |
| RUN(5,2) | – | – | – | 1/88 | 2/257 | 2 1 1 1 (5) |

- **Pattern.** The failures start on the side b = 1 (bounds 14–18), reach b = 2 at bound 20, and RUN(1,3) at 18.
  The onset bound grows with b; it is not "only when one side is short" in any stable sense. RUN(a, b) with
  a ≥ 6 needs slack ≥ 21 and is barely tested. RUN(a, b) with b ≥ 3 other than RUN(1,3) has not failed through 22
  (RUN(2,3): 0 of 15,791 at B = 20). All shortest failing prefixes have no negative
  letter, so restricting to the canonical step (first negative letter) does not help.
- **Short rules die too** (`short.txt`, `out_short_22.txt`, B = 22): (0,0) → (0,0,0) fails 2 of 41,527;
  (−1) → (−1,0,0) fails; (−1,−1) → (0,−1,−1) fails; RUN(2,1) followed by −1 fails. Still alive at 22:
  () → (0,0,0), (0) → (0,0,0), (−1) → (0,0,−1), (−1,−2) → (0,−1,−2), (0) → (1,0,−1,0), (0) → (1,0,0,−1),
  (1,0,−1) → (2,1,0,−1,−2). Of the 64,761 rules with |v| ≤ 5 valid at B = 10 (`enum_rules.py 10 5`), 41,885 survive
  B = 16 and 33,025 survive B = 20; the short, often-tested ones keep dying as B grows. I found no complete system
  among the survivors (words that are one long descending run need rules of unbounded length, and those are the RUN
  family above), and I do not expect one: each rule seems to need only enough slack to fail.
- **The weaker set-level forms do not repair it** (columns `fails1`, `failsLive`, `failsSim` of `./rules`):
  - one more letter (F(xuz) ⊆ F(xvz) for every z): fails in almost the same situations;
  - live states only (states that can still be completed after x u): **every** missing state is live, B ≤ 22;
  - domination: the largest simulation that ignores the last letter (s ≤ t if every move of s is matched by t) is
    exactly transposition at B = 16 (17,278 pairs = the 17,278 states that differ from their transpose). This is a
    sub-relation of the one in `../simorder` (trivial there at bound 10), so it adds only the larger bound.

Why it matters: the induction on n by set-monotone rules (cards shorten3 / interface) cannot be proved as stated,
for any choice of rules I could find; a set of reachable interface states is the wrong invariant.

## 2. LEAD: the rules hold at word level with multiplicity (tested)

N(w) = number of permutation matrices with diagonal word w.

**COUNT.** For every legal x, y and every rule u → v of PEAK, ZERO, RUN(a, b): N(x u y) ≤ N(x v y).
Also **DEL0**: deleting one letter 0 from a valid word (when the result is legal) never increases N.

- COUNT implies the conjecture by the proved reduction in the docstring of `../interface/run_rule.py`
  (N(all zeros) = 1). It is weaker than the state-level count inequality (false, `count_rule.py`) and than the set
  inclusion (false, §1), and stronger than "x u y solvable ⇒ x v y solvable".
- Tested: all 19,559 valid nonzero words with slacks ≤ 8 and length ≤ 12: 0 violations in 15,718 ZERO, 7,929 PEAK,
  9,334 RUN and 63,161 DEL0 applications (`out_wordcount_8_12.txt`). Least ratio N(longer)/N(shorter): 1 for
  ZERO / DEL0 (e.g. (1,0,0,−1) ← (1,0,−1)), 1.75 for PEAK, 1.5 for RUN.
- Tested exactly where the set inclusion fails: behind 15 failing prefixes of §1 (`cases.txt` at B = 18, every
  closing continuation y of length ≤ 9; `cases20.txt` at B = 20, length ≤ 7), 22,017 words: 0 violations, and
  N(x v y) ≥ 2.2 · N(x u y) throughout (`out_wcount_18_9.txt`, `out_wcount_20_7.txt`). The missing states carry
  little weight; the inclusion fails but the count inequality has a factor 2 to spare.
- Not tested beyond this; no proof idea yet. In operator form N(w) = ⟨0| T_{e_1} … T_{e_n} |0⟩ with T_e ≥ 0 on pairs
  of Maya diagrams, COUNT says ⟨L_x| T_v − T_u |R_y⟩ ≥ 0 for the reachable vectors L_x, R_y only; the entrywise
  versions L_x (T_v − T_u) ≥ 0 are the false statements above.

## Recheck (under 10 minutes in total)

```
cd agents/runrule && g++ -O2 -o rules rules.cpp && g++ -O2 -o wcount wcount.cpp
python3 genrules.py 10 | ./rules 18            # 4 s: PEAK fails 1 of 8417, x = 3 4 3 3 2 1 (table column 18)
python3 genrules.py 10 | SIM=1 ./rules 14      # 1 s: simulation = transposition; failsSim = fails
python3 wordcount.py 8 12                      # 70 s: COUNT and DEL0, 0 violations
./wcount 18 9 < cases.txt                      # 3 min: COUNT behind 9 failing prefixes
```
Longer: `python3 genrules.py 10 | ./rules 22` (2 min, 1.2 GB) for the last column; `./rules 22 < short.txt`.

## Files

`rules.cpp` rule checker (set inclusion, one more letter, live states, simulation); `genrules.py` PEAK / ZERO / RUN
list; `enum_rules.py`, `cover.py` enumerate valid rules at a bound and test which words they shorten;
`wordcount.py`, `wcount.cpp` word-level counts; `out_*.txt` outputs quoted above.
