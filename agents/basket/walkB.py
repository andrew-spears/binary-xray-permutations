import random
def part(X):
    X=sorted(X); return tuple(sorted([x-i-1 for i,x in enumerate(X) if x-i-1>0],reverse=True))
def word(n,B,seed):
    random.seed(seed)
    while True:
        e=[];s=0
        ok=True
        for k in range(n):
            lo=max(0 if k==0 else e[-1]-1, -s+ (1 if k<n-1 else 0)); hi=B-s
            if k==n-1: lo=hi=-s
            c=[x for x in range(lo,hi+1) if k==0 or x>=e[-1]-1]
            if not c: ok=False;break
            x=random.choice(c); e.append(x); s+=x
        if ok and s==0: return e
n,B=20,3
e=word(n,B,7)
b=[2*(k+1)+e[k] for k in range(n)]
D=[x-n-1 for x in b]
print("e",e); print("D",D)
sig=[sum(e[:k+1]) for k in range(n)]; print("slack",sig)
# forward: layers of {state: (R,C,parent_state,cell)}
layer={((),()):(frozenset(),frozenset(),None,None)}
layers=[layer]
for k in range(n):
    new={}
    for st,(R,C,_,_) in layer.items():
        for r in range(1,n+1):
            c=b[k]-r
            if 1<=c<=n and r not in R and c not in C:
                R2,C2=R|{r},C|{c}; s2=(part(R2),part(C2))
                if s2 not in new: new[s2]=(R2,C2,st,(r,c))
    layer=new; layers.append(layer)
    print(f"stone {k+1:2d}  e={e[k]:+d}  slack={sig[k]}  reachable={len(layer):2d}  ", sorted(layer)[:6])
# backtrack
st=((),()); cells=[]
for k in range(n,0,-1):
    R,C,par,cell=layers[k][st]; cells.append(cell); st=par
cells.reverse()
pi=[0]*n
for r,c in cells: pi[n-r]=c   # original row from top = n+1-r'
print("witness",pi, "diagonals",sorted(pi[i]-(i+1) for i in range(n))==sorted(D))
