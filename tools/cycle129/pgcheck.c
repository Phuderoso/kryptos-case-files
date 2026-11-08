/* Cycle 129: Periodic Gromark key streams (from mkcfg.py) x transposition bank (perms97.bin, 165,065 perms incl.
   identity; each used as sigma and sigma^-1) x model A (key at plaintext position, then transposition) / model B
   (transposition, then key at carved position) x Vigenere form (ct = CA[pa+k], ACA) / Beaufort form (ct = CA[k-pa]).
   Exact: all 24 crib letters must match. usage: pgcheck CT cfgfile perms.bin label */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char*CR1="EASTNORTHEAST",*CR2="BERLINCLOCK";
int main(int argc,char**argv){
  const char*C=argv[1]; FILE*cf=fopen(argv[2],"r"); FILE*pf=fopen(argv[3],"rb"); const char*lab=argv[4];
  fseek(pf,0,SEEK_END); long np=ftell(pf)/(2*N); rewind(pf);
  short*P=malloc(np*N*2*sizeof(short)); fread(P,2,np*N,pf);
  for(long q=0;q<np;q++){ short*s=P+q*N,*t=P+(np+q)*N; for(int i=0;i<N;i++) t[s[i]]=i; }
  int cp[24],cl[24]; for(int i=0;i<13;i++){cp[i]=21+i;cl[i]=CR1[i]-'A';} for(int i=0;i<11;i++){cp[13+i]=63+i;cl[13+i]=CR2[i]-'A';}
  char name[256],CA[32],PA[32],K[128]; long ncfg=0,surv=0;
  while(fscanf(cf,"%255s %31s %31s %127s",name,CA,PA,K)==4){ ncfg++;
    int pai[26]; for(int i=0;i<26;i++) pai[PA[i]-'A']=i;
    for(int m=0;m<2;m++) for(int be=0;be<2;be++){
      static unsigned char ok[24][N];
      for(int t=0;t<24;t++) for(int j=0;j<N;j++){
        int k= m? K[j]-'A' : K[cp[t]]-'A'; int a=pai[cl[t]]; int idx= be? ((k-a)%26+26)%26 : (a+k)%26;
        ok[t][j]= (C[j]==CA[idx]); }
      for(long q=0;q<2*np;q++){ short*s=P+q*N; int t=0;
        for(;t<24;t++) if(!ok[t][s[cp[t]]]) break;
        if(t==24){ surv++; printf("S %s %s perm=%ld dir=%d model=%c form=%s\n",lab,name,q%np,(int)(q/np),m?'B':'A',be?"beau":"vig"); } }
    } }
  printf("C %s configs %ld perms %ld survivors %ld\n",lab,ncfg,np,surv);
}
