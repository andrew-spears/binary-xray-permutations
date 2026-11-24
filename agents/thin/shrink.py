"""Shrinks a symmetric killer x 0^z x~ of T(a, b): repeatedly deletes a letter of x, a zero (one is kept: 1 -1 is not legal), or lowers a whole run of x,
while the word stays valid and has no walk in T(a, b) (checked by ./steep).   Usage: python3 shrink.py a b z x..."""
import sys, subprocess
a, b, z = sys.argv[1:4]; z = int(z); x = tuple(map(int, sys.argv[4:]))
word = lambda x, z: x + (0,) * z + tuple(-e for e in reversed(x))
ok = lambda x: len(x) > 0 and min(x) >= 1 and x[-1] == 1 and all(q >= p - 1 for p, q in zip(x, x[1:]))
def killers(cands):
    inp = "\n".join(" ".join(map(str, word(*c))) for c in cands) + "\n"
    out = subprocess.run(["./steep", a, b, "-"], input=inp, capture_output=True, text=True).stdout
    bad = {tuple(map(int, l.split(":")[1].split())) for l in out.splitlines() if l.startswith("NO WALK")}
    return [c for c in cands if word(*c) in bad]
while True:
    cands = set()
    for i in range(len(x)):
        cands.add((x[:i] + x[i + 1:], z))
        for j in range(i + 1, len(x) + 1): cands.add((x[:i] + tuple(e - 1 for e in x[i:j]) + x[j:], z))
    if z > 1: cands.add((x, z - 1))
    cands = [c for c in cands if ok(c[0])]
    k = killers(sorted(cands, key=lambda c: (sum(c[0]), len(c[0]))))
    if not k: break
    x, z = min(k, key=lambda c: (sum(c[0]), len(c[0]) * 2 + c[1]))
    print("slack", sum(x), "letters", 2 * len(x) + z, ":", " ".join(map(str, word(x, z))), flush=True)
print("locally minimal killer of T(%s,%s): slack %d, %d letters: %s" % (a, b, sum(x), 2 * len(x) + z, " ".join(map(str, word(x, z)))))
