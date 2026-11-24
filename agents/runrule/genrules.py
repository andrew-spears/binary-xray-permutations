"""Print the rule list PEAK, ZERO, RUN(a,b) (a, b <= amax) in the format read by ./rules."""
import sys
def urun(a, b):
    out = []
    for t in range(a - 1, -b, -1):
        out.append(t)
        if t == a - b: out.append(t)
    return out
if __name__ == "__main__":
    amax = int(sys.argv[1])
    f = lambda w: " ".join(map(str, w))
    print("PEAK : 0 | 1 0 -1"); print("ZERO : -1 | 0 -1"); print("RUN(1,1) : 0 0 | 1 0 -1")
    for a in range(1, amax + 1):
        for b in range(1, amax + 1):
            if (a, b) != (1, 1): print(f"RUN({a},{b}) : {f(urun(a, b))} | {f(range(a, -b - 1, -1))}")
