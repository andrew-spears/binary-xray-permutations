import json, math, numpy as np, time
from caplib import *
for n in (9,10,11):
    rows=json.load(open(f'task2_n{n}.json'))
    rk=[i for i,r in enumerate(rows) if r['D']==Pn(n) or sorted(-d for d in r['D'])==Pn(n)]
    g=[]
    for r in rows[:20]:
        lc,t,res=logcap(r['D'],n); g.append(np.abs(res.jac).max())
    lowW=[(r['W'],round(r['R'],2)) for r in rows if r['W']<=10]
    print(n,'P_n rank',rk,'of',len(rows),'maxgrad(worst20)=%.1e'%max(g),'W<=10 cases (W,R):',sorted(lowW))
# central band family D={-m..m}, n=2m+1
for m in range(1,8):
    n=2*m+1; D=list(range(-m,m+1)); t0=time.time()
    W=witnesses(D,n); lc,_,_=logcap(D,n)
    print('band n=%d W=%d logcap=%.4f R=%.3f (%.1fs)'%(n,W,lc,math.exp(math.log(W)+n*math.log(n)-math.lgamma(n+1)-lc),time.time()-t0),flush=True)
