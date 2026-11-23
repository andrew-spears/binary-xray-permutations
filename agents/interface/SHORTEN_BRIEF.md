# Brief: proving the three shortening rules (card `shorten3`)

Read first: `README.md`, `docs/claims-map-guide.md`, `docs/state.md` (interface section), `agents/interface/README.md`,
`agents/interface/run_rule.py` (docstring = the reduction, proved), `agents/interface/letters_notes.md` (last sections).

## Setting (order-free form)
Reflect rows (r' = n+1-r). The k-th stone of a word e_1 … e_n sits at (a, b), a, b ≥ 1, with **sum** a + b = 2k + e_k.
A prefix x of length k is a set Σ(x) of k distinct sums. `F(x)` = set of pairs (A, B) = (rows used, columns used) over
all placements of Σ(x) with distinct rows and distinct columns. F depends only on the set of sums, not on their order.
The interface state is (A, B) written relative to {1..k} (a pair of Young diagrams with |λ| + |μ| = slack).
Shift: Sh(A) = (A + 1) ∪ {1}. Exactly: F(0 x) = Sh F(x) (a first stone with sum 2 must sit at (1, 1)).

## CORRECTION (after slack 14 run)
As set inclusions ZERO and RUN(2,1) are FALSE: RUN(2,1) fails after x = (4, 3, 2, 1) (slack reaches 13), ZERO after
x = (2, 3, 3, 2, 2, 1, 1, 0) (slack 14); `zero_fail.py 14` prints the missing states. PEAK holds through 14.
What the induction needs is only the word-level statement: x u y solvable ⇒ x v y solvable.

## The rules (machine-checked for every legal prefix with slack ≤ 12, 6,061 cases, 0 failures; see correction)
- ZERO: F(x −1) ⊆ F(x 0 −1).            Same as: F(0 x −1) ⊆ F(x 0 −1) as sets of (A, B).
- PEAK: F(x 0) ⊆ F(x 1 0 −1).           Same as: F(0 0 x 0) ⊆ F(x 1 0 −1).
- RUN(a, b), a, b ≥ 1, (a, b) ≠ (1, 1): F(x u) ⊆ F(x v), v = (a, a−1, …, −b), u = (a−1, …, −(b−1)) with a−b doubled.
Legal prefix: e_1 ≥ 0, e_{k+1} ≥ e_k − 1, all partial sums ≥ 0. The three rules for all legal x give the conjecture by
induction on n (proved; see run_rule.py).

## Known facts
- Not state by state: in general the placement of x itself must change. With the placement of x kept, PEAK works
  only when A and B have no gaps inside each parity class (derivation by hand, not machine-checked).
- With multiplicity (number of placements per state; `count_rule.py 6 8`): PEAK holds in all 2,812 tests, RUN(a, b)
  holds except RUN(2, 1) (288 failures of 1,939), ZERO fails (43 of 1,715). So PEAK may have an injective proof.
- Nearby rules that FAIL: (0) → (0 0) from slack 8; (0 0) → (1 0 −1) from slack 6; c → (0 c) for every c ≥ 0.
  Valid at slack ≤ 8 (few tests): (0, −1) → (−1, 0), i.e. F(x 0 −1) ⊆ F(x −1 0).
- Single ±1 transfers between two sums are not monotone for F in either direction (`agents/transfer/transfer.py`).
- Earlier proved tool that may apply: leapfrog paths (card `leapfrog`, agents/leapfrog/), parity counts (card
  `paritycount`).

## Conventions for sub-tasks
- Branch from `devin/1795444188-two-marks`; put code and notes in `agents/<task-name>/`; open a PR **into that
  branch** (not main). Do not edit `map/build.py` or `docs/state.md`; write `agents/<task-name>/REPORT.md` instead:
  HIT or NOTHING (format in `docs/delegation-queue.md`), exact claim, range, recheck command under 10 minutes,
  and for a proof the full argument in plain steps. Say clearly what is proved and what is only tested.
- Small targeted computations only; no large sweeps.
