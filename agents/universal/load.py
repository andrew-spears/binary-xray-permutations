"""Loader for the output of ./cores B.  D[(s, l)] = (CF, CA, LE) as sets of states; a state is (rowholes, colholes),
two partitions (tuples, weakly decreasing)."""
def P(t): return () if t == "-" else tuple(int(a) for a in t.split("."))
def load(fn):
    D = {}
    for line in open(fn):
        s, l, lam, mu, f, a, le = line.split(); k = (int(s), int(l)); CF, CA, LE = D.setdefault(k, (set(), set(), set()))
        st = (P(lam), P(mu))
        if f == "1": CF.add(st)
        if a == "1": CA.add(st)
        if le == "1": LE.add(st)
    return D
def conj(p): return tuple(sum(1 for x in p if x > i) for i in range(p[0])) if p else ()
def cc(st): return (conj(st[0]), conj(st[1]))
def tr(st): return (st[1], st[0])
def nm(st):
    f = lambda p: "".join(str(x) if x < 10 else f"({x})" for x in p) or "-"
    return f(st[0]) + "|" + f(st[1])
