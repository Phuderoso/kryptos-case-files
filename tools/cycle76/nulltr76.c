/* Cycle 76: nulls between the cribs as an extra crib-offset loop behind transpositions (model A).
   Model A: plaintext P (no nulls) -> substitution (key indexed by plaintext position) -> b null letters
   dropped in between the cribs (and any number before/after) -> transposition -> carved.
   Intermediate X_i = carved[perm[i]]; EASTNORTHEAST at X 21..33, BERLINCLOCK at X 63..73;
   their plaintext-stream indices are 21+j1 and 63+j2-b (up to a common shift a, irrelevant here).
   Families (tableau KA or AZ, mode vig/beau/var):
     F0 periodic key p 1..26, b mod p           (consistency of key classes)
     F1 plaintext-fed autokey lag L, nulls b     (exact checks: crib pairs at stream distance L)
     F2 ciphertext-fed autokey lag L, nulls b    (same, key = previous cipher letter at distance L)
   For L>12 only the cross distance d=j2-j1=L-42+b matters; configurations are deduplicated to
   their effective form: periodic (p, b mod p); autokey (L<=12 intra only), (L<=12, d), (d only).
   Usage: nulltr76 CARVED perms.bin minprint [maxperms] -> hits (checks>=minprint) + histograms */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char *KA="KRYPTOSABCDEFGHIJLMNQUVWXZ", *AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ";
static const char *CR1="EASTNORTHEAST", *CR2="BERLINCLOCK";
int ix(const char*A,char c){for(int i=0;i<26;i++)if(A[i]==c)return i;return -1;}
static inline int m26(int x){x%=26;return x<0?x+26:x;}
/* expected cipher letter given plain p and key k */
static inline int enc(int mode,int p,int k){return mode==0?m26(p+k):mode==1?m26(k-p):m26(p-k);}
static inline int keyof(int mode,int c,int p){return mode==0?m26(c-p):mode==1?m26(c+p):m26(p-c);}
long hist[3][25];
int main(int argc,char**argv){
  const char*carved=argv[1]; int minpr=atoi(argv[3]);
  FILE*f=fopen(argv[2],"rb"); fseek(f,0,SEEK_END); long sz=ftell(f); rewind(f);
  int np=sz/(2*N); short*perms=malloc(sz); if(fread(perms,2,(size_t)np*N,f)!=(size_t)np*N)return 1; fclose(f);
  if(argc>4){int m=atoi(argv[4]); if(m<np)np=m;}
  long tests[3]={0,0,0}, hits=0;
  for(int pi=0;pi<np;pi++){ short*P=perms+(long)pi*N;
   for(int t=0;t<2;t++){const char*A=t?AZ:KA;
    int X1[13],X2[11],P1[13],P2[11];
    for(int j=0;j<13;j++){X1[j]=ix(A,carved[P[21+j]]);P1[j]=ix(A,CR1[j]);}
    for(int j=0;j<11;j++){X2[j]=ix(A,carved[P[63+j]]);P2[j]=ix(A,CR2[j]);}
    for(int mode=0;mode<3;mode++){
     /* F0 periodic */
     int k1[13],k2[11]; for(int j=0;j<13;j++)k1[j]=keyof(mode,X1[j],P1[j]); for(int j=0;j<11;j++)k2[j]=keyof(mode,X2[j],P2[j]);
     for(int p=1;p<=26;p++) for(int b=0;b<p&&b<30;b++){ tests[0]++;
       int cls[26]; for(int r=0;r<p;r++)cls[r]=-1; int ok=1,distinct=0;
       for(int j=0;j<13&&ok;j++){int r=(21+j)%p; if(cls[r]<0){cls[r]=k1[j];distinct++;} else if(cls[r]!=k1[j])ok=0;}
       for(int j=0;j<11&&ok;j++){int r=((63+j-b)%p+p)%p; if(cls[r]<0){cls[r]=k2[j];distinct++;} else if(cls[r]!=k2[j])ok=0;}
       if(ok){int ck=24-distinct; hist[0][ck]++; if(ck>=minpr){hits++;printf("HIT F0 perm=%d tab=%s mode=%d p=%d b=%d checks=%d\n",pi,t?"AZ":"KA",mode,p,b,ck);}}
     }
     /* F1/F2 autokey */
     for(int fam=1;fam<=2;fam++){
       int intraok[13],intrack[13]; /* L 1..12 */
       for(int L=1;L<=12;L++){int ok=1,ck=0;
         for(int j=L;j<13;j++){int K=fam==1?P1[j-L]:X1[j-L]; ck++; if(enc(mode,P1[j],K)!=X1[j])ok=0;}
         for(int j=L;j<11;j++){int K=fam==1?P2[j-L]:X2[j-L]; ck++; if(enc(mode,P2[j],K)!=X2[j])ok=0;}
         intraok[L]=ok; intrack[L]=ck;}
       int crok[23],crck[23]; /* d=-12..10 */
       for(int d=-12;d<=10;d++){int ok=1,ck=0;
         for(int j1=0;j1<13;j1++){int j2=j1+d; if(j2<0||j2>10)continue; int K=fam==1?P1[j1]:X1[j1]; ck++; if(enc(mode,P2[j2],K)!=X2[j2])ok=0;}
         crok[d+12]=ok; crck[d+12]=ck;}
       for(int L=1;L<=12;L++){ tests[fam]++; if(intraok[L]){int ck=intrack[L]; hist[fam][ck>24?24:ck]++;
           if(ck>=minpr){hits++;printf("HIT F%d perm=%d tab=%s mode=%d L=%d d=none checks=%d\n",fam,pi,t?"AZ":"KA",mode,L,ck);}}
         for(int d=-12;d<=L-13;d++){ tests[fam]++; if(intraok[L]&&crok[d+12]){int ck=intrack[L]+crck[d+12]; hist[fam][ck>24?24:ck]++;
           if(ck>=minpr){hits++;printf("HIT F%d perm=%d tab=%s mode=%d L=%d d=%d checks=%d\n",fam,pi,t?"AZ":"KA",mode,L,d,ck);}}}
       }
       for(int d=-12;d<=10;d++){ tests[fam]++; if(crok[d+12]){int ck=crck[d+12]; hist[fam][ck]++;
           if(ck>=minpr){hits++;printf("HIT F%d perm=%d tab=%s mode=%d L=any d=%d checks=%d\n",fam,pi,t?"AZ":"KA",mode,d,ck);}}}
     }
    }}}
  printf("perms=%d tests F0=%ld F1=%ld F2=%ld hits(checks>=%d)=%ld\n",np,tests[0],tests[1],tests[2],minpr,hits);
  for(int fm=0;fm<3;fm++){printf("F%d consistent-by-checks:",fm); for(int k=0;k<25;k++)if(hist[fm][k])printf(" %d:%ld",k,hist[fm][k]); printf("\n");}
  return 0;}
