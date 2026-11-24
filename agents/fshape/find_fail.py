"""Find words for the failures of ZERO / RUN(2,1) / (0)->(0,0) at slack bound B (they first appear at B = 14 / 14 / 8).
Same machine as ../interface/run_rule.py but each situation remembers one word.  Usage: python3 find_fail.py B [out.json]"""
import sys, json
sys.path.insert(0, "../interface")
from rewrite import machine, run
B = int(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else None
step, start = machine(B)
s0 = (frozenset([start]), 0, None); word = {s0: ()}; todo = [s0]
while todo:
    S, s, last = todo.pop()
    lo = 0 if last is None else max(-s, last - 1)
    for e in range(lo, B - s + 1):
        x = (step(S, e), s + e, e)
        if x not in word: word[x] = word[(S, s, last)] + (e,); todo.append(x)
print(len(word), "situations", flush=True)
rules = [("ZERO", (-1,), (0, -1)), ("RUN(2,1)", (1, 1, 0), (2, 1, 0, -1)), ("PEAK", (0,), (1, 0, -1)), ("ZZ", (0,), (0, 0))]
res = []
for name, u, v in rules:
    t = bad = 0
    for (S, s, last), w in word.items():
        x = run(S, s, last, u, B, step, 1); y = run(S, s, last, v, B, step, 1)
        if x is None or y is None: continue
        t += 1
        if not x <= y:
            bad += 1; miss = sorted(x - y)
            print(name, "fails after", w, "missing", len(miss), "of", len(x), miss[:3], flush=True)
            res.append((name, w, miss))
    print(name, t, bad, flush=True)
if out: json.dump(res, open(out, "w"))
