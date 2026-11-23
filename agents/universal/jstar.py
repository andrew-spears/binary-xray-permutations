"""Explicit sets for the old prefixes (REPORT3.md, conjecture OLD).  u = (lam, nu) as in ../l1sets, (a, b) = 2-core charges of
lam and nu, c = a + b (c has the parity of the slack s), D = |a - b|.  For an old prefix x (every suffix of j letters has
sum <= j) of slack s >= 11 ending in
  1 1          : J* = {0 <= c <= 1,  D <= 4} minus SC
  1 after <= 0 : J* = {-1 <= c <= 2, D <= 3} minus SC minus A(s) minus k|k
  1 0          : J* = {-1 <= c <= 2, D <= 3} minus one-row states minus E0 minus R
  0 0          : J* = {-2 <= c <= 3, D <= 2} minus one-row states
  0 after < 0  : J* = {-2 <= c <= 3, D <= 3} minus one-row states
SC: lam = nu.  E0 and A(s) (four states, only for s = 4 m^2 + 1): as in ../l1sets/l1.py.  one-row: -|s and s|-.  R: -|nn and nn|-.
k|k: lam = mu = (k), s = 2k.
MODE=2: D <= 2 for every tail and k|k not removed (a smaller family except for k|k).  MODE=1: no bound on D except for the tail
0 0, A(s) and k|k not removed (fails, see REPORT3.md).
Test: J*(s, tail) against the largest step-closed family J of  KLO=0 ./types B YA1  (J is inside F(x) for every old prefix x with
that tail and all slacks <= B), for S0 <= s <= B.   Usage: python3 jstar.py B [S0 = 11] [show]"""
import sys, os, re, subprocess, pickle
import exc, l1
def onerow(u): return (not u[0] and len(set(u[1])) == 1 and len(u[1]) == l1.slack(u)) or (not u[1] and len(u[0]) == 1)
def rect2(u):
    s = l1.slack(u); n = s // 2
    return s % 2 == 0 and ((not u[0] and u[1] == (2,) * n) or (not u[1] and u[0] == (n, n)))
MODE = int(os.environ.get("MODE", "3"))
DMAX = {("1", "1"): 4, (".", "1"): 3, ("1", "0"): 3, ("0", "0"): 2, (".", "0"): 3}
def jstar(u, tail):
    a, b = l1.c0(u[0]), l1.c0(u[1]); c = a + b; D = abs(a - b)
    if (MODE == 2 and D > 2) or (MODE == 3 and D > DMAX[tail]): return False
    if tail == ("1", "1"): return 0 <= c <= 1 and not l1.is_SC(u)
    if tail == (".", "1"): return -1 <= c <= 2 and not l1.is_SC(u) and not (MODE >= 2 and l1.slack(u) % 4 == 1 and l1.in_T(u)) and not (MODE == 3 and u == ((len(u[1]),), (1,) * len(u[1])))
    if tail == ("1", "0"): return -1 <= c <= 2 and not onerow(u) and not l1.is_E0(u) and not rect2(u)
    return -2 <= c <= 3 and not onerow(u)
def load(B, c=99):
    f = f"/tmp/ya1_{B}_{c}.pkl"
    if os.path.exists(f): return pickle.load(open(f, "rb"))
    out = subprocess.run(["./types", str(B), "YA1", "dump"], env=dict(os.environ, KLO="0", LET=f"-99,{c}", DUMPMAX=str(B)), capture_output=True, text=True).stdout
    J = {}
    for line in out.split("\n"):
        m = re.match(r"J\(([^)]*)\) \[([^\]]*)\] (\d+):(.*)", line)
        if m: k = m.group(1).split(","); J[int(k[0]), (k[3], k[1])] = set(exc.parse(t) for t in m.group(4).split())
    assert "WORKS" in out; pickle.dump(J, open(f, "wb")); return J
if __name__ == "__main__":
    B = int(sys.argv[1]); S0 = int(sys.argv[2]) if len(sys.argv) > 2 else 11; show = len(sys.argv) > 3; J = load(B); bad = 0
    print("tail, slack: |states| |J*| |J| ; J* minus J (must be empty) ; |J minus J*|")
    for (s, tail) in sorted(J, key=lambda k: (k[1], k[0])):
        if s < S0: continue
        St = exc.states(s); Js = set(u for u in St if jstar(u, tail)); d = Js - J[s, tail]; e = J[s, tail] - Js; bad += len(d)
        print(f"  {' '.join(tail)}  {s:2d}: {len(St):5d} {len(Js):5d} {len(J[s, tail]):5d} ; {len(d)}" + (" [" + " ".join(sorted(l1.name(u) for u in d)[:10]) + "]" if d else "") + f" ; {len(e)}" + (" [" + " ".join(sorted(l1.name(u) for u in e)[:10]) + "]" if e and show else ""))
    print("HOLDS" if not bad else f"FAILS ({bad} states)", f"for slack {S0}..{B}")
