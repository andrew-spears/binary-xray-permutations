"""DEL0 at a cut of slack 2.  States of slack 2 up to transposition: three classes, with per-state counts
   alpha = L_x(11|-) = L_x(-|11),   beta = L_x(2|-) = L_x(-|2),   gamma = L_x(1|1)      (labels of cone.part).
Then (checked here on every pair)   N(x y) = 2 alpha beta' + 2 beta alpha' + gamma gamma',
   N(x 0 y) = 2 alpha alpha' + 2 beta beta' + 2 beta gamma' + 2 gamma beta',   primes = L_{y*}, y* = y reversed, negated,
so N(x 0 y) - N(x y) = 2 p p' + 4 beta beta' - q q',  p = alpha - beta, q = gamma - 2 beta.
The letter 0 acts on (alpha, beta, gamma) by T_0 = (beta + gamma, alpha, 2 beta).
S2: for every legal prefix x ending at slack 2 with last letter <= 1
   gamma <= 4 beta,   beta <= 2 alpha,   and the three triangle inequalities
   alpha <= beta + gamma,   gamma <= alpha + beta,   beta <= alpha + gamma.
S2 implies N(x 0 y) >= N(x y) at every cut of slack 2: in the coordinates P = alpha/beta - 1, Q = gamma/beta - 2 the
difference is beta beta' (2 P P' + 4 - Q Q'), S2 is the pentagon with vertices (-1/2,-3/2), (0,-2), (4,2), (2,2),
(-1/2,-1/2), and the form is >= 0 at all vertex pairs (checked below; it is affine in each argument).
S2 is preserved by T_0 (see COUNT2_REPORT.md).  Tests S2 on all legal prefixes x (slacks <= B, length <= N) ending at
slack 2, split by the last letter; also (i) alpha >= beta, which holds only after a last letter 0 or 1, and for ALL prefixes at slack 2 (any last letter)
whether u = (beta + gamma - alpha)/2, v = (alpha + gamma - beta)/2, w = (alpha + beta - gamma)/2 are nonnegative integers.
Usage: python3 slack2.py B N"""
import sys
from collections import Counter, defaultdict
from fractions import Fraction
sys.path.insert(0, "../interface")
from count_rule import cstep
from cone import part, prefixes
B, N = int(sys.argv[1]), int(sys.argv[2])
A, Bt, G = ((), (1, 1)), ((), (2,)), ((1,), (1,))
stat = defaultdict(lambda: [0, 0, 0, None, None, Fraction(0), None, None])
S2 = defaultdict(lambda: [0, 0, 0, 0, 0, 0, None]); tight = {}
dirs = {}; uvw = [0, 0]
for w, C, s in prefixes(B, N):
    if s != 2 or not w: continue
    d = {}
    for t, c in C.items():
        k = tuple(sorted((part(t[0], B), part(t[1], B)))); assert d.setdefault(k, c) == c, "not symmetric"
    al, be, ga = d.get(A, 0), d.get(Bt, 0), d.get(G, 0)
    st = stat[min(w[-1], 2)]; st[0] += 1
    uvw[0] += 1; uvw[1] += any(v < 0 or v % 2 for v in (be + ga - al, al + ga - be, al + be - ga))
    if al < be:
        st[1] += 1
        if st[3] is None: st[3] = (w, al, be, ga)
    if ga > 4 * be:
        st[2] += 1
        if st[4] is None: st[4] = (w, al, be, ga)
    if be and Fraction(ga, be) > st[5]: st[5] = Fraction(ga, be); st[6] = w
    if w[-1] <= 1:
        r = S2[w[-1]]; r[0] += 1
        for i, (ok, eq) in enumerate(((ga <= 4 * be, ga == 4 * be), (be <= 2 * al, be == 2 * al), (al <= be + ga, al == be + ga), (ga <= al + be, ga == al + be), (be <= al + ga, be == al + ga))):
            if not ok:
                r[1 + i] += 1
                if r[6] is None: r[6] = (w, al, be, ga)
            if eq: tight.setdefault(i, w)
        tot = al + be + ga; dirs.setdefault((Fraction(al, tot), Fraction(be, tot)), (w, al, be, ga))
for l in sorted(stat):
    st = stat[l]
    print(f"last letter {'>= 2' if l == 2 else l}: prefixes {st[0]}; alpha < beta: {st[1]} {st[3] or ''}; gamma > 4 beta: {st[2]} {st[4] or ''}; max gamma/beta = {float(st[5]):.4f} at {st[6]}")
V = list(dirs.values()); worst = None
for (w, a, b, g) in V:
    for (w2, a2, b2, g2) in V:
        Dv = 2 * (a - b) * (a2 - b2) + 4 * b * b2 - (g - 2 * b) * (g2 - 2 * b2); r = Fraction(Dv + 2*a*b2 + 2*b*a2 + g*g2, 2*a*b2 + 2*b*a2 + g*g2)
        if worst is None or r < worst[0]: worst = (r, w, w2)
print(f"{len(V)} directions with last letter <= 1; least N(x0y)/N(xy) over all pairs of directions: {float(worst[0]):.4f} at x = {worst[1]}, y* = {worst[2]}")
print("least alpha/beta:", min((Fraction(a, b), w) for w, a, b, g in V if b)[:2], " least beta/gamma:", min((Fraction(b, g), w) for w, a, b, g in V if g)[:2])
names = ["gamma <= 4 beta", "beta <= 2 alpha", "alpha <= beta + gamma", "gamma <= alpha + beta", "beta <= alpha + gamma"]
print("S2, violations by last letter (prefixes; then one count per inequality):")
for l in sorted(S2): print(f"   last letter {l}: {S2[l][0]} prefixes; violations {S2[l][1:6]} {S2[l][6] or ''}")
for i in range(5): print(f"   {names[i]:22} equality at x = {tight.get(i)}")
Vx = [(Fraction(-1, 2), Fraction(-3, 2)), (0, -2), (4, 2), (2, 2), (Fraction(-1, 2), Fraction(-1, 2))]
print("form 2PP' + 4 - QQ' at the 15 pairs of vertices of the pentagon: min =", min(2 * a * a2 + 4 - b * b2 for a, b in Vx for a2, b2 in Vx))
print(f"all {uvw[0]} prefixes at slack 2 (any last letter): (u, v, w) not nonnegative integers: {uvw[1]}")
