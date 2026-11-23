"""Simulation preorder on interface states.
t <=_l t'  (same slack s, last letter l) is the largest relation with:  t empty => t' empty, and for every legal next
letter e (e >= l-1, e >= -s, s+e <= B) every e-successor u of t has an e-successor u' of t' with u <=_e u'.
If t <=_l t' then every continuation that completes t completes t'.  (Truncated at slack B: letters that would exceed
B are not challenged, so the relation at slacks near B is too generous; compare across B.)
Usage: python3 sim.py B"""
import sys, pickle
sys.path.insert(0, "../interface")
from rewrite import machine
def parts(mask, B):
    """mask -> partition (Young diagram) in the Maya/bead reading"""
    bits = [mask >> i & 1 for i in range(2 * B + 1)]
    lam = []; zeros = 0
    for b in bits:
        if b == 0: zeros += 1
        else: lam.append(zeros)
    # number of holes below each bead, drop trailing structure
    lam = [x for x in lam if x > 0]
    return tuple(sorted(lam, reverse=True))
def build(B):
    step, start = machine(B)
    slack = {start: 0}; todo = [start]; succ = {}
    while todo:
        t = todo.pop(); s = slack[t]
        for e in range(-s, B - s + 1):
            out = step(frozenset([t]), e); succ[(t, e)] = out
            for u in out:
                if u not in slack: slack[u] = s + e; todo.append(u)
    return step, start, slack, succ
def simulate(B):
    step, start, slack, succ = build(B)
    lev = {}
    for t, s in slack.items(): lev.setdefault(s, []).append(t)
    L = range(-B, B + 1)
    R = {l: {(t, t2) for s in lev for t in lev[s] for t2 in lev[s] if s <= B and l - 1 <= B - s or True} for l in L}
    changed = True; rounds = 0
    while changed:
        changed = False; rounds += 1
        for l in L:
            bad = []
            for (t, t2) in R[l]:
                if t == t2: continue
                s = slack[t]; ok = True
                for e in range(max(l - 1, -s), B - s + 1):
                    A = succ[(t, e)]
                    if not A: continue
                    A2 = succ[(t2, e)]; Re = R[e]
                    for u in A:
                        if not any((u, u2) in Re for u2 in A2): ok = False; break
                    if not ok: break
                if not ok: bad.append((t, t2))
            if bad:
                changed = True
                for p in bad: R[l].discard(p)
    return step, start, slack, lev, R, rounds
if __name__ == "__main__":
    B = int(sys.argv[1])
    step, start, slack, lev, R, rounds = simulate(B)
    pickle.dump((slack, R), open(f"sim{B}.pkl", "wb"))
    print(f"B = {B}: {len(slack)} states, {rounds} rounds")
    for l in (-B, -2, -1, 0, 1, 2):
        row = []
        for s in sorted(lev):
            n = len(lev[s]); strict = sum(1 for (t, t2) in R[l] if slack[t] == s and t != t2)
            both = sum(1 for (t, t2) in R[l] if slack[t] == s and t != t2 and (t2, t) in R[l])
            row.append(f"{s}:{n}/{strict}/{both}")
        print(f"  last {l:3d}  slack:states/comparable ordered pairs/equivalent  ", " ".join(row))
