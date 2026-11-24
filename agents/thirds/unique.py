# Is there always an S with T(S) = 1 (a set S of stones that lies in the rows of R in exactly one solution)?
# Reads the output of ./counts and prints the D with no such S, with their smallest odd T.
# Usage: ./counts n 100 | python3 unique.py
import sys
tot = bad = 0
for line in sys.stdin:
    f = line.split('|')
    if len(f) < 4: continue
    T = [int(x.split(':')[1]) for x in f[3].split()]
    tot += 1
    if 1 not in T:
        bad += 1; odd = [t for t in T if t % 2]
        print(f"  no S with T(S) = 1: e = {f[0].strip()}, N = {f[1].strip()}, tight = {f[2].strip()}, smallest odd T = {min(odd) if odd else None}, odd S: {len(odd)} of {len(T)}")
print(f"valid D: {tot}; without an S with T(S) = 1: {bad}")
