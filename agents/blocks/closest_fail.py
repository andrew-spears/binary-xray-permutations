"""closest_fail.py: per-n failures of 'pair closest to middle is a 2-block in some witness'."""
import sys
exec(open("analyze.py").read().split("NMAX = ")[0])
NMAX=int(sys.argv[1])
for n in range(4,NMAX+1):
    data=load(n); tot=fail=fail0=0; ex=[]
    for D,r in sorted(data.items()):
        if tight(D) or not r["flags"]&1: continue
        S=set(D); P=[x for x in D if x+2 in S]
        b=min(abs(x+1) for x in P); C=[x for x in P if abs(x+1)==b]
        W=set(xs(r["W2"],n)); tot+=1
        if not any(x in W for x in C):
            fail+=1; fail0+= (b==0)
            if len(ex)<3: ex.append((D,C,sorted(W)))
    print(n,tot,fail,"centre0:",fail0,ex[:2])
