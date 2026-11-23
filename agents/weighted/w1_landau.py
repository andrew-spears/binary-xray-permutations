"""Weighted x-ray instances, widths in {1,2}: a width-1 blocks, b width-2 blocks, W=a+2b.
Row order and column order of blocks both free; need col_start - row_start = target.
Compares achievable instances against
  block:  sum_S w*t >= -V(W-V) for every block subset S of width V, total sum w*t = 0
  point:  ordinary Landau on expanded D = singletons U {c-1, c+1}.
Usage: python3 w1_landau.py Wmax [block|point]
"""
import sys, itertools, pickle
MODE = sys.argv[2] if len(sys.argv) > 2 else "block"
from math import comb

def arrangements(a, b):
    for pos in itertools.combinations(range(a + b), b):
        seq = [1] * (a + b)
        for p in pos: seq[p] = 2
        yield seq

def starts(seq):
    s1, s2, x = [], [], 0
    for w in seq:
        (s1 if w == 1 else s2).append(x); x += w
    return s1, s2

def achievable(a, b):
    out = set()
    arrs = [starts(s) for s in arrangements(a, b)]
    p1 = list(itertools.permutations(range(a)))
    p2 = list(itertools.permutations(range(b)))
    for r1, r2 in arrs:
        for c1, c2 in arrs:
            T1 = set(tuple(sorted(c1[p[i]] - r1[i] for i in range(a))) for p in p1)
            T2 = set(tuple(sorted(c2[p[i]] - r2[i] for i in range(b))) for p in p2)
            for t1 in T1:
                for t2 in T2:
                    out.add((t1, t2))
    return out

def g(a_, b_, W):
    mn = comb(a_, 2) + a_ * b_ + 2 * comb(b_, 2)
    mx = (a_ + b_) * W - comb(a_ + 1, 2) - a_ * b_ - b_ * (b_ + 1)
    return mx - mn

def landau_block(t1, t2, a, b, W):
    # whole blocks, width-weighted: sum_S w*t >= -V(W-V), V = width of S; total 0
    if sum(t1) + 2 * sum(t2) != 0: return False
    P1 = [0]; [P1.append(P1[-1] + x) for x in t1]
    P2 = [0]; [P2.append(P2[-1] + 2 * x) for x in t2]
    for i in range(a + 1):
        for j in range(b + 1):
            V = i + 2 * j
            if P1[i] + P2[j] < -V * (W - V): return False
    return True

def expand(t1, t2):
    return sorted(list(t1) + [c - 1 for c in t2] + [c + 1 for c in t2])

def landau_point(t1, t2, a, b, W):
    D = expand(t1, t2); s = 0
    for k, d in enumerate(D, 1):
        s += d
        if s < -k * (W - k): return False
    return s == 0

landau = landau_point if MODE == "point" else landau_block

def sorted_tuples(k, lo, hi, W, w):
    # nondecreasing tuples with single-class prefix/suffix pruning (necessary)
    res = []
    def rec(cur, mn, s):
        i = len(cur)
        if i == k: res.append(tuple(cur)); return
        for v in range(mn, hi + 1):
            # prefix lower bound: single class i+1 elements
            if s + w * v < -(w * (i + 1)) * (W - w * (i + 1)): continue
            cur.append(v); rec(cur, v, s + w * v); cur.pop()
    rec([], lo, 0)
    return res

def main():
    Wmax = int(sys.argv[1])
    results = {}
    for W in range(2, Wmax + 1):
        for b in range(1, W // 2 + 1):
            a = W - 2 * b
            ach = achievable(a, b)
            L1 = sorted_tuples(a, -(W - 1), W - 1, W, 1)
            L2 = sorted_tuples(b, -(W - 2), W - 2, W, 2)
            val = set((t1, t2) for t1 in L1 for t2 in L2 if landau(t1, t2, a, b, W))
            bad = [x for x in ach if x not in val]
            fails = sorted(val - ach)
            results[(a, b)] = (len(val), len(ach), fails)
            print(f"W={W} a={a} b={b}: landau-valid={len(val)} achievable={len(ach)} "
                  f"necessity-violations={len(bad)} failures={len(fails)}", flush=True)
            for f in fails[:3]: print("   fail:", f, flush=True)
            with open(f"w1_results_{MODE}.pkl", "wb") as fh: pickle.dump(results, fh)

if __name__ == "__main__":
    main()
