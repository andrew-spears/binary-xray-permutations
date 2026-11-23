# runrule follow-up: what shape can a proof of COUNT take? — REPORT

COUNT: N(x u y) ≤ N(x v y) for PEAK, ZERO, RUN (card `countrule`); N(w) = number of permutation matrices with word w.

**HIT (proved, small):** cuts of slack 1 factor like tight cuts (§2). **HIT (tested):** which one-sided refinements of
COUNT are true (§1), and a cleaner statement that contains PEAK and ZERO: inserting a valid block multiplies N by at
least the block's own count (§3). **NOTHING** on a proof strategy: five concrete proof shapes are refuted (§4).

Everything "tested" is brute force over all permutations, all words of length ≤ 10 (2,241 solvable words;
`countlib.py`); each command below runs in under a minute.

## 1. Refinements (tested): one side yes, both sides no
Notation: N(x u y) = Σ_t L_x(t)·R_{uy}(t) over states t = (λ, μ) after x (row diagram, column diagram). "Class by
class" means Σ_{c(t)=c} L_x(t)·[R_{vy}(t) − R_{uy}(t)] ≥ 0 for every c. Four cuts: after x ("left"), before y
("right"), and one letter further out on either side. Canonical steps of all valid nonzero words of length ≤ 10: 623
PEAK, 862 RUN, 746 ZERO. Number of steps with a violating class (`python3 refine.py 10`, table in `out_refine_10.txt`):

| statistic c(t) | PEAK (4 cuts) | RUN (4 cuts) | ZERO left−1 / left / right / right+1 |
|---|---|---|---|
| full state (λ, μ) | 0 / 6 / 6 / 0 | 1 / 21 / 21 / 1 | 55 / 89 / 34 / 6 |
| row diagram λ alone | **0 / 0 / 0 / 0** | 1 / 7 / 7 / 1 | 52 / 28 / 31 / 5 |
| (\|λ\|, \|μ\|) | **0** | **0 / 0 / 0 / 0** | 1 / 6 / 10 / 0 |
| number of row holes | **0** | **0 / 0 / 0 / 0** | 0 / 17 / 0 / 0 |
| (row holes, column holes) | **0** | 0 / 1 / 1 / 0 | 19 / 19 / 11 / 0 |
| row holes + column holes | **0** | 0 / 1 / 1 / 0 | 19 / **0** / 11 / 0 |
| largest row and column extras | **0** | 1 / 13 / 3 / 1 | 47 / 71 / 29 / 6 |

- PEAK: every statistic short of the full state works at all four cuts; the finest is the whole row diagram (or the
  whole column diagram). First failure of the full state: (3,2,1,1,0,−1,−1,−2,−3) ← (3,2,1,0,−1,−2,−3), 3 > 2.
- RUN: (|λ|, |μ|) and the number of row holes work everywhere; the row diagram does not.
- ZERO: no statistic works at all four cuts; at the cut after x only the total number of holes, one letter after
  the block (|λ|, |μ|) and both hole counts.
- **Both sides at once: false immediately** (`python3 joint.py 10`, `out_joint_10.txt`). Fixing even (|λ| after x,
  |λ| before y) fails in 219 of 623 PEAK steps and 173 of 862 RUN steps; for (1,1,1,0,−1,−1,−1) ← (1,1,0,−1,−1) the class
  (2, 2) has 1 solution of the short word and 0 of the long one. So for PEAK there is no version "for each fixed position of the
  0-stone" against a class of positions of the three stones defined by the rows or columns they use: an injection
  can keep the row diagram at ONE cut, and must then change the part of the solution on the other side (as the
  transposition does in §2).

## 2. Equality cases, and the slack-1 factorisation (proved)
**Lemma (proved).** There are two states of slack 1, A (one row box) and B (one column box), exchanged by
transposing the board; so L_x(A) = L_x(B) and R_y(A) = R_y(B) for all x, y. Hence, if the slack after x is 1,

    2·N(x y) = N(x 0 −1)·N(1 0 y),        and        N(x b y) = c₁(b)·N(x 0 y),  c₁(b) = N(1 0 b 0 −1)/2,

for every block b of letter sum 0 (x b y legal). Proof: N(x y) = L_x(A)R_y(A) + L_x(B)R_y(B) = 2L_x(A)R_y(A).
In state A after m stones (rows 1..m−1, m+1 and columns 1..m used) the only stone for a next letter 0 is (m, m+2)
and it leads to B; the only stone for a next letter −1 is (m, m+1) and it leads to the empty state. So
N(x 0 −1) = 2L_x(A),
by the mirror N(1 0 y) = 2R_y(A), and N(x b y) = L_x(A)R_y(A)·Σ_{t,t'} T_b(t, t'), which is N(x 0 y) times a
number depending on b only. Check: `python3 slack1.py 10`: 3,617 cuts and 5,529 blocks, 0 failures.

Consequences. (i) A word with a cut of slack 1 at distance ≥ 3 from both ends is solvable iff two shorter words
are. (ii) A rule applied at slack ≤ 1 (u, v of letter sum 0) is a finite check c₁(u) ≤ c₁(v), with ratio independent
of x and y. (iii) All ratios are determined by the excursion above slack 1 that contains the changed place.

**The bijection for DEL0 at slack 1** (N(x 0 y) = N(x y)): keep the stones of x; add (m, m+2) in state A, (m+2, m)
in state B; move every stone (r, c) of y to (c+1, r+1) (shift by one row and column, then reflect in the main
diagonal). Example (1,0,−1) → (1,0,0,−1): {(1,2),(3,1),(2,3)} ↦ {(1,2),(3,1),(2,4),(4,3)}. It keeps the x-part and
the state after x, and transposes the y-part — consistent with §1.

**Equality cases, tested** (`python3 equal.py 10`, `out_equal_10.txt`; DEL0 = delete any letter 0):
- DEL0 / ZERO, ratio 1: always when the slack at the 0 is 0 (tight cut, 2,410 of 2,410) or 1 (the lemma, 1,639 of
  1,639); never at slack 2 (ratio ≥ 5/4) or ≥ 4 (≥ 7/5); at slack 3 in 50 of 750 placements, and those are exactly
  the ones where the excursion above slack 1 is (2, 1, 0, 0, −1, −2) with one of its two zeros deleted (253 contexts,
  none mixed). There the states of slack 3 are reached through the forced staircase (2,1), so it is again a
  one-dimensional situation.
- canonical PEAK, ratio 2: always at slack 0 or 1 before the block (371 of 371; c₁(1,0,−1) = 2); at slack 2 in 92 of
  94 (exceptions (1,1,0,0,1,0,−1,0,−1,−1) and its mirror, ratio 5/2); never at slack ≥ 3 (≥ 2.36).
  Where the factor 2 comes from: replace the 0-stone at (r, c) by a 3×3 block; exactly 2 = N(1,0,−1) of the six
  blocks have diagonals 3, 4, 5. The result is a solution of x 1 0 −1 y exactly when no other stone lies
  north-east or south-west of the 0-stone (those stones move by 2 diagonals instead of 0 or 4).
- RUN, ratio 3/2: only RUN(1,2) and RUN(2,1) (21 of 224, 27 of 260), e.g. (1,1,0,1,0,−1,−2) ← (1,1,0,0,−1,−1).

## 3. Formula side (tested): block insertion
Σ_τ ∏ z_k^{τ(k)} is the monomial symmetric function m_ρ, ρ = (n, …, 1), so N(D) is the coefficient of m_D in m_ρ²
(a product of two monomial symmetric functions). I found no recursion in n for these coefficients that is visibly
nonnegative, and no expansion along the deleted stone: §4, first item. What the formula does suggest is to compare with products:

    INSERT(b):  N(x b y) ≥ N(b)·N(x y)        SUBST(b):  N(x b y) ≥ N(b)·N(x 0 y)

for every valid word b. DEL0 (hence ZERO) is INSERT(0); PEAK is SUBST(1,0,−1) (N = 2, which explains its ratio ≥ 2);
at a tight cut both are equalities; INSERT says N(x b y) ≥ N(x y b), i.e. a block is worth more inside than at the end.
`python3 insert.py 10 7` (`out_insert_10.txt`): all 98 valid blocks of length ≤ 7, words of length ≤ 10: 0 violations
in 12,812 INSERT and 4,470 SUBST placements. Also N(x 0 0 y) ≤ N(x 1 0 −1 y) (295 placements, 0 violations), so PEAK
= DEL0 followed by the one-stone step (0,0) → (1,0,−1), and every rule adds exactly one stone. RUN(a, b) with a ≠ b is
not a block insertion; it stays a separate statement.

## 4. Proof shapes refuted (NOTHING)
- **One new stone.** Every rule changes the diagonals as "insert a row and a column with a stone at the crossing"
  does (stones north-west +0, south-east +2, others +1). But the graph "P is Q with one stone deleted" has no
  matching saturating the solutions of the short word in 514 of 1,958 DEL0 placements, 66 of 295 for (0,0) → (1,0,−1),
  88 of 275 for RUN; (1,1,0,−1,−1) → (1,1,0,0,−1,−1): 4 and 8 solutions, largest matching 2 (`python3 delgraph.py 9`).
- **Fixed-n moves.** PEAK is not "two DEL0, then squeeze": (0,0,0) → (1,0,−1) lowers N in 20 of 295 placements
  ((1,1,0,0,0,−1,−1): 12 → 8). Of 176 blocks changed by a move, 136 never lower N (`python3 moves.py 9`).
- **Positive form.** With J the half-turn, N(x v y) − N(x u y) = L_x^T G_s L_{y*}, G_s = (T_v − T_u)J on the states of
  slack s. G_s is symmetric, but indefinite with about half its eigenvalues negative for s ≥ 2, and has entries −1
  (DEL0: one per state; PEAK: 2, 8, 29, 60 at s = 2..5) (`python3 gram.py 5`). No Cauchy–Schwarz argument.
- **Invariant cone.** The cone spanned by the vectors L_x at slack 2 and 3 gets new extreme rays at every prefix
  length (85 facets at slack 3 for length ≤ 9) (`python3 cone.py 6 9 3`). No finite list of inequalities between
  counts of states.
- **Two-sided refinement**: §1.

## What I would try next
The lemma of §2 is the case s = 1 of "the space spanned by the L_x at slack s is small": after transposition it has
dimension 1, 3, 5 at s = 1, 2, 3, and equality cases are the situations where it is effectively one-dimensional.
INSERT/SUBST at slack 2 is a statement about 3×3 matrices and the letters next to the cut; a proof there would show
whether the mechanism is an inequality between the three counts or a bijection that transposes one side.
