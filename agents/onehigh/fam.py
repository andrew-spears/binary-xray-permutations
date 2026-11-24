"""Slack-only families after one letter 2 (bottom-up; a family at slack s only depends on slacks <= s).
Types after the 2 (letters 0, 1 until the first negative letter, which is a -1 after a 0):
 after 2            L0(s) = level-2 states with a 2-predecessor in G(s-2);  K0(s) = central states with one.
 after 2 1^j, j>=1  Lam(s) (level 2), Kap(s) (central): largest families inside step_1(L0), step_1(K0) closed under the letter 1.
 after 2 1^j 0      C1(s) = central states with a 0-predecessor in Lam(s) u Kap(s)   (C1L: in Lam(s) only)
 later, letters 0/1 Q(s): largest family inside step_e(C1) and step_e(Q), e = 0, 1.
 exit               number of states of G-(s-1) with no (-1)-predecessor in C1(s), resp. Q(s).
  python3 fam.py SMAX [v]"""
import sys
from oh import *
SM = int(sys.argv[1]); setup(SM + 2); V = len(sys.argv) > 2
lvl2 = lambda s: frozenset(u for u in states(s) if cls(u) == (2 if s % 2 == 0 else -1))
E = frozenset()
def has(u, e, fam): return any(t in fam for k, t in preds(u, e))
L0, K0, Lam, Kap, C1, C1L, Q = {}, {}, {}, {}, {}, {}, {}
for s in range(2, SM + 1):
    L0[s] = frozenset(u for u in lvl2(s) if has(u, 2, G(s - 2))); K0[s] = frozenset(u for u in Cen(s) if has(u, 2, G(s - 2)))
for s in range(3, SM + 1):
    Lam[s] = frozenset(u for u in lvl2(s) if has(u, 1, L0[s - 1]) and (s == 3 or has(u, 1, Lam[s - 1])))
    Kap[s] = frozenset(u for u in Cen(s) if has(u, 1, K0[s - 1]) and (s == 3 or has(u, 1, Kap[s - 1])))
    C1L[s] = frozenset(u for u in Cen(s) if has(u, 0, Lam[s])); C1[s] = frozenset(u for u in Cen(s) if has(u, 0, Lam[s] | Kap[s]))
for s in range(3, SM + 1):
    cand = set(u for u in Cen(s) if has(u, 0, C1[s]) and (s == 3 or (has(u, 1, C1[s - 1]) and has(u, 1, Q[s - 1]))))
    while True:
        new = set(u for u in cand if has(u, 0, cand))
        if new == cand: break
        cand = new
    Q[s] = frozenset(cand)
print(" s |lvl2-L0| |lvl2-Lam| |G-K0| |G-Kap|   |G| |G-C1L| |G-C1| |G-Q|  exit: C1L  C1   Q")
for s in range(3, SM + 1):
    ex = [[u for u in Gm(s - 1) if not has(u, -1, F[s])] for F in (C1L, C1, Q)]
    print(f"{s:2d} {len(lvl2(s) - L0[s]):8d} {len(lvl2(s) - Lam[s]):9d} {len(G(s) - K0[s]):7d} {len(G(s) - Kap[s]):6d} {len(G(s)):6d} {len(G(s) - C1L[s]):6d} {len(G(s) - C1[s]):6d} {len(G(s) - Q[s]):5d}        {len(ex[0]):3d} {len(ex[1]):3d} {len(ex[2]):3d}")
    if V:
        print("     lvl2 - Lam:", " ".join(sorted(map(nm, lvl2(s) - Lam[s]))[:14]))
        print("     G - Kap:", " ".join(sorted(map(nm, G(s) - Kap[s]))[:14]))
        print("     G - C1:", " ".join(sorted(map(nm, G(s) - C1[s]))[:14]), "   C1 - G:", " ".join(sorted(map(nm, C1[s] - G(s)))[:8]))
        print("     G - Q:", " ".join(sorted(map(nm, G(s) - Q[s]))[:14]), "  exit C1:", " ".join(map(nm, ex[1][:6])), "  exit Q:", " ".join(map(nm, ex[2][:6])))
print("\nafter the first zero plus one letter e: states of G (G- for e = -1) with no e-predecessor in C1L / C1")
for s in range(3, SM + 1):
    row = []
    for e in (0, 1, -1):
        if s - e < 3 or s - e > SM: row.append("      -"); continue
        fam = Gm(s) if e < 0 else G(s)
        row.append(f"{sum(1 for u in fam if not has(u, e, C1L[s - e])):3d}/{sum(1 for u in fam if not has(u, e, C1[s - e])):3d}")
    print(f"{s:2d}  |G| {len(G(s)):5d}   e=0: {row[0]}   e=1: {row[1]}   e=-1: {row[2]}")
print("\nclosed forms (slack <= %d)" % SM)
def conjp(p): return tuple(sum(1 for x in p if x > i) for i in range(p[0])) if p else ()
for s in range(3, SM + 1):
    d = lvl2(s) - Lam[s]; sc = {u for u in lvl2(s) if u[1] == conjp(u[0])}
    ex = [u for u in Gm(s - 1) if not has(u, -1, C1L[s])]
    print(f"{s:2d}  lvl2 - Lam = the {len(sc)} states (l|l') of level 2" + ("" if d == sc else " and " + " ".join(sorted(map(nm, d - sc)))),
          " | lvl2 - L0:", " ".join(sorted(map(nm, lvl2(s) - L0[s]))) or "none", " | G - C1:", " ".join(sorted(map(nm, G(s) - C1[s]))),
          " | no 0-pred in C1:", " ".join(sorted(nm(u) for u in G(s) if not has(u, 0, C1[s]))),
          " | G-(s-1) with no (-1)-pred in C1L:", " ".join(sorted(map(nm, ex))) or "none", "(in G: %d)" % sum(map(inG, ex)))
print("G alone does not carry a letter -2: G-(s-2) minus step_-2(G(s)) has", ", ".join(f"{len(Gm(s - 2) - step(G(s), -2))} states at s = {s}" for s in range(2, SM + 1) if Gm(s - 2) - step(G(s), -2)))
