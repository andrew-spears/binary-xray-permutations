# Which words have a two-chain solution?  (python, small n.)  Prints the words without one, by class.
import sys
from blocks import words, sols, lis
n = int(sys.argv[1]); bad = []
for w in words(n):
    D = [e + 2 * (k + 1) - n - 1 for k, e in enumerate(w)]
    if not any(lis(p) <= 2 for p in sols(D, n)): bad.append(w)
pm1 = [w for w in bad if max(w) <= 1 and min(w) >= -1]
print("n =", n, ":", len(bad), "words without a two-chain solution;", len(pm1), "of them with letters in {-1, 0, 1}")
for w in pm1[:10]: print("   ", *w)
one = [w for w in bad if (max(w) <= 1 or min(w) >= -1) and w not in pm1]
print("  with no high stone or no low stone:", len(one))
for w in one[:14]: print("   ", *w)
