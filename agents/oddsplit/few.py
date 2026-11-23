"""Which words without a tight cut have the fewest RR-splits?  Usage: python3 few.py n   (needs ./esplit)"""
import sys, subprocess, re
from ext import words
n = int(sys.argv[1]); out = []
for e in words(n, False):
    if not any(e) or any(sum(e[:k]) == 0 for k in range(1, n)): continue
    t = subprocess.run(["./esplit", "w"] + [str(x) for x in e], capture_output=True, text=True).stdout
    h, r, o = map(int, re.search(r"H (\d+), RR not H (\d+), only RC/CR/CC (\d+)", t).groups()); out.append((h + r, h + r + o, e))
out.sort(); print(f"n = {n}: {len(out)} words; fewest RR-splits (RR, all E, word), out of {2**n - 2} sets S:")
for q in out[:4]: print("  ", q)
print("   most:", out[-1])
