"""Compare the block-type sets J(s, tail) with the class sets of ../l1sets (Central(s), T(s)).
Usage: python3 exc.py C B FEATURES [show [SMAX]]     runs  LET=-99,C KLO=0 ./types B FEATURES dump  (DUMPMAX = B)
For each type (slack, tail): |J|, |J not central|, |Central minus T minus J| ; with show: the excluded states (slack <= SMAX)."""
import sys, os, re, subprocess, collections
sys.path.insert(0, "../l1sets")
import l1
def parse(tok):
    out = []
    for side in tok.split("|"):
        p = []; i = 0
        while i < len(side):
            if side[i] == "-": i += 1
            elif side[i] == "(": j = side.index(")", i); p.append(int(side[i+1:j])); i = j + 1
            else: p.append(int(side[i])); i += 1
        out.append(tuple(p))
    return (out[0], l1.conj(out[1]))                 # u = (lam, nu), nu = mu'
def parts(n, m=None):
    m = n if m is None else m
    if n == 0: yield (); return
    for a in range(min(n, m), 0, -1):
        for p in parts(n - a, a): yield (a,) + p
def states(s): return [(a, b) for k in range(s + 1) for a in parts(k) for b in parts(s - k)]
def load(C, B, feats, env=None):
    e = dict(os.environ, LET=f"-99,{C}", KLO="0", DUMPMAX=str(B)); e.update(env or {})
    out = subprocess.run(["./types", str(B), feats, "dump"], env=e, capture_output=True, text=True).stdout
    J = {}; verdict = ""
    for line in out.split("\n"):
        if line.startswith("summary"): verdict = line.split("=>")[1].strip()
        m = re.match(r"J\(([^)]*)\) \[([^\]]*)\] (\d+):(.*)", line)
        if m:
            k = m.group(1).split(","); s = int(k[0]); tail = tuple(int(x) for x in k[2:] if x != ".") + (int(k[1]),)
            J[s, tail] = set(parse(t) for t in m.group(4).split())
    return J, verdict
if __name__ == "__main__":
    C = int(sys.argv[1]); B = int(sys.argv[2]); feats = sys.argv[3]; show = len(sys.argv) > 4; smax = int(sys.argv[5]) if len(sys.argv) > 5 else 8
    J, verdict = load(C, B, feats); print(f"letters <= {C}, bound {B}, {feats}: {verdict}; {len(J)} sets")
    G = {s: set(u for u in states(s) if l1.central(u) and not l1.in_T(u)) for s in range(1, B + 1)}
    tails = sorted(set(t for s, t in J), key=lambda t: (len(t), t))
    print("tail            : per slack  |J| / |J not central| / |G minus J|     (G = Central minus T)")
    for t in tails:
        row = []
        for s in range(1, B + 1):
            if (s, t) in J: j = J[s, t]; row.append(f"{len(j)}/{len(j - G[s])}/{len(G[s] - j)}")
            else: row.append("-")
        print(f"{' '.join(map(str, t)):16s}: " + "  ".join(row))
    if show:
        for t in tails:
            for s in range(1, smax + 1):
                if (s, t) in J and G[s] - J[s, t]: print(f"tail {t} slack {s}: G minus J =", " ".join(sorted(l1.name(u) for u in G[s] - J[s, t])))
