# NOTHING: reflection positivity (a proof idea for COUNT, card countrule)

Idea. For prefixes x, y ending at the same slack, G[x, y] = N(x mirror(y)) = Σ_t L_x(t) L_y(θ t), θ = mirror of
an interface state. If G were positive semidefinite, Cauchy–Schwarz and chessboard estimates would be available
for witness counts.

Result. G is not positive semidefinite from slack 2 on. Smallest violation of Cauchy–Schwarz: x = (1, 1, 0),
y = (2): N(x mirror x) = 8, N(y mirror y) = 1, N(x mirror y) = 4, and 4² > 8 · 1.
The rank of G equals the number of orbits of states under row/column swap (1, 1, 3, 5, 11, 18 for slack 0…5):
the vectors L_x satisfy no linear relation beyond that symmetry, and G has the signature of θ on that space.

Recheck: python3 rp.py 5 4 (20 seconds).
