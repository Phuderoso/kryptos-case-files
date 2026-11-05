// Cycle 59: exact periodic-key test behind a transposition family.
// For each perm (int16 x97, -1 = omitted), alphabet (Quagmire III: same keyed alphabet both sides),
// mode (Vig k=c-p, Beau k=c+p, in alphabet index space; variant Beaufort = Vig consistency),
// key-position order (0: key indexed by PT position j; 1: key indexed by carved position perm[j]),
// period p = 1..PMAX: all 24 crib letters must agree with one key letter per residue class.
// Output: hits per period, and lines for each hit with p <= PREPORT.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
int main(int argc,char**argv){
  if(argc<6){fprintf(stderr,"usage: perm.bin alpha.bin nalpha ct.txt pmax [preport]\n");return 1;}
  FILE*f=fopen(argv[1],"rb"); fseek(f,0,SEEK_END); long sz=ftell(f); rewind(f);
  long np=sz/(2*N); short*P=malloc(sz); fread(P,1,sz,f); fclose(f);
  f=fopen(argv[2],"rb"); int na=atoi(argv[3]); unsigned char*A=malloc(26*na); fread(A,1,26*na,f); fclose(f);
  char ct[200]; f=fopen(argv[4],"r"); fscanf(f,"%199s",ct); fclose(f);
  int pmax=atoi(argv[5]); int prep=argc>6?atoi(argv[6]):12;
  const char*cr1="EASTNORTHEAST",*cr2="BERLINCLOCK"; int cpos[24]; char cpt[24]; int nc=0;
  for(int i=0;i<13;i++){cpos[nc]=21+i;cpt[nc++]=cr1[i];}
  for(int i=0;i<11;i++){cpos[nc]=63+i;cpt[nc++]=cr2[i];}
  long hits[64]={0};
  #pragma omp parallel
  { long lh[64]={0};
  #pragma omp for schedule(dynamic,64)
  for(long t=0;t<np;t++){ short*pp=P+t*N; int ok=1;
    for(int i=0;i<nc;i++) if(pp[cpos[i]]<0){ok=0;break;} if(!ok) continue;
    for(int a=0;a<na;a++){ unsigned char*al=A+26*a; int idx[26]; for(int i=0;i<26;i++) idx[al[i]]=i;
      int ci[24],pi[24]; for(int i=0;i<nc;i++){ci[i]=idx[ct[pp[cpos[i]]]-'A'];pi[i]=idx[cpt[i]-'A'];}
      for(int m=0;m<2;m++){ int k[24]; for(int i=0;i<nc;i++) k[i]=m==0?(ci[i]-pi[i]+26)%26:(ci[i]+pi[i])%26;
        for(int o=0;o<2;o++){ int pos[24]; for(int i=0;i<nc;i++) pos[i]=o==0?cpos[i]:pp[cpos[i]];
          for(int p=1;p<=pmax;p++){ int key[64]; for(int r=0;r<p;r++) key[r]=-1; int good=1;
            for(int i=0;i<nc;i++){int r=pos[i]%p; if(key[r]<0) key[r]=k[i]; else if(key[r]!=k[i]){good=0;break;}}
            if(good){ lh[p]++; if(p<=prep){
              #pragma omp critical
              { printf("HIT perm %ld alpha %d mode %s order %d p %d key ",t,a,m?"beau":"vig",o,p);
                for(int r=0;r<p;r++) putchar(key[r]<0?'?':al[key[r]]+'A'); putchar('\n'); } }
              break; } } } } } }
  #pragma omp critical
  for(int p=0;p<64;p++) hits[p]+=lh[p]; }
  fprintf(stderr,"perms %ld alphabets %d; minimal-period hits:",np,na);
  for(int p=1;p<=pmax;p++) fprintf(stderr," p%d:%ld",p,hits[p]); fprintf(stderr,"\n"); return 0; }
