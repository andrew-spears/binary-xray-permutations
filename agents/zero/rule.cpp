// Fast check of rewrite rules u -> v on the interface machine with slack bound B (distinct diagonals).
// Claim tested for each rule: F(x u) subset of F(x v) for every legal prefix x (slacks <= B) after which both are legal.
// Usage: ./rule B "u1,u2:v1,v2,v3" ...      (letters comma separated; empty u allowed, e.g. ":0,0";
//        prefix "s13@" restricts the test to prefixes x of slack 13)
// Prints per rule: situations tested, failures, and for the first failures a shortest prefix x and the missing states.
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
int B;
vector<pair<u64,u64>> states; vector<int> slackOf, localIdx; map<pair<u64,u64>,int> sid;
vector<vector<int>> bySlack;
vector<vector<vector<int>>> trans; // trans[id][e+B]
int getId(u64 r, u64 c, int s){ auto k=make_pair(r,c); auto it=sid.find(k); if(it!=sid.end()) return it->second;
  int id=states.size(); sid[k]=id; states.push_back(k); slackOf.push_back(s); localIdx.push_back(bySlack[s].size()); bySlack[s].push_back(id); trans.emplace_back(); return id; }
const vector<int>& tr(int id, int e){
  if(trans[id].empty()) trans[id].resize(2*B+2);
  auto &v=trans[id][e+B+1 - 1]; // index e+B
  static vector<int> dummy;
  if(!v.empty()) return v;
  u64 rm=states[id].first, cm=states[id].second; int s=slackOf[id];
  vector<int> out;
  for(int u=-B;u<=B;u++){ int bit=B+u; if(rm>>bit&1) continue; u64 m=rm|(1ULL<<bit); if(!(m&1)) continue; int v2=e-u; if(v2<-B||v2>B) continue; if(cm>>(B+v2)&1) continue; u64 c2=cm|(1ULL<<(B+v2)); if(!(c2&1)) continue; out.push_back(getId(m>>1,c2>>1,s+e)); }
  if(out.empty()) out.push_back(-1);
  trans[id][e+B]=out; return trans[id][e+B];
}
typedef vector<int> Set; // sorted global ids
Set step(const Set&S,int e){ Set out; for(int id:S){ const auto&t=tr(id,e); for(int x:t) if(x>=0) out.push_back(x);} sort(out.begin(),out.end()); out.erase(unique(out.begin(),out.end()),out.end()); return out; }
const int NONE=-100;
struct Sit{ Set S; int s,last,parent,letter; };
vector<Sit> sits; map<tuple<Set,int,int>,int> seen;
bool legal(int last,int s,int e){ if(last==NONE){ if(e<0) return false;} else if(e<last-1) return false; return s+e>=0&&s+e<=B; }
bool run(Set S,int s,int last,const vector<int>&w,Set&out){ for(int e:w){ if(!legal(last,s,e)) return false; S=step(S,e); s+=e; last=e;} out=S; return true; }
string desc(u64 m){ string h="holes[",x="] extras["; for(int j=0;j<B;j++) if(!(m>>j&1)) h+=to_string(j-B+1)+" "; for(int j=B;j<2*B+1;j++) if(m>>j&1) x+=to_string(j-B+1)+" "; return h+x+"]"; }
vector<int> parse(const string&s){ vector<int> v; string t; stringstream ss(s); while(getline(ss,t,',')) if(!t.empty()) v.push_back(stoi(t)); return v; }
int main(int argc,char**argv){ B=atoi(argv[1]); bySlack.resize(B+1);
  u64 base=(1ULL<<B)-1; int st=getId(base,base,0);
  sits.push_back({Set{st},0,NONE,-1,0}); seen[make_tuple(Set{st},0,NONE)]=0;
  for(size_t i=0;i<sits.size();i++){ int s=sits[i].s,last=sits[i].last; for(int e=-B;e<=B;e++){ if(!legal(last,s,e)) continue; Set T=step(sits[i].S,e); auto key=make_tuple(T,s+e,e); if(seen.count(key)) continue; seen[key]=sits.size(); sits.push_back({T,s+e,e,(int)i,e}); } }
  fprintf(stderr,"B=%d: %zu situations, %zu states\n",B,sits.size(),states.size());
  for(int a=2;a<argc;a++){ string r=argv[a]; int only=-1; if(r[0]=='s'){ size_t q=r.find('@'); only=stoi(r.substr(1,q-1)); r=r.substr(q+1); } size_t p=r.find(':'); vector<int> u=parse(r.substr(0,p)), v=parse(r.substr(p+1));
    int tested=0,bad=0;
    for(size_t i=0;i<sits.size();i++){ Set X,Y; if(only>=0&&sits[i].s!=only) continue; if(!run(sits[i].S,sits[i].s,sits[i].last,u,X)) continue; if(!run(sits[i].S,sits[i].s,sits[i].last,v,Y)) continue; tested++;
      if(!includes(Y.begin(),Y.end(),X.begin(),X.end())){ bad++; if(bad<=4){ vector<int> w; for(int j=i;sits[j].parent>=0;j=sits[j].parent) w.push_back(sits[j].letter); reverse(w.begin(),w.end());
          printf("  FAIL x = ("); for(int e:w) printf("%d,",e); printf(") slack %d  |F(xu)|=%zu |F(xv)|=%zu missing:\n",sits[i].s,X.size(),Y.size());
          int c=0; for(int id:X) if(!binary_search(Y.begin(),Y.end(),id)){ if(c++<6) printf("     rows %s   cols %s\n",desc(states[id].first).c_str(),desc(states[id].second).c_str()); } } } }
    printf("%s: tested %d, fails %d\n",argv[a],tested,bad); fflush(stdout); }
}
