/* Cycle 96: single-rotor (Hebern-style) machine with ARBITRARY wiring P (any of 26!).
   Letters indexed by an alphabet ordering s (AZ, KA, keyed). Rotor advances every m letters; entry side moves d1, exit d2 per advance:
     P( s(p_i) + d1*t_i ) = s(c_i) + d2*t_i  (mod 26),  t_i = floor(i/m).   Real Hebern: d1 = d2 (conjugation); we allow any pair.
   Crib test: the 24 (x,y) pairs must define a partial bijection. Optional transposition first: carved c at position perm[j].
   reflector mode (R): P is a fixed-point-free involution (Enigma-like one rotor + reflector, d1=d2), pairs must be symmetric.
   Usage: ./rotor CT alphabets.bin M mmax [perms.bin] [R] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PT="EASTNORTHEASTBERLINCLOCK";
int main(int argc,char**argv){ const char*CT=argv[1]; FILE*f=fopen(argv[2],"rb"); fseek(f,0,2); long na=ftell(f)/26; fseek(f,0,0);
  unsigned char*A=malloc(na*26); fread(A,26,na,f); fclose(f); long M=atol(argv[3]); if(M>na)M=na; int mmax=atoi(argv[4]);
  long np=1; short*P=NULL; int refl=0;
  for(int a=5;a<argc;a++){ if(!strcmp(argv[a],"R")) refl=1; else { f=fopen(argv[a],"rb"); fseek(f,0,2); np=ftell(f)/194; fseek(f,0,0); P=malloc(np*194); fread(P,194,np,f); fclose(f);} }
  long long runs=0,hits=0;
  #pragma omp parallel for schedule(dynamic,1) reduction(+:runs,hits)
  for(long a=0;a<M;a++){ int s[26]; for(int k=0;k<26;k++) s[A[a*26+k]]=k;
    for(long t=0;t<np;t++) for(int m=1;m<=mmax;m++) for(int d1=0;d1<26;d1++) for(int d2=0;d2<26;d2++){
      if(refl && d1!=d2) continue; if(d1==0&&d2==0) continue; runs++;
      signed char fw[26],bw[26]; memset(fw,-1,26); memset(bw,-1,26); int ok=1;
      for(int q=0;q<24&&ok;q++){ int i=CI[q]; int ci = P? P[t*97+i] : i; int ti=i/m;
        int x=(s[PT[q]-65]+d1*ti)%26, y=(s[CT[ci]-65]+d2*ti)%26;
        if(refl){ if(x==y){ok=0;break;} if(fw[x]==-1&&fw[y]==-1){fw[x]=y;fw[y]=x;} else if(fw[x]!=y||fw[y]!=x) ok=0; }
        else { if(fw[x]==-1&&bw[y]==-1){fw[x]=y;bw[y]=x;} else if(fw[x]!=y||bw[y]!=x) ok=0; } }
      if(ok){ hits++;
        #pragma omp critical
        printf("HIT a=%ld t=%ld m=%d d1=%d d2=%d\n",a,t,m,d1,d2); } } }
  printf("ALPHABETS %ld PERMS %ld MMAX %d REFL %d RUNS %lld HITS %lld\n",M,np,mmax,refl,runs,hits); return 0; }
