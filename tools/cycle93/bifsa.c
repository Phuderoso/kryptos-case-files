/* Cycle 93: simulated annealing for Bifid 5x5 (W-free 25-letter alphabet) with one or two arbitrary squares,
   fixed period p, orientation o (0: ct = Bifid_enc(pt; A in, B out) so pt = dec; 1: pt = Bifid_enc(ct; A in, B out)).
   Score = quadgram log10 sum over plaintext + CW * crib matches (cribs 20-32 EASTNORTHEAST, 60-70 BERLINCLOCK).
   usage: bifsa CT p o nsq restarts iters seed qg.bin */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static const char *SYM="ABCDEFGHIJKLMNOPQRSTUVXYZ";
static float *QG; static int N, P, O, NSQ; static int ct[200]; static int crib[200];
static unsigned long long rs;
static unsigned rnd(void){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return (unsigned)(rs>>11);}
static double ur(void){return (rnd()&0xffffff)/16777216.0;}
static int letidx(char c){const char*q=strchr(SYM,c);return q?(int)(q-SYM):-1;}
static void decode(int*A,int*B,int*pt){ /* A,B: cell->symbol; need symbol->cell for one side */
  int posA[25],posB[25]; for(int i=0;i<25;i++){posA[A[i]]=i;posB[B[i]]=i;}
  for(int b=0;b<N;b+=P){int L=N-b<P?N-b:P; int st[200];
    if(O==0){ /* ct coords from B as stream r0 c0 r1 c1..; pt[k]=A[(st[k],st[L+k])] */
      for(int k=0;k<L;k++){int c=posB[ct[b+k]];st[2*k]=c/5;st[2*k+1]=c%5;}
      for(int k=0;k<L;k++)pt[b+k]=A[st[k]*5+st[L+k]];
    } else { /* pt = enc(ct): stream = rows of ct (via A) then cols; pt[k]=B[(st[2k],st[2k+1])] */
      for(int k=0;k<L;k++){int c=posA[ct[b+k]];st[k]=c/5;st[L+k]=c%5;}
      for(int k=0;k<L;k++)pt[b+k]=B[st[2*k]*5+st[2*k+1]];
    }}
}
static const double CW=3.0;
static int AZ(int s){return SYM[s]-'A';}
static double score(int*A,int*B,int*pt,int*ch){decode(A,B,pt);double s=0;int h=0;
  for(int i=0;i+3<N;i++)s+=QG[((AZ(pt[i])*26+AZ(pt[i+1]))*26+AZ(pt[i+2]))*26+AZ(pt[i+3])];
  for(int i=0;i<N;i++)if(crib[i]>=0&&pt[i]==crib[i])h++; *ch=h; return s+CW*h;}
int main(int argc,char**argv){
  if(argc<9){fprintf(stderr,"usage\n");return 1;}
  N=strlen(argv[1]); for(int i=0;i<N;i++)ct[i]=letidx(argv[1][i]);
  P=atoi(argv[2]);O=atoi(argv[3]);NSQ=atoi(argv[4]);int R=atoi(argv[5]);long IT=atol(argv[6]);rs=88172645463325252ULL^(unsigned long long)atol(argv[7])*2654435761ULL;
  QG=malloc(4*456976);FILE*f=fopen(argv[8],"rb");if(fread(QG,4,456976,f)!=456976)return 2;fclose(f);
  for(int i=0;i<N;i++)crib[i]=-1;const char*c1="EASTNORTHEAST",*c2="BERLINCLOCK";
  for(int i=0;i<13;i++)crib[20+i]=letidx(c1[i]);for(int i=0;i<11;i++)crib[60+i]=letidx(c2[i]);
  int pt[200],bestpt[200];double gbest=-1e18;int gh=0;
  for(int r=0;r<R;r++){int A[25],B[25];for(int i=0;i<25;i++)A[i]=B[i]=i;
    for(int i=24;i>0;i--){int j=rnd()%(i+1),t=A[i];A[i]=A[j];A[j]=t;}
    if(NSQ==2)for(int i=24;i>0;i--){int j=rnd()%(i+1),t=B[i];B[i]=B[j];B[j]=t;}
    int*Bp=(NSQ==2)?B:A; int h; double cur=score(A,Bp,pt,&h),best=cur;
    for(long it=0;it<IT;it++){double T=12.0*(1.0-(double)it/IT)+0.2;
      int*S=(NSQ==2&&(rnd()&1))?B:A; int i=rnd()%25,j=rnd()%25; if(i==j)continue;
      int t=S[i];S[i]=S[j];S[j]=t; int h2;double ns=score(A,Bp,pt,&h2);
      if(ns>=cur||ur()<exp((ns-cur)/T)){cur=ns;if(cur>best)best=cur; if(cur>gbest){gbest=cur;gh=h2;memcpy(bestpt,pt,sizeof(pt));}}
      else{t=S[i];S[i]=S[j];S[j]=t;}}
  }
  printf("p=%d o=%d nsq=%d best=%.1f qg/char=%.3f crib=%d/24 ",P,O,NSQ,gbest,(gbest-CW*gh)/(N-3),gh);
  for(int i=0;i<N;i++)putchar(SYM[bestpt[i]]);putchar('\n');return 0;}
