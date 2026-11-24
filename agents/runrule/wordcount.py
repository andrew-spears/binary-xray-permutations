"""Word-level counts.  N(w) = number of permutation matrices whose diagonal word is w.  For every valid nonzero word w
(slacks <= B, length <= N) and its shortening w' = shorten(w) by PEAK / ZERO / RUN (../interface/run_rule.py):
is N(w') <= N(w)?  Also the same for every single application x u y -> x v y of the three rules inside the range, and for DEL0
(delete any one letter 0 whose removal leaves a legal word).
Usage: python3 wordcount.py B N"""
import sys
from collections import Counter, defaultdict
sys.path.insert(0, "../interface")
from count_rule import cstep
from run_rule import shorten, urun
B, N = int(sys.argv[1]), int(sys.argv[2]); base = (1 << B) - 1; cnt = {}
def rec(w, C, s, last):
    if s == 0: cnt[w] = C[(base, base)]
    if len(w) == N: return
    for e in range(0 if last is None else max(-s, last - 1), B - s + 1): rec(w + (e,), cstep(C, e, B), s + e, e)
rec((), Counter({(base, base): 1}), 0, None)
ws = [w for w in cnt if any(w)]
print(f"valid nonzero words (slacks <= {B}, length <= {N}): {len(ws)}; unsolvable: {sum(cnt[w] == 0 for w in ws)}")
stat = defaultdict(lambda: [0, 0, None, None])       # tested, violations, example, least ratio (ratio, longer, shorter)
def note(st, w, w2):
    st[0] += 1; r = (cnt[w] / cnt[w2] if cnt[w2] else float('inf'), w, w2)
    if st[3] is None or r[0] < st[3][0] or (r[0] == st[3][0] and len(w) < len(st[3][1])): st[3] = r
    if cnt[w2] > cnt[w]: st[1] += 1; st[2] = st[2] or (w, cnt[w], w2, cnt[w2])
for w in ws:
    w2, name = shorten(w); note(stat[name.split("(")[0] + " (canonical step)"], w, w2)
rules = [("PEAK", (0,), (1, 0, -1)), ("ZERO", (-1,), (0, -1))]
rules += [(f"RUN({a},{b})", urun(a, b), tuple(range(a, -b - 1, -1))) for a in range(1, B + 1) for b in range(1, B + 1) if (a, b) != (1, 1)]
for w in ws:
    for name, u, v in rules:
        for i in range(len(w) - len(v) + 1):
            if w[i:i + len(v)] == v:
                w2 = w[:i] + u + w[i + len(v):]
                if w2 not in cnt: continue
                note(stat[name + " (anywhere)"], w, w2)
    for i in range(len(w)):                         # DEL0: delete any letter 0 whose removal leaves a legal word
        if w[i] == 0 and w[:i] + w[i + 1:] in cnt and any(w[:i] + w[i + 1:]): note(stat["DEL0 (anywhere)"], w, w[:i] + w[i + 1:])
for name in sorted(stat):
    t, f, ex, r = stat[name]
    print(f"{name:22} tested {t:6}  N(shorter) > N(longer): {f}  least N(longer)/N(shorter) = {r[0]:.3f} at {r[1]} <- {r[2]}  {'VIOLATION longer %s N=%d, shorter %s N=%d' % ex if ex else ''}")
