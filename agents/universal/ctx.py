"""Variable windows.  A context = (slack, last k letters), k >= 1.  The list N of contexts that keep one more letter
defines a type (./types B Lm with NEED=file).  Start from all contexts of length <= m (the full window, which must
work at bound B) and greedily remove contexts while the family still works (longest contexts first; within a length
in the given order, by bisection).  Prints the surviving list: one locally minimal set, not canonical.
Usage: python3 ctx.py B m [up|down|rand<seed>] [out file]"""
import sys, subprocess, os, random
B=int(sys.argv[1]); m=int(sys.argv[2]); order=sys.argv[3] if len(sys.argv)>3 else "up"
fn=sys.argv[4] if len(sys.argv)>4 else f"/tmp/need_{B}_{m}_{order}.txt"
ctx=set(); seen=set(); todo=[(0,())]
while todo:
    s,w=todo.pop()
    for e in range(max(w[-1]-1,-s) if w else 0, B-s+1):
        w2=(w+(e,))[-m:]; k=(s+e,w2)
        if k in seen: continue
        seen.add(k); todo.append(k)
        for j in range(1,len(w2)+1): ctx.add((s+e,)+tuple(reversed(w2[-j:])))    # (slack, last, the one before, ...)
runs=0
def works(N):
    global runs; runs+=1
    with open(fn,"w") as f:
        for c in N: f.write(" ".join(map(str,c))+"\n")
    r=subprocess.run(["./types",str(B),f"L{m}"],env=dict(os.environ,NEED=fn),capture_output=True,text=True).stdout.strip().split("\n")
    return "WORKS" in r[-1], r[-1]
N=set(ctx); assert works(N)[0], "the full window does not work"
def process(C):
    global N
    C=[c for c in C if c in N]
    if not C: return
    if works(N-set(C))[0]: N-=set(C); return
    if len(C)==1: return
    h=len(C)//2; process(C[:h]); process(C[h:])
LV=int(os.environ.get("LEVELS","99"))
for k in range(m,max(0,m-LV),-1):
    C=sorted(c for c in ctx if len(c)==k+1)
    if order=="down": C.reverse()
    if order.startswith("rand"): random.Random(int(order[4:] or 0)).shuffle(C)
    process(C)
    # contexts whose shorter context was removed are dead
    N={c for c in N if all(c[:j] in N for j in range(2,len(c)))}
ok,line=works(sorted(N))
print(f"bound {B}, window {m}, order {order}: {len(ctx)} contexts, {len(N)} kept, {runs} runs;", line)
for c in sorted(N, key=lambda c:(len(c),c)): print("  slack",c[0],"letters (last first)",*c[1:])
