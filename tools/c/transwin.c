/* Cycle 12: transposition-undone small-digit window test.
   For each transposition t (perm[j] = carved CT index paired with PT position j, -1 = omitted letter) and each
   alphabet pair (PA, CA), the crib offsets CA^-1(c) -+ PA^-1(p) must fit a cyclic window of width <= B for a
   digit key in base B (any generator).  Tier D: PA = CA over all alphabets (K1/K2 Quagmire-III style).
   Tier F: every PA, CA pair among the first M alphabets (single words).  Modes: vig (=variant Beaufort width), beau.
   Build: gcc -O3 -fopenmp transwin.c -o transwin ; Run: ./transwin alpha.bin perm.bin CT M WPRINT WMAX */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PT="EASTNORTHEASTBERLINCLOCK";
static int test(const unsigned char*inv_p,const unsigned char*inv_c,const short*perm,const char*CT,int m,int WMAX,int*s0,int*nn){
  int lo=0,hi=0,k0=-1,n=0;
  for(int i=0;i<24;i++){int t=perm[CI[i]]; if(t<0) continue; int P=inv_p[PT[i]-65],C=inv_c[CT[t]-65];
    int k=m?(C+P)%26:(C-P+26)%26; if(k0<0){k0=k;n++;continue;} n++;
    int d=((k-k0+13+26)%26)-13; if(d<lo)lo=d; if(d>hi)hi=d; if(hi-lo>=WMAX) return 99;}
  *s0=(k0+lo+26)%26; *nn=n; return hi-lo+1;}
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"rb"); fseek(f,0,2); long na=ftell(f)/26; fseek(f,0,0);
  unsigned char*A=malloc(na*26); fread(A,26,na,f); fclose(f);
  f=fopen(argv[2],"rb"); fseek(f,0,2); long nt=ftell(f)/194; fseek(f,0,0);
  short*Pm=malloc(nt*194); fread(Pm,194,nt,f); fclose(f);
  const char*CT=argv[3]; long M=atol(argv[4]); int WP=atoi(argv[5]), WMAX=atoi(argv[6]);
  unsigned char*INV=malloc(na*26);
  for(long a=0;a<na;a++) for(int j=0;j<26;j++) INV[a*26+A[a*26+j]]=j;
  long long hist[2][2][16]; memset(hist,0,sizeof hist);
  #pragma omp parallel
  { long long h[2][2][16]; memset(h,0,sizeof h);
    #pragma omp for schedule(dynamic,16)
    for(long t=0;t<nt;t++){ const short*p=Pm+t*97; int s,n,w;
      for(long a=0;a<na;a++) for(int m=0;m<2;m++){
        w=test(INV+a*26,INV+a*26,p,CT,m,WMAX,&s,&n); if(w>WMAX) continue; h[0][m][w]++;
        if(w<=WP){
          #pragma omp critical
          printf("HIT D t=%ld a=%ld %s w=%d s=%d n=%d\n",t,a,m?"beau":"vig",w,s,n);} }
      for(long a=0;a<M;a++) for(long b=0;b<M;b++){ if(a==b) continue; for(int m=0;m<2;m++){
        w=test(INV+a*26,INV+b*26,p,CT,m,WMAX,&s,&n); if(w>WMAX) continue; h[1][m][w]++;
        if(w<=WP){
          #pragma omp critical
          printf("HIT F t=%ld pa=%ld ca=%ld %s w=%d s=%d n=%d\n",t,a,b,m?"beau":"vig",w,s,n);} } } }
    #pragma omp critical
    for(int x=0;x<2;x++)for(int m=0;m<2;m++)for(int w=0;w<16;w++) hist[x][m][w]+=h[x][m][w];
  }
  printf("TRANSPOSITIONS %ld ALPHABETS %ld M %ld\n",nt,na,M);
  for(int x=0;x<2;x++)for(int m=0;m<2;m++){printf("HIST %s %s",x?"F":"D",m?"beau":"vig");
    for(int w=1;w<=WMAX;w++) printf(" %d:%lld",w,hist[x][m][w]); printf("\n");}
  return 0;}
