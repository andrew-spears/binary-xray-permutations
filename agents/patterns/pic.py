# Draw one width<=3 solution of a word as three worldlines: time u = row + column (the diagonal), place v = column - row.
import sys, subprocess
from show import chains
def draw(e):
    out = subprocess.run(["./width1", "50000000"] + [str(x) for x in e], capture_output=True, text=True).stdout
    line = [l for l in out.splitlines() if l.strip().startswith("pi =")]
    if not line: print("no solution found", out); return
    pi = [int(x) - 1 for x in line[0].split()[2:]]; n = len(pi); col = chains(pi)
    grid = [[" "] * (2 * n - 1) for _ in range(2 * n - 1)]
    for i, c in enumerate(pi): grid[(c - i) + n - 1][i + c] = "ABC"[col[i]]
    print("word", " ".join(map(str, e))); print("pi  ", " ".join(str(c + 1) for c in pi))
    for v in range(2 * n - 2, -1, -1):
        s = "".join(grid[v]).rstrip()
        if s: print("%4d |%s" % (v - n + 1, s))
if __name__ == "__main__": draw([int(x) for x in sys.argv[1:]])
