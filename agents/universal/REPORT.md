# NOTHING (no closed-form family), with one lead: universal states have an inductive certificate with finite memory

Follow-up to `../peak/REPORT.md` §3. Notation as there: F(x), A(y); a state is `λ|μ` (row holes | column holes),
slack = |λ| + |μ|; conj = conjugate both partitions; U(s, l) = CF(s, l) ∩ CA(s, l) = universal states.
All sets were computed for every s ≤ 24, l ∈ {0, 1} (`cores.cpp`, tables in `analyze_24.txt`).
Only §1 is proved; everything else is "tested for s ≤ 24" unless a smaller range is given.

## 1. Reversal symmetry (proved): the A side is the F side
Rotating a full placement by 180° reverses the order of the stones, negates and reverses the word, and turns
the state left by the suffix stones into the conjugate state (complement + reversal of a Maya diagram). Hence
A(y) = conj F(−reverse(y)), and with LE(s, l) = ∩ F(x) over prefixes ending at slack s with last letter ≤ l:

    CA(s, l) = conj LE(s, 1 − l),     U(s, 0) = CF(s, 0) ∩ conj LE(s, 1),     U(s, 1) = CF(s, 1) ∩ conj LE(s, 0).

(Checked against the direct A-side computation: equal in all 48 cases.) So "universal state at (s, 0)" is a
statement about prefixes only: one state c with c ∈ F(x) for all x ending (s, 0) and conj c ∈ F(x') for all x'
ending (s, ≤ 1). Tested: LE(s, 1) = CF(s, 0) ∩ CF(s, 1) always (negative last letters never bind), and
LE(s, 0) = CF(s, 0) except at s = 15, 22, 23.

**Binding side.** The last-letter-1 family is the binding one: |CF(24, 0)| = 29340, |LE(24, 1)| = 2956,
|U(24, 0)| = 2460, i.e. 83% of conj LE(s, 1) is universal. The tightest slacks are 6 and 7 (U(6, 0) = {111|21, 21|111},
U(7, 0) = {−|331, 11|32} and transposes); from s = 8 on |U| grows (12, 8, 14, 12, 22, 26, 36, 36, 78, 128, …).
The symmetric shortcut "c and conj c both in LE(s, 1)" is false: that set is empty at s = 6, 7, 12, 15.

**Binding prefixes** (`./cores 22 w`, greedy cover of the complement of CF): at every slack the first is the steepest
staircase (j, a, a−1, …, 1 with or without the final 0: `3 5 4 3 2 1 0` at s = 18), which alone removes 84–89% of
the states that have to go (6423 of 7660 at s = 18, 23912 of 26978 at s = 21); second is 1 1 … 1; then concatenated staircases (`4 3 2 1 4 3 2 1 0`) and 2 2 … 2 1 0. The greedy cover
never uses a negative letter, but it needs 66 (l = 0) and 145 (l = 1) prefixes at s = 22, so U is not cut out by
two or three words.

## 2. No closed-form family
Slacks s ≤ 24 at which NO universal state of the given shape exists (up to transpose; l = 0, l = 1 similar):

| shape | missing at |
|---|---|
| λ = ∅ (no row hole) | 3, 5, 6, 8, 10, 11, 14, 15, 18, 21, 23 |
| self-mirror (conj c = c or its transpose) | all except 1, 4, 9, 13, 16, 20, 24 |
| λ = μ, or μ = conj λ | all |
| both rectangles | 4, 6, 7, 8, 11, 12, 14–24 |
| μ a staircase | 2, 7, 9, 11, 14, 23 |
| λ a rectangle and μ a hook (33\|411, 333\|4111, 444\|51111, 4444\|611, …) | 7, 15, 18, 20 |
| λ = 1^j and μ with ≤ 2 part sizes | 16, 22 |
| λ = 1^j, j ≥ 1 (one missing row) | none for l = 0 (6, 9 for l = 1) |
| λ a rectangle; λ a hook; μ a rectangle; μ with ≤ 2 part sizes | none |

The classes in the last two rows always contain a universal state, but the state itself follows no formula I could
find: e.g. with λ = 1^j the only choices are 111|21 (s = 6), 11|32 (7), 1111|32 (9), 111|53 (11), 111|6331 (16), and the
admissible j jump around (s = 12: j ∈ {1, 2, 5}; s = 16: j = 3; s = 23: j ∈ {2..7}). The λ = ∅ universal states are
−|1, −|11, −|2, −|211, −|31, −|331, −|333, −|4431, −|44311, −|5332, −|544111, −|54422, then 5, 2, 0, 3, 0, 16 states at
s = 19..24; no test for them simpler than the definition was found.

Necessary conditions that do hold (all with trivial reasons): U(s, l) is closed under transpose; conj U(s, 0) ⊆ U(s, 1)
(except s = 22); every universal state at (s, 0) fits λ, μ in an (a + 1) × a box, a = ⌈triangular root of s⌉ (the
shortest prefix has a + 1 letters); the parity charges of λ and μ lie in {−1, 0, 1} and add up to s mod 2; λ ≠ μ.
Neighbouring slacks are only loosely related: at s = 24, 514 of 2460 states of U(s, 0) have a 0-predecessor in U(s, 1),
1128 of 2476 states of U(s, 1) have a 1-predecessor in U(s − 1, 0), 1332 of 2460 have a one-box-smaller state in
U(s − 1, 0); at s = 7 the last two counts are 0. No rim-hook or core/quotient rule fits. A signed count of placements
(`signed.py`) vanishes on some prefix for every universal state from s = 5 on, so no determinant argument.

## 3. The lead: an induction with memory (step tested, small range)
**Invariant.** Call the type of a prefix (end slack, its last m letters); prefixes with ≤ m letters are their own type.
Look for sets J(type) with J(empty word) = {start} and, for every prefix x and letter e,
J(type of x e) ⊆ step_e(J(type of x)). Then J(type of x) ⊆ F(x) by induction on x, and by §1
conj J(type of −reverse(y)) ⊆ A(y). `memory_inv.py B m` computes the LARGEST such family for words with all
slacks ≤ B, so "none exists" is exact, and reports
- pairs: is J(t) ∩ conj J(t') ≠ ∅ for all types t, t' at the same slack with last letters adding to ≤ 1
  (this proves the conjecture for all words with slacks ≤ B, by a local certificate);
- universal: is ∩ J(t) over t ending (s, 0), intersected with conj ∩ J(t') over t' ending (s, ≤ 1), nonempty.

| memory m | every J nonempty and all pairs meet, for B ≤ | universal state from J at | first failure |
|---|---|---|---|
| 1 | 2 | s ≤ 2 | B = 3: J(3; 0) = ∅ |
| 2 | 4 | s ≤ 4 | B = 5: e.g. J(4; 0 −1) = ∅ |
| 3 | 8 | s ≤ 4 | B = 9: J(9; 0 0 0) = ∅ |
| 4 | 13 | s ≤ 8 | B = 14: 14,642 types empty |
| 5 | 14 (not run further) | every s ≤ 14 | not reached |

So: (i) the induction over (slack, last letter) alone, or with any fixed memory, fails: the needed memory grows
(failures at B = 3, 5, 9, 14, i.e. T_{m+1} − 1 for m ≥ 2, when the steepest staircase no longer fits in the
memory); (ii) with memory about the length a + 1 of the steepest staircase, a step-closed invariant exists and
its common part is a universal state (m = 5: all s ≤ 14; the certified sets are smaller than U, e.g. 4 of the 8
states at s = 9). When memory m fails, the first empty type is a run of zeros: the invariant after `… 0 0 0` must
map into itself under the letter 0 while lying in F(x 0 0 0) for the steepest x.

**What a proof would need.** A description of J(s; last a + 1 letters) by a formula; I do not have one. The
natural next experiment is a coarser type than "last m letters" that still works (e.g. the final descending run
plus the length of the final run of zeros), small enough to read the sets J off.

## Recheck (all under 10 minutes together)
    cd agents/universal && g++ -O2 -o cores cores.cpp && ./cores 24 > cores_24.txt   # 85 seconds, 1.2 GB
    python3 analyze.py cores_24.txt        # 5 seconds: the tables of §1, §2 (stored in analyze_24.txt)
    ./cores 22 w 2>&1 >/dev/null | less    # 30 seconds: binding prefixes
    python3 memory_inv.py 13 4 q; python3 memory_inv.py 14 4 q; python3 memory_inv.py 14 5 q   # 15 + 35 + 75 seconds
    python3 signed.py 10 12                # 10 seconds (needs cores_24.txt)
    python3 memory_inv.py 10 5             # 3 seconds, per-slack table with the certified universal states
