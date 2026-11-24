# Repairing a solution after a minimal move by reflecting a chain of stones in an anti-diagonal.
# Board language of the claims map: stone = (row r, column c), 1 <= r, c <= n, diagonal d = c - r.
# D valid (Landau).  Minimal move: stones X on x and Y on y (x < y, x+1 and y-1 empty, x+2..y-2 all occupied)
# go to x+1 and y-1.
#
# For an integer s let psi_s(r) = the row of the stone in column s - r (undefined if s - r is off the board).
# Reflection in the anti-diagonal r + c = s:  (r, c) -> (s - c, s - r); it keeps the diagonal c - r.
# psi_s is a one-to-one partial map of the rows; its orbits are closed loops and exactly |s - (n+1)| open paths.
#
# REPAIR(s, start), s in {s1, s2} with s1 = r_X + c_Y - 1, s2 = r_Y + c_X + 1, start in {X, Y}:
#   take X and Y off; follow r -> psi_s(r) from the start stone's row until the column s - r is one of the two free
#   columns (stop) or off the board (fail); reflect every stone met on the way; put X and Y back on their new diagonals
#   in the two rows and two columns that are now free.
# Checked here for every solution of every valid D, every minimal move:
#   (1) a REPAIR that does not fail gives a solution of the new set (asserted);
#   (2) for given s, both starts fail  <=>  the rows of X and Y lie on two different open paths of psi_s (asserted);
#       so s in {n, n+1, n+2} never fails;
#   (3) statistic: does every move have a solution with s1 or s2 in {n, n+1, n+2}?
import sys
def valid_sets(n):
    out = []
    def rec(k, last, tot, cur):
        if k == n:
            if tot == n * (n - 1) // 2: out.append(tuple(cur))
            return
        for d in range(last + 1, n):
            t = tot + d + n - (k + 1)
            if t < k * (k + 1) // 2: continue
            cur.append(d); rec(k + 1, d, t, cur); cur.pop()
    rec(0, -n, 0, []); return out
def solutions(D):
    n = len(D); res = []; usedr = [False] * (n + 2); usedc = [False] * (n + 2); cur = []
    def rec(i):
        if i == n: res.append(tuple(cur)); return
        d = D[i]
        for r in range(max(1, 1 - d), min(n, n - d) + 1):
            c = r + d
            if usedr[r] or usedc[c]: continue
            usedr[r] = usedc[c] = True; cur.append((r, c)); rec(i + 1); cur.pop(); usedr[r] = usedc[c] = False
    rec(0); return res
def moves(D):
    S = set(D); out = []
    for i, x in enumerate(D):
        for j in range(i + 1, len(D)):
            y = D[j]
            if y - x >= 3 and x + 1 not in S and y - 1 not in S and all(v in S for v in range(x + 2, y - 1)): out.append((i, j))
    return out
def path_start(n, colof, s, r):
    """None if the row r is on a closed loop of psi_s, else the first row of its open path."""
    x = r
    while True:
        y = s - colof[x]                    # the row whose psi_s is x
        if y < 1 or y > n: return x
        x = y
        if x == r: return None
def repair(n, sol, i, j, s, start):
    (rX, cX), (rY, cY) = sol[i], sol[j]
    rowof = {c: (r, k) for k, (r, c) in enumerate(sol)}
    new = list(sol); stop = {cX, cY}
    r = rX if start == 0 else rY
    while True:
        c = s - r
        if c < 1 or c > n: return None
        if c in stop: break
        rz, k = rowof[c]
        new[k] = (s - c, s - rz)            # reflect stone k
        r = rz
    rest = [new[k] for k in range(n) if k not in (i, j)]
    freer = set(range(1, n + 1)) - {r for r, c in rest}; freec = set(range(1, n + 1)) - {c for r, c in rest}
    assert len(freer) == 2 and len(freec) == 2
    (r1, r2), (c1, c2) = sorted(freer), sorted(freec)
    for (a, b) in (((r1, c1), (r2, c2)), ((r1, c2), (r2, c1)), ((r2, c2), (r1, c1)), ((r2, c1), (r1, c2))):
        if a[1] - a[0] == sol[i][1] - sol[i][0] + 1 and b[1] - b[0] == sol[j][1] - sol[j][0] - 1:
            new[i] = a; new[j] = b; return new
    raise AssertionError("the two moving stones do not fit")
N = int(sys.argv[1])
for n in range(3, N + 1):
    nm = 0; none_ok = 0; none_small = 0; pairs = 0; okpairs = 0; minshare = 1.0
    for D in valid_sets(n):
        mv = moves(D)
        if not mv: continue
        sols = solutions(D)
        for (i, j) in mv:
            nm += 1; good = 0; small = False
            T = list(D); T[i] += 1; T[j] -= 1; Tset = set(T)
            for sol in sols:
                pairs += 1; any_ok = False
                (rX, cX), (rY, cY) = sol[i], sol[j]
                colof = {r: c for (r, c) in sol}
                for s in (rX + cY - 1, rY + cX + 1):
                    res = [repair(n, sol, i, j, s, st) for st in (0, 1)]
                    for nw in res:
                        if nw is not None:
                            assert sorted(r for r, c in nw) == list(range(1, n + 1)) and sorted(c for r, c in nw) == list(range(1, n + 1))
                            assert {c - r for r, c in nw} == Tset
                            any_ok = True
                    a, b = path_start(n, colof, s, rX), path_start(n, colof, s, rY)
                    twopaths = a is not None and b is not None and a != b
                    assert twopaths == (res[0] is None and res[1] is None)
                    if abs(s - (n + 1)) <= 1: small = True
                if any_ok: good += 1
            okpairs += good
            if good == 0: none_ok += 1
            if not small: none_small += 1
            minshare = min(minshare, good / len(sols))
    print("n =", n, "| minimal moves", nm, "| moves where no solution can be repaired:", none_ok,
          "| moves where no solution has s in {n, n+1, n+2}:", none_small,
          "| (move, solution) pairs", pairs, "repaired", okpairs, "| smallest share of repairable solutions %.3f" % minshare, flush=True)
