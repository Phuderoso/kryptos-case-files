/* Cycle 132: model Q of cycle 131 (both keyword layers at the plaintext position, then a bank transposition)
   made exhaustive over the full vocabulary by hashing.  For every bank permutation (and its inverse) the 24
   carved letters that land on the crib positions, ct[sigma(i_t)], form a signature; a configuration survives iff
   its 24 required letters equal some signature.  So each configuration costs one hash lookup instead of 330,130
   permutation checks.  usage: dblq CT list1 list2 perms.bin label lo hi */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define N 97
static const char*ALPH[2]={"ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"};
static int inv[2][26]; static char W1[20000][32],W2[20000][32]; static int L1[20000],L2[20000];
static int op(int f,int a,int s){ int r= f==0? a+s : f==1? s-a : a-s; return ((r%26)+26)%26; }
static int lay(int T,int f,int letter,int keyletter){ return ALPH[T][op(f,inv[T][letter],inv[T][keyletter])]-'A'; }
static int rd(const char*fn,char W[][32],int*L){ FILE*f=fopen(fn,"r"); int n=0; while(fscanf(f,"%31s",W[n])==1){ L[n]=strlen(W[n]); n++; } fclose(f); return n; }
#define HB 22
static uint64_t keyA[1<<HB]; static uint64_t keyB[1<<HB]; static int32_t val[1<<HB];
static void sig(const int*r,uint64_t*a,uint64_t*b){ *a=0;*b=0; for(int t=0;t<12;t++) *a=*a*26+r[t]; for(int t=12;t<24;t++) *b=*b*26+r[t]; }
static uint64_t hh(uint64_t a,uint64_t b){ uint64_t h=a*0x9E3779B97F4A7C15ULL ^ (b+0x632BE59BD9B4E019ULL)*0xC2B2AE3D27D4EB4FULL; return h^(h>>29); }
static void ins(uint64_t a,uint64_t b,int v){ uint64_t h=hh(a,b)&((1<<HB)-1); while(val[h]>=0){ if(keyA[h]==a&&keyB[h]==b) return; h=(h+1)&((1<<HB)-1);} keyA[h]=a;keyB[h]=b;val[h]=v; }
static int look(uint64_t a,uint64_t b){ uint64_t h=hh(a,b)&((1<<HB)-1); while(val[h]>=0){ if(keyA[h]==a&&keyB[h]==b) return val[h]; h=(h+1)&((1<<HB)-1);} return -1; }
int main(int argc,char**argv){
  const char*Cs=argv[1]; int C[N]; for(int i=0;i<N;i++) C[i]=Cs[i]-'A';
  int n1=rd(argv[2],W1,L1), n2=rd(argv[3],W2,L2); const char*lab=argv[5]; long lo=atol(argv[6]),hi=atol(argv[7]);
  for(int t=0;t<2;t++) for(int i=0;i<26;i++) inv[t][ALPH[t][i]-'A']=i;
  const char*c1="EASTNORTHEAST",*c2="BERLINCLOCK"; int cp[24],cl[24];
  for(int i=0;i<13;i++){cp[i]=21+i;cl[i]=c1[i]-'A';} for(int i=0;i<11;i++){cp[13+i]=63+i;cl[13+i]=c2[i]-'A';}
  FILE*pf=fopen(argv[4],"rb"); fseek(pf,0,SEEK_END); long np=ftell(pf)/(2*N); rewind(pf); short*P=malloc(np*N*2); fread(P,2,np*N,pf);
  memset(val,-1,sizeof val); long nsig=0;
  for(long q=0;q<np;q++){ short*s=P+q*N; short u[N]; for(int i=0;i<N;i++) u[s[i]]=i;
    int r[24]; uint64_t a,b; for(int t=0;t<24;t++) r[t]=C[s[cp[t]]]; sig(r,&a,&b); ins(a,b,(int)q); 
    for(int t=0;t<24;t++) r[t]=C[u[cp[t]]]; sig(r,&a,&b); ins(a,b,(int)(np+q)); nsig+=2; }
  long cfg=0,surv=0;
  for(long x=lo;x<hi&&x<n1;x++) for(int y=0;y<n2;y++){ const char*w1=W1[x],*w2=W2[y]; int l1=L1[x],l2=L2[y];
    for(int T1=0;T1<2;T1++) for(int f1=0;f1<3;f1++) for(int T2=0;T2<2;T2++) for(int f2=0;f2<3;f2++){ cfg++;
      int r[24]; for(int t=0;t<24;t++){ int i=cp[t]; r[t]=lay(T2,f2,lay(T1,f1,cl[t],w1[i%l1]-'A'),w2[i%l2]-'A'); }
      uint64_t a,b; sig(r,&a,&b); int v=look(a,b);
      if(v>=0){ surv++; printf("S %s Q %s %s T1=%d f1=%d T2=%d f2=%d perm=%ld dir=%d\n",lab,w1,w2,T1,f1,T2,f2,v%np,(int)(v/np)); } } }
  printf("C %s Q configs %ld signatures %ld survivors %ld\n",lab,cfg,nsig,surv);
}
