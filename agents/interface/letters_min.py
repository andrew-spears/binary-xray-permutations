"""|e| <= 1, any letter order.  Smallest slack-only inductive family (integer program):
choose a set F of interface states with (empty, empty) in F such that every T in F of slack s has, for each letter
e in {-1,0,1} with 0 <= s-e <= B, a predecessor S in F of slack s-e with S -e-> T.  Minimise |F| (or a weighted size).
Prints F per slack as pairs of partitions.   Usage: python3 letters_min.py B [weight: size|adv]"""
import sys, pulp
from itertools import combinations
B = int(sys.argv[1]); mode = sys.argv[2] if len(sys.argv) > 2 else "size"
W = B + 2; base = (1 << W) - 1
def part(mask):
    xs = sorted((j - W + 1 for j in range(2 * W) if mask >> j & 1), reverse=True)
    return tuple(x + i for i, x in enumerate(xs) if x + i > 0)
def excess(mask): return sum(part(mask))
masks = {}
for comb in combinations(range(2 * W), W):
    m = sum(1 << j for j in comb)
    if m & 3 != 3: continue                      # excess <= B < W-1 keeps the two lowest positions filled
    ex = excess(m)
    if ex <= B: masks.setdefault(ex, []).append(m)
states = {s: [(r, c) for a in range(s + 1) for r in masks[a] for c in masks[s - a]] for s in range(B + 1)}
def succ(S, e):
    rm, cm = S; out = []
    for u in range(-W, W):
        if rm >> (W + u) & 1: continue
        v = e - u
        if v < -W or v >= W or cm >> (W + v) & 1: continue
        r2 = rm | 1 << (W + u); c2 = cm | 1 << (W + v)
        if r2 & c2 & 1: out.append((r2 >> 1, c2 >> 1))
    return out
pred = {}
for s in range(B + 1):
    for S in states[s]:
        for e in (-1, 0, 1):
            if not 0 <= s + e <= B: continue
            for T in succ(S, e): pred.setdefault((T, e), []).append(S)
prob = pulp.LpProblem("F", pulp.LpMinimize)
x = {S: pulp.LpVariable(f"x{i}_{j}", cat="Binary") for i in range(B + 1) for j, S in enumerate(states[i])}
adv = lambda m: bin(m >> W).count("1")
wt = (lambda S: 1) if mode == "size" else (lambda S: 1 + 10 * max(0, adv(S[0]) + adv(S[1]) - 2))
prob += pulp.lpSum(wt(S) * x[S] for S in x)
prob += x[(base, base)] == 1
for s in range(B + 1):
    for T in states[s]:
        for e in (-1, 0, 1):
            if not 0 <= s - e <= B: continue
            prob += x[T] <= pulp.lpSum(x[S] for S in pred.get((T, e), []))
prob.solve(pulp.PULP_CBC_CMD(msg=0, timeLimit=200))
print("status", pulp.LpStatus[prob.status])
fmt = lambda p: "".join(map(str, p)) or "."
for s in range(B + 1):
    F = sorted((part(r), part(c)) for (r, c) in states[s] if x[(r, c)].value() > 0.5)
    print(f"slack {s}: {len(F)} of {len(states[s])}:", "  ".join(fmt(a) + "|" + fmt(b) for a, b in F))
