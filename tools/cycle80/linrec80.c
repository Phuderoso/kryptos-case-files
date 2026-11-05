/* Cycle 80: affine linear-recurrence key mod 26 (lagged-Fibonacci generalised):
   k[i] = c1 k[i-1] + ... + cL k[i-L] + d (mod 26), key indexed by plaintext position (model A: substitute, then transpose).
   pt[i] sits at carved position j=P[i]. Tableau KA or AZ; Vigenere k=c-p, Beaufort k=c+p (variant = Vigenere negated, same family).
   Exact: all L recurrence equations inside crib block 1 (pos 21-33) must hold, then the key is propagated through 34-62
   and must reproduce all 11 key values of block 2 (63-73).
   usage: linrec80 CT perms.bin lo hi Lmax */
#include <stdio.h>
#include <stdlib.h>
static const char *KA="KRYPTOSABCDEFGHIJLMNQUVWXZ", *AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ";
static const char *CR="EASTNORTHEASTBERLINCLOCK";
static int K1[13],K2[11]; static long hits=0;
static int test(int L,int *c,long pi,int t,int mode){
  int d=K1[L]; for(int j=1;j<=L;j++) d-=c[j]*K1[L-j]; d=((d%26)+26)%26;
  for(int i=L+1;i<13;i++){int v=d; for(int j=1;j<=L;j++) v+=c[j]*K1[i-j]; if(v%26!=K1[i]) return 0;}
  int k[80]; for(int i=0;i<13;i++) k[21+i]=K1[i];
  for(int i=34;i<=73;i++){int v=d; for(int j=1;j<=L;j++) v+=c[j]*k[i-j]; k[i]=v%26; if(i>=63 && k[i]!=K2[i-63]) return 0;}
  hits++; printf("HIT perm=%ld tab=%s mode=%s L=%d d=%d c=",pi,t?"AZ":"KA",mode?"Beau":"Vig",L,d);
  for(int j=1;j<=L;j++) printf("%d%s",c[j],j<L?",":"\n"); return 1;}
int main(int argc,char**argv){
  const char*ct=argv[1]; FILE*f=fopen(argv[2],"rb"); long lo=atol(argv[3]),hi=atol(argv[4]); int Lmax=atoi(argv[5]);
  int ix[2][26]; for(int t=0;t<2;t++){const char*T=t?AZ:KA; for(int q=0;q<26;q++) ix[t][T[q]-'A']=q;}
  short P[97]; long tests=0; fseek(f,lo*97*2,SEEK_SET);
  for(long pi=lo;pi<hi;pi++){ if(fread(P,2,97,f)!=97)break;
    for(int t=0;t<2;t++)for(int mode=0;mode<2;mode++){
      for(int n=0;n<24;n++){int i= n<13?21+n:63+n-13; int cc=ix[t][ct[P[i]]-'A'], q=ix[t][CR[n]-'A'];
        int k= mode? cc+q : cc-q; k=((k%26)+26)%26; if(n<13)K1[n]=k; else K2[n-13]=k;}
      for(int L=1;L<=Lmax;L++){ int c[9]={0}; long tot=1; for(int j=0;j<L;j++) tot*=26;
        for(long x=0;x<tot;x++){ long y=x; for(int j=1;j<=L;j++){c[j]=y%26; y/=26;} tests++; test(L,c,pi,t,mode);} }
    }}
  printf("tests=%ld hits=%ld\n",tests,hits); return 0;}
