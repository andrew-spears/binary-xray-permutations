// conn.c: witness-graph connectivity and move-lift radius for binary x-rays.
// Usage: ./conn n   (prints summary; writes per-D details to stderr-free files via stdout sections)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned long long u64;
int n; int perm[16];
u64 *P; uint32_t *DM; long cnt=0, cap=1<<20;
void rec(int r, uint32_t ud, uint32_t uc, u64 code){
  if(r==n){ if(cnt==cap){cap*=2;P=realloc(P,cap*8);DM=realloc(DM,cap*4);} P[cnt]=code; DM[cnt]=ud; cnt++; return;}
  for(int c=0;c<n;c++){ if(uc>>c&1) continue; int m=c-r+n-1; if(ud>>m&1) continue;
    rec(r+1, ud|1u<<m, uc|1u<<c, code | ((u64)c<<(4*r))); }
}
static int cmpi(const void*a,const void*b){ long x=*(long*)a,y=*(long*)b; if(DM[x]!=DM[y]) return DM[x]<DM[y]?-1:1; return P[x]<P[y]?-1:(P[x]>P[y]); }
static inline int get(u64 c,int r){return (c>>(4*r))&15;}
static inline int ham(u64 a,u64 b){ u64 x=a^b; x=(x|x>>1|x>>2|x>>3)&0x1111111111111111ULL; return __builtin_popcountll(x);}
// returns 1 if pi' = pi o tau with tau a single cycle on differing rows
static int single(u64 a,u64 b,int h){
  int inv[16]; for(int r=0;r<n;r++) inv[get(a,r)]=r; // inv of pi: col->row
  int s=-1; for(int r=0;r<n;r++) if(get(a,r)!=get(b,r)){s=r;break;}
  int x=s,len=0; do{ x=inv[get(b,x)]; len++; }while(x!=s && len<=n);
  return len==h;
}
int uf[1<<17];
int fd(int x){while(uf[x]!=x){uf[x]=uf[uf[x]];x=uf[x];}return x;}
uint32_t mirror(uint32_t m){uint32_t r=0; for(int i=0;i<2*n-1;i++) if(m>>i&1) r|=1u<<(2*n-2-i); return r;}
int notight(uint32_t m){ int k=0; long s=0; for(int i=0;i<2*n-1;i++) if(m>>i&1){ int d=i-(n-1); k++; s+=d+n-k; if(k<n && s==(long)k*(k-1)/2) return 0;} return 1;}
void prD(FILE*f,uint32_t m){ fprintf(f,"{"); int first=1; for(int i=0;i<2*n-1;i++) if(m>>i&1){fprintf(f,first?"%d":",%d",i-(n-1));first=0;} fprintf(f,"}");}
void prP(FILE*f,u64 c){ for(int r=0;r<n;r++) fprintf(f,"%d",get(c,r)+1>9?0:get(c,r)+1); }
long *ord; long *st; long nD;
long findD(uint32_t m){ long lo=0,hi=nD-1; while(lo<=hi){long md=(lo+hi)/2; uint32_t x=DM[ord[st[md]]]; if(x==m) return md; if(x<m) lo=md+1; else hi=md-1;} return -1;}
long nmovesG[40]; long nfailG=0;
int main(int argc,char**argv){
  n=atoi(argv[1]); P=malloc(cap*8); DM=malloc(cap*4);
  rec(0,0,0,0);
  ord=malloc(cnt*sizeof(long)); for(long i=0;i<cnt;i++) ord[i]=i; qsort(ord,cnt,sizeof(long),cmpi);
  st=malloc((cnt+1)*sizeof(long)); nD=0; for(long i=0;i<cnt;i++) if(i==0||DM[ord[i]]!=DM[ord[i-1]]) st[nD++]=i; st[nD]=cnt;
  printf("n=%d witnesses=%ld validD=%ld\n",n,cnt,nD);
  // ---- Task 1: connectivity. variants: C_k (single cycle length<=k), R_k (any rearrangement of <=k rows)
  int K=n; static int maxcompC[17],maxcompR[17]; static long ndisC[17],ndisR[17]; static uint32_t exC[17],exR[17]; static int exCc[17],exRc[17];
  long nNT=0; int maxW=0;
  int *e=malloc(sizeof(int)*0); (void)e;
  int movesonly=argc>2;
  for(long d=0;d<nD && !movesonly;d++){
    uint32_t m=DM[ord[st[d]]]; if(!notight(m)) continue; uint32_t mm=mirror(m); if(mm>m) continue; // canonical up to mirror: keep larger mask
    nNT++; int W=st[d+1]-st[d]; if(W>maxW) maxW=W;
    u64 *w=malloc(W*8); for(int i=0;i<W;i++) w[i]=P[ord[st[d]+i]];
    // store pair types: hist edges per (h, single)
    // do UF per k for both variants
    for(int var=0;var<2;var++) for(int k=3;k<=K;k++){
      for(int i=0;i<W;i++) uf[i]=i; int comps=W;
      for(int i=0;i<W;i++) for(int j=i+1;j<W;j++){ int h=ham(w[i],w[j]); if(h>k) continue; if(var==0 && !single(w[i],w[j],h)) continue;
        int a=fd(i),b=fd(j); if(a!=b){uf[a]=b;comps--;} }
      int *mc= var?maxcompR:maxcompC; long *nd= var?ndisR:ndisC; uint32_t *ex= var?exR:exC; int *exc= var?exRc:exCc;
      if(comps>mc[k]) mc[k]=comps; if(comps>1){ if(nd[k]==0){ex[k]=m;exc[k]=comps;} nd[k]++; }
      if(comps==1) { /* larger k also connected */ for(int kk=k+1;kk<=K;kk++){} break; }
    }
    free(w);
  }
  printf("noTightCut canonical D=%ld maxW=%d\n",nNT,maxW);
  for(int var=0;var<2;var++) for(int k=3;k<=K;k++){
    int *mc= var?maxcompR:maxcompC; long *nd= var?ndisR:ndisC; uint32_t *ex= var?exR:exC; int *exc= var?exRc:exCc;
    printf("%s k=%d: #disconnected D=%ld maxComponents=%d", var?"R(any<=k rows)":"C(single cycle<=k)",k,nd[k],mc[k]);
    if(nd[k]){ printf(" firstEx="); prD(stdout,ex[k]); printf(" comps=%d",exc[k]); }
    printf("\n"); if(nd[k]==0) break;
  }
  fflush(stdout);
  // ---- Task 2: moves
  int maxr=0, maxrNT=0, maxrArb=0; static long rhist[17]; uint32_t exMove=0; int exA=0;
  static int maxcompR3[17]; // max over moves of max over components (C_k graph of D) of min r in component
  for(long d=0;d<nD;d++){
    uint32_t m=DM[ord[st[d]]];
    for(int a=0;a+3<2*n-1;a++) for(int b=a+3;b<2*n-1;b++){
      if(!((m>>a&1)&&(m>>b&1)&&!(m>>(a+1)&1)&&!(m>>(b-1)&1))) continue;
      int okm=1; for(int c=a+2;c<=b-2;c++) if(!(m>>c&1)) okm=0; if(!okm) continue;
      uint32_t m2=(m&~(1u<<a)&~(1u<<b))|(1u<<(a+1))|(1u<<(b-1));
      { // direct swap-position check: a-point row i, b-point row i-(b-a-1)
        int W0=st[d+1]-st[d], found=0, g=b-a-1;
        for(int t=0;t<W0 && !found;t++){ u64 c=P[ord[st[d]+t]]; int ra=-1,rb=-1;
          for(int r=0;r<n;r++){int dg=get(c,r)-r+n-1; if(dg==a)ra=r; if(dg==b)rb=r;}
          if(rb==ra-g) found=1; }
        nmovesG[b-a]++; if(!found){ nfailG++; if(nfailG==1){printf("FIRST SWAP FAILURE: D="); prD(stdout,m); printf(" stones %d,%d\n",a-(n-1),b-(n-1));} }
      }
      long d2=findD(m2); if(d2<0){ printf("MOVE TARGET WITHOUT WITNESS! "); prD(stdout,m2); printf("\n"); continue; }
      int W=st[d+1]-st[d], W2=st[d2+1]-st[d2];
      u64 *w=malloc(W*8),*w2=malloc(W2*8); for(int i=0;i<W;i++) w[i]=P[ord[st[d]+i]]; for(int i=0;i<W2;i++) w2[i]=P[ord[st[d2]+i]];
      int *r=malloc(W*sizeof(int)); int best=99, worst=0;
      for(int i=0;i<W;i++){ int b=99; for(int j=0;j<W2;j++){int h=ham(w[i],w2[j]); if(h<b)b=h;} r[i]=b; if(b<best)best=b; if(b>worst)worst=b; }
      rhist[best]++; if(best>2){printf("  min r=%d at D=",best);prD(stdout,m);printf(" stones %d,%d\n",a-(n-1),b-(n-1));} if(best>maxr){maxr=best;exMove=m;exA=a;} (void)exA;
      if(notight(m)&&notight(m2)&&best>maxrNT) maxrNT=best;
      if(worst>maxrArb) maxrArb=worst;
      for(int k=3;k<=K && !movesonly;k++){
        for(int i=0;i<W;i++) uf[i]=i;
        for(int i=0;i<W;i++) for(int j=i+1;j<W;j++){int h=ham(w[i],w[j]); if(h<=k && single(w[i],w[j],h)){int x=fd(i),y=fd(j); if(x!=y) uf[x]=y;}}
        int *cm=malloc(W*sizeof(int)); for(int i=0;i<W;i++) cm[i]=99; for(int i=0;i<W;i++){int c=fd(i); if(r[i]<cm[c]) cm[c]=r[i];}
        int mx=0; for(int i=0;i<W;i++) if(fd(i)==i && cm[i]>mx) mx=cm[i]; if(mx>maxcompR3[k]) maxcompR3[k]=mx; free(cm);
      }
      free(w);free(w2);free(r);
    }
  }
  printf("general moves by gap b-a:"); for(int g=3;g<2*n;g++) if(nmovesG[g]) printf(" %d:%ld",g,nmovesG[g]); printf("  swap-position failures=%ld\n",nfailG);
  printf("moves: max over moves of min_witness r = %d (both ends no-tight-cut: %d); max over witnesses (arbitrary) = %d\n",maxr,maxrNT,maxrArb);
  printf("  hist of min r:"); for(int i=0;i<=n;i++) if(rhist[i]) printf(" r=%d:%ld",i,rhist[i]); printf("\n");
  if(maxr>0){ printf("  worst move: D="); prD(stdout,exMove); printf(" (a=%d)\n",exA-(n-1)); }
  printf("  per-component (C_k graph of D) worst min-r:"); for(int k=3;k<=K;k++) printf(" k=%d:%d",k,maxcompR3[k]); printf("\n");
  return 0;
}
