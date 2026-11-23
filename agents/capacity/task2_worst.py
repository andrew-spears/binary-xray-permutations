import sys, math, time, json
from caplib import *
out = {}
for n in map(int, sys.argv[1:]):
    t0 = time.time()
    seqs = strong_score_sequences(n)
    rows = []
    for s in seqs:
        rev = tuple(n - 1 - v for v in reversed(s))
        if s < rev:  # keep one of each mirror pair (lex-larger score vector)
            continue
        D = D_from_scores(s, n)
        W = witnesses(D, n)
        lc, t, res = logcap(D, n)
        logR = math.log(W) + n * math.log(n) - math.lgamma(n + 1) - lc if W > 0 else -math.inf
        rows.append(dict(s=list(s), D=D, W=W, logcap=lc, R=math.exp(logR),
                         c=math.exp((math.log(W) - lc) / n) if W else 0, conv=bool(res.success)))
    rows.sort(key=lambda r: r["R"])
    json.dump(rows, open(f"task2_n{n}.json", "w"), indent=0)
    print(f"n={n}: {len(seqs)} strong seqs, {len(rows)} up to mirror, {time.time()-t0:.1f}s, minW={min(r['W'] for r in rows)}")
    for r in rows[:5]:
        print("  R=%.4f W=%d cap=%.3f s=%s D=%s" % (r["R"], r["W"], math.exp(r["logcap"]), r["s"], r["D"]))
    print("  isPn(worst):", rows[0]["D"] == Pn(n), " max R=%.2f" % rows[-1]["R"],
          " nonconverged:", sum(not r["conv"] for r in rows), flush=True)
