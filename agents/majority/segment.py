"""Segment game.  Cut a word after every letter 0 or 1 (and wherever the slack is 0).  A SEGMENT is the piece between
two consecutive cuts: letters not in {0,1}, then one closing letter 0 or 1 (or a return to slack 0).
G(s, l) = largest sets of states (slack s, just after a letter l in {0,1}) such that from every g in G(s, l) and for
EVERY legal segment z starting there, some walk along z ends in G(s', l') (or in the empty state if s' = 0).
If the empty state is good at slack 0, every word with slacks <= B is solvable by a solver that only looks ahead
to the next 0 or 1.          Usage: python3 segment.py B"""
import sys
sys.path.insert(0, __import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "..", "interface"))
from rewrite import machine
from core import name
def levels(B, step, start):
    slack = {start: 0}; todo = [start]
    while todo:
        t = todo.pop(); s = slack[t]
        for e in range(-s, B - s + 1):
            for u in step(frozenset([t]), e):
                if u not in slack: slack[u] = s + e; todo.append(u)
    lev = {}
    for t, s in slack.items(): lev.setdefault(s, []).append(t)
    return lev
def solve(B, closing=(0, 1), verbose=True):
    step, start = machine(B); lev = levels(B, step, start)
    G = {(s, l): set(lev[s]) for s in range(1, B + 1) for l in closing}
    G[(0, 0)] = {start}
    rounds = 0
    while True:
        rounds += 1; memo = {}
        def ok(S, s, last):
            key = (S, s, last)
            if key in memo: return memo[key]
            res = True
            for e in range(max(last - 1, -s), B - s + 1):
                S2 = step(S, e); s2 = s + e
                if s2 == 0: good = start in S2
                elif e in closing: good = not S2.isdisjoint(G[(s2, e)])
                else: good = bool(S2) and ok(S2, s2, e)
                if not good: res = False; break
            memo[key] = res; return res
        changed = False
        for (s, l), states in G.items():
            bad = [g for g in states if not ok(frozenset([g]), s, l if s else 1)]
            if bad: changed = True; states.difference_update(bad)
        if verbose: print(f"  round {rounds}: sizes", " ".join(f"{s}/{l}:{len(G[(s, l)])}" for (s, l) in sorted(G) if s <= 6), flush=True)
        if not changed: break
    return G, lev, start
if __name__ == "__main__":
    B = int(sys.argv[1]); G, lev, start = solve(B)
    print(f"B = {B}: empty state good at slack 0: {start in G[(0, 0)]}")
    for (s, l) in sorted(G):
        if s == 0: continue
        print(f"slack {s:2d} after letter {l}: {len(G[(s, l)]):4d} good of {len(lev[s]):4d}: ", " ".join(sorted(name(t, B) for t in G[(s, l)]))[:160])
