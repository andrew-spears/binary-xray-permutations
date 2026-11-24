"""General interval orders with 1..n (order of diagonals) a linear extension.
Keep the earlier stones in a list ordered by right endpoint.  A new stone is incomparable to exactly the last m stones of
the list (their labels 'number of later incomparable stones still owed' drop by 1) and gets label e + m; it is inserted
anywhere among the last m + 1 places.  A stone whose label reaches 0 must have only finished stones before it.
Question 1: does every legal word have such an interval order?  Question 2: one that is 2-dimensional (= a solution)?
usage: python3 iv2.py n [2]   (with 2: also search for a 2-dimensional one)"""
import sys
from functools import lru_cache
from iv import words, comparability
def solve(w, want2=False):
    n = len(w); found = [None]
    seen = set()
    def rec(k, L, E):
        # L: tuple of (label, id) alive, in list order
        if found[0] is not None: return
        if k == n:
            if not L and (not want2 or comparability(n, E)): found[0] = E
            return
        if not want2:
            key = (k, tuple(x for x, _ in L))
            if key in seen: return
            seen.add(key)
        e = w[k]; t = len(L)
        for m in range(max(0, -e), t + 1):
            lab = e + m
            if lab > n - 1 - k: break
            head = L[:t - m]; tail = [(x - 1, i) for x, i in L[t - m:]]
            zeros = [j for j, (x, _) in enumerate(tail) if x == 0]
            if zeros:
                if head or zeros != list(range(len(zeros))): continue
                tail = tail[len(zeros):]
            E2 = E + [(i, k) for _, i in L[t - m:]]
            if lab == 0:   # a stone comparable to every later stone: it must be first among the unfinished ones
                if not head: rec(k + 1, tuple(tail), E2)
                continue
            for pos in range(len(tail) + 1):
                rec(k + 1, tuple(head) + tuple(tail[:pos]) + ((lab, k),) + tuple(tail[pos:]), E2)
                if found[0] is not None: return
    rec(0, (), [])
    return found[0]
if __name__ == "__main__":
    want2 = len(sys.argv) > 2
    for n in range(2, int(sys.argv[1]) + 1):
        W = words(n); bad = [w for w in W if solve(w, want2) is None]
        print(f"n = {n}: {len(W)} words; without an interval order{' of dimension 2' if want2 else ''}: {len(bad)}", bad[:3])
