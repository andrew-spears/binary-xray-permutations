import itertools, numpy as np
from scipy.optimize import linprog
R=[1,2,3,4,5,6]; C=[1,2,5,6,7,8]; D=[-3,-2,0,2,5,6]
cells=[(r,c) for r in R for c in C if c-r in D]
def lp(allowed):
    cs=[x for x in cells if allowed(x)]
    A=[];b=[]
    for r in R: A.append([1 if x[0]==r else 0 for x in cs]); b.append(1)
    for c in C: A.append([1 if x[1]==c else 0 for x in cs]); b.append(1)
    for d in D: A.append([1 if x[1]-x[0]==d else 0 for x in cs]); b.append(1)
    res=linprog(np.zeros(len(cs)),A_eq=A,b_eq=b,bounds=(0,1),method='highs')
    return res.status==0, {x:round(v,3) for x,v in zip(cs,res.x)} if res.status==0 else None
ok,sol=lp(lambda x:True); print(ok,{k:v for k,v in sol.items() if v>1e-6})
good=0
for par in itertools.product([0,1],repeat=len(D)):
    a=dict(zip(D,par))
    if lp(lambda x:x[0]%2==a[x[1]-x[0]])[0]: good+=1; print("feasible parity",a)
print("feasible parity choices:",good)
