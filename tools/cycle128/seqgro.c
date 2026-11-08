/* Cycle 128: "one key, two jobs". The SAME chain-addition digit stream (5-digit primer, ACA/Gromark rule)
   drives an ACA Sequence Transposition and a Gromark-style digit substitution.
   Substitution: idx = PA(p) + d (Vigenere form) or d - PA(p) (Beaufort form) mod 26, cipher letter = CA[idx],
   with PA = A-Z or KRYPTOS and CA an ARBITRARY cipher alphabet (enforced as a bijection idx<->letter),
   so CA = A-Z / KRYPTOS / any keyword alphabet are all included.
   Model A: substitution before transposition, digit indexed by plaintext position.
   Model B: substitution after transposition, digit indexed by carved position.
   Exact DFS over all 10! column orders, all 24 crib letters.
   usage: seqgro CT P0 P1 label */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char*KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static const char*CR1="EASTNORTHEAST",*CR2="BERLINCLOCK";
int ai[2][26],ct[N],cp[24],cl[24],d[N],rk[N],cnt[10],ncl[10],clist[10][24],primer,ord[10];
signed char fwd[8][26],bwd[8][26]; int alive[8]; long long nodes,surv; const char*lab;
typedef struct{signed char*p;signed char o;}U; U us[100000]; int un;
static inline void setv(signed char*p,int v){us[un].p=p;us[un].o=*p;un++;*p=v;}
void dfs(int lev,int used,int off){
  nodes++;
  if(lev==10){ for(int v=0;v<8;v++) if(alive[v]){ surv++;
      printf("S %s %05d ",lab,primer); for(int k=0;k<10;k++) printf("%d",ord[k]);
      printf(" model=%c PA=%s form=%s\n",(v&4)?'B':'A',(v&2)?"KA":"AZ",(v&1)?"beau":"vig"); } return; }
  for(int c=0;c<10;c++){ if(used>>c&1) continue;
    int u0=un, sa[8]; memcpy(sa,alive,sizeof sa); int any=0;
    for(int v=0;v<8;v++){ if(!alive[v]) continue; int be=v&1,pa=(v>>1)&1,mB=v>>2, ok=1;
      for(int q=0;q<ncl[c]&&ok;q++){ int t=clist[c][q]; int pos=off+rk[cp[t]]; int dig=mB? d[pos]: d[cp[t]];
        int a=ai[pa][cl[t]]; int idx= be? ((dig-a)%26+26)%26 : (a+dig)%26; int L=ct[pos];
        if(fwd[v][idx]<0 && bwd[v][L]<0){ setv(&fwd[v][idx],L); setv(&bwd[v][L],idx);}
        else if(fwd[v][idx]!=L || bwd[v][L]!=idx) ok=0; }
      alive[v]=ok; if(ok) any=1; }
    if(any){ ord[lev]=c; dfs(lev+1,used|1<<c,off+cnt[c]); }
    while(un>u0){un--;*us[un].p=us[un].o;} memcpy(alive,sa,sizeof sa);
  }
}
int main(int argc,char**argv){
  if(argc<5) return 1;
  const char*C=argv[1]; int P0=atoi(argv[2]),P1=atoi(argv[3]); lab=argv[4];
  for(int i=0;i<26;i++) ai[0][i]=i; for(int i=0;i<26;i++) ai[1][KA[i]-'A']=i;
  for(int i=0;i<N;i++) ct[i]=C[i]-'A';
  for(int i=0;i<13;i++){cp[i]=21+i;cl[i]=CR1[i]-'A';} for(int i=0;i<11;i++){cp[13+i]=63+i;cl[13+i]=CR2[i]-'A';}
  for(primer=P0;primer<P1;primer++){
    int x=primer; for(int k=4;k>=0;k--){d[k]=x%10;x/=10;} for(int i=5;i<N;i++) d[i]=(d[i-5]+d[i-4])%10;
    memset(cnt,0,sizeof cnt); for(int i=0;i<N;i++) rk[i]=cnt[d[i]]++;
    memset(ncl,0,sizeof ncl); for(int t=0;t<24;t++){int c=d[cp[t]]; clist[c][ncl[c]++]=t;}
    memset(fwd,-1,sizeof fwd); memset(bwd,-1,sizeof bwd); for(int v=0;v<8;v++) alive[v]=1; un=0;
    dfs(0,0,0);
  }
  printf("C %s %d %d nodes %lld survivors %lld\n",lab,P0,P1,nodes,surv);
}
