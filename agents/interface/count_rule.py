"""Do the three shortening rules hold with multiplicity?  c_x(t) = number of placements of the prefix x ending in the
interface state t.  Test: c_{xu}(t) <= c_{xv}(t) for every state t (an injection would prove the rule).
Usage: python3 count_rule.py B N    (prefixes x of length <= N, slacks <= B)"""
import sys
from collections import Counter
from run_rule import urun
def succ(mask, B):
    out = []
    for u in range(-B, B + 1):
        bit = B + u
        if mask >> bit & 1: continue
        m = mask | (1 << bit)
        if m & 1: out.append((u, m >> 1))
    return out
def cstep(C, e, B):
    out = Counter()
    for (rm, cm), c in C.items():
        for u, r2 in succ(rm, B):
            v = e - u
            if v < -B or v > B or cm >> (B + v) & 1: continue
            c2 = cm | (1 << (B + v))
            if c2 & 1: out[(r2, c2 >> 1)] += c
    return out
def crun(C, s, last, w, B):
    for e in w:
        if (last is None and e < 0) or (last is not None and e < last - 1): return None
        s += e
        if s < 0 or s > B: return None
        C = cstep(C, e, B); last = e
    return C
if __name__ == "__main__":
    B, N = int(sys.argv[1]), int(sys.argv[2]); base = (1 << B) - 1
    rules = [("PEAK", (0,), (1, 0, -1)), ("ZERO", (-1,), (0, -1))]
    rules += [(f"RUN({a},{b})", urun(a, b), tuple(range(a, -b - 1, -1))) for a in range(1, 4) for b in range(1, 4) if (a, b) != (1, 1)]
    stat = {name: [0, 0, 0, None] for name, u, v in rules}     # tested, set-fail, count-fail, example
    def rec(w, C, s, last):
        for name, u, v in rules:
            a = crun(C, s, last, u, B); b = crun(C, s, last, v, B)
            if a is None or b is None: continue
            st = stat[name]; st[0] += 1
            if any(t not in b for t in a): st[1] += 1
            if any(b[t] < c for t, c in a.items()):
                st[2] += 1
                if st[3] is None: st[3] = (w, [(a[t], b[t]) for t in a if b[t] < a[t]][:3])
        if len(w) == N: return
        for e in range(0 if last is None else max(-s, last - 1), B - s + 1): rec(w + (e,), cstep(C, e, B), s + e, e)
    rec((), Counter({(base, base): 1}), 0, None)
    for name, (t, sf, cf, ex) in stat.items(): print(f"{name:9} tested {t:6}  set fails {sf}  count fails {cf}  {ex if ex else ''}")
