// Independent addition-only DRUP (RUP) certificate checker, exact Boolean arithmetic.
// Usage: check_drup INPUT.cnf PROOF.drup
// Each proof line must be a clause followed by 0. Deletion lines are rejected.
// A proof is accepted iff every learned clause passes reverse unit propagation
// and the final proof line is the empty clause. No solver is trusted.
#include <bits/stdc++.h>
using namespace std;
struct Clause{vector<int> lits; int w0=0,w1=0;};
class Checker {
 public:
  int vars=0;
  vector<Clause> clauses;
  vector<vector<int>> watch;
  vector<int> units;
  vector<signed char> assignment;
  vector<int> trail;
  size_t checked=0;
  static int wid(int lit){return 2*abs(lit)+(lit<0);}
  void setup(int n){vars=n;watch.resize(2*(n+1)+2);assignment.assign(n+1,0);}
  int value(int lit) const {
    signed char a=assignment[abs(lit)];
    return a==0?0:(a==(lit>0?1:-1)?1:-1);
  }
  bool enqueue(int lit){
    signed char v=(lit>0)?1:-1;
    int a=abs(lit);
    if(assignment[a]!=0) return assignment[a]==v;
    assignment[a]=v;trail.push_back(lit);return true;
  }
  void add(vector<int> lits){
    Clause c; c.lits=std::move(lits);
    int id=clauses.size();
    if(c.lits.size()>1){ c.w0=0;c.w1=1;watch[wid(c.lits[0])].push_back(id); watch[wid(c.lits[1])].push_back(id);}
    else if(c.lits.size()==1){units.push_back(c.lits[0]);}
    else {units.push_back(0);}
    clauses.push_back(std::move(c));
  }
  bool propagate(){
    for(int u:units){if(u==0 || !enqueue(u))return false;}
    size_t head=0;
    while(head<trail.size()){
      int false_lit=-trail[head++];
      auto &bucket=watch[wid(false_lit)];
      for(size_t j=0;j<bucket.size();){
        int ci=bucket[j]; Clause &c=clauses[ci];
        int& wa=c.w0;
        int& wb=c.w1;
        // Put false watcher at position wa.
        if(c.lits[wb]==false_lit)std::swap(wa,wb);
        if(c.lits[wa]!=false_lit){ ++j; continue; }
        int other=c.lits[wb];
        if(value(other)==1){ ++j; continue; }
        int next=-1;
        for(int k=0;k<(int)c.lits.size();k++){
          if(k!=wa && k!=wb && value(c.lits[k])!=-1){next=k;break;}
        }
        if(next>=0){
          wa=next;
          bucket[j]=bucket.back(); bucket.pop_back();
          watch[wid(c.lits[next])].push_back(ci);
          continue;
        }
        if(value(other)==-1 || !enqueue(other))return false;
        ++j;
      }
    }
    return true;
  }
  bool rup(const vector<int>& clause){
    for(int v:trail)assignment[abs(v)]=0;
    trail.clear();
    bool consistent=true;
    for(int lit:clause){if(!enqueue(-lit)){consistent=false;break;}}
    if(consistent)consistent=propagate();
    return !consistent;
  }
};
static vector<int> parse_line(const string& line,int vars,int lineno){
  istringstream ss(line);string tok;vector<int> ls;bool end=false;
  while(ss>>tok){
    if(tok=="c")break;
    char* last=nullptr;long long v=strtoll(tok.c_str(),&last,10);
    if(*last || last==tok.c_str())throw runtime_error("Noninteger token on line "+to_string(lineno));
    if(v==0){end=true;break;}
    if(llabs(v)>vars)throw runtime_error("Out-of-range literal on line "+to_string(lineno));
    ls.push_back((int)v);
  }
  if(!end)throw runtime_error("Missing 0 terminator on line "+to_string(lineno));
  return ls;
}
int main(int argc,char**argv){
 try{
  if(argc!=3){cerr<<"Usage: check_drup INPUT.cnf PROOF.drup\n";return 2;}
  ifstream in(argv[1]),proof(argv[2]);
  if(!in || !proof)throw runtime_error("Could not open CNF or proof");
  Checker ck;string line;int lineno=0,expected=-1;
  while(getline(in,line)){
    lineno++;
    if(line.empty()||line[0]=='c')continue;
    if(line[0]=='p'){
      string p,fmt;int n,c;istringstream ss(line);ss>>p>>fmt>>n>>c;
      if(p!="p"||fmt!="cnf"||n<=0||c<0||expected!=-1)throw runtime_error("Bad header");
      ck.setup(n);expected=c;continue;
    }
    if(expected<0)throw runtime_error("Clause before header");
    ck.add(parse_line(line,ck.vars,lineno));
  }
  if(expected<0 || (int)ck.clauses.size()!=expected)throw runtime_error("Incorrect original clause count");
  lineno=0;bool empty=false;
  while(getline(proof,line)){
    lineno++;
    if(line.empty() || line[0]=='c')continue;
    if(line[0]=='d')throw runtime_error("Deletion steps not supported: use addition-only DRUP");
    vector<int> lits=parse_line(line,ck.vars,lineno);
    if(!ck.rup(lits))throw runtime_error("RUP FAILED at proof line "+to_string(lineno));
    ck.checked++;
    if(lits.empty()){
       empty=true;
       // Require the last non-comment clause to be the empty clause.
    }
    else if(empty)throw runtime_error("Derived clauses after empty clause");
    ck.add(std::move(lits));
  }
  if(!empty)throw runtime_error("Proof does not derive empty clause");
  cout<<"PASS: "<<ck.checked<<" RUP-derived clauses, empty clause YES\n";
  return 0;
 }catch(const exception&e){cerr<<"REJECT: "<<e.what()<<"\n";return 1;}
}
