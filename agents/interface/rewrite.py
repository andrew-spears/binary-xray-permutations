"""Monotone rewrites of words on the interface machine.
F(x) = set of interface states reachable after the prefix x (letters e_k; slack = sum of letters).
A rewrite u -> v (two letter strings with the same sum) is MONOTONE if F(xu) is a subset of F(xv) for every prefix x
after which both xu and xv are legal prefixes with all slacks <= B.  Then for every continuation y legal after both,
'xuy is solvable' implies 'xvy is solvable': xvy is the easier word.
Legal: e_1 >= 0, e_{k+1} >= e_k - gap, all partial sums >= 0   (gap = 1: distinct diagonals; gap = 2: repeats allowed,
which this script only uses to let a rewrite pass through a doubled diagonal -- no triple is ever created by len-1/2 strings
checked here unless stated).
Usage: python3 rewrite.py B [maxlen] [gap]"""
import sys
from itertools import product
def machine(B):
    def succ(mask):
        out = []
        for u in range(-B, B + 1):
            bit = B + u
            if mask >> bit & 1: continue
            m = mask | (1 << bit)
            if not (m & 1): continue
            out.append((u, m >> 1))
        return out
    cache = {}
    def step1(st, e):
        key = (st, e)
        if key not in cache:
            rm, cm = st; out = set()
            for u, r2 in succ(rm):
                v = e - u
                if v < -B or v > B or cm >> (B + v) & 1: continue
                c2 = cm | (1 << (B + v))
                if c2 & 1: out.add((r2, c2 >> 1))
            cache[key] = frozenset(out)
        return cache[key]
    def step(S, e):
        out = set()
        for st in S: out |= step1(st, e)
        return frozenset(out)
    base = (1 << B) - 1
    return step, (base, base)
def situations(B, step, start, gap=1):
    """all (F, slack, last letter) over legal prefixes with slacks <= B (no completability pruning)"""
    s0 = (frozenset([start]), 0, None); seen = {s0}; todo = [s0]
    while todo:
        S, s, last = todo.pop()
        lo = -s if last is None else max(-s, last - gap)
        if last is None: lo = 0
        for e in range(lo, B - s + 1):
            x = (step(S, e), s + e, e)
            if x not in seen: seen.add(x); todo.append(x)
    return seen
def run(S, s, last, u, B, step, gap):
    for e in u:
        if last is not None and e < last - gap: return None
        if last is None and e < 0: return None
        s += e
        if s < 0 or s > B: return None
        S = step(S, e); last = e
    return S
if __name__ == "__main__":
    B = int(sys.argv[1]); maxlen = int(sys.argv[2]) if len(sys.argv) > 2 else 2; gap = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    step, start = machine(B); sits = situations(B, step, start, gap)
    print(f"B = {B}: {len(sits)} situations", flush=True)
    strings = [w for n in range(0, maxlen + 1) for w in product(range(-3, 4), repeat=n)]
    for u in strings:
        for v in strings:
            if u == v or sum(u) != sum(v): continue
            tested = bad = 0
            for S, s, last in sits:
                a = run(S, s, last, u, B, step, gap); b = run(S, s, last, v, B, step, gap)
                if a is None or b is None: continue
                tested += 1
                if not a <= b: bad += 1
            if tested >= 20 and bad == 0: print(f"MONOTONE  {u} -> {v}   ({tested} situations)", flush=True)
