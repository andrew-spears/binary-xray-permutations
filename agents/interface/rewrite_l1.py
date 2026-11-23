"""Monotone rewrites (see rewrite.py) inside the class of letters -1, 0, +1 (card l1).
Prefixes x range over legal words with letters in {-1,0,1} (no repeated diagonal: '+ -' adjacent is not allowed) and slack <= B.
Lists every u -> v with len(u) < len(v) <= maxlen, same sum, F(xu) a subset of F(xv) whenever both are legal.
If such a rule holds for all x, a word x v y is solvable as soon as the shorter word x u y is (when x u y is legal).
Usage: python3 rewrite_l1.py B maxlen [B2]     (B2: recheck the survivors at the larger bound B2)"""
import sys
from itertools import product
from rewrite import machine
def sits_l1(B):
    step, start = machine(B)
    s0 = (frozenset([start]), 0, None); seen = {s0}; todo = [s0]
    while todo:
        S, s, last = todo.pop()
        for e in (-1, 0, 1):
            if s + e < 0 or s + e > B or (last == 1 and e == -1): continue
            x = (step(S, e), s + e, e)
            if x not in seen: seen.add(x); todo.append(x)
    return seen, step
def run(S, s, last, u, B, step):
    for e in u:
        if s + e < 0 or s + e > B or (last == 1 and e == -1): return None
        S = step(S, e); s += e; last = e
    return S
def test(rules, B):
    sits, step = sits_l1(B); out = []
    for u, v in rules:
        t = bad = 0
        for S, s, last in sits:
            a = run(S, s, last, u, B, step); b = run(S, s, last, v, B, step)
            if a is None or b is None: continue
            t += 1
            if not a <= b: bad += 1; break
        if t >= 10 and not bad: out.append((u, v, t))
    return out, len(sits)
if __name__ == "__main__":
    B, maxlen = int(sys.argv[1]), int(sys.argv[2])
    strings = [w for n in range(0, maxlen + 1) for w in product((-1, 0, 1), repeat=n)]
    rules = [(u, v) for u in strings for v in strings if len(u) < len(v) and sum(u) == sum(v)]
    good, ns = test(rules, B)
    print(f"B = {B}: {ns} situations, {len(good)} of {len(rules)} rules survive", flush=True)
    if len(sys.argv) > 3:
        B2 = int(sys.argv[3]); good, ns = test([(u, v) for u, v, _ in good], B2)
        print(f"B = {B2}: {ns} situations, {len(good)} survive", flush=True)
    sym = lambda w: "".join("-0+"[e + 1] for e in w) or "(empty)"
    for u, v, t in good: print(f"  {sym(u):>6} -> {sym(v):<6} ({t} situations)")
