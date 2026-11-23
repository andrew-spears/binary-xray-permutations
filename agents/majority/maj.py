"""Majority measure test.  F(x) = states reachable after prefix x; A(y) = states from which the suffix y reaches the
empty state.  xy is solvable iff F(x) meets A(y).  If for each slack s there are weights w >= 0 on the states of
slack s, total 1, with  min_x w(F(x)) + min_y w(A(y)) > 1, then every F meets every A: the conjecture for the words
considered.  This computes the best such w by linear programming, for all prefixes/suffixes with slacks <= B.
Usage: python3 maj.py B [junction]     (junction=1: only require pairs with first(y) >= last(x) - 1, one LP per cut)"""
import os, sys
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "interface"))
from rewrite import machine
def families(B):
    step, start = machine(B)
    # forward
    Fs = {}; seen = set(); todo = [(frozenset([start]), 0, None)]
    slack = {start: 0}
    while todo:
        S, s, last = todo.pop()
        if (S, s, last) in seen or not S: continue
        seen.add((S, s, last)); Fs.setdefault(s, set()).add((S, last))
        for e in range(0 if last is None else max(-s, last - 1), B - s + 1): todo.append((step(S, e), s + e, e))
    # all states by slack (reachable by any letters)
    todo = [start]; succ = {}
    while todo:
        t = todo.pop(); s = slack[t]
        for e in range(-s, B - s + 1):
            out = step(frozenset([t]), e); succ[(t, e)] = out
            for u in out:
                if u not in slack: slack[u] = s + e; todo.append(u)
    lev = {}
    for t, s in slack.items(): lev.setdefault(s, []).append(t)
    def pre(A, s, e):   # states of slack s - e with an e-successor in A
        return frozenset(t for t in lev.get(s - e, []) if succ[(t, e)] & A)
    As = {}; seen = set(); todo = [(frozenset([start]), 0, None)]
    while todo:
        A, s, first = todo.pop()
        if (A, s, first) in seen or not A: continue
        seen.add((A, s, first)); As.setdefault(s, set()).add((A, first))
        for e in range(s - B, (B if first is None else first + 1) + 1):
            if first is None and e > 0: continue      # last letter of a valid word is <= 0
            if s - e < 0: continue
            todo.append((pre(A, s, e), s - e, e))
    return lev, Fs, As
def best(states, FF, AA):
    """max m1 + m2 with w(F) >= m1, w(A) >= m2"""
    idx = {t: i for i, t in enumerate(states)}; n = len(states)
    c = np.zeros(n + 2); c[n] = c[n + 1] = -1
    rows = []
    for F in FF:
        r = np.zeros(n + 2); r[n] = 1
        for t in F: r[idx[t]] = -1
        rows.append(r)
    for A in AA:
        r = np.zeros(n + 2); r[n + 1] = 1
        for t in A: r[idx[t]] = -1
        rows.append(r)
    eq = np.zeros((1, n + 2)); eq[0, :n] = 1
    res = linprog(c, A_ub=np.array(rows), b_ub=np.zeros(len(rows)), A_eq=eq, b_eq=[1], bounds=[(0, None)] * n + [(0, 1)] * 2, method="highs")
    return -res.fun, res.x[:n], res.x[n], res.x[n + 1]
if __name__ == "__main__":
    B = int(sys.argv[1]); junction = len(sys.argv) > 2 and sys.argv[2] == "1"
    lev, Fs, As = families(B)
    for s in range(1, B + 1):
        if junction:
            for l in sorted({l for F, l in Fs[s]}):
                FF = {F for F, l2 in Fs[s] if l2 == l}; AA = {A for A, f in As[s] if f >= l - 1}
                if not AA: continue
                val, w, m1, m2 = best(lev[s], FF, AA)
                print(f"slack {s} last letter {l:2d}: {len(FF)} reachable sets, {len(AA)} completable sets;  best m1 + m2 = {val:.4f} (m1 {m1:.3f}, m2 {m2:.3f}), support {int((w > 1e-9).sum())}", flush=True)
            continue
        FF = {F for F, l in Fs.get(s, [])}; AA = {A for A, f in As.get(s, [])}
        # sanity: all compatible pairs meet?
        bad = sum(1 for F, l in Fs[s] for A, f in As[s] if f >= l - 1 and not (F & A))
        val, w, m1, m2 = best(lev[s], FF, AA)
        supp = int((w > 1e-9).sum())
        print(f"slack {s}: {len(lev[s])} states, {len(FF)} reachable sets, {len(AA)} completable sets, disjoint compatible pairs {bad};  best m1 + m2 = {val:.4f} (m1 {m1:.3f}, m2 {m2:.3f}), support {supp}", flush=True)
