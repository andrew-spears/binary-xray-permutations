# Where does 'three chains' bite?  For each valid word: all solutions vs solutions with at most three chains.
import sys
from blocks import words, sols, lis
n = int(sys.argv[1]); rows = []
for w in words(n):
    D = [e + 2 * (k + 1) - n - 1 for k, e in enumerate(w)]
    ss = sols(D, n); c3 = sum(1 for p in ss if lis(p) <= 3)
    if c3 < len(ss): rows.append((c3, len(ss), w))
rows.sort()
print("n =", n, ":", len(rows), "words have a solution that needs more than three chains")
print("fewest three-chain solutions among them:")
for c3, tot, w in rows[:12]: print("  ", c3, "of", tot, ":", *w)
print("smallest share:")
for c3, tot, w in sorted(rows, key=lambda x: x[0] / x[1])[:6]: print("  ", c3, "of", tot, ":", *w)
