"""What a tail excludes (REPORT3.md section 1).  For words with letters <= c and slack <= B, and every tail tau = final
non-increasing run (at most 4 letters, type A3 of types.cpp):
    C(s, tau) = intersection of F(x) over all prefixes x of slack s with tail tau          (exact, CORE=3 of ./types)
    Loc(s, tau) = states of slack s that have a chain of predecessors along the letters of tau, starting anywhere
                  (the states not in Loc are excluded by the last |tau| stones alone)
    G(s) = Central(s) minus T(s)                                                             (../l1sets)
Usage: python3 tail.py c B [show SMAX | cls S]
per tail and slack:  |C| / |C minus Central| / |G minus Loc| / |G n Loc minus C|     ; show: the states of G n Loc minus C;
cls S: instead, at slack S, per charge class c = c0(lam) + c0(nu):  |C n class| / |Loc n class| / |class|."""
import sys, os, re, subprocess
import exc, l1
c, B = int(sys.argv[1]), int(sys.argv[2]); prof = len(sys.argv) > 3 and sys.argv[3] == 'cls'; show = len(sys.argv) > 3 and not prof; smax = int(sys.argv[4]) if show else 0
out = subprocess.run(["./types", str(B), "A3"], env=dict(os.environ, LET=f"-99,{c}", CORE="3", DUMPMAX=str(B)), capture_output=True, text=True).stdout
C = {}
for line in out.split("\n"):
    m = re.match(r"  C\(([^)]*)\) =(.*)", line)
    if m:
        k = m.group(1).split(","); tail = tuple(int(x) for x in k[2:] if x != ".") + (int(k[1]),)
        C[int(k[0]), tail] = set(exc.parse(t) for t in m.group(2).split())
St = {s: exc.states(s) for s in range(B + 1)}
G = {s: set(u for u in St[s] if l1.central(u) and not l1.in_T(u)) for s in St}
def loc(s, tail):
    s0 = s - sum(tail)
    if s0 < 0: return None
    S = set(St[s0])
    for e in tail: S = set(v for u in S for k, v in l1.succs(u, e))
    return S
tails = sorted(set(t for s, t in C), key=lambda t: (len(t), t)); tot = [0, 0, 0, 0]
if prof:
    S = int(sys.argv[4]); cl = sorted(set(l1.cls(u) for u in St[S])); print(f"letters <= {c}, bound {B}, slack {S}: classes {cl};  |C n class| / |Loc n class| / |class|")
    for t in tails:
        if any(e < 0 for e in t) or (S, t) not in C: continue
        L = loc(S, t); print(f"{' '.join(map(str, t)):10s}: " + "  ".join(f"{sum(1 for u in C[S, t] if l1.cls(u) == k)}/{sum(1 for u in L if l1.cls(u) == k)}/{sum(1 for u in St[S] if l1.cls(u) == k)}" for k in cl))
    sys.exit()
print(f"letters <= {c}, slack <= {B}: per slack  |C| / |C minus Central| / |G minus Loc| / |G n Loc minus C|")
for t in tails:
    if any(e < 0 for e in t): continue
    row = []
    for s in range(1, B + 1):
        if (s, t) not in C: row.append("-"); continue
        L = loc(s, t); Cs = C[s, t]
        if L is None: row.append("?"); continue
        assert Cs <= L
        row.append(f"{len(Cs)}/{sum(1 for u in Cs if not l1.central(u))}/{len(G[s] - L)}/{len((G[s] & L) - Cs)}")
        if show and s <= smax and (G[s] & L) - Cs: print(f"   tail {t} slack {s}: in G and Loc, not in C:", " ".join(sorted(l1.name(u) for u in (G[s] & L) - Cs)))
    print(f"{' '.join(map(str, t)):10s}: " + "  ".join(row))
