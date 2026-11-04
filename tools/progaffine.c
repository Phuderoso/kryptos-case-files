/* Cycle 40: PROGRESSIVE affine substitution (Trithemius-style stepping of both the multiplier and the shift)
   on either side of a transposition, A-Z or KRYPTOS numbering, exact check against the 24 known letters.
   Index i = plaintext position (model A) or carved position (model B); same conventions as tools/affine.c.
   Form E (encryption form): y = a0*r^i*x + b0 + d*i (mod 26)
   Form D (decryption form): x = a0*r^i*y + b0 + d*i (mod 26)
   a0, r units (12 each), d 0..25, b0 fixed by the first crib.  r=1,d=0 is plain affine; a0=r=1 is a
   progressive (Trithemius) shift; r=1 is a fixed-multiplier progressive shift.  (An additively stepping
   multiplier a0+k*i cannot stay a unit mod 26 unless k=0, so multiplicative stepping is the only option.)
   Every consistent config fixes all 97 letters: decrypt and score with English quadgrams.
   With Q=1 the shift also gets a second-order term q*i*(i-1)/2 (accelerating progression), q 0..25.
   usage: progaffine CARVED perms.bin qg.bin [start end Q] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char*KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static const int U[12]={1,3,5,7,9,11,15,17,19,21,23,25};
float*QG; int inva[26];
static float score(const int*x){float s=0;for(int i=0;i+3<N;i++)s+=QG[((x[i]*26+x[i+1])*26+x[i+2])*26+x[i+3]];return s/(N-3);}
int main(int argc,char**argv){
  const char*car=argv[1]; FILE*f=fopen(argv[2],"rb"); fseek(f,0,SEEK_END); long sz=ftell(f); fseek(f,0,SEEK_SET);
  int np=sz/(2*N); short*perms=malloc(sz); if(fread(perms,2,(size_t)np*N,f)!=(size_t)np*N)return 1; fclose(f);
  int p0=0,Qm=0; if(argc>5){p0=atoi(argv[4]); int m=atoi(argv[5]); if(m<np)np=m;} if(argc>6)Qm=atoi(argv[6]);
  int tri[N]; for(int i=0;i<N;i++)tri[i]=i*(i-1)/2%26;
  QG=malloc(sizeof(float)*456976); f=fopen(argv[3],"rb"); if(fread(QG,4,456976,f)!=456976)return 1; fclose(f);
  for(int a=1;a<26;a+=2)for(int b=1;b<26;b++)if(a*b%26==1)inva[a]=b;
  int num[2][26],den[2][26]; for(int l=0;l<26;l++){num[0][l]=l; num[1][l]=strchr(KA,'A'+l)-KA;} for(int e=0;e<2;e++)for(int l=0;l<26;l++)den[e][num[e][l]]=l;
  int pw[12][N]; for(int u=0;u<12;u++){pw[u][0]=1; for(int i=1;i<N;i++)pw[u][i]=pw[u][i-1]*U[u]%26;}
  const char*cr1="EASTNORTHEAST",*cr2="BERLINCLOCK"; int cp[24],cl[24],nc=0;
  for(int i=0;i<13;i++){cp[nc]=21+i;cl[nc++]=cr1[i]-'A';} for(int i=0;i<11;i++){cp[nc]=63+i;cl[nc++]=cr2[i]-'A';}
  long cons[2][2][2]={{{0}}}; float best=-99; long tests=0;
  for(int p=p0;p<np;p++){short*P=perms+(long)p*N; int inv[N]; for(int k=0;k<N;k++)inv[P[k]]=k;
   for(int e=0;e<2;e++)for(int m=0;m<2;m++){
    int ct[N]; for(int k=0;k<N;k++) ct[k]=num[e][(m==0? car[P[k]] : car[k])-'A'];
    int ki[24],px[24],cx[24]; for(int j=0;j<24;j++){ki[j]= m==0? cp[j] : inv[cp[j]]; px[j]=num[e][cl[j]]; cx[j]=ct[ki[j]];}
    for(int form=0;form<2;form++){
     const int*IN= form==0? px:cx; const int*OUT= form==0? cx:px;   /* OUT = a0 r^i IN + b0 + d i */
     for(int ua=0;ua<12;ua++)for(int ur=0;ur<12;ur++){int a0=U[ua];
      int v[24]; for(int j=0;j<24;j++) v[j]=((OUT[j]-a0*pw[ur][ki[j]]*IN[j])%26+26)%26;
      for(int q=0;q<(Qm?26:1);q++)for(int d=0;d<26;d++){tests++; int b0=((v[0]-d*ki[0]-q*tri[ki[0]])%26+52*26)%26; int ok=1;
        for(int j=1;j<24;j++) if((b0+d*ki[j]+q*tri[ki[j]])%26!=v[j]){ok=0;break;}
        if(!ok)continue; cons[e][m][form]++;
        int pt[N],po[N];
        for(int k=0;k<N;k++){int A=a0*pw[ur][k]%26, B=(b0+d*k+q*tri[k])%26, x;
          if(form==0) x=((ct[k]-B)%26+26)%26*inva[A]%26; else x=(A*ct[k]+B)%26; pt[k]=den[e][x];}
        if(m==1){for(int i=0;i<N;i++)po[i]=pt[inv[i]];} else memcpy(po,pt,sizeof pt);
        float sc=score(po); if(sc>best)best=sc;
        char o[N+1];for(int i=0;i<N;i++)o[i]='A'+po[i];o[N]=0;
        printf("HIT perm=%d num=%c model=%c form=%c a0=%d r=%d b0=%d d=%d q=%d score=%.3f pt=%s\n",p,e?'K':'A',m?'B':'A',form?'D':'E',a0,U[ur],b0,d,q,sc,o);}}}}}
  printf("SUMMARY perms=%d tests=%ld best_qg=%.3f\n",np,tests,best);
  for(int e=0;e<2;e++)for(int m=0;m<2;m++)for(int fm=0;fm<2;fm++)printf("num=%c model=%c form=%c consistent=%ld\n",e?'K':'A',m?'B':'A',fm?'D':'E',cons[e][m][fm]);
  return 0;}
