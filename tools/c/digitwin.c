/* Cycle 11: generator-agnostic small-digit-key test.
   Model: c_i = CA[(PA^-1(p_i) + s + d_i) mod 26] (vig) or CA^-1(c_i) = s + d_i - PA^-1(p_i) (beau),
   d_i in {0..B-1} from ANY source (Gromark, base conversion, dates, clock lamps...), s = unknown rotation.
   Then the 24 crib offsets must lie in a cyclic window of width <= B.  Variant Beaufort = vig negated (same width).
   Prints every (PA, CA, mode) whose window width <= WMAX, plus a histogram.
   Build: gcc -O3 -fopenmp digitwin.c -o digitwin ; Run: ./digitwin alpha.bin CT97 WMAX */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PT="EASTNORTHEASTBERLINCLOCK";
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"rb"); fseek(f,0,2); long n=ftell(f)/26; fseek(f,0,0);
  unsigned char*A=malloc(n*26); fread(A,26,n,f); fclose(f);
  const char*CT=argv[2]; int WMAX=atoi(argv[3]);
  unsigned char*pv=malloc(n*24),*cv=malloc(n*24);
  for(long a=0;a<n;a++){unsigned char inv[26]; for(int j=0;j<26;j++) inv[A[a*26+j]]=j;
    for(int i=0;i<24;i++){pv[a*24+i]=inv[PT[i]-65]; cv[a*24+i]=inv[CT[CI[i]]-65];}}
  long long hist[2][14]; memset(hist,0,sizeof hist);
  #pragma omp parallel
  { long long h[2][14]; memset(h,0,sizeof h);
    #pragma omp for schedule(dynamic,64)
    for(long a=0;a<n;a++) for(long b=0;b<n;b++) for(int m=0;m<2;m++){
      const unsigned char*P=pv+a*24,*C=cv+b*24; int k0=m? (C[0]+P[0])%26 : (C[0]-P[0]+26)%26;
      int lo=0,hi=0,ok=1; int k[24]; k[0]=k0;
      for(int i=1;i<24;i++){int ki=m?(C[i]+P[i])%26:(C[i]-P[i]+26)%26; k[i]=ki;
        int d=((ki-k0+13+26)%26)-13; if(d<lo)lo=d; if(d>hi)hi=d; if(hi-lo>=WMAX){ok=0;break;}}
      if(!ok) continue; int w=hi-lo+1; h[m][w]++;
      #pragma omp critical
      { printf("HIT %ld %ld %s w=%d s=%d d=",a,b,m?"beau":"vig",w,(k0+lo+26)%26);
        for(int i=0;i<24;i++) printf("%d",(((k[i]-k0+13+26)%26)-13)-lo); printf("\n"); }
    }
    #pragma omp critical
    for(int m=0;m<2;m++)for(int w=0;w<14;w++) hist[m][w]+=h[m][w];
  }
  printf("PAIRS %ld\n",n*n);
  for(int m=0;m<2;m++){printf("HIST %s",m?"beau":"vig"); for(int w=1;w<=WMAX;w++) printf(" %d:%lld",w,hist[m][w]); printf("\n");}
  return 0;}
