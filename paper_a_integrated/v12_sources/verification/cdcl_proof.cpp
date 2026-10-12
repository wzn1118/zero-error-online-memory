#include <bits/stdc++.h>
using namespace std;
struct Clause{vector<int> lits; bool learnt; double act=0;};
struct Solver {
 int n=0;vector<Clause> cs; vector<vector<int>> ws;
 vector<signed char> val; vector<int> lev,reason,trail,lim; size_t qhead=0;
 vector<char>seen; vector<double>act; priority_queue<pair<double,int>> order;
 double inc=1.0, decay=0.95; long long decisions=0, conflicts=0, propagations=0;
 int base=0; ofstream proof; bool quiet=false;
 inline int idx(int l)const{return 2*abs(l)+(l<0);}
 inline int v(int l)const{int x=val[abs(l)];return x==0?0:((l>0?x:-x));}
 int level()const{return (int)lim.size();}
 bool enqueue(int l,int r){int var=abs(l);signed char w=(l>0?1:-1); if(val[var])return val[var]==w;val[var]=w;lev[var]=level();reason[var]=r;trail.push_back(l);return true;}
 void setup(int nv,string pr,int bases){base=bases;n=nv;ws.resize(2*(n+1)+2);val.assign(n+1,0);lev.assign(n+1,0);reason.assign(n+1,-1);seen.assign(n+1,0);act.assign(n+1,0);proof.open(pr);for(int x=1;x<=n;x++){act[x]=(x<=bases?10.0:0.0);order.push({act[x],x});}}
 int add(vector<int> l,bool learn){int id=cs.size();cs.push_back({move(l),learn});if(cs.back().lits.size()>1){ws[idx(cs[id].lits[0])].push_back(id);ws[idx(cs[id].lits[1])].push_back(id);}else if(cs.back().lits.size()==1){if(!enqueue(cs[id].lits[0],id))return -2;}else return -2;return id;}
 int propagate(){while(qhead<trail.size()){int lit=-trail[qhead++];propagations++; auto &w=ws[idx(lit)];int i=0,j=0;
  while(i<(int)w.size()){
   int ci=w[i++];auto &c=cs[ci].lits;
   if(c[0]!=lit && c[1]==lit)swap(c[0],c[1]);
   if(c[0]!=lit){w[j++]=ci;continue;}
   if(v(c[1])>0){w[j++]=ci;continue;}
   bool move=false;
   for(int k=2;k<(int)c.size();k++)if(v(c[k])>=0){swap(c[0],c[k]);ws[idx(c[0])].push_back(ci);move=true;break;}
   if(move)continue;
   w[j++]=ci;
   if(v(c[1])<0 || !enqueue(c[1],ci)){
     while(i<(int)w.size())w[j++]=w[i++];w.resize(j);return ci;
   }
  }w.resize(j);
 }return -1;}
 void bump(int v){act[v]+=inc;order.push({act[v],v});if(act[v]>1e90){for(int i=1;i<=n;i++)act[i]*=1e-90;inc*=1e-90;priority_queue<pair<double,int>> tmp;for(int i=1;i<=n;i++)if(!val[i])tmp.push({act[i],i});swap(order,tmp);}}
 vector<int> analyze(int confl,int &back){vector<int>learnt(1,0),toclear;int count=0,p=0;int index=(int)trail.size()-1;
  do{
   const auto &c=cs[confl].lits;
   for(int lit:c){int vv=abs(lit);if(vv==abs(p)||seen[vv]||lev[vv]==0)continue;seen[vv]=true;toclear.push_back(vv);bump(vv);if(lev[vv]==level())count++;else learnt.push_back(lit);}
   while(index>=0 && !seen[abs(trail[index])])index--;
   if(index<0){cerr<<"ERROR ANALYSIS TRAIL\n";exit(10);}
   p=trail[index--];seen[abs(p)]=false;count--;confl=reason[abs(p)];
   if(count>0 && confl<0){cerr<<"ERROR ANALYSIS REASON\n";exit(11);}
  }while(count>0);
  learnt[0]=-p;for(int v:toclear)seen[v]=false;
  int maxlev=0,maxindex=1;
  for(int i=1;i<(int)learnt.size();i++){int l=lev[abs(learnt[i])];if(l>maxlev){maxlev=l;maxindex=i;}}
  if(learnt.size()>1)swap(learnt[1],learnt[maxindex]);
  back=maxlev;inc/=decay;return learnt;
 }
 void backtrack(int k){if(level()<=k)return;int target=lim[k];for(int i=(int)trail.size()-1;i>=target;i--){int v=abs(trail[i]);val[v]=0;reason[v]=-1;order.push({act[v],v});}trail.resize(target);lim.resize(k);qhead=trail.size();}
 int next(){while(!order.empty()){auto [a,x]=order.top();order.pop();if(!val[x] && a==act[x])return x;}for(int x=1;x<=n;x++)if(!val[x])return x;return 0;}
 void emit(const vector<int>&cl){for(int l:cl)proof<<l<<' ';proof<<"0\n";}
 bool solve(){int c=propagate();if(c!=-1){emit({});return false;}long long restart=100;long long since=0;
  while(true){int conflict=propagate();if(conflict!=-1){conflicts++;since++;
    if(level()==0){emit({});return false;}
    int back;auto learnt=analyze(conflict,back); emit(learnt);backtrack(back);int id=add(learnt,true);if(id==-2 || !enqueue(learnt[0],id)){emit({});return false;}
    if(inc>1e100){inc*=1e-100;}
    if(since>=restart){backtrack(0);since=0;restart=(long long)(restart*1.35)+10;}
    if(conflicts%10000==0){cerr<<"conflicts="<<conflicts<<" decision="<<decisions<<" learnt="<<cs.size()<<" trail="<<trail.size()<<"\n";}
  }else{int x=next();if(!x)return true;decisions++;lim.push_back(trail.size()); // false favored, especially original pair decisions
     if(!enqueue(x<=base?x:-x,-1)){cerr<<"bad decision";exit(12);}
  }}
 }
};
int main(int argc,char**argv){if(argc!=3){cerr<<"usage: cdcl_proof file.cnf out.drup\n";return 3;}
 ifstream f(argv[1]);if(!f){cerr<<"missing CNF\n";return 3;}Solver s;string line;int target=-1,count=0;
 while(getline(f,line)){if(line.empty()||line[0]=='c')continue; if(line[0]=='p'){string p,cnf;int v,k;istringstream ss(line);ss>>p>>cnf>>v>>k;s.setup(v,argv[2],string(argv[1]).find("B.antipodal")!=string::npos?64:512);target=k;continue;}istringstream ss(line);int l;vector<int>cl;while(ss>>l && l)cl.push_back(l);int c=s.add(move(cl),false);count++;if(c==-2){s.emit({});cerr<<"trivial UNSAT\n";return 0;}}
 if(target<0||count!=target){cerr<<"bad input count "<<count<<" expected "<<target<<"\n";return 4;}
 auto t=chrono::steady_clock::now();bool sat=s.solve();if(sat){ofstream mf(string(argv[2])+".model");for(int k=1;k<=s.n;k++)mf<<int(s.val[k])<<" ";mf<<"\n";cerr<<"SAT_SELECT:";for(int k=1;k<=min(512,s.n);k++)if(s.val[k]>0)cerr<<" "<<k;cerr<<"\n";}cerr<<(sat?"SAT":"UNSAT")<<" decisions="<<s.decisions<<" conflicts="<<s.conflicts<<" propagations="<<s.propagations<<" sec="<<chrono::duration<double>(chrono::steady_clock::now()-t).count()<<"\n";return sat?2:0;
}
