"""Young prefixes ending in a letter 0, word by word (REPORT4.md).  Runs  ZERO=1 JSTAR=3 ./fw  on the words given (one per
argument, or one per line of stdin) and, for every prefix x ending in 0, compares J*(s, tail) minus F(x) with
    N_y(s) = { d(u) <= y - 1 }  u  { a row of length >= s - y in lambda or mu },      y = young excess of x,
d(u) = s - (longest row or column of lambda or mu).  One line per prefix: its length, slack, y, |J* minus F|, |N_y n J*|, the
number of missing states outside N_y with their largest d and their levels max(c, 1 - c), |N_y n F|, and missing/all of J* by level.
Usage: python3 zero.py "1 1 1 1 1 4 3 2 1 0 0 0 0 0 0" ...     [SHOW=k: list k missing states outside N_y]  [S0=11]"""
import sys, os, re, subprocess, collections
sys.path.insert(0, "../l1sets")
import exc, l1, jstar, young
jstar.MODE = 3          # the family ./fw is run with (JSTAR=3), whatever MODE says
def parse(t):
    def part(p): return () if p == "-" else tuple(int(x.strip("()")) for x in re.findall(r"\(\d+\)|\d", p))
    lam, mu = t.split("|"); return (part(lam), l1.conj(part(mu)))
def level(u): c = l1.cls(u); return max(c, 1 - c)
TAIL = {"10": ("1", "0"), "00": ("0", "0"), ".0": (".", "0")}
def run(words, S0=11):
    out = subprocess.run(["./fw"], input="\n".join(words) + "\n", capture_output=True, text=True,
                         env=dict(os.environ, ZERO="1", JSTAR="3", LIST="1000000", S0=str(S0))).stdout
    res = []; w = None
    for line in out.split("\n"):
        m = re.match(r"\s+(\d+) slack (\d+) tail (\S+) y (\d+) (\d+) (\d+) missing (\d+) :(.*)", line)
        if m: res.append((w, int(m.group(1)), int(m.group(2)), m.group(3), int(m.group(4)), int(m.group(5)), [parse(t) for t in m.group(8).split()]))
        elif line.startswith("word "): w = line.strip()
        elif line.strip(): print(f"STOPPED, {w}: {line.strip()}", file=sys.stderr)
    return res
if __name__ == "__main__":
    words = sys.argv[1:] or [l.strip() for l in sys.stdin if l.strip()]; show = int(os.environ.get("SHOW", 0)); last = None
    for (w, n, s, tail, y, nj, miss) in run(words, int(os.environ.get("S0", 11))):
        if w != last: print(w); last = w
        Js = [u for u in exc.states(s) if jstar.jstar(u, TAIL[tail])]; N = set(u for u in Js if young.ball(u, y)); out = [u for u in miss if u not in N]
        assert len(Js) == nj, (w, n, len(Js), nj)
        lv = collections.Counter(level(u) for u in out); la = collections.Counter(level(u) for u in miss); lt = collections.Counter(level(u) for u in Js)
        print(f"  n {n:2d} slack {s:2d} y {y:2d} tail {tail}: missing {len(miss):5d} of {len(Js):5d}, |N_y| {len(N):4d}, outside N_y {len(out):4d}"
              + (f" (d <= {max(young.d(u) for u in out)}; levels " + " ".join(f"{k}:{lv[k]}" for k in sorted(lv)) + ")" if out else "")
              + f", N_y reached {len(N - set(miss))}; missing by level " + " ".join(f"{k}:{la[k]}/{lt[k]}" for k in sorted(lt)))
        if show and out: print("      " + " ".join(sorted(l1.name(u) for u in out)[:show]))
