# NOTHING: reflection positivity (a proof idea for COUNT, card countrule)

Idea. For prefixes x, y ending at the same slack, G[x, y] = N(x mirror(y)) = Σ_t L_x(t) L_y(θ t), θ = mirror of
an interface state. If G were positive semidefinite, Cauchy–Schwarz and chessboard estimates would be available
for witness counts.

Result. G is not positive semidefinite from slack 2 on. Only prefixes with last letter ≤ 0 are used, so that every
join x mirror(y) is a legal word (an earlier version also joined illegal pairs, which can repeat a diagonal).
Smallest violation of Cauchy–Schwarz: x = (1, 1, 0), y = (1, 1, 0, 0): N(1,1,0,0,−1,−1) = 8,
N(1,1,0,0,0,0,−1,−1) = 16, N(1,1,0,0,0,−1,−1) = 12, and 12² > 8 · 16.
Rank of G for slack 0…4 with prefixes of length ≤ 6: 1, 1, 3, 5, 10; it is at most the number of orbits of states
under row/column swap, and G has the signature of θ on the span of the vectors L_x.

Recheck: python3 rp.py 6 4 (20 seconds).
