"""Reachable sets F(x) for prefixes x with letters -1, 0, +1 (distinct diagonals: no '+ -' adjacent).
Lists, per slack, the distinct sets with a shortest word, their size, and the number of all states of that slack.
Usage: python3 sets.py B"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "interface"))
from rewrite import machine
def explore(B, rep=False):
    step, start = machine(B)
    word = {(frozenset([start]), 0, None): ""}; layer = list(word)
    while layer:
        nxt = []
        for S, s, last in layer:
            for e, ch in ((-1, "-"), (0, "0"), (1, "+")):
                if s + e < 0 or s + e > B or (last == 1 and e == -1 and not rep): continue
                x = (step(S, e), s + e, e)
                if x not in word: word[x] = word[(S, s, last)] + ch; nxt.append(x)
        layer = nxt
    return word, step, start
def allstates(B, step, start):
    """every interface state, by slack (reachable by arbitrary letters)"""
    lvl = {0: {start}}; seen = {start}; todo = [(start, 0)]
    while todo:
        st, s = todo.pop()
        for e in range(-s, B - s + 1):
            for t in step(frozenset([st]), e):
                if t not in seen: seen.add(t); lvl.setdefault(s + e, set()).add(t); todo.append((t, s + e))
    return lvl
if __name__ == "__main__":
    B = int(sys.argv[1]); word, step, start = explore(B); lvl = allstates(B, step, start)
    for s in range(B):
        fam = sorted(((len(S), last, w) for (S, s2, last), w in word.items() if s2 == s), key=lambda t: (t[1] is None, t[1], t[0]))
        print(f"slack {s}: {len(lvl[s])} states; {len(fam)} sets:", "  ".join(f"{w or 'empty'}:{n}" for n, last, w in fam))
