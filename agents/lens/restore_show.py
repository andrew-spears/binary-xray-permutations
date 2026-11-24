import sys
exec(open("restore.py").read().split("s0 = int")[0])
s0 = int(sys.argv[1]); word = sys.argv[2]
F = G(s0, False); s = s0
for e in map(int, word.split()):
    F = frozenset(v for u in F for k, v in l1.succs(u, e)); s += e
    miss = G(s, e < 0) - F
    print(e, s, len(miss), sorted(l1.name(u) for u in miss)[:70])
