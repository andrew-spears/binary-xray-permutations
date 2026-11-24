"""Cuts of slack 1 factor (PROVED in COUNT_REPORT.md section 2; this is the numerical check).
For a word w = x y with slack 1 after x:      2 N(x y) = N(x 0 -1) * N(1 0 y).
For w = x b y with slack 1 after x and after x b:   N(x b y) * 2 = N(x y') ... is checked in the form
     N(x b y) * N(1 0 0 -1) = N(1 0 b 0 -1) * N(x 0 y)      (N(1 0 0 -1) = 2; the ratio does not depend on x, y).
Usage: python3 slack1.py n"""
import sys
from countlib import solutions
n = int(sys.argv[1]); N = {w: len(s) for w, s in solutions(n).items()}
cuts = bad = blocks = badb = 0
for w in N:
    pre = [sum(w[:i]) for i in range(len(w) + 1)]; ones = [k for k in range(1, len(w)) if pre[k] == 1]
    for k in ones:
        a, b = w[:k] + (0, -1), (1, 0) + w[k:]
        if len(a) > n or len(b) > n: continue
        cuts += 1; bad += 2 * N[w] != N.get(a, 0) * N.get(b, 0)
    for k in ones:
        for l in ones:
            if l <= k: continue
            blk = (1, 0) + w[k:l] + (0, -1); w0 = w[:k] + (0,) + w[l:]
            if len(blk) > n or len(w0) > n: continue
            blocks += 1; badb += 2 * N[w] != N.get(blk, 0) * N.get(w0, 0)
print(f"words of length <= {n}: {len(N)};  cuts of slack 1 tested: {cuts}, identity fails: {bad};  blocks between two cuts of slack 1: {blocks}, identity fails: {badb}")
