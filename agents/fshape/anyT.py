"""Does exactness of the parity test need the prefix to be legal?  Random (A, B, T): k rows, k columns in 1..N, k distinct sums
with sum(T) = sum(A) + sum(B).  Usage: python3 anyT.py k N samples"""
import sys, random
from core import *
from lp import lp, plp
k, N, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); random.seed(1)
def has(A, B, T):
    S = {(0, 0)}
    for t in T: S = step(S, t)
    return (mask(A), mask(B)) in S
tot = unr = lpf = par = 0; ex = None
while tot < n:
    A = sorted(random.sample(range(1, N + 1), k)); B = sorted(random.sample(range(1, N + 1), k))
    T = sorted(random.sample(range(2, 2 * N + 1), k))
    if sum(T) != sum(A) + sum(B): continue
    tot += 1
    if has(A, B, T): continue
    unr += 1
    if lp(mask(A), mask(B), T):
        lpf += 1
        if plp(mask(A), mask(B), T, 2):
            par += 1
            if ex is None: ex = (A, B, T)
print(f"k = {k}, N = {N}: {tot} random (A, B, T) with matching totals; unreachable {unr}; of these LP-feasible {lpf}; pass the parity test {par}; first: {ex}")
