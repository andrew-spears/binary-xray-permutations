import pickle,sys
from exlib import valid,wits,Pn,Ds
from nearP import moves,three_cycles
G=pickle.load(open(sys.argv[1],"rb")); N=max(G)
for n in range(4,N+1):
    miss=[];tot=0
    for D in Ds(n):
        if tuple(sorted(-x for x in D))<D: continue
        tot+=1
        Ws=wits(D)
        if not any(w in G[n] for w in Ws): miss.append((three_cycles(D)-three_cycles(Pn(n)),D,len(Ws)))
    print(n,"valid",tot,"missed",len(miss))
    for m in sorted(miss)[:12]: print("   layer",m[0],m[1],"W",m[2])
