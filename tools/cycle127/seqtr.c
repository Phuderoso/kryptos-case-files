/* Cycle 127: ACA Sequence Transposition (chain-addition primer -> digit per plaintext letter -> 10 columns
   read in a key order) combined with a periodic tableau key, exact 24-crib consistency, ALL 10! column orders
   by depth-first search with pruning.
   Model A: key indexed by plaintext position (substitution before transposition).
   Model B: key indexed by carved position (substitution after transposition).
   Alphabets A-Z / KRYPTOS (same both sides), Vigenere (k=c-p; variant has the same consistency) and Beaufort (k=c+p).
   usage: seqtr CT P0 P1 PMAX label   (primers P0..P1-1, 5 digits with leading zeros)
   output: S label primer order(read digits) model alph beau period ;  C label P0 P1 nodes counts...  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char*KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static const char*CR1="EASTNORTHEAST",*CR2="BERLINCLOCK";
int ai[2][26],ct[N],cp[24],cl[24],PMAX,d[N],rk[N],cnt[10],ncl[10],clist[10][24];
/* key store: [m][v][p][res] */
signed char key[2][4][19][19]; unsigned mask[2][4]; long long nodes,surv[19]; const char*lab; int primer; int ord[10];
int fv(int v,int c,int p){int al=v>>1,be=v&1;int a=ai[al][c],b=ai[al][p];return be?(a+b)%26:(a-b+26)%26;}
typedef struct{signed char*ptr;signed char old;}U; U ust[200000]; int un;
void dfs(int lev,int used,int off){
  nodes++;
  if(lev==10){
    for(int m=0;m<2;m++)for(int v=0;v<4;v++){unsigned mk=mask[m][v];
      for(int p=1;p<=PMAX;p++)if(mk>>p&1){ int minp=p; surv[p]++;
        printf("S %s %05d ",lab,primer);for(int k=0;k<10;k++)printf("%d",ord[k]);
        printf(" %c %d %d %d\n",m?'B':'A',v>>1,v&1,minp); break; }}
    return;}
  for(int c=0;c<10;c++){ if(used>>c&1) continue;
    int u0=un; unsigned sm[2][4]; memcpy(sm,mask,sizeof sm); int any=0;
    for(int m=0;m<2;m++)for(int v=0;v<4;v++){ unsigned mk=mask[m][v]; if(!mk) continue;
      for(int q=0;q<ncl[c]&&mk;q++){int t=clist[c][q]; int pos=off+rk[cp[t]]; int kv=fv(v,ct[pos],cl[t]);
        int idx=m? pos: cp[t];
        for(int p=1;p<=PMAX;p++) if(mk>>p&1){ signed char*s=&key[m][v][p][idx%p];
          if(*s<0){ust[un].ptr=s;ust[un].old=*s;un++;*s=kv;} else if(*s!=kv) mk&=~(1u<<p);} }
      mask[m][v]=mk; if(mk) any=1; }
    if(any){ord[lev]=c; dfs(lev+1,used|1<<c,off+cnt[c]);}
    while(un>u0){un--;*ust[un].ptr=ust[un].old;} memcpy(mask,sm,sizeof sm);
  }
}
int main(int argc,char**argv){
  if(argc<6){fprintf(stderr,"usage\n");return 1;}
  const char*C=argv[1]; int P0=atoi(argv[2]),P1=atoi(argv[3]); PMAX=atoi(argv[4]); lab=argv[5];
  for(int i=0;i<26;i++){ai[0][i]=i;} for(int i=0;i<26;i++) ai[1][KA[i]-'A']=i;
  for(int i=0;i<N;i++) ct[i]=C[i]-'A';
  for(int i=0;i<13;i++){cp[i]=21+i;cl[i]=CR1[i]-'A';} for(int i=0;i<11;i++){cp[13+i]=63+i;cl[13+i]=CR2[i]-'A';}
  for(primer=P0;primer<P1;primer++){
    int x=primer; for(int k=4;k>=0;k--){d[k]=x%10;x/=10;} for(int i=5;i<N;i++) d[i]=(d[i-5]+d[i-4])%10;
    memset(cnt,0,sizeof cnt); for(int i=0;i<N;i++) rk[i]=cnt[d[i]]++;
    memset(ncl,0,sizeof ncl); for(int t=0;t<24;t++){int c=d[cp[t]]; clist[c][ncl[c]++]=t;}
    memset(key,-1,sizeof key); unsigned full=0; for(int p=1;p<=PMAX;p++) full|=1u<<p;
    for(int m=0;m<2;m++)for(int v=0;v<4;v++) mask[m][v]=full; un=0;
    dfs(0,0,0);
  }
  printf("C %s %d %d nodes %lld",lab,P0,P1,nodes); for(int p=1;p<=PMAX;p++) printf(" p%d=%lld",p,surv[p]); printf("\n");
}
