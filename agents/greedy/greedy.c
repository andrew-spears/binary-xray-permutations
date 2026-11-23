// Greedy witness constructions for BMPS / Nordh Conj. 10.
// For each n, enumerates every no-tight-cut Landau D (both D and -D, since rules are not mirror-symmetric),
// runs each greedy rule (no backtracking) and records failures.
// Usage: ./greedy NMAX
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int n, FULL;
static int D[32];          // current instance, sorted
static int ND;             // = n

static inline int pc(int x){ return __builtin_popcount(x); }
static inline int shiftc(int colfree, int d){ // row i available iff col i+d free
  int r = d >= 0 ? (colfree >> d) : (colfree << (-d));
  return r & FULL;
}
static inline int availmask(int rf, int cf, int d){ return rf & shiftc(cf, d); }

// necessary test: every remaining diagonal has a cell, sums match, generalized Landau on (rows, cols, diags)
static int sumtest(int rf, int cf, int dm){
  int dv[32], m=0, rs[32], cs[32], a=0, b=0;
  for(int t=0;t<ND;t++) if(dm>>t&1){ if(!availmask(rf,cf,D[t])) return 0; dv[m++]=D[t]; } // D sorted asc
  for(int i=0;i<n;i++){ if(rf>>i&1) rs[a++]=i; if(cf>>i&1) cs[b++]=i; }   // ascending
  int s1=0,s2=0,top=0,bot=0;
  for(int k=1;k<=m;k++){
    s1 += dv[m-k];                // k largest d
    top += cs[m-k] - rs[k-1];     // k largest cols - k smallest rows
    if(s1 > top) return 0;
    s2 += dv[k-1];                // k smallest d
    bot += cs[k-1] - rs[m-k];     // k smallest cols - k largest rows
    if(s2 < bot) return 0;
  }
  return s1==top;
}
static int exact_cnt; // exact solvability (diagnostic)
static int solvable(int rf, int cf, int dm){
  if(!dm) return 1;
  // branch on diagonal with fewest cells
  int bt=-1, bc=99;
  for(int t=0;t<ND;t++) if(dm>>t&1){ int c=pc(availmask(rf,cf,D[t])); if(c<bc){bc=c;bt=t;} }
  if(bc==0) return 0;
  int am=availmask(rf,cf,D[bt]);
  while(am){ int i=__builtin_ctz(am); am&=am-1; int j=i+D[bt];
    if(solvable(rf&~(1<<i), cf&~(1<<j), dm&~(1<<bt))) return 1; }
  return 0;
}

// ---- cell scores (lower = better) ----
enum { S_MINROW, S_MAXROW, S_CENTER, S_FAR, S_DAMAGE, S_WDAMAGE, NS };
static const char* SN[]={"minrow","maxrow","center","far","leastdamage","leastweighteddamage"};
static int cellscore(int S, int i, int j, int rf, int cf, int dm, int self){
  switch(S){
    case S_MINROW: return i;
    case S_MAXROW: return -i;
    case S_CENTER: return 64*abs(i+j-(n-1)) + i;
    case S_FAR:    return -64*abs(i+j-(n-1)) + i;
    case S_DAMAGE: { // number of other diagonals' available cells killed
      int k=0; for(int t=0;t<ND;t++) if((dm>>t&1) && t!=self){
        int am=availmask(rf,cf,D[t]); int jj;
        if(am>>i&1) k++;               // same row
        int ii=j-D[t]; if(ii>=0&&ii<n&&ii!=i&&(am>>ii&1)) k++; // same column
        (void)jj; }
      return 64*k + i; }
    case S_WDAMAGE: { // killed cells weighted by 1/(cells left on that diagonal)
      long k=0; for(int t=0;t<ND;t++) if((dm>>t&1) && t!=self){
        int am=availmask(rf,cf,D[t]); int c=pc(am), h=0;
        if(am>>i&1) h++;
        int ii=j-D[t]; if(ii>=0&&ii<n&&ii!=i&&(am>>ii&1)) h++;
        if(h) k += h*(720720L/c)/(c>h? c-h:1) ; }  // ~ 1/(c(c-h)): hurts more when few remain
      return (int)(k*16 + i); }
  }
  return 0;
}

// ---- Type A: pick diagonal by order policy, then cell by score ----
enum { P_ABSPOS, P_ABSNEG, P_DDESC, P_DASC, P_MRV, NP };
static const char* PN[]={"|d|desc(+first)","|d|desc(-first)","d desc","d asc","fewest-cells(MRV)"};
static int pickdiag(int P, int rf, int cf, int dm){
  int best=-1; long bk=1L<<40;
  for(int t=0;t<ND;t++) if(dm>>t&1){
    int d=D[t]; long k;
    switch(P){
      case P_ABSPOS: k = -64L*abs(d) - (d>0); break;
      case P_ABSNEG: k = -64L*abs(d) - (d<0); break;
      case P_DDESC: k=-d; break;
      case P_DASC: k=d; break;
      default: k = 4096L*pc(availmask(rf,cf,d)) - 64L*abs(d) - (d>0); break;
    }
    if(k<bk){bk=k;best=t;}
  }
  return best;
}
static int runA(int P, int S, int F){
  int rf=FULL, cf=FULL, dm=(1<<ND)-1;
  while(dm){
    int t=pickdiag(P,rf,cf,dm), d=D[t];
    int am=availmask(rf,cf,d); if(!am) return 0;
    int bi=-1, bs=1<<30;
    for(int i=0;i<n;i++) if(am>>i&1){
      int j=i+d;
      if(F && !sumtest(rf&~(1<<i), cf&~(1<<j), dm&~(1<<t))) continue;
      int s=cellscore(S,i,j,rf,cf,dm,t); if(s<bs){bs=s;bi=i;}
    }
    if(bi<0) return 0;
    rf&=~(1<<bi); cf&=~(1<<(bi+d)); dm&=~(1<<t);
  }
  return 1;
}

// ---- Type B: Havel-Hakimi. options tried in order; F: require sumtest after move ----
// O1: dmax in top row; O2: dmin in bottom row; O3: dmax in right col; O4: dmin in left col
static int runB(const int* ord, int no, int F){
  int rf=FULL, cf=FULL, dm=(1<<ND)-1;
  while(dm){
    int tmax=31-__builtin_clz(dm), tmin=__builtin_ctz(dm);
    int top=__builtin_ctz(rf), bot=31-__builtin_clz(rf), lc=__builtin_ctz(cf), rc=31-__builtin_clz(cf);
    int done=0;
    for(int o=0;o<no && !done;o++){
      int t,i,j;
      switch(ord[o]){
        case 1: t=tmax; i=top; j=i+D[t]; break;
        case 2: t=tmin; i=bot; j=i+D[t]; break;
        case 3: t=tmax; j=rc; i=j-D[t]; break;
        default: t=tmin; j=lc; i=j-D[t]; break;
      }
      if(i<0||i>=n||j<0||j>=n||!(rf>>i&1)||!(cf>>j&1)) continue;
      if(F && !sumtest(rf&~(1<<i), cf&~(1<<j), dm&~(1<<t))) continue;
      rf&=~(1<<i); cf&=~(1<<j); dm&=~(1<<t); done=1;
    }
    if(!done) return 0;
  }
  return 1;
}

// ---- Type C: row by row (row 0..n-1), urgency key ----
enum { U_CELLS, U_DEADLINE, U_DMAX, U_DMIN, U_DAMAGE, NU };
static const char* UN[]={"fewest-cells","earliest-deadline","largest-d","smallest-d","leastdamage"};
static int runC(int U, int tie, int F){
  int rf=FULL, cf=FULL, dm=(1<<ND)-1;
  for(int i=0;i<n;i++){
    int bt=-1; long bk=1L<<40;
    for(int t=0;t<ND;t++) if(dm>>t&1){
      int d=D[t], j=i+d; if(j<0||j>=n||!(cf>>j&1)) continue;
      if(F && !sumtest(rf&~(1<<i), cf&~(1<<j), dm&~(1<<t))) continue;
      int am=availmask(rf,cf,d); long k;
      switch(U){
        case U_CELLS: k=pc(am); break;
        case U_DEADLINE: k=31-__builtin_clz(am); break;
        case U_DMAX: k=-d; break;
        case U_DMIN: k=d; break;
        default: k=cellscore(S_DAMAGE,i,j,rf,cf,dm,t)/64; break;
      }
      k = k*256 + (tie? d+64 : 64-d);
      if(k<bk){bk=k;bt=t;}
    }
    if(bt<0) return 0;
    rf&=~(1<<i); cf&=~(1<<(i+D[bt])); dm&=~(1<<bt);
  }
  return 1;
}

// ---- Type D: global MRV over rows, cols and diagonals; fill it with least-damage choice ----
static int runD(int F, int SC){
  int rf=FULL, cf=FULL, dm=(1<<ND)-1;
  while(dm){
    // options of each element
    int best=1<<30, kind=-1, idx=-1;
    for(int t=0;t<ND;t++) if(dm>>t&1){ int c=pc(availmask(rf,cf,D[t])); if(c<best){best=c;kind=0;idx=t;} }
    for(int i=0;i<n;i++) if(rf>>i&1){ int c=0; for(int t=0;t<ND;t++) if(dm>>t&1){int j=i+D[t]; if(j>=0&&j<n&&(cf>>j&1)) c++;} if(c<best){best=c;kind=1;idx=i;} }
    for(int j=0;j<n;j++) if(cf>>j&1){ int c=0; for(int t=0;t<ND;t++) if(dm>>t&1){int i=j-D[t]; if(i>=0&&i<n&&(rf>>i&1)) c++;} if(c<best){best=c;kind=2;idx=j;} }
    if(best==0) return 0;
    int bi=-1,bt=-1,bs=1<<30;
    for(int t=0;t<ND;t++) if(dm>>t&1){ int am=availmask(rf,cf,D[t]);
      while(am){ int i=__builtin_ctz(am); am&=am-1; int j=i+D[t];
        if(kind==0&&t!=idx) continue; if(kind==1&&i!=idx) continue; if(kind==2&&j!=idx) continue;
        if(F && !sumtest(rf&~(1<<i), cf&~(1<<j), dm&~(1<<t))) continue;
        int s=cellscore(SC,i,j,rf,cf,dm,t); if(s<bs){bs=s;bi=i;bt=t;} } }
    if(bi<0) return 0;
    rf&=~(1<<bi); cf&=~(1<<(bi+D[bt])); dm&=~(1<<bt);
  }
  return 1;
}

// ---- rule table ----
#define MAXR 400
static int NR=0; static char rname[MAXR][96];
static int rtype[MAXR], ra[MAXR], rb[MAXR], rc_[MAXR];
static int firstfail_n[MAXR]; static int firstfail_D[MAXR][32]; static long failcnt[MAXR][32];
static const int BO[4][4]={{1,2,0,0},{2,1,0,0},{1,2,3,4},{1,3,2,4}}; static const int BN[4]={2,2,4,4};
static const char* BNm[]={"[top-max,bot-min]","[bot-min,top-max]","[top-max,bot-min,rcol-max,lcol-min]","[top-max,rcol-max,bot-min,lcol-min]"};
static void addrules(void){
  for(int F=0;F<2;F++){
    for(int P=0;P<NP;P++) for(int S=0;S<NS;S++){ int r=NR++; rtype[r]=0; ra[r]=P; rb[r]=S; rc_[r]=F;
      sprintf(rname[r],"A diag=%s cell=%s%s",PN[P],SN[S],F?" +test":""); }
    for(int b=0;b<4;b++){ int r=NR++; rtype[r]=1; ra[r]=b; rc_[r]=F; sprintf(rname[r],"B HH %s%s",BNm[b],F?" +test":""); }
    for(int U=0;U<NU;U++) for(int tie=0;tie<2;tie++){ int r=NR++; rtype[r]=2; ra[r]=U; rb[r]=tie; rc_[r]=F;
      sprintf(rname[r],"C row-by-row %s tie=%s%s",UN[U],tie?"small-d":"large-d",F?" +test":""); }
    for(int SC=S_DAMAGE;SC<=S_WDAMAGE;SC++){ int r=NR++; rtype[r]=3; rc_[r]=F; ra[r]=SC; sprintf(rname[r],"D global-MRV(rows/cols/diags) cell=%s%s",SN[SC],F?" +test":""); }
  }
}
static int runrule(int r){
  switch(rtype[r]){
    case 0: return runA(ra[r],rb[r],rc_[r]);
    case 1: return runB(BO[ra[r]],BN[ra[r]],rc_[r]);
    case 2: return runC(ra[r],rb[r],rc_[r]);
    default: return runD(rc_[r],ra[r]);
  }
}

static long ninst; static int DIAG=0; static long dwalks,dstuck,dfalsepos,dsteps;
static unsigned long long rng=88172645463325252ULL;
static unsigned xr(void){ rng^=rng<<13; rng^=rng>>7; rng^=rng<<17; return (unsigned)rng; }
static void diagwalk(void){ // random move among moves passing sumtest; count stuck walks and test false positives
  for(int w=0;w<20;w++){ int rf=FULL,cf=FULL,dm=(1<<ND)-1; dwalks++;
    while(dm){ int mi[256],mt[256],k=0;
      for(int t=0;t<ND;t++) if(dm>>t&1){ int am=availmask(rf,cf,D[t]);
        while(am){int i=__builtin_ctz(am); am&=am-1; if(sumtest(rf&~(1<<i),cf&~(1<<(i+D[t])),dm&~(1<<t))){mi[k]=i;mt[k]=t;k++;}}}
      if(!k){dstuck++;break;}
      int c=xr()%k; int i=mi[c],t=mt[c]; rf&=~(1<<i); cf&=~(1<<(i+D[t])); dm&=~(1<<t);
      dsteps++; if(dm && !solvable(rf,cf,dm)){ if(!dfalsepos && getenv("SHOW")){ printf("  example n=%d D=",n); for(int q=0;q<n;q++) printf("%d ",D[q]); printf("| rows "); for(int q=0;q<n;q++) if(rf>>q&1) printf("%d ",q+1); printf("cols "); for(int q=0;q<n;q++) if(cf>>q&1) printf("%d ",q+1); printf("diags "); for(int q=0;q<n;q++) if(dm>>q&1) printf("%d ",D[q]); printf("\n"); } dfalsepos++; }
    } } }
static void process(void){
  ninst++; if(DIAG){ diagwalk(); return; }
  for(int r=0;r<NR;r++){
    if(!runrule(r)){
      failcnt[r][n]++;
      if(!firstfail_n[r]){ firstfail_n[r]=n; memcpy(firstfail_D[r],D,sizeof(int)*n); }
    }
  }
}
// enumerate D sorted ascending with Landau strict for k<n, equality at n
static int cur[32];
static void rec(int k, int lo, int psum){
  if(k==n){
    if(psum != n*(n-1)/2) return;
    memcpy(D,cur,sizeof(int)*n); process(); return; }
  for(int d=lo; d<=n-1; d++){
    // remaining n-k values must fit above d
    if((n-1)-d < n-k-1) break;
    int s=d+n-(k+1), ps=psum+s, need=(k+1)*k/2;
    if(k+1<n){ if(ps<=need) continue; } else { if(ps!=need) continue; }
    cur[k]=d; rec(k+1,d+1,ps);
  }
}
int main(int argc,char**argv){
  int NMAX=argc>1?atoi(argv[1]):10;
  addrules(); DIAG = argc>2;
  for(n=1;n<=NMAX;n++){
    FULL=(1<<n)-1; ND=n; ninst=0; rec(0,-(n-1),0);
    int alive=0; for(int r=0;r<NR;r++) if(!firstfail_n[r]) alive++;
    fprintf(stderr,"n=%d instances=%ld rules still unbeaten=%d\n",n,ninst,alive);
    printf("N %d %ld\n",n,ninst); if(DIAG){ printf("  random test-passing walks: %ld, stuck %ld (%.2f%%); test-passing moves into unsolvable state: %ld of %ld\n",dwalks,dstuck,100.0*dstuck/(dwalks?dwalks:1),dfalsepos,dsteps); dwalks=dstuck=dfalsepos=dsteps=0; }
  }
  for(int r=0;r<NR;r++){
    printf("%-70s ",rname[r]);
    if(!firstfail_n[r]) printf("NEVER FAILS up to n=%d\n",NMAX);
    else { printf("first fail n=%d D={",firstfail_n[r]); for(int i=0;i<firstfail_n[r];i++) printf("%d%s",firstfail_D[r][i],i+1<firstfail_n[r]?",":"");
      printf("} fails:"); for(int m=firstfail_n[r];m<=NMAX;m++) printf(" n%d=%ld",m,failcnt[r][m]); printf("\n"); }
  }
  return 0;
}
