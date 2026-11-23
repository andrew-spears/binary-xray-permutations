# NOTHING: concavity of the solution count along a root direction

Idea (from agents/runrule/COUNT2_REPORT.md, where a + c ≤ 2b holds for the three ways to finish a beginning of
slack 2): with f(μ) = number of solutions of the sum vector μ (tied stones ordered), is
f(μ + α) + f(μ − α) ≤ 2 f(μ) for every root α = e_i − e_j? It would make every neighbour of a solvable vector solvable.

Result: false already at n = 4, also for regular μ: μ = (0, 3, 4, 5), α = e_1 − e_3 (0-based): f = 1, 2, 6 at μ − α, μ, μ + α.
The weaker f(μ) ≥ f(μ ± α)/2 also fails (same example). n = 7: 576 of 1,239 regular tests fail.

Recheck: python3 conc.py 6 (1 second).
