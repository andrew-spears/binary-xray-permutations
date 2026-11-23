"""Other prefix summaries for the inductive-invariant test (see invariant.py).
Each summary keeps sigma and the last letter, plus one more statistic capped at K.
Usage: python3 invariant_other.py B"""
import sys
from invariant import analyse
B = int(sys.argv[1])
def mk(kind, K):
    # hist = (extra, e_last); invariant.py reads hist[-1] as the last letter
    def upd(hist, e, s2):
        x = hist[0] if hist else (0 if kind != "minsig" else K)
        if kind == "len": x = min(x + 1, K)
        elif kind == "maxsig": x = min(max(x, s2), K)
        elif kind == "sumsig": x = min(x + s2, K)
        elif kind == "maxe": x = min(max(x, e), K)
        elif kind == "sincetop":   # steps since slack last increased
            x = 0 if e > 0 else min(x + 1, K)
        return (x, e)
    return upd
for kind in ["len", "maxsig", "sumsig", "maxe", "sincetop"]:
    for K in range(0, 2 * B + 2):
        nodes, I, fails, _ = analyse(B, 0, upd=mk(kind, K))
        if not fails:
            print(f"B={B} summary (sigma, e_last, min({kind}, K)): suffices from K = {K} ({len(nodes)} summaries)"); break
    else:
        print(f"B={B} summary (sigma, e_last, min({kind}, K)): FAILS for all K <= {2*B+1}")
