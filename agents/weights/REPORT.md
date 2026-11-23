# HIT (empirical): explicit weights with the majority property at the cut 1|0, slack ≤ 24. NOTHING on a proof.

Notation as in `../majority/REPORT.md`: F(x) = states reachable after the prefix x, A(y) = states from which the
suffix y reaches the empty state; states of slack s are pairs of partitions (λ | μ), |λ| + |μ| = s. For weights w ≥ 0
on the states of slack s, total 1:  a_s(l) = min of w(F(x)) over prefixes x ending at slack s with last letter l.

## 0. Only the cut 1|0 is needed (proved)
**Lemma.** Every valid word with a nonzero letter contains two neighbouring letters 1, 0.
*Proof.* The letters sum to 0, so some letter is negative; let e_j be the first. All earlier letters are ≥ 0 and
their sum is ≥ −e_j > 0, so one is positive; let e_i be the last positive one before j. The letters between are 0.
If i + 1 = j then e_j ≥ e_i − 1 ≥ 0, impossible. So e_{i+1} = 0 ≥ e_i − 1, hence e_i = 1. ∎
(Brute force agrees: all 4,623 nonzero valid words of length 11, and all shorter ones.)

**Mirror.** (λ | μ) → (λ′ | μ′) (conjugate both) maps the family of sets F(x), last letter l, onto the family of sets
A(y), first letter −l (`mirror.py`, exact equality of the families of minimal sets at bound 16).

So for w with w(λ | μ) = w(λ′ | μ′) the whole conjecture follows from one inequality per slack:

> **(M)  a_s(0) + a_s(1) > 1 for every s ≥ 1.**

(Cut the word at a 1|0; the prefix ends in 1, the mirrored suffix ends in 0; two sets of total weight > 1 meet.)

**Consequence, apparently not recorded yet.** A universal cut state for l = 1 (`../peak/REPORT.md` §3, bound 24) is in
every F(x) ending in 1 and every A(y) starting with 0. With the lemma: **every valid word of any length with all
slacks ≤ 24 is solvable** (docs/state.md has 16, from the determinised automaton). `universal.py` recounts the states
that work at 1|0 from this directory's own dump: 40, 78, 136, 184, 270, 348, 366, 926, 1740, 2476 for s = 15..24
(matches peak §3 except 926 vs 924 at s = 22, where peak also asks for suffixes starting with a positive letter).
This rests on the same machine and pruning as `cut_check.cpp`; only the lemma is new.

## 1. Explicit weights that satisfy (M) for all s ≤ 24
dim(λ | μ) = C(s, |λ|) f^λ f^μ = number of standard fillings of the pair = dimension of the irreducible
representation (λ, μ) of the hyperoctahedral group B_s (dim² / 2^s s! is its Plancherel measure).
core2 = 1 if both 2-cores are empty (s even) / one is empty and the other a single box (s odd), else 0.
Both are invariant under the mirror and under rows ↔ columns.

| weight | min over s ≤ 24 of a(0) + a(1) | at s | value at s = 20..24 |
|---|---|---|---|
| **dim** | 1.293 | 21 | 1.355, 1.293, 1.407, 1.395, 1.385 |
| **core2 · dim²** | 1.219 | 4 | 1.685, 1.644, 1.808, 1.818, 1.766 |
| core2 · dim | 1.301 | 21 | 1.414, 1.301, 1.574, 1.629, 1.565 |
| dim² | 1.297 | 23, 24 | 1.345, 1.324, 1.302, 1.297, 1.297 |
| core2 · dim³ | 1.123 | 4 | 1.655, 1.777, 1.793, 1.812, 1.632 |
| core2 · dim², inside the k × k square, k(k+1)/2 ≥ s | 1.186 | 6 | 1.737, 1.825, 1.833, 1.853, 1.789 |

**Range.** Every s ≤ 24; all prefixes ending in 0 or 1 whose slacks stay ≤ 24 (s ≤ 20: bound 20, all letters;
s = 19..24: bound 24, last letters 0 and 1 only; s = 19, 20 agree between the two bounds). Tables:
`out/essential_20.txt`, `out/essential_24.txt`.

Candidates that fail (M): uniform (s = 10: 0.798), f^λ f^μ (s = 10: 0.765; any power behaves alike), core2 alone
(s = 6: 0.900), number of prefixes reaching t times the same for t* (N N*, s = 10: 0.971), Perron vector of the
letter 0 times its mirror (s = 10: 0.863), number of minimal reachable sets containing t (s = 15: 0.848; its 4th
power passes to 16 with 1.003 at s = 15). `out/paths_16.txt`.

**LP optimum.** At the cut 1|0 the LP optimum is 2: a delta weight on a universal cut state. For odd s ≤ 24 every
state lying in all F(x) (last letter 0 or 1) has core2; for even s about half do. No formula: with no row holes the
column diagrams 333, 3333, 33333, 44444, 444444 work (s = 9, 12, 15, 20, 24) but 22, 222, 2222, 4444, 333333 do not;
s = 6 has only 21|3 and 3|21 (`out/universal_24.txt`).

## 2. Per letter, and where the minimum sits
a_s(l) for core2 · dim², bound 20 (`out/perletter_core2dim2_20.txt`; dim: `out/perletter_dim_20.txt`):

| s | l = −1 | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|---|
| 10 | 0.990 | 0.909 | 0.597 | 0.391 | 0.240 | 0.169 |
| 14 | 0.934 | 0.908 | 0.667 | 0.467 | 0.268 | 0.083 |
| 18 | 0.973 | 0.938 | 0.768 | 0.527 | 0.278 | 0.139 |
| 20 | – | 0.928 | 0.757 | 0.503 | 0.311 | 0.108 |

- **One-sided form w(F(x)) > ½.** False for last letter ≥ 2 with every candidate (a(3) ≤ 0.35), and no
  mirror-symmetric weight can have it at every last letter: it would give a(l) + b(f) > 1 without the junction
  condition, where the LP optimum is below 1 from slack 4 (`../majority/REPORT.md`). For last letter ≤ 1:
  core2 · dim² has a(1) > ½ for every s ≤ 24 except s = 4 (0.417) and s = 6 (0.456), rising to 0.7–0.85 for s ≥ 15;
  dim has a(1) ≥ 0.528 for every s ≤ 24, slowly falling.
- **dim must lose the one-sided form at s = 32.** F(1^s) lies in the parity set #odd(R) = #even(C) (card
  paritycount, z = 0), whose dim-weight P(s) is 0.574, 0.559, 0.536, 0.518, 0.498, 0.477, 0.470 at s = 16, 20, 24,
  28, 32, 40, 44 (`ones.py - 44`, exact enumeration). F(1^s) is the minimiser of dim at l = 1 for every s ≤ 20 except 6, 10, 15 (staircases). (M) may still
  hold for dim beyond 32 (a(0) ≈ 0.8), not tested.
- **Why core2.** core2 is a subset of the parity set (the smallest possible 2-cores). For s not divisible by 4
  (s ≤ 20) F(1^s) is exactly the parity set, so it contains every core2 state and has core2-weight 1; for s = 4, 8,
  …, 20 it is smaller. So core2 removes states that the all-ones prefix cannot reach (`out/ones_20.txt`).
- **Steep prefixes.** For core2 · dim² the minimisers are steep staircases and near-staircases: s = 20: l = 0 at
  5 5 4 3 2 1 0 (0.928), l = 1 at 5 5 4 3 2 1 (0.757); s = 19: 5 4 4 3 2 1 (0); s = 15: 5 4 3 2 1 0 and 4 3 3 2 2 1.
  For dim: l = 0 at steep prefixes (s = 20: 5 5 4 3 2 1 0), l = 1 at 1^s. `out/argmin_*.txt`.

## 3. Every cut (all last letters): passes at bound 20, but the numbers are not stable in the bound
min over all junctions f ≥ l − 1 of a(l) + b(f), bound 20, s = 1..20: dim ≥ 1.061 (s = 10), core2 · dim² ≥ 1.049
(s = 9), every dim-type candidate > 1 at every s (`out/allcuts_20.txt`). But the minimum sits at junctions like
(l, f) = (−4, −5), which only exist once the bound allows a climb and a steep descent: at s = 10, dim gives 1.249,
1.198, 1.198, 1.061 at bounds 14, 16, 18, 20. So this is not evidence for all words; by §0 these cuts are not needed.

## 4. Mechanism: NOTHING, with three tested facts
- **Pairing.** No natural involution works: {t, t*} meets every F(x) (last letter 0 or 1) for only 218 of 1,114
  states at s = 12 (conjugate both), 133 of 899 (conjugate one diagram). Covering pairs exist in bulk (146,086 at
  s = 12) but a greedy matching covers 858 of the 1,135 states that are not in every set; a pairing would also need to be compatible with the
  mirror. `out/pairing.txt`.
- **Step by step.** With dim, a letter 0 never lowers the weight of a reachable set (0 of 1,130 minimal sets, bound
  16), letters ±1 do (ratio down to 0.89). With core2 · dim² a letter 1 can lose a quarter (0.728). `out/ratio_16.txt`.
- **A letter 0 loses nothing on any set of states (tested, s ≤ 13).** By max-flow / Hall: for every set S of states
  of slack s, dim(N_0(S)) ≥ dim(S) and |N_0(S)| ≥ |S| (N_0 = 0-successors); equivalently the letter 0 carries a flow
  with both marginals dim, and contains a bijection of the states. Not true for dim² (constant 0.34 at s = 11), and no
  bijection preserves dim. So w(F(x 0)) ≥ w(F(x)) for w = dim and w = uniform. `out/transport.txt`.
  This gives a(0) ≥ min over l ≤ 1 of a(l), but nothing for the letters that change the slack.
- **The step in partition language (checked, slack ≤ 10, `rowinsert.py`).** A letter e sends (λ | μ) to all
  (ins(λ; j, m) | ins(μ; j′, m′)) with (m − j + 1) + (m′ − j′ + 1) = e, where
  ins(λ; j, m) = (λ_1 − 1, …, λ_{j−1} − 1, m, λ_j, …): the Bernstein (row-creation) operator of Schur functions
  without its sign. A possible route to the flow statement: a bijection on standard fillings of pairs (growth
  diagram) that realises a 0-step. Not attempted.

## Recheck
`sh runs.sh` (about 5 minutes, 0.7 GB; data in /tmp/weights). Fast part: `g++ -O2 -o dump dump.cpp;
./dump 20 /tmp/w20 0; python3 essential.py /tmp/w20` (40 seconds).

## Files
`dump.cpp` (minimal sets F(x), A(y) per (s, l) and the transitions; machine and pruning copied from
`../peak/cut_check.cpp`), `load.py`, `weights.py` (candidates; every junction), `essential.py` (the cut 1|0),
`perletter.py`, `argmin.py`, `paths.py`, `ones.py`, `universal.py`, `pairing.py`, `ratio.py`, `transport.py`,
`rowinsert.py`, `mirror.py`, `runs.sh`, `out/`.
