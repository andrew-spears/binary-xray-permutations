"""As lens.py, but a move may change a by any vector with L1 norm <= 2r (r unit exchanges at once).
usage: python3 lens2.py n r"""
import sys
exec(open("lens.py").read().split("def main")[0])
n, r = int(sys.argv[1]), int(sys.argv[2])
top = 2 * sum(i * i for i in range(n)); bad = 0; nD = 0; ex = None
for d in valid_sets(n):
    nD += 1
    L = lattice(n, d); V = {a: val(a, d) for a in L}
    stuck = 0
    for a in L:
        v = V[a]
        if v == top: continue
        if not any(V[c] > v and sum(abs(x - y) for x, y in zip(a, c)) <= 2 * r for c in L):
            stuck += 1
            if ex is None: ex = (d, a)
    if stuck: bad += 1
print(f"n = {n}, r = {r}: {nD} sets; with a stuck non-solution: {bad}", ex)
