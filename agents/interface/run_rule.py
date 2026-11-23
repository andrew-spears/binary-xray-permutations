"""An induction on n for ALL words, by three shortening rules on the interface machine (found with shorten.py).
F(x) = set of interface states reachable after the prefix x.  Rules u -> v, claim F(xu) inside F(xv) for every prefix x:
  RUN(a, b), a, b >= 1, (a, b) != (1, 1):
        v = (a, a-1, ..., -b)                      a + b + 1 consecutive diagonals whose letters cross zero
        u = (a-1, ..., -(b-1)), letter a-b twice   one stone fewer
  PEAK: v = (1, 0, -1),  u = (0)                   three consecutive diagonals -> one stone
  ZERO: v = (0, -1),     u = (-1)                  drop a 0 that stands before a -1
WHY THEY SUFFICE.  In a valid word that is not all zeros let j be the first negative letter.  Letters drop by at most
1, so e_j = -1, e_{j-1} = 0, e_{j-2} is 0 or 1.  If e_{j-2} = 0: ZERO deletes e_{j-1}.  If e_{j-2} = 1: take the maximal
descending run (a, ..., -b) through (1, 0, -1); apply PEAK if (a, b) = (1, 1), else RUN(a, b).  The shorter word is
again legal and valid (maximality gives the drop rule at both ends; the partial sums inside a descending run are
concave, so they stay >= 0).  The all-zero word is the anti-diagonal.  So the three rules for all x imply the conjecture.
This script (1) checks the rules for every legal prefix x with slacks <= B, (2) reduces every valid word of length <= N
with slacks <= B to the all-zero word using these rules only.        Usage: python3 run_rule.py B [N]"""
import sys
from rewrite import machine, situations, run
def urun(a, b):
    out = []
    for t in range(a - 1, -b, -1):
        out.append(t)
        if t == a - b: out.append(t)
    return tuple(out)
def shorten(w):
    """one shortening step of a valid nonzero word (tuple of letters)"""
    j = next(i for i, e in enumerate(w) if e < 0)
    if w[j - 2] == 0: return w[:j - 1] + w[j:], "ZERO"
    lo = j - 2
    while lo > 0 and w[lo - 1] == w[lo] + 1: lo -= 1
    hi = j
    while hi + 1 < len(w) and w[hi + 1] == w[hi] - 1: hi += 1
    a, b = w[lo], -w[hi]
    if (a, b) == (1, 1): return w[:lo] + (0,) + w[hi + 1:], "PEAK"
    return w[:lo] + urun(a, b) + w[hi + 1:], f"RUN({a},{b})"
def valid(w, B):
    s = 0
    for i, e in enumerate(w):
        if (i == 0 and e < 0) or (i and e < w[i - 1] - 1): return False
        s += e
        if s < 0 or s > B: return False
    return s == 0
if __name__ == "__main__":
    B = int(sys.argv[1]); N = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    step, start = machine(B); sits = situations(B, step, start, 1)
    print(f"B = {B}: {len(sits)} situations (reachable set, slack, last letter)", flush=True)
    rules = [("PEAK", (0,), (1, 0, -1)), ("ZERO", (-1,), (0, -1))]
    rules += [(f"RUN({a},{b})", urun(a, b), tuple(range(a, -b - 1, -1))) for a in range(1, B + 1) for b in range(1, B + 1) if (a, b) != (1, 1)]
    tot = totbad = nr = 0
    for name, u, v in rules:
        t = bad = 0
        for S, s, last, dbl in sits:
            x = run(S, s, last, u, B, step, 1); y = run(S, s, last, v, B, step, 1)
            if x is None or y is None: continue
            t += 1; bad += not x <= y
        if t:
            nr += 1; tot += t; totbad += bad
            if bad or name in ("PEAK", "ZERO"): print(f"  {name:9} tested in {t} situations, fails {bad}", flush=True)
    print(f"  {nr} rules apply somewhere; {tot} (rule, situation) checks, {totbad} failures", flush=True)
    if N:
        cnt = 0; used = {}
        def gen(w, s):
            global cnt
            if w and s == 0 and any(w):
                cnt += 1; x = tuple(w)
                while any(x):
                    y, name = shorten(x); assert valid(y, B) and len(y) < len(x), (x, y, name)
                    used[name.split("(")[0]] = used.get(name.split("(")[0], 0) + 1; x = y
            if len(w) == N: return
            for e in range(0 if not w else max(-s, w[-1] - 1), B - s + 1):
                w.append(e); gen(w, s + e); w.pop()
        gen([], 0)
        print(f"  all {cnt} valid nonzero words of length <= {N} with slacks <= {B} reduce to the all-zero word; steps used: {used}")
