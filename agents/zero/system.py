"""The replacement system for ZERO / PEAK / RUN (see REPORT.md).
Word-level step used at the first negative letter of a valid word  x (a, ..., 1) 0^m (-1, ..., -b) y  (runs maximal):
  m >= 3            delete one 0                                      needs I1 : (0,0,-1) -> (0,0,0,-1)
  m = 2             replace the block by urun(a,b)  [(0) if a=b=1]    needs I2(a,b): urun(a,b) -> (a..1,0,0,-1..-b)
  m = 1, a < b      replace the block by urun(a,b)                    needs I3(a,b): urun(a,b) -> (a..-b)
  m = 1, a > b      the same step, read from the right                needs I3(b,a)
  m = 1, a = b >= 2 the same step                                     needs I3(a,a)
  m = 1, a = b = 1  x empty: trivial;  x ends in 0:                   needs I4 : (0,0) -> (0,1,0,-1)
                    x ends in 1: read from the right                  needs I5 : (0,-1) -> (1,0,-1,-1)
"needs u -> v" means F(x u) inside F(x v) for every legal prefix x.  "Read from the right": the mirror word
(reverse and negate) turns the inclusion on the suffix side into an inclusion on the prefix side (REPORT.md, duality).
STATUS: every needed inclusion holds at slack bound 14 (this script), but I1, I2(3,1), I3(1,2), I3(2,2) and I4 FAIL
between slack 16 and 23 (by_7_24.txt, by_8_20.txt), so this is not a proof route; see REPORT.md.
Usage: python3 system.py B        tests every needed inclusion (and the old rules, for comparison) with ./rule B
       python3 system.py B N      also reduces every valid word of length <= N, slacks <= B, to the all-zero word"""
import sys, subprocess
def urun(a, b):
    if (a, b) == (1, 1): return (0,)
    out = []
    for t in range(a - 1, -b, -1):
        out.append(t)
        if t == a - b: out.append(t)
    return tuple(out)
def block(a, b, m): return tuple(range(a, 0, -1)) + (0,) * m + tuple(range(-1, -b - 1, -1))
def shorten(w):
    j = next(i for i, e in enumerate(w) if e < 0)
    z = j
    while w[z - 1] == 0: z -= 1
    m = j - z
    if m >= 3: return w[:j - 1] + w[j:], "I1"
    lo = z - 1
    while lo > 0 and w[lo - 1] == w[lo] + 1: lo -= 1
    hi = j
    while hi + 1 < len(w) and w[hi + 1] == w[hi] - 1: hi += 1
    a, b = w[lo], -w[hi]
    new = w[:lo] + urun(a, b) + w[hi + 1:]
    if m == 2: return new, "I2"
    if (a, b) != (1, 1): return new, "I3" if a <= b else "I3 from the right"
    if lo == 0: return new, "trivial"
    return new, "I4" if w[lo - 1] == 0 else "I5 from the right"
def valid(w, B):
    s = 0
    for i, e in enumerate(w):
        if (i == 0 and e < 0) or (i and e < w[i - 1] - 1): return False
        s += e
        if s < 0 or s > B: return False
    return s == 0
def fmt(u, v): return ",".join(map(str, u)) + ":" + ",".join(map(str, v))
if __name__ == "__main__":
    B = int(sys.argv[1]); N = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    R = range(1, 7)
    rules = [("I1", (0, 0, -1), (0, 0, 0, -1))]
    rules += [(f"I2({a},{b})", urun(a, b), block(a, b, 2)) for a in R for b in R]
    rules += [(f"I3({a},{b})", urun(a, b), block(a, b, 1)) for a in R for b in R if a <= b and b > 1]
    rules += [("I4", (0, 0), (0, 1, 0, -1)), ("I5", (0, -1), (1, 0, -1, -1))]
    rules += [("old ZERO", (0, -1), (0, 0, -1)), ("old PEAK", (0,), (1, 0, -1))]
    rules += [(f"old RUN({a},{b})", urun(a, b), block(a, b, 1)) for a in R for b in R if a > b]
    out = subprocess.run(["./rule", str(B)] + [fmt(u, v) for _, u, v in rules], capture_output=True, text=True).stdout
    res = [l for l in out.splitlines() if "tested" in l]
    bad = 0
    for (name, u, v), l in zip(rules, res):
        t, f = l.split("tested ")[1].split(", fails ")
        if int(t): print(f"{name:14} {str(u):30} -> {str(v):36} situations tested {t:>5} fails {f}")
        if not name.startswith("old"): bad += int(f)
    print("failures among the needed inclusions I1..I5:", bad)
    if N:
        cnt = 0; used = {}
        def gen(w, s):
            global cnt
            if w and s == 0 and any(w):
                cnt += 1; x = tuple(w)
                while any(x):
                    y, name = shorten(x); assert valid(y, B) and len(y) < len(x), (x, y, name)
                    used[name] = used.get(name, 0) + 1; x = y
            if len(w) == N: return
            for e in range(0 if not w else max(-s, w[-1] - 1), B - s + 1):
                w.append(e); gen(w, s + e); w.pop()
        gen([], 0)
        print(f"all {cnt} valid nonzero words of length <= {N} with slacks <= {B} reduce to the all-zero word; steps used: {used}")
