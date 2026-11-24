"""Sets on every prefix that ends in a letter 0, young or old (REPORT4.md).
Runs  CLOSE=0 CLAMP=-1,1 [YCAP=c] ./types B YL1 dump : the largest family Z(s, y, p) (y = young excess, p = class of the letter
before the final 0: -1, 0 or 1 = "letter >= 1") closed under blocks (nonzero letters)* 0, and compares it with J*(s, tail) of
jstar.py (tail 1 0 for p = 1, 0 0 for p = 0, . 0 for p = -1).  d(u) = s - (longest row or column of either diagram).
EXACT=1: instead of Z, the exact cores C(s, y, p) = intersection of F(x) over all prefixes of that type (slacks <= B).
NEG=1: the family of CLOSE=n (sets also on the prefixes ending in a negative letter) against CLOSE=0 and against G-(s) of ../l2sets.
Usage: python3 young.py B [S0 = 8] [show]     env YCAP, LET=lo,hi, EXACT, NEG"""
import sys, os, re, subprocess, collections
import exc, l1, jstar
def d(u):
    s = l1.slack(u); return s - max([0] + [max(p[0], len(p)) for p in u if p])
def row(u): return max([0] + [q[0] for q in (u[0], l1.conj(u[1])) if q])
def ball(u, y):
    """N_y of REPORT4.md: within y - 1 of a one-line state, or a row of length >= s - y in lambda or mu"""
    return y > 0 and (d(u) <= y - 1 or row(u) >= l1.slack(u) - y)
def load(B, env=None):
    e = dict(os.environ, CLOSE="0", CLAMP="-1,1", DUMPMAX=str(B)); e.update(env or {})
    out = subprocess.run(["./types", str(B), "YL1", "dump"], env=e, capture_output=True, text=True).stdout
    J = {}
    for line in out.split("\n"):
        m = re.match(r"J\(([^)]*)\) \[([^\]]*)\] (\d+):(.*)", line)
        if m:
            k = m.group(1).split(",")
            key = (int(k[0]), int(k[2]), int(k[3]) if k[3] != "." else -1)
            if k[1] == "0": J[key] = (set(exc.parse(t) for t in m.group(4).split()), m.group(2))
            elif k[1] not in (".", "0"): J[key + ("neg",)] = (set(exc.parse(t) for t in m.group(4).split()), m.group(2))
    return J, [l for l in out.split("\n") if l.startswith("summary") or l.startswith("bound")]
def cores(B, env=None):
    """exact cores C(s, y, p) = intersection of F(x) over all prefixes x of that type with all slacks <= B, and a worst word"""
    e = dict(os.environ, CLOSE="0", CLAMP="-1,1", DUMPMAX=str(B), CORE="3"); e.update(env or {})
    out = subprocess.run(["./types", str(B), "YL1"], env=e, capture_output=True, text=True).stdout; C = {}; w = {}
    for line in out.split("\n"):
        m = re.match(r"C\(([^)]*)\): .*? minimal:\s+\d+ \[([^\]]*)\]", line)
        if m: w[m.group(1)] = m.group(2).strip()
        m = re.match(r"  C\(([^)]*)\) =(.*)", line)
        if m:
            k = m.group(1).split(",")
            if k[1] == "0": C[int(k[0]), int(k[2]), int(k[3]) if k[3] != "." else -1] = (set(exc.parse(x) for x in m.group(2).split()), w.get(m.group(1), ""))
    return C, [l for l in out.split("\n") if l.startswith("cores")]
TAIL = {1: ("1", "0"), 0: ("0", "0"), -1: (".", "0")}
if __name__ == "__main__":
    B = int(sys.argv[1]); S0 = int(sys.argv[2]) if len(sys.argv) > 2 else 8; show = len(sys.argv) > 3
    if os.environ.get("NEG"):                      # closing also at the prefixes ending in a negative letter
        sys.path.insert(0, "../l2sets"); import neg0
        J0, _ = load(B); Jn, summ = load(B, {"CLOSE": "n"}); print("\n".join(summ))
        same = sum(1 for k in J0 if J0[k][0] == Jn[k][0]); n0 = len(J0)
        print(f"sets on the prefixes ending in 0: {same} of {n0} types have the same set with CLOSE=0 and CLOSE=n;",
              "lost by closing at negative letters:", " ".join(f"{k}:{len(J0[k][0] - Jn[k][0])}" for k in sorted(J0) if J0[k][0] != Jn[k][0] and k[0] >= S0))
        print("prefixes ending in a negative letter.  p y slack: |states| |G-| |Z| ; |G- minus Z| by d ; |Z minus G-|")
        for k in sorted((k for k in Jn if len(k) == 4 and k[0] >= S0), key=lambda k: (k[2], k[1], k[0])):
            s, y, p, _ = k; St = exc.states(s); G = set(u for u in St if neg0.in_Gm(u)); Z = Jn[k][0]; m = G - Z; h = collections.Counter(d(u) for u in m)
            print(f"  {p:2d} {y:2d} {s:2d}: {len(St):5d} {len(G):5d} {len(Z):5d} ; {len(m):4d} " + " ".join(f"d{i}:{h[i]}" for i in sorted(h)) + f" ; {len(Z - G)}  [{Jn[k][1]}]")
        sys.exit()
    J, summ = cores(B) if os.environ.get("EXACT") else load(B); print("\n".join(summ))
    print("p y slack: |states| |J*| |Z| ; |J* minus Z| by d (missing/all of J*) ; |Z minus J*| ; comparison of J* minus Z with N_y = ball")
    for (s, y, p) in sorted(J, key=lambda k: (k[2], k[1], k[0])):
        if s < S0: continue
        St = exc.states(s); Js = set(u for u in St if jstar.jstar(u, TAIL[p])); Z = J[s, y, p][0]; m = Js - Z
        h = collections.Counter(d(u) for u in m); tot = collections.Counter(d(u) for u in Js)
        Nb = set(u for u in Js if ball(u, y))
        print(f"  {p:2d} {y:2d} {s:2d}: {len(St):5d} {len(Js):5d} {len(Z):5d} ; {len(m):4d} " + " ".join(f"d{k}:{h[k]}/{tot[k]}" for k in sorted(h)) + f" ; {len(Z - Js)} ; N_y {len(Nb)}, missing outside N_y {len(m - Nb)}, N_y not missing {len(Nb - m)}  [{J[s, y, p][1]}]")
        if show: print("        outside N_y: " + " ".join(sorted(l1.name(u) for u in m - Nb)[:60]))
