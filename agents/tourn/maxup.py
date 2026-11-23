# Claim: for every valid s, max over witnesses of (strict) upsets of gamma(phi) == max strict upsets over ALL tournaments with s.
import sys; sys.path.insert(0,'/home/claude/agents/tourn')
from tourn import *
import networkx as nx
from collections import defaultdict
def max_upsets(s, strict=True):
    n=len(s); G=nx.DiGraph()
    G.add_node('S',demand=-n*(n-1)//2); 
    for v in range(n): G.add_edge(('v',v),'T',capacity=s[v],weight=0)
    G.add_node('T',demand=n*(n-1)//2)
    for x in range(n):
        for y in range(x+1,n):
            G.add_edge('S',(x,y),capacity=1,weight=0)
            up = (s[x]<s[y]) if strict else True   # x lower-ranked: x beats y is an upset
            G.add_edge((x,y),('v',x),capacity=1,weight=-1 if up else 0)
            G.add_edge((x,y),('v',y),capacity=1,weight=0)
    f=nx.min_cost_flow(G); return -nx.cost_of_flow(G,f)
def strict_ups(phi):
    n=len(phi); s=scores_of(phi); order=sorted(range(n),key=lambda i:i+phi[i]); rk={v:r for r,v in enumerate(order)}
    return sum(1 for a in range(n) for b in range(a+1,n) if (a-b)*(phi[a]-phi[b])<0 and s[rk[a]]!=s[rk[b]])
n=int(sys.argv[1])
best=defaultdict(lambda:-1); cnt=defaultdict(int)
for p in witnesses(n):
    s=scores_of(p); u=strict_ups(p); best[s]=max(best[s],u)
fails=[]; seqs=valid_seqs(n)
for s in seqs:
    m=max_upsets(s)
    if best[s]!=m: fails.append((s,best[s],m))
print("n",n,"valid",len(seqs),"fails",len(fails),fails[:8],flush=True)
