# thirds: fixed rows r ≡ 1 (mod 3)

**Main question: NOTHING.** No proof, and no rule that names an odd S (n ≤ 13). What blocks each direction is listed in §3.

**HIT (partial), three precise statements.** Conventions: rows and columns 0-based, marks d = row + column ∈ 0..2n−2,
R_p = rows r ≡ p (mod 3) (the card's R is R_0), T(R, S) = number of solutions whose stones in the rows of R are exactly S,
ω² + ω + 1 = 0 in the field with 4 elements.

## 1. Proved for all n: the F_4 sums are 0 or a known phase

**Theorem 1.** For u ∈ {1, ω, ω²}ⁿ let F(u) = Σ_solutions ∏_k u_k^(row of stone k). Then
F(u) = τ(u) · ∏_k u_k^(−d_k), where τ(u) ∈ {0, 1} is the parity of the number of tournaments with score d (2 points a game)
whose ties are only between stones with different u.

*Proof.* F(u) is the coefficient of x^d in ∏_{i<j} (u_i x_i² + (u_i + u_j) x_i x_j + u_j x_j²) (`rowcut/NOTES.md`).
Put x_i = y_i / u_i² (u_i⁴ = u_i, so u_i x_i² = y_i²). The middle coefficient becomes (u_i + u_j) u_i u_j, which is 0 if
u_i = u_j and 1 otherwise (1·ω·ω² = 1 and the sum of two different cube roots of 1 is the third). So the product is
∏_{i<j} (y_i² + [u_i ≠ u_j] y_i y_j + y_j²), whose coefficient of y^d is τ(u), and y^d = x^d ∏ u_k^(2 d_k), so the
coefficient of x^d is τ(u) ∏ u_k^(2 d_k) = τ(u) ∏ u_k^(−d_k) (u³ = 1). ∎

**Corollary 2 (tournament form of the card).** For a set Z of stones let G_p(Z) be the parity of the number of pairs
(unordered split {A, B} of the stones outside Z; tournament with score d whose ties are only between different classes
of (Z, A, B)) with Σ_{k∈A} (d_k + p) − Σ_{k∈B} (d_k + p) ≢ 0 (mod 3); G_p(all) = 1 iff D is evenly spaced. Then
T(R_p, S) ≡ Σ_{Z ⊆ S} G_p(Z) (mod 2). So **some T(R_p, S) is odd ⇔ some G_p(Z) is odd**: the card is a statement about
tournaments with three teams, with no permutations in it.

*Proof.* In characteristic 2, [ρ ≡ p] = 1 + ω^(ρ−p) + ω^(2(ρ−p)). Expand ∏_{k∈S} [ρ_k ≡ p] ∏_{k∉S} (1 + [ρ_k ≡ p]), sum over
solutions, apply Theorem 1, and pair each colouring with the one that swaps ω and ω² (ω^a + ω^(−a) = [3 ∤ a]). ∎

Why it matters: Theorem 1 removes the phases, which is what defeated the search for a rule for u (`rowcut/NOTES.md`):
every F(u) is decided by a 0/1 count. Why 3: with u = v² the middle coefficient is v_i/v_j + v_j/v_i, which is 0 or 1
for all v only in the field with 4 elements; in GF(2^m), m > 2 (rows mod 2^m − 1), it is not constant.

**Proposition 3 (one marked stone, closed form).** For a stone k, Σ_r N(k, r) u^r ≡ c · u^a (1 + u)^b (mod 2), N(k, r) =
number of solutions with stone k in row r; c = 1 iff the other stones, sorted, satisfy m_h ∈ [2h, 2h+2] (h = 0..n−2);
b = number of other stones on odd marks; a = number of other stones on even marks with m_h = 2h. Proof: all u_j = 1
except u_k = u gives V(x)² ∏_{j≠k} (u x_k² + (1+u) x_k x_j + x_j²) and V² = Σ_σ ∏ x_j^(2σ(j)); the stone-segment graph is a
forest, so one term survives. This is the Proposition of `oddsplit/REPORT.md` §3 in closed form (same family, uni2); not new as a solvable family.

## 2. Computed

- **Card extended to n = 15, all three phases.** `lowslack.cpp` evaluates P(t) = Σ_S T(R, S) t^S at random t ∈ GF(2^64) by a
  transfer matrix; a nonzero value certifies an odd S. Every word without a tight cut, every phase: n ≤ 15 (223,971 words
  at n = 15); prefix sums ≤ 2: n ≤ 28; ≤ 3: n ≤ 21; ≤ 4: n ≤ 18; ≤ 5: n ≤ 16 (`lowslack_100.txt`). Words with a tight cut follow (T is a product
  over blocks, and every phase is covered).
- **Mixed gaps 2 and 3 fail; only period 3 survives** (direction 3). Exact counterexamples (all T(R, S) even):
  pattern 00101, n = 17; 00100101, n = 15; 001011, n = 14 (commands below). 00101101 has no failure for n ≤ 15.
- **Exact class of row sets** (`forbid.cpp`, `forbid_14.txt`): a row pattern works for every D of size n iff each of its
  factors has an odd S for every D without a tight cut, so the class is factor-, complement- and reversal-closed.
  Working patterns: 90, 134, 192, 272, 374, 498 for n = 9..14; new minimal forbidden words at every length 9..14
  (2, 1, 3, 4, 5, 8 up to symmetry), so no finite list of forbidden factors is in sight. Necessary through n = 14: no run
  longer than 2, no factor 001100. All 25 killing D listed have prefix sums ≤ 3; 24 start 1 1 and end −1 −1.

## 3. Ruled out (what blocks each direction)

1. **RR-split with the fixed rows R** (`rrfixed.cpp`): exists for 3/7, 0/21, 9/61, 26/184, 0/573, 82/1835, 230/5969 of the
   words without a tight cut at n = 6..12. The two leads are not linked; with λ fixed the parity is a sum of many
   products of two LR numbers, not one skew Schur coefficient.
2. **Rule for S** (`rules.py`, `unique.py`): S from the first / last solution (by columns or by diagonals) and S = stones
   k ≡ c (mod 3) fail at n = 9 (for 112 to 471 of the 490 D). "Some S has T = 1" holds for n ≤ 8, fails for 2 D at n = 9.
   "Smallest marked set" (`levels.cpp`): an odd count with |A| = level(D) stones forced into R exists for n ≤ 10, fails
   for 1, 4, 26 words at n = 11, 12, 13 (all at level 2; level-1 words never fail, n ≤ 13).
3. **Induction through interface states** (`states.py`, `bridge.cpp`): the claim is false for partial placements in a
   general state (first failure at slack 2: m = 3 with absolute rows, m = 4 with rows counted inside the state). It holds
   in the two slack-1 states for m ≤ 13 (`bridge.cpp`), where every other row already fails at m = 8. An induction needs an invariant on
   sets of states, as in `l1`; none found.
4. **Single surviving term**: by Theorem 1 a term is a tournament with ties between classes; one marked stone
   (Proposition 3) covers only uni2, two classes of arbitrary size were not reduced to a closed form.

## Recheck (under 10 minutes in total)

```
cd agents/thirds
python3 f4phase.py 6          # Theorem 1, every valid D and every u, n = 6 (seconds; n = 3..6 all pass)
python3 partition.py 6        # Corollary 2, every D, p, S (1 s; n = 3..6 all pass)
python3 formula.py 9 all      # Proposition 3, every n-set with sum n(n-1) (seconds)
python3 verify.py "1 1 0 -1 0 0 0 0 0 0 0 0 1 0 0 -1 -1" 00101 1      # 16 solutions, 7 sets S, all T even
python3 verify.py "1 1 0 -1 0 0 0 0 0 0 1 0 0 -1 -1" 00100101 6      # same
python3 verify.py "1 1 0 0 -1 0 0 0 0 1 0 0 -1 -1" 001011 1          # 32 solutions, 14 sets S, all T even
g++ -O2 -o rrfixed rrfixed.cpp && ./rrfixed 12 100                    # 230 of 5969 (1 s)
sh sweep.sh                   # lowslack_100.txt, 6 minutes (n = 15 unbounded is 4 of them)
```
Longer: `./forbid 14` (12 minutes), `./levels 13` (2 minutes).
