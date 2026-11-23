# Structure of the working row patterns listed by ./forbid (file forbid_<n>.txt).  Usage: python3 lang.py forbid_13.txt
import sys, re, collections
ws = []
for line in open(sys.argv[1]):
    if line.startswith("working"): ws = re.findall(r"\b[01]{3,}\b", line)
n = len(ws[0])
def cl(w):
    c = w.translate(str.maketrans("01", "10")); return {w, w[::-1], c, c[::-1]}
allw = set()
for w in ws: allw |= cl(w)
print("n = %d: working words %d (classes %d)" % (n, len(allw), len(ws)))
def defects(w):   # least number of positions where w differs from being 3-periodic: count i with w[i] != w[i+3]
    return sum(w[i] != w[i + 3] for i in range(len(w) - 3))
h = collections.Counter(defects(w) for w in allw)
print("  number of i with w[i] != w[i+3] -> words:", dict(sorted(h.items())))
runs = collections.Counter()
for w in allw:
    r = [len(m.group()) for m in re.finditer(r"0+|1+", w)]
    runs[max(r)] += 1
print("  longest run -> words:", dict(sorted(runs.items())))
# periods 2 and 3 as factors
for f in ["010101", "0101010", "01010101", "001100", "0011001", "100100", "110110", "1001001", "10010010", "1011011"]:
    print("  words containing %s: %d" % (f, sum(f in w for w in allw)))
# periodic patterns: which (p)^infinity have all factors of length n working?
seen = set()
print("  periodic patterns all of whose factors of length %d work (period <= 9, up to shift, complement, reversal):" % n)
for p in range(1, 10):
    for x in range(1 << p):
        s = format(x, "0%db" % p)
        if any(s == s[:q] * (p // q) for q in range(1, p) if p % q == 0): continue
        rots = {s[i:] + s[:i] for i in range(p)}
        key = min(min(cl(r)) for r in rots)
        if key in seen: continue
        seen.add(key)
        big = s * (n // p + 2)
        if all(big[i:i + n] in allw for i in range(p)): print("    (%s)   gaps between ones: %s" % (key, [len(g) + 1 for g in re.findall(r"(?<=1)0*(?=1)", (key * 3))][:key.count("1")]))
# words by number of ones
print("  number of ones -> words:", dict(sorted(collections.Counter(w.count("1") for w in allw).items())))
