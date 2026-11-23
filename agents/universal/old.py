"""Direct test of conjecture OLD (REPORT3.md) on exact sets F(x): for an old prefix x (every suffix of j letters has sum <= j) that
ends in a letter 0 or 1 and has slack s >= 11,   F(x) contains J*(s, tail of x)   (J* as in jstar.py; MODE = 3 is conjecture OLD,
MODE = 1 and 2 are the earlier versions that fail or are smaller, see fw.cpp).
Random legal words (every letter >= its predecessor - 1, slack in [0, S], letters <= c) are run through ./fw.
Odd seeds give random letters; even seeds give concatenated falling runs (each letter 0 or 1 below its predecessor, then a rise);
seed 0 gives N words of the steep family  1^i 2 3 .. c^k .. 2 1 0 -1 .. (-j)^m + a short old ending  (final slack > S - 8), which
contains the words that bound the sets from above (1 1 2^k 1 0^m 1 excludes every state with D = 4: run mode 1 to see it).
python3 old.py S c N seed [MODE = 3] [LEN = 3 S]    prints per (slack, tail): number of old prefixes, |J*|, number of states,
the largest number of missing states, and every missing state with one word."""
import sys, os, random, subprocess, collections
S, c, N, seed = map(int, sys.argv[1:5]); mode = sys.argv[5] if len(sys.argv) > 5 else "3"; LEN = int(sys.argv[6]) if len(sys.argv) > 6 else 3 * S
random.seed(seed); words = []
if seed == 0:
    fam = set()
    for c in range(2, 8):
        for i in range(4):
            for k in range(1, S):
                for j in range(3):
                    for m in range(1, S):
                        w = [1] * i + list(range(2, c)) + [c] * k + list(range(c - 1, -j, -1)) + [-j] * m; sl = [sum(w[:n]) for n in range(len(w) + 1)]; y = 0
                        for e in w: y = max(0, y + e - 1)
                        if y > 0 or min(sl) < 0: continue
                        for end in ([1], [0, 1], [1, 1], [1, 0], [0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1], [2, 1, 0], [2, 1, 0, 1], [0, 2, 1, 0, 0]):
                            if S - 8 < sl[-1] + sum(end) and max(sl) <= S and sl[-1] + sum(end) + (2 in end) <= S: fam.add(" ".join(map(str, w + end)))
    words = random.sample(sorted(fam), min(N, len(fam)))
for _ in range(N if seed else 0):
    w = []; s = 0; l = None; p = random.choice([0.05, 0.15, 0.3]); up = random.choice([0.3, 0.45, 0.6])   # p = chance of a letter >= 2; up = chance of 1 among small letters
    q = random.choice([0.5, 0.8, 1.0]); fall = False
    while len(w) < LEN:
        lo = -s if l is None else max(l - 1, -s); hi = max(e for e in range(-s, c + 1) if e <= 0 or s + e * (e + 1) // 2 <= S)   # the word can always come down again
        if seed % 2 == 0:
            if fall and lo <= l and random.random() < 0.85: e = l - 1 if (lo < l and random.random() < q) else l
            else: e = random.randint(lo, max(lo, hi)) if random.random() < 0.5 else random.randint(lo, max(lo, min(hi, 2)))
            fall = True
        elif random.random() < p and hi >= 2: e = random.randint(max(lo, 2), hi)
        elif hi >= 1 and random.random() < up: e = max(lo, 1)
        else: e = random.randint(lo, max(lo, min(hi, 0)))
        e = min(e, hi); w.append(e); s += e; l = e
    words.append(" ".join(map(str, w)))
out = subprocess.run([os.environ.get("FW", "./fw")], input="\n".join(words) + "\n", capture_output=True, text=True, env={"OLD": "1", "JSTAR": mode, "LIST": "30"}).stdout
cnt = collections.Counter(); worst = collections.Counter(); size = {}; bad = {}; word = ""; big = collections.Counter()
for line in out.splitlines():
    if line.startswith("word"): word = line[5:].split(); continue
    if "tail" not in line: continue
    h = line.split(); n, s, tail, nj, nall, nm = int(h[0]), int(h[2]), h[4], int(h[5]), int(h[6]), int(h[8])
    cnt[s, tail] += 1; size[s, tail] = (nj, nall); worst[s, tail] = max(worst[s, tail], nm); big[s] = max(big[s], max(map(int, word[:n])))
    for t in h[10:]: bad.setdefault((s, tail, t), " ".join(word[:n]))
print(f"letters <= {c}, slack <= {S}, {N} words, mode {mode}: {sum(cnt.values())} old prefixes ending in 0 or 1 with slack >= 11, {sum(1 for k in worst if worst[k])} (slack, tail) with a missing state")
for s in sorted(set(k[0] for k in cnt)):
    print(f"  slack {s:2d}:" + "".join(f"  {t} {cnt[s, t]:4d} {size[s, t][0] / size[s, t][1]:.3f}" + (f" MISSING {worst[s, t]}" if worst[s, t] else "") for t in ("11", ".1", "10", "00", ".0") if cnt[s, t]) + f"   (largest letter in such a prefix {big[s]})")
for (s, tail, t), w in sorted(bad.items()): print(f"  missing: slack {s} tail {tail} state {t}   after {w}")
print("HOLDS" if not bad else "FAILS")
