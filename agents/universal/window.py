"""Windows whose length depends on the context.  Writes the list of contexts (slack, last k letters, newest first) in
which one more letter is kept, for a rule given by name, and runs ./types B Lm with it.
Usage: python3 window.py B RULE [theta_1,theta_2,...]
  slack   keep the j-th letter before the last one iff slack >= theta_j     (default theta = 3, 5, 9, 14, 20, 27)
  small   the same, and only while the last j letters are all in [-1, 3]
  stair   the same for j = 1; for j >= 2 only if the last j letters fall by exactly 1 each
  nonincr the same, and only while the last j letters are non-increasing (window stops at a rise)"""
import sys, subprocess, os
B=int(sys.argv[1]); rule=sys.argv[2]
th=[int(a) for a in sys.argv[3].split(",")] if len(sys.argv)>3 else [3,5,9,14,20,27]
m=sum(1 for t in th if t<=B)
def keep(s,w):                      # w = last j letters, newest first
    j=len(w)
    if j>len(th) or s<th[j-1]: return False
    if rule=="slack": return True
    if rule=="small": return all(-1<=a<=3 for a in w)
    if rule=="stair": return j==1 or all(w[i+1]==w[i]+1 for i in range(j-1))
    if rule=="nonincr": return all(w[i+1]>=w[i] for i in range(j-1))
ctx=set(); seen=set(); todo=[(0,())]
while todo:
    s,w=todo.pop()
    for e in range(max(w[-1]-1,-s) if w else 0, B-s+1):
        w2=(w+(e,))[-max(m,1):]; k=(s+e,w2)
        if k in seen: continue
        seen.add(k); todo.append(k)
        for j in range(1,len(w2)+1):
            c=tuple(reversed(w2[-j:]))
            if keep(s+e,c): ctx.add((s+e,)+c)
fn=f"/tmp/win_{B}_{rule}.txt"
with open(fn,"w") as f:
    for c in sorted(ctx): f.write(" ".join(map(str,c))+"\n")
r=subprocess.run(["./types",str(B),f"L{max(m,1)}"],env=dict(os.environ,NEED=fn),capture_output=True,text=True).stdout.strip().split("\n")
print(f"{rule} theta={th[:m]}:", r[-1])
