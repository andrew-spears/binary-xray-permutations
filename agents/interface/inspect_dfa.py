import sys
from slack_dfa import run, word_of
B = int(sys.argv[1])
bad, seen, nstates, maxset = run(B)
# number of pairs of partitions of total size s
def parts(n, m=None):
    m = n if m is None else m
    if n == 0: return 1
    return sum(parts(n - j, j) for j in range(1, min(n, m) + 1))
p2 = [sum(parts(i) * parts(s - i) for i in range(s + 1)) for s in range(B + 1)]
rows = {}
for st in seen:
    eprev, S, sig = st
    w = word_of(seen, st)
    rows.setdefault((sig, eprev, len(S)), []).append(w)
for key in sorted(rows, key=lambda t: (t[0], t[1] if t[1] is not None else -99, t[2])):
    sig, eprev, sz = key
    ws = rows[key]
    print(f"sigma={sig} eprev={eprev} |S|={sz}/{p2[sig]}  #dfa={len(ws)}  shortest word={min(ws, key=len)}")
