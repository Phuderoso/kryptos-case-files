/* Cycle 81: cycle 80's affine linear-recurrence key mod 26, extended to order L (default 4) behind transpositions.
   Speed-up: enumerate c1..c_{L-1}; the first in-block equation after d is fixed is linear in c_L:
   c_L*(K1[L+1-L]-K1[L-L]) = (K1[L+1]-K1[L]) - sum_{j<L} c_j (K1[L+1-j]-K1[L-j])  (mod 26) -> solved by table (0,1,2 or 26 roots).
   Then identical exact check to linrec80 (all block-1 equations, propagation 34-73 must reproduce block 2).
   usage: linrec81 CT perms.bin lo hi Lmin Lmax */
#include <stdio.h>
#include <stdlib.h>
static const char *KA="KRYPTOSABCDEFGHIJLMNQUVWXZ", *AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ";
static const char *CR="EASTNORTHEASTBERLINCLOCK";
static int K1[13],K2[11]; static long hits=0, tests=0; static int nsol[26][26], sol[26][26][26];
static void test(int L,int *c,long pi,int t,int mode){ tests++;
  int d=K1[L]; for(int j=1;j<=L;j++) d-=c[j]*K1[L-j]; d=((d%26)+26)%26;
  for(int i=L+1;i<13;i++){int v=d; for(int j=1;j<=L;j++) v+=c[j]*K1[i-j]; if(v%26!=K1[i]) return;}
  int k[80]; for(int i=0;i<13;i++) k[21+i]=K1[i];
  for(int i=34;i<=73;i++){int v=d; for(int j=1;j<=L;j++) v+=c[j]*k[i-j]; k[i]=v%26; if(i>=63 && k[i]!=K2[i-63]) return;}
  hits++; printf("HIT perm=%ld tab=%s mode=%s L=%d d=%d c=",pi,t?"AZ":"KA",mode?"Beau":"Vig",L,d);
  for(int j=1;j<=L;j++) printf("%d%s",c[j],j<L?",":"\n"); }
int main(int argc,char**argv){
  const char*ct=argv[1]; FILE*f=fopen(argv[2],"rb"); long lo=atol(argv[3]),hi=atol(argv[4]); int Lmin=atoi(argv[5]),Lmax=atoi(argv[6]);
  for(int a=0;a<26;a++)for(int b=0;b<26;b++){nsol[a][b]=0; for(int x=0;x<26;x++) if((a*x)%26==b) sol[a][b][nsol[a][b]++]=x;}
  int ix[2][26]; for(int t=0;t<2;t++){const char*T=t?AZ:KA; for(int q=0;q<26;q++) ix[t][T[q]-'A']=q;}
  short P[97]; fseek(f,lo*97*2,SEEK_SET);
  for(long pi=lo;pi<hi;pi++){ if(fread(P,2,97,f)!=97)break;
    for(int t=0;t<2;t++)for(int mode=0;mode<2;mode++){
      for(int n=0;n<24;n++){int i= n<13?21+n:63+n-13; int cc=ix[t][ct[P[i]]-'A'], q=ix[t][CR[n]-'A'];
        int k= mode? cc+q : cc-q; k=((k%26)+26)%26; if(n<13)K1[n]=k; else K2[n-13]=k;}
      int D[13]; for(int i=1;i<13;i++) D[i]=((K1[i]-K1[i-1])%26+26)%26;  /* D[i]=K1[i]-K1[i-1] */
      for(int L=Lmin;L<=Lmax;L++){ int c[9]={0}; long tot=1; for(int j=1;j<L;j++) tot*=26;
        int a=D[1]; /* coefficient of c_L: K1[1]-K1[0] */
        for(long x=0;x<tot;x++){ long y=x; for(int j=1;j<L;j++){c[j]=y%26; y/=26;}
          int b=D[L+1]; for(int j=1;j<L;j++) b-=c[j]*D[L+1-j]; b=((b%26)+26)%26;
          for(int s=0;s<nsol[a][b];s++){ c[L]=sol[a][b][s]; test(L,c,pi,t,mode);} } }
    }}
  printf("tests=%ld hits=%ld\n",tests,hits); return 0;}
