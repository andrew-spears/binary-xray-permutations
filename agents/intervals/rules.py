import sys
from iv import words
from pm import succ
def run(w, pick):
    u = ()
    for e in w:
        S = succ(u, e)
        if not S: return False
        u = pick(S)
    return True
rules = {"smallest m": lambda S: S[0], "largest m": lambda S: S[-1],
         "most parts": lambda S: max(S, key=lambda u: (len(u), u)), "fewest parts": lambda S: min(S, key=lambda u: (len(u), u)),
         "lex largest": max, "lex smallest": min,
         "most parts, then flattest": lambda S: max(S, key=lambda u: (len(u), [-x for x in u]))}
for n in range(4, int(sys.argv[1]) + 1):
    W = words(n)
    print(n, len(W), {r: sum(not run(w, p) for w in W) for r, p in rules.items()})
