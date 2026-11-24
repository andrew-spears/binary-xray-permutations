"""Upper bound for the slack of a valid word of length n (REPORT.md, HIT 1 step 5), and the true maximum for small n.
A prefix of length a with last letter e, in a word of length n = a + b, has slack
  f <= a e + a(a-1)/2   (earlier letters are <= e + distance)   and   f <= -b e + b(b+1)/2   (later letters >= e - distance).
bound(n) = max over a, e of the smaller of the two.  usage: python3 maxslack.py N [M]  (true maximum by enumeration for n <= M)"""
import sys
sys.path.insert(0, "../intervals")
def bound(n):
    return max(min(a * e + a * (a - 1) // 2, -(n - a) * e + (n - a) * (n - a + 1) // 2) for a in range(1, n) for e in range(-n, n + 1))
print("bound:", [(n, bound(n)) for n in range(2, int(sys.argv[1]) + 1)])
if len(sys.argv) > 2:
    from iv import words
    print("true :", [(n, max(max(sum(w[:j]) for j in range(n + 1)) for w in words(n))) for n in range(2, int(sys.argv[2]) + 1)])
