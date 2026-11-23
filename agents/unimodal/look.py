"""Print the solutions of a word that are centrally symmetric (sigma(n+1-i) = n+1-sigma(i)), or all if none.
Usage: python3 look.py e1 e2 ... en"""
import sys
from itertools import permutations
w = tuple(int(x) for x in sys.argv[1:]); n = len(w); D = sorted(2 * (k + 1) + e for k, e in enumerate(w))
sols = [p for p in permutations(range(1, n + 1)) if sorted(i + 1 + p[i] for i in range(n)) == D]
sym = [p for p in sols if all(p[n - 1 - i] == n + 1 - p[i] for i in range(n))]
print(f"word {w}: D = {D}; {len(sols)} solutions, {len(sym)} centrally symmetric")
for p in (sym or sols)[:6]: print("   sigma =", p)
