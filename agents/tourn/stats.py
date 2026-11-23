# per valid (no tight cut) score sequence: #labelled tournaments, #accepted (tie-closure of gamma image), inv stats
import sys, math; sys.path.insert(0,'/home/claude/agents/tourn')
from tourn import *
from collections import defaultdict
def inv(p): n=len(p); return sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
n=int(sys.argv[1]); docount = n<=9
W=witnesses(n); by=defaultdict(list)
for p in W: by[scores_of(p)].append(p)
seqs=valid_seqs(n); fr=[]; nonec=0
print("s | Ntot | Nacc | frac | #wit | inv range | minupset bound | maxupset bound")
for s in seqs:
    ws=by.get(s,[])
    if not ws: nonec+=1
    img=set(canon_ties(gamma(p),s) for p in ws)
    tf=1
    for c in tie_classes(s): tf*=math.factorial(len(c))
    # closure size = sum over canonical reps of orbit size; compute exactly
    clo=set()
    for p in ws:
        T=gamma(p)
        for q in tie_perms(s): clo.add(relabel(T,q))
    Nt=count_tourn(s) if docount else -1
    lb=sum(max(0,s[i]-i) for i in range(n))
    ub=sum(min(s[i], n-1-i) for i in range(n))  # crude: upsets out of i <= min(s_i, #higher)
    iv=[inv(p) for p in ws]
    f=len(clo)/Nt if Nt>0 else float('nan'); fr.append(f)
    print(s,"|",Nt,"|",len(clo),"|",round(f,4),"|",len(ws),"|",(min(iv),max(iv)) if iv else None,"|",lb,"|",ub)
print("n",n,"valid seqs",len(seqs),"with no accepted tournament",nonec,"min frac",min(fr),"mean frac",sum(fr)/len(fr))
