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
