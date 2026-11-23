// Check rewrite rules u -> v over ALL legal prefixes x of length <= K (no slack bound), order-free model:
// stone j has row + column = 2j + e_j (rows, columns >= 1); F(x) = set of (rows used, columns used).
// Claim per rule: F(x u), shifted |v| - |u| times (Sh(A) = (A+1) u {1}), is a subset of F(x v), whenever both are legal.
// Usage: ./bylen K B rule ...   (prefixes of length <= K whose slacks, and those of x u and x v, stay <= B)
//        ./bylen K B rule ...     rule = "u:v" (comma separated letters)  or  "search:v" (try every u != v of length <= |v|
//        with the same letter sum and letters in [min v - 1, max v + 1]).
// Prints for each rule: prefixes tested, failures, a shortest failing prefix (ties: least slack).
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64; typedef unsigned __int128 St; typedef vector<St> Set;   // state = rows mask << 64 | columns mask (rows, columns <= 64)
int K, BB;
static Set place(const Set&S,int s){ Set out; out.reserve(S.size()*4);
  for(St st:S){ u64 A=(u64)(st>>64),B=(u64)st; if(s>65){ fprintf(stderr,"sum too large\n"); exit(1);} for(int a=1;a<s;a++){ int b=s-a; if(A>>(a-1)&1) continue; if(B>>(b-1)&1) continue; out.push_back(((St)(A|1ull<<(a-1))<<64)|(B|1ull<<(b-1))); } }
  sort(out.begin(),out.end()); out.erase(unique(out.begin(),out.end()),out.end()); return out; }
static bool legalw(int last,int s,const vector<int>&w,bool first){ for(int e:w){ if(first){ if(e<0) return false;} else if(e<last-1) return false; s+=e; if(s<0||s>BB) return false; last=e; first=false;} return true; }
static Set runw(Set S,int k,const vector<int>&w){ for(int e:w){ k++; S=place(S,2*k+e);} return S; }
struct Rule{ vector<int> u,v; string name; long tested=0,fails=0; vector<int> ex; int exs=1<<30; bool dead=false; };
vector<Rule> rules; bool stopAtFail=false;
vector<int> parse(const string&s){ vector<int> v; string t; stringstream ss(s); while(getline(ss,t,',')) if(!t.empty()) v.push_back(stoi(t)); return v; }
string show(const vector<int>&w){ string s="("; for(size_t i=0;i<w.size();i++){ if(i) s+=","; s+=to_string(w[i]); } return s+")"; }
int cmax; vector<int> x;
void rec(const Set&S,int s,int last){ int k=x.size();
  map<vector<int>,Set> cacheV;
  for(auto&r:rules){ if(r.dead) continue; bool first=(k==0);
    if(!legalw(last,s,r.u,first)||!legalw(last,s,r.v,first)) continue;
    if(!cacheV.count(r.v)) cacheV[r.v]=runw(S,k,r.v);
    const Set&Y=cacheV[r.v]; Set X=runw(S,k,r.u); int d=r.v.size()-r.u.size(); u64 low=(1ull<<d)-1; r.tested++;
    bool ok=true; for(St st:X){ u64 A=(u64)(st>>64),B=(u64)st; St t=((St)((A<<d)|low)<<64)|((B<<d)|low); if(!binary_search(Y.begin(),Y.end(),t)){ ok=false; break; } }
    if(!ok){ r.fails++; if(r.ex.empty()&&r.fails==1||(int)x.size()<(int)r.ex.size()||((int)x.size()==(int)r.ex.size()&&s<r.exs)){ r.ex=x; r.exs=s; } if(stopAtFail) r.dead=true; } }
  if(k==K) return;
  for(int e=(k==0?0:last-1);e<=cmax+(K-(k+1));e++){ if(s+e<0) continue; if(s+e>BB) break; x.push_back(e); Set T=place(S,2*(k+1)+e); if(!T.empty()) rec(T,s+e,e); x.pop_back(); } }
int main(int argc,char**argv){ K=atoi(argv[1]); BB=atoi(argv[2]); cmax=-100;
  for(int a=3;a<argc;a++){ string r=argv[a]; if(r=="-stop"){ stopAtFail=true; continue; } size_t p=r.find(':'); string us=r.substr(0,p); vector<int> v=parse(r.substr(p+1));
    if(us=="search"){ int lo=*min_element(v.begin(),v.end())-1,hi=*max_element(v.begin(),v.end())+1,sum=accumulate(v.begin(),v.end(),0);
      for(int L=0;L<=(int)v.size();L++){ vector<int> u(L,lo); while(true){ bool ok=accumulate(u.begin(),u.end(),0)==sum; for(int i=1;i<L&&ok;i++) if(u[i]<u[i-1]-1) ok=false;
          if(ok&&u!=v) rules.push_back({u,v,show(u)+" -> "+show(v)}); int i=L-1; while(i>=0&&u[i]==hi){ u[i]=lo; i--; } if(i<0) break; u[i]++; } } }
    else rules.push_back({parse(us),v,show(parse(us))+" -> "+show(v)}); }
  for(auto&r:rules){ cmax=max(cmax,r.v.empty()?0:r.v[0]+1); }
  rec(Set{0},0,0);
  for(auto&r:rules){ if(stopAtFail&&r.fails) continue; printf("%-40s tested %ld fails %ld",r.name.c_str(),r.tested,r.fails); if(r.fails) printf("   first: x = %s slack %d",show(r.ex).c_str(),r.exs); printf("\n"); }
}
