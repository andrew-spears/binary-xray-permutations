# rowcut: NOTHING — odd counts across a horizontal cut of the board

T_a(S) = number of solutions in which the stones of S are exactly those in the top a rows. An odd T_a(S) proves solvability,
and (unlike an odd split) it is one number, not a pair: by the parity theorem it should be a single Littlewood–Richardson
coefficient of a rectangle in a product of two skew Schur functions (not written out or checked).

Tested (`rowcut.cpp`, all valid D of size n, all a, all S):
- every D without a tight cut and n ≤ 8 has an odd T_a(S);
- at n = 9 four D without a tight cut have none: 2 1 0 −1 0 1 0 −1 −2, 2 1 0 −1 −1 1 0 −1 −1, 1 1 0 −1 1 1 0 −1 −2,
  1 1 0 −1 0 1 0 −1 −1 (each is two blocks joined almost tightly);
- D with a tight cut usually have none (1 0 −1 1 0 −1 already), as expected: the count is a product of even numbers.

So the row cut alone is not a criterion. Recheck: `g++ -O2 -o rowcut rowcut.cpp && ./rowcut 9` (10 s).

# thirds: HIT (tested, n ≤ 14) — every third row

**Claim.** Let R = the rows r ≡ 1 (mod 3) (or ≡ 2, or ≡ 0; or the complement). For every valid D there is a set S of
stones such that the number of solutions whose stones in the rows of R are exactly S is odd. (So D is solvable, and D
has an odd split.)

**Range.** Every valid D with n ≤ 14 for r ≡ 1 (158,808 D at n = 14); n ≤ 13 for r ≡ 2; n ≤ 12 for r ≡ 0 and for the
pattern 110. Recheck: `g++ -O2 -o fixedR fixedR.cpp && ./fixedR 12 100` (2 s; n = 13: 18 s; n = 14: 3 min, 1.4 GB).

**What fails.** Every other row (`./fixedR 9 10`: 2 D fail at n = 9, 483 at n = 13); the top a rows (above, n = 9);
periods 4 and 5 except the pattern 10010 (n ≤ 11). With R free, some (R, S) is odd for every D with n ≤ 10
(`rowset.cpp`), and the R that work for every D of a given n are the evenly spread ones (`rowset_R.cpp`: n = 9, three
rows: {1,4,7}, {2,4,7}, {2,5,7}, {2,5,8}, {3,5,8}, {3,6,8}, {3,6,9} only).

**Why 3 (not a proof).** Over a field of characteristic 2 the number of solutions weighted by u_k^(row of stone k) is the
coefficient of x^d in a(ux) · a(x), a = ∏_{i<j} (x_i + x_j) (permanent = determinant), which equals
∏_{i<j} (u_i x_i² + (u_i + u_j) x_i x_j + u_j x_j²): a sum over tournaments with ties, 2 points a game, score d.
With all u_k = 1 the ties vanish and only the evenly spaced D survives. In the field with 4 elements, u_k ∈ {1, ω, ω²}
keeps the ties between stones of different u, and x³ + y³ = (x + y)(x + ωy)(x + ω²y). The claim says the weighted count
is nonzero for some u ∈ {1, ω, ω²}^n. `f4.py n` computes all these character sums (about half are nonzero); no rule
u_k = φ(sign of e_k, e_k mod 3, d_k mod 3, k mod 3, slack mod 3) works for every D (n ≤ 8).
