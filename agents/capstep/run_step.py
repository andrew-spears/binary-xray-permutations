"""Task 1+2: one-step Gurvits inequality cap(q_{S+d}) >= g(k) cap(q_S) over all subsets/orders.
usage: python3 run_step.py n  -> writes step_n{n}.json"""
import sys, json, math, numpy as np
from multiprocessing import Pool
from steplib import *

def analyze(D):
    n = len(D); m = n
    P = poly(D, n)
    N = 1 << m
    lcap = [None]*N; deg = [None]*N
    for S in range(N):
        Sl = [k for k in range(m) if (S >> k) & 1]
        E, C, rem = restrict(P, set(Sl), m)
        if len(rem) == 0:
            lcap[S] = math.log(C.sum()); deg[S] = {}
        else:
            lcap[S] = logcap(E, C)
            deg[S] = {k: int(E[:, i].max()) for i, k in enumerate(rem)}
    W = math.exp(lcap[N-1])
    edges = {}  # (S,k) -> (log ratio, kdeg)
    for S in range(N-1):
        for k, kd in deg[S].items():
            T = S | (1 << k)
            edges[(S, k)] = (lcap[T] - lcap[S], kd)
    # bottleneck DP: best[S] = max over paths from 0 to S of min step value
    def bottleneck(val):
        best = [-1e18]*N; best[0] = 1e18; arg = [None]*N
        for S in range(N):
            if best[S] == -1e18: continue
            for k in deg[S]:
                T = S | (1 << k); v = min(best[S], val(S, k))
                if v > best[T]: best[T] = v; arg[T] = (S, k)
        order = []; T = N-1
        while T: S, k = arg[T]; order.append(D[k]); T = S
        return best[N-1], order[::-1]
    gurv = lambda S, k: edges[(S, k)][0] - math.log(g(edges[(S, k)][1]))
    plain = lambda S, k: edges[(S, k)][0]
    bg, og = bottleneck(gurv)
    bp, op = bottleneck(plain)
    def negalpha(S, k):
        lr, kd = edges[(S, k)]
        if kd <= 1: return 0.0
        return lr / (-math.log(g(kd)))   # = -alpha, ratio = g(k)^alpha
    ba, oa = bottleneck(negalpha)
    # worst edge
    wS, wk = min(edges, key=lambda e: gurv(*e))
    wp = min(edges, key=lambda e: plain(*e))
    def run_order(seq_rule):
        S = 0; vals = []; pv = []
        while S != N-1:
            k = seq_rule(S)
            vals.append(gurv(S, k)); pv.append(plain(S, k)); S |= 1 << k
        return min(vals), min(pv)
    rules = {
        'outer_first': lambda S: max(deg[S], key=lambda k: (abs(D[k]), D[k])),
        'inner_first': lambda S: min(deg[S], key=lambda k: (abs(D[k]), D[k])),
        'left_to_right': lambda S: min(deg[S]),
        'min_deg_first': lambda S: min(deg[S], key=lambda k: (deg[S][k], -abs(D[k]))),
        'max_deg_first': lambda S: max(deg[S], key=lambda k: (deg[S][k], abs(D[k]))),
        'greedy_best_gurv': lambda S: max(deg[S], key=lambda k: gurv(S, k)),
    }
    rr = {nm: [math.exp(v) for v in run_order(r)] for nm, r in rules.items()}
    gb = math.exp(lcap[0])
    return dict(D=D, W=W, cap=gb, slack=W*n**n/(math.factorial(n)*gb),
                best_order_gurv=math.exp(bg), best_order=og,
                best_order_plain=math.exp(bp), best_plain_order=op, best_alpha=-ba, best_alpha_order=oa,
                worst_edge_gurv=math.exp(gurv(wS, wk)), worst_edge=dict(S=[D[i] for i in range(m) if wS>>i&1], d=D[wk], k=edges[(wS,wk)][1], ratio=math.exp(edges[(wS,wk)][0])),
                worst_edge_plain=math.exp(plain(*wp)), worst_plain=dict(S=[D[i] for i in range(m) if wp[0]>>i&1], d=D[wp[1]], k=edges[wp][1]),
                rules=rr, n_bad_edges=sum(1 for e in edges if gurv(*e) < -1e-7), n_edges=len(edges))

if __name__ == '__main__':
    n = int(sys.argv[1])
    Ds = canon_Ds(n)
    with Pool(2) as p: res = p.map(analyze, Ds)
    json.dump(res, open(f'step_n{n}.json', 'w'), indent=1)
    print(f'n={n} #D={len(res)}')
    print(' min best-order gurv ratio:', min(r['best_order_gurv'] for r in res))
    print(' #D with no working order:', sum(r['best_order_gurv'] < 1-1e-7 for r in res))
    print(' min worst-edge gurv:', min(r['worst_edge_gurv'] for r in res))
    print(' min best-order plain ratio:', min(r['best_order_plain'] for r in res))
    ra = max(res, key=lambda r: r['best_alpha'])
    print(' max over D of best-order alpha (ratio>=g(k)^alpha):', ra['best_alpha'], ra['D'], ra['best_alpha_order'])
    print(' min worst-edge plain:', min(r['worst_edge_plain'] for r in res))
    for nm in res[0]['rules']:
        print(f'  rule {nm}: min gurv {min(r["rules"][nm][0] for r in res):.4f}  #fail {sum(r["rules"][nm][0]<1-1e-7 for r in res)}  min plain {min(r["rules"][nm][1] for r in res):.4f}')
