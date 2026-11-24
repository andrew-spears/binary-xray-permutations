# Two-chain solutions of one word, as the chain, row and column of each stone in order of lines (rows, columns 1-based; line = row + column).
import sys
from ab import ab
w = [int(x) for x in sys.argv[1:]]; n = len(w); D = [e + 2 * (k + 1) - n - 1 for k, e in enumerate(w)]
assert all(D[i] < D[i + 1] for i in range(n - 1)), "not a word of distinct diagonals"
r = ab(D, n, 2); print(*w, "| lines", [d + n + 1 for d in D], "|", len(r), "two-chain solutions")
for a, b, q in sorted(r)[:int(1e9)]:
    st = {i + c + 2: (a[i], i + 1, c + 1) for i, c in enumerate(q)}
    print("  a =", a, " b =", b, " |", " ".join("%s(%d,%d)" % st[d + n + 1] for d in D))
