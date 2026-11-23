"""Exceptions made by one staircase (REPORT3.md, "How far to trust it").  Words  q + (k, k-1, .., -j) + 0^z + t  with q in {empty, 1, 1 1}
(with TWO=1: q = a first staircase (k1, .., a), 3 <= k1 <= KMAX, a >= 0, followed by a rise to k),
z the number of zeros needed to make the prefix old (0 if j >= k - 2), t a word of N letters 0 / 1; for every old prefix ending
in 0 or 1 with slack >= S0 the states of J*(slack, tail) (MODE 3 of jstar.py) that are not in F(x).
Usage: python3 stair.py KMIN KMAX [N = 3] [S0 = 9]"""
import sys, os, itertools, subprocess, collections
K0, K1 = int(sys.argv[1]), int(sys.argv[2]); N = int(sys.argv[3]) if len(sys.argv) > 3 else 3; S0 = sys.argv[4] if len(sys.argv) > 4 else "9"; SMAX = int(os.environ.get("SMAX", "30"))
words = []
for k in range(K0, K1 + 1):
    for q in ([list(range(k1, a - 1, -1)) for k1 in range(3, K1 + 1) for a in range(0, min(k, k1 + 1))] if os.environ.get("TWO") else ([], [1], [1, 1])):
        for j in range(0, k + 2):
            w = q + list(range(k, -j - 1, -1)); s = sum(w)
            if min(sum(w[:i]) for i in range(len(w) + 1)) < 0 or max(sum(w[:i]) for i in range(len(w) + 1)) > SMAX: continue
            y = 0
            for e in w: y = max(0, y + e - 1)
            for t in itertools.product((0, 1), repeat=N): words.append(" ".join(map(str, w + [0] * y + list(t))))
out = subprocess.run(["./fw"], input="\n".join(words) + "\n", capture_output=True, text=True, env={"OLD": "1", "JSTAR": "3", "LIST": "60", "S0": S0}).stdout
bad = {}; n = 0
for line in out.splitlines():
    if line.startswith("word"): word = line[5:].split(); continue
    if "tail" not in line: continue
    h = line.split(); n += 1
    for t in h[10:]: bad.setdefault((int(h[2]), h[4], t), " ".join(word[:int(h[0])]))
print(f"k = {K0}..{K1}: {len(words)} words, {n} old prefixes ending in 0 or 1 with slack >= {S0}, {len(bad)} (slack, tail, state) missing")
by = collections.defaultdict(list)
for (s, tail, t), w in sorted(bad.items()): by[w].append((s, tail, t))
for w, l in sorted(by.items(), key=lambda kv: (len(kv[0].split()), kv[0])): print(f"  after {w}  (slack {l[0][0]}, tail {l[0][1]}): " + " ".join(t for _, _, t in l))
