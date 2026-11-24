# All width<=3 solutions of one word, shown as: the permutation, and the chain (greedy first-fit) of each stone in diagonal order.
import sys
def sols(e, w=3):
    n = len(e); D = {e[j] + 2 * j for j in range(n)}; out = []
    def rec(i, pi, used, t):
        if i == n: out.append(tuple(pi)); return
        for c in range(n):
            if c in used or i + c not in D or (i + c) in {r + pi[r] for r in range(i)} or c < t[w]: continue
            u = list(t)
            for j in range(w - 1, 0, -1):
                if c < t[j]: u[j + 1] = max(u[j + 1], c)
            u[1] = max(u[1], c)
            rec(i + 1, pi + [c], used | {c}, u)
    rec(0, [], frozenset(), [10**9] + [-1] * w)
    return out
def chains(pi):
    tops = []; col = []
    for c in pi:                         # first-fit: put on the chain with the largest top below c  (patience sorting)
        best = None
        for j, t in enumerate(tops):
            if t < c and (best is None or t > tops[best]): best = j
        if best is None: tops.append(c); col.append(len(tops) - 1)
        else: tops[best] = c; col.append(best)
    return col
if __name__ == "__main__":
    e = [int(x) for x in sys.argv[1:]]; n = len(e)
    S = sols(e); print(len(S), "solutions of width <= 3 for", e)
    for pi in S[:40]:
        col = chains(pi); order = sorted(range(n), key=lambda i: i + pi[i])
        print("  pi", " ".join(str(c + 1) for c in pi), "| rows by chain", "".join("ABC"[col[i]] for i in range(n)),
              "| cols by chain", "".join("ABC"[col[pi.index(c)]] for c in range(n)), "| diagonals by chain", "".join("ABC"[col[i]] for i in order))
