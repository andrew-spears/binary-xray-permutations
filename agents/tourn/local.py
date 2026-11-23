# "staircase/local" tournaments: vertices in score order, i<j is an upset (i beats j) iff j<=f(i), f nondecreasing.
# For each valid s: how many staircase tournaments have score s, and how many are accepted by delta.
import sys; sys.path.insert(0,'/home/claude/agents/tourn')
from tourn import *
from collections import defaultdict
def staircases(n):
    res=[]
    def rec(i,f):
        if i==n:
            b=[0]*n
            for x in range(n):
                for y in range(n):
                    if x<y and y<=f[x]: b[x]|=1<<y
                    elif x>y and not (x<=f[y]): b[x]|=1<<y
            res.append((tuple(f),tuple(b))); return
        lo=max(i, f[-1] if f else 0)
        for v in range(lo,n): rec(i+1,f+[v])
    rec(0,[]); return res
n=int(sys.argv[1])
W=witnesses(n); by=defaultdict(list)
for p in W: by[scores_of(p)].append(p)
st=defaultdict(list)
for f,T in staircases(n): st[svec(T)].append((f,T))
tot=good=allgood=noacc=0; bad=[]
for s in valid_seqs(n):
    clo=set()
    for p in by[s]:
        T=gamma(p)
        for q in tie_perms(s): clo.add(relabel(T,q))
    S=st.get(s,[]); a=[f for f,T in S if T in clo]
    tot+=1; good+= bool(a); allgood += (len(a)==len(S)>0)
    if not a: bad.append((s,len(S)))
    print(s,"#staircase",len(S),"#accepted",len(a), a[:3])
print("n",n,"seqs",tot,"with an accepted staircase",good,"all staircases accepted",allgood,"failures",bad[:10])
