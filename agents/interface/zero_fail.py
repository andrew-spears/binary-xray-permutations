"""Find the situations where a shortening rule fails as a set inclusion, each with a shortest prefix x, and test whether
the missing states are alive (some legal continuation with slacks <= B leads them to the empty state).
Rules tested: ZERO, PEAK, RUN(2,1), RUN(1,2).     Usage: python3 zero_fail.py B"""
import sys
from collections import deque
from rewrite import machine, run
def show(m, B):
    holes = [u + 1 for u in range(-B, 0) if not m >> (B + u) & 1]; ex = [u + 1 for u in range(0, B + 1) if m >> (B + u) & 1]
    return f"holes{holes} extra{ex}"
if __name__ == "__main__":
    B = int(sys.argv[1]); step, start = machine(B)
    seen = {}; todo = deque([((), frozenset([start]), 0, None)])
    while todo:
        w, S, s, last = todo.popleft()
        if (S, s, last) in seen: continue
        seen[(S, s, last)] = w
        for e in range(0 if last is None else max(-s, last - 1), B - s + 1): todo.append((w + (e,), step(S, e), s + e, e))
    print(f"B = {B}: {len(seen)} situations", flush=True)
    def alive(t, s, last):
        """is there a legal continuation from the single state t to the empty state, slacks <= B"""
        memo = set(); st = [(frozenset([t]), s, last)]
        while st:
            S, s1, l1 = st.pop()
            if not S or (S, s1, l1) in memo: continue
            memo.add((S, s1, l1))
            if s1 == 0 and start in S: return True
            for e in range(max(-s1, l1 - 1), B - s1 + 1): st.append((step(S, e), s1 + e, e))
        return False
    rules = [("ZERO", (-1,), (0, -1)), ("PEAK", (0,), (1, 0, -1)), ("RUN(2,1)", (1, 1, 0), (2, 1, 0, -1)), ("RUN(1,2)", (0, -1, -1), (1, 0, -1, -2))]
    for (S, s, last), w in seen.items():
        for name, u, v in rules:
            a = run(S, s, last, u, B, step, 1); b = run(S, s, last, v, B, step, 1)
            if a is None or b is None: continue
            for t in a - b:
                print(name, "x =", w, " slack", s, " missing state rows:", show(t[0], B), " cols:", show(t[1], B), " alive:", alive(t, s + sum(u), u[-1]), flush=True)
