import sys
from collections import Counter
from hw import valid_sets, solutions, walk, moves
N = int(sys.argv[1])
for n in range(4, N + 1):
    byvar = Counter(); pairs = 0; nm = 0; nomove = 0; minfrac = 1; lens = Counter(); worst = None; allok_moves = 0
    for L in valid_sets(n):
        sols = solutions(L)
        for (x, y, T) in moves(L):
            nm += 1; good = 0
            for pi in sols:
                pairs += 1; a = False
                for vi, (p, q) in enumerate(((x, y), (y, x))):
                    for first in (0, 1):
                        for swap in (0, 1):
                            ok, st = walk(L, T, pi, p, q, first, swap)
                            if ok: byvar[(vi, first, swap)] += 1; a = True; lens[st] += 1
                if a: good += 1
            if good == 0: nomove += 1
            if good == len(sols): allok_moves += 1
            f = good / len(sols)
            if f < minfrac: minfrac = f; worst = (L, T, good, len(sols))
    print("n =", n, "moves", nm, "none repairable:", nomove, "all repairable:", allok_moves, "pairs", pairs, "smallest share", round(minfrac, 3), worst)
    print("   successes by variant (pending low/high, first free row own/other, rows/cols):", sorted(byvar.items()))
    print("   walk lengths:", sorted(lens.items()))
