# REPORT3. Mixing: zeros mix single states exactly inside the classes of K = #odd(R) − #odd(C) (K proved conserved; mixing tested s ≤ 10, b* = 2(s − K²) + 2, NOT proved). Blocks 1 0 −1 mix everything in ≤ 6 blocks (s ≤ 9, tested). Runs of 1 do not saturate.

Verdicts. Item 1: statement and b*(s) found, reductions proved, **no proof of mixing: NOTHING** on the theorem itself.
Item 4: **HIT** — the part of the machine that zeros never mix is exactly K (proved), and legal prefixes do miss classes.
Item 2: tested only. Item 3: conditional statements only.

N_e^b(t) = states reached from the single state t by b letters e. Coordinates as in REPORT2; D = #odd(R) − #even(C).

## 1. What is proved

**Lemma 1 (machine on Maya diagrams).** Let M(λ) = {λ_i − i : i ≥ 1} ⊂ ℤ ("beads"; the rest are holes). Stone n + 1 with
letter e is: choose a hole i of M(λ) and a hole j of M(μ) with i + j = e, add them, and shift both diagrams by −1.
(Row r = n + 1 + i, column c = n + 1 + j; this is (LAST) of REPORT2.) `maya.py`, checked against `fx.py`.

**Lemma 2 (matching criterion).** u ∈ N_e^b(t) iff I = (M(λ_u) + b) ∖ M(λ_t) and J = (M(μ_u) + b) ∖ M(μ_t) have b elements
each (i.e. M(λ_t) ⊆ M(λ_u) + b, same for μ) and there is a bijection I → J whose sums x + y are
**e, e + 2, …, e + 2b − 2, each once**. Proof: put x_k = i_k + k − 1, y_k = j_k + k − 1 for the k-th stone; the x_k are
distinct holes of M(λ_t), nothing else is required. ∎
So a run of a constant letter is again a binary x-ray problem, on the board I × J, with sums in arithmetic progression.

**Corollaries (letter 0).**
- *K is conserved*: x ≡ y mod 2 for every stone. With n stones K = #odd(R) − #odd(C); as a function of the two diagrams it
  changes sign with the parity of n. In general K changes by ±1 at each odd letter and not at even letters, so
  |K| ≤ #odd letters, the companion of card `paritycount` (which is the same for D and even letters).
- *Containment*: u ∈ N_0^b(t) needs M(λ_t) ⊆ M(λ_u) + b; a loop t ∈ N_0^b(t) needs λ_t, μ_t to be b-cores (2-loops only at
  pairs of 2-cores, the only fixed point is ∅|∅).
- *Reversal*: u ∈ N_0^b(t) iff t* ∈ N_0^b(u*), * = conjugate both diagrams.
- *2-adic splitting*: odd and even elements are matched separately; if the even class takes every second sum, both classes are
  zero-run problems of half the length on the 2-quotients (in general the two classes see constant letters e and −e).

**Lemma 3 (the classes are copies of each other).** In the fixed frame A = M(λ) + n, B = n − holes(M(μ)), a letter 0 moves
one element a ∈ B ∖ A from B to A and then translates B by 2. Translating the odd sites by 2d and the even sites by −2d
in both A and B commutes with this. It maps the class (slack s, K) onto the class (s + 4d² − 4dK, K − 2d), so
**m = s − K² is the only parameter of a class** (for K of fixed parity), and |K| ≤ √s. `items.py shift 6 1` checks the
commutation and the slack change on all states of slack ≤ 6. ∎

**Obstruction (item 4).** N_0^b(t) ⊆ {K = K(t)} for every b, hence F(x 0^b) ⊆ {u : K(u) ∈ K(F(x))} for every b, and this
is not everything for legal x: x = (4) has F = {4|−, 3|1, 2|2, 1|3, −|4}, all with K = 0, and 21|1, 1|21 (K = ±2) are never
in F(4 0^b). Among legal prefixes (distinct diagonals) with letters in [−1, 3], length ≤ 9, slacks ≤ 8: 3 of 14 sets F(x)
at slack 4, 3 of 45 at slack 6, 3 of 140 at slack 8 miss a class; none at odd slack (`items.py sets 8 9`).

## 2. What is tested (item 1)

**Conjecture (zero mixing).** For states t, u of slack s with the same K and b ≥ 2(s − K²) + 2 zeros: u ∈ N_0^b(t).
Tested for every pair, s ≤ 10, b ≤ 26 (`items.py class 10 26`), and b ≤ 40 for the classes together (`mix.py 10 40`):

| m = s − K² | 0 | 2 | 4 | 6 | 8 | 10 |
|---|---|---|---|---|---|---|
| states in the class | 1 | 5 | 18 | 55 | 149 | 371 |
| b* (least b that works for all t) | 0 | 6 | 10 | 14 | 18 | 22 |

- Sharp: slowest starts are −|1^s and 1^s|− (s even). For 2 ≤ b < b* the pairs passing containment and K but not joined
  are counted in `out2/mix2.txt` (s = 8: 1,062 … 7,036 … 8, 4, 2); so "containment + K" is not the exact description for small b.
- Monotone: N_0^b(t) ⊆ N_0^{b+2}(t) for all t from b = 2m on (s ≤ 8, `mix2.py`). It fails before, and cannot be proved by
  inserting two stones into a matching: that needs a pair of 2-cores on the path.
- Hubs: the first b at which one state is reached from every t of the class K = 0 is b = s + 2, and the common states are
  (a | s − a), 2 ≤ a ≤ s − 2 (s = 4..10, `hub.py 10`). By reversal (1^a | 1^(s−a)) reaches everything in s + 2 steps. A proof of mixing could go:
  every t reaches a two-row state in exactly s + 2 steps. I did not find it.
- Structure: out-degrees are small (≤ 2 for s ≤ 4). "Always the largest i"
  runs into cycles of pairs of b-cores: length s + 1 (1^a | (s − a) → 1^(a+1) | (s − a − 1), 1^s|− → −|s) and others
  (s = 8: 9, 6, 3); one-sided hooks form a cycle of length 2s sharing the edge 1^s|− → −|s (`greedy.py 9`).
- **Sets mix much faster**: for the prefixes above, F(x 0^b) = {u : |K(u)| ∈ |K|(F(x))} from b = 3, 3, 5, 5, 5, 5, 6 on
  (s = 2..8, maximum over x), against 6..18 for single states.

## 3. Runs of 1, of −1, blocks 1 0 −1 (item 2, tested)
- **Runs of 1 do not saturate from a single state.** Necessary for u ∈ N_1^b(t): slack s + b, D(u) = D(t), containment,
  u ≠ (λ | λ′) (REPORT2 §3). For t = ∅|∅ this is exact (Theorem 1 with its exceptions, b ≤ 7). For s ≥ 1 it is not, and the
  exceptions do not die out: t = 1|− does not reach (b + 1)|−, nor 1|b (b even) or −|b1 (b odd), for b = 6..9 (4 such pairs at each b, with the swaps). Share reached at b = 7:
  248/252 (s = 1), 872/896, 2,520/2,728, 7,268/8,152 (s = 4) (`items.py ones 4 7`). Runs of −1: the mirror statement.
- **Blocks 1 0 −1 mix completely and fast.** From every state of slack s, b blocks reach every state of slack s for
  b ≥ 1, 2, 3, 4, 4, 4, 5, 6, 6 (s = 1..9; `items.py block 9 6`). No invariant survives (the block has one even and two odd
  letters). No proof.

## 4. Consequences for a shortest unsolvable word (item 3)
All conditional; and every word with slacks ≤ 24 is already solvable, so they have content only once §2/§3 are proved.
- If zero mixing holds at slack s: a shortest unsolvable valid word has **no run of ≥ 2s + 2 zeros at slack s**.
  (w = x 0^b y; x 0^(b−2) y is valid, shorter, so some t ∈ F(x) reaches some u ∈ A(y) in b − 2 zeros; then K fits for b
  too, and b ≥ b* gives u ∈ N_0^b(t). One must drop two zeros, not one: K changes sign.)
  The monotone form needs only b ≥ 2(s − K²) + 2.
- If b blocks 1 0 −1 join all states of slack s: no factor (1 0 −1)^b at slack s (drop one block; F(x), A(y) nonempty).
- With ZERO / PEAK / RUN of card `shorten3` I found no clean combined statement.

## Recheck
`sh runs3.sh` (about 2 minutes), outputs in `out2/` (`mix.txt`, `mix2.txt`, `hub.txt`, `greedy.txt`, `items.txt`).
