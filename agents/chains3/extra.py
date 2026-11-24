# Two chains plus one stone.  For a word without a two-chain solution list the solutions that become two chains
# after deleting one stone: the deleted stone x (its position in line order and its letter), the stones incomparable
# to x on earlier lines (I-) and on later lines (I+), and the word of the remaining two-chain solution.
# Usage: python3 extra.py e_1 ... e_n
import sys
from lib import *
import two
def extras(e):
    out = []; n = len(e); L = lines(e)
    for pi in sols(e, 3):
        for r in range(n):
            rest = [(i, c) for i, c in enumerate(pi) if i != r]
            q = [c - (c > pi[r]) for i, c in rest]
            if width(q) > 2: continue
            pos = sorted(range(n), key=lambda i: i + pi[i]); rank = {i: t for t, i in enumerate(pos)}
            inc = [i for i in range(n) if i != r and (i < r) != (pi[i] < pi[r])]
            Im = sorted(rank[i] for i in inc if rank[i] < rank[r]); Ip = sorted(rank[i] for i in inc if rank[i] > rank[r])
            w = word_of(sorted(i2 + c for i2, c in enumerate(q)))
            out.append((rank[r], e[rank[r]], Im, Ip, tuple(w), pi))
    return out
if __name__ == "__main__":
    e = tuple(map(int, sys.argv[1:]))
    for x in sorted(extras(e)): print("stone %d (letter %d)  I- %s  I+ %s  rest %s   %s" % (x[0], x[1], x[2], x[3], " ".join(map(str, x[4])), fmt(x[5])))
