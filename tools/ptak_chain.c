/* Cycle 22: plaintext-fed autokey behind a transposition, exact chain test.
   P_i = dec(C'_i, P_{i-L}) links every position to the one L before it, so each crib letter
   fixes its whole residue chain mod L; two crib letters on one chain give a check.
   Models: A = autokey then transpose (C'_i = carved[perm[i]], cribs at i);
           B = transpose then autokey (C = carved, cribs at invperm[i]).
   Usage: ptak_chain CARVED perms.bin minchecks  -> prints hits and summary */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char *KA="KRYPTOSABCDEFGHIJLMNQUVWXZ", *AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ";
static const char *CR1="EASTNORTHEAST", *CR2="BERLINCLOCK";
int ix(const char*A,char c){for(int i=0;i<26;i++)if(A[i]==c)return i;return -1;}
int main(int argc,char**argv){
  const char*carved=argv[1]; int minck=atoi(argv[3]);
  FILE*f=fopen(argv[2],"rb"); fseek(f,0,SEEK_END); long sz=ftell(f); rewind(f);
  int np=sz/(2*N); short*perms=malloc(sz); fread(perms,2,np*N,f); fclose(f);
  int cpos[24],ccha[24],nc=0;
  for(int i=0;i<13;i++){cpos[nc]=21+i;ccha[nc++]=CR1[i];}
  for(int i=0;i<11;i++){cpos[nc]=63+i;ccha[nc++]=CR2[i];}
  long tests=0,hits=0; long hist[25]={0}; /* best checks among fully consistent, per (ck) */
  for(int p=0;p<np;p++){ short*P=perms+p*N; int inv[N]; for(int k=0;k<N;k++)inv[P[k]]=k;
   for(int t=0;t<2;t++){const char*A=t?AZ:KA;
    int cv[N]; for(int k=0;k<N;k++)cv[k]=ix(A,carved[k]);
    for(int model=0;model<2;model++){
     int C[N],kv[N]; for(int k=0;k<N;k++)kv[k]=-1;
     if(model==0){for(int i=0;i<N;i++)C[i]=cv[P[i]]; for(int j=0;j<nc;j++)kv[cpos[j]]=ix(A,ccha[j]);}
     else {for(int i=0;i<N;i++)C[i]=cv[i]; for(int j=0;j<nc;j++)kv[inv[cpos[j]]]=ix(A,ccha[j]);}
     for(int mode=0;mode<3;mode++) for(int L=1;L<N;L++){
      tests++; int checks=0,ok=1;
      for(int r=0;r<L&&ok;r++){ int v=-1;
        for(int i=r;i<N;i+=L){
          if(v>=0){ int c=C[i]; int np_ = mode==0?(c-v+26)%26: mode==1?(v-c+26)%26:(c+v)%26; v=np_; }
          if(kv[i]>=0){ if(v>=0){checks++; if(v!=kv[i]){ok=0;break;}} v=kv[i]; }
        }}
      if(ok){ hist[checks>24?24:checks]++;
        if(checks>=minck){hits++; printf("HIT perm=%d tab=%s model=%c mode=%d L=%d checks=%d\n",p,t?"AZ":"KA",model?'B':'A',mode,L,checks);} }
     }}}}
  printf("tests=%ld hits(checks>=%d)=%ld\nconsistent-by-checks:",tests,minck,hits);
  for(int k=0;k<25;k++)if(hist[k])printf(" %d:%ld",k,hist[k]); printf("\n"); return 0;}
