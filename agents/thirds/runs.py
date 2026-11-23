# Run-length form of the working row patterns.  A pattern is a sequence of runs of equal letters (lengths 1 or 2; complement
# = same run lengths).  Prints the run-length factors of length k that occur strictly inside some working word (not touching
# its first or last run), and those that never do.     Usage: python3 runs.py forbid_14.txt
import sys, re, itertools
ws = []
for line in open(sys.argv[1]):
    if line.startswith("working"): ws = re.findall(r"\b[01]{3,}\b", line)
n = len(ws[0]); allw = set()
for w in ws:
    c = w.translate(str.maketrans("01", "10")); allw |= {w, w[::-1], c, c[::-1]}
rl = {"".join(str(len(m.group())) for m in re.finditer(r"0+|1+", w)) for w in allw}
for k in range(2, 9):
    inside = set()
    for r in rl:
        for i in range(1, len(r) - k): inside.add(r[i:i + k])
    out = sorted("".join(t) for t in itertools.product("12", repeat=k) if "".join(t) not in inside)
    # minimal: no proper factor already missing
    if k == 2: missing = set()
    mins = [f for f in out if not any(f[i:i + j] in missing for j in range(2, k) for i in range(k - j + 1))]
    missing |= set(out)
    print("n = %d, run factors of length %d: inside %d of %d; new minimal missing: %s" % (n, k, len(inside), 2 ** k, " ".join(mins)))
