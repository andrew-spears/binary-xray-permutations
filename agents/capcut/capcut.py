"""Universal hole patterns at a cut 1|0 for words with capped letters.
CF(s, l) = states in F(x) for every legal prefix x with letters in [-C, C], length <= LEN, slacks <= SMAX, ending at slack s with last letter l.
A word with letters in [-C, C] cut between a letter 1 and a letter 0 at slack s is solvable if CF(s, 1) meets conj CF(s, 0)
(the second half turned around is a prefix ending in the letter 0).   U(s) = CF(s, 1) & conj CF(s, 0).
  python3 capcut.py LEN SMAX C [v]"""
import sys
sys.path.insert(0, "../l1sets")
import l1
LEN, SMAX, C = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); V = len(sys.argv) > 4
l1.depth = lambda u: len(u[0]) + len(u[1]) + 6 + 2 * LEN
CF = {}; cnt = {}
def rec(w, s, F):
    if w and w[-1] in (0, 1):
        k = (s, w[-1]); CF[k] = F if k not in CF else CF[k] & F; cnt[k] = cnt.get(k, 0) + 1
    if len(w) == LEN: return
    for e in range(max((w[-1] - 1) if w else 0, -s, -C), C + 1):
        if s + e > SMAX: break
        rec(w + (e,), s + e, frozenset(v for u in F for k, v in l1.succs(u, e)))
rec((), 0, frozenset([((), ())]))
def cj(u): return (l1.conj(u[0]), l1.conj(u[1]))
def show(u): return ".".join(map(str, u[0])) or "-", ".".join(map(str, u[1])) or "-"
for s in range(1, SMAX + 1):
    if (s, 1) not in CF or (s, 0) not in CF: continue
    U = CF[s, 1] & frozenset(cj(u) for u in CF[s, 0])
    print(f"s = {s}: prefixes {cnt[s, 1]}/{cnt[s, 0]}  |CF(s,1)| = {len(CF[s, 1])}  |CF(s,0)| = {len(CF[s, 0])}  |U| = {len(U)}", "  " + "  ".join("%s|%s" % show(u) for u in sorted(U)[:10 if not V else 400]))
