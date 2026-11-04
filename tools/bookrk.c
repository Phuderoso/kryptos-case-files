/* Cycle 35: a named book as running key, exact crib test via bitsets, with and without a transposition,
   both layer orders. Substitutions: 24 additive tableaux = {Vigenere C=P+K, Beaufort C=K-P, variant C=P-K}
   x plain alphabet {AZ,KA} x cipher alphabet {AZ,KA} x key-letter numbering {AZ,KA} (covers Quagmire I-III
   built on KRYPTOS), plus 5 five-bit XOR codes (cycle 33). Model A: substitute in plaintext order, then transpose
   (key index = plaintext position). Model B: transpose, then substitute in carved order (key index = carved pos).
   For each (perm, model, mode) we AND shifted letter bitsets of the book for the 24 crib constraints in a fixed
   order and stop when no offset survives; depth = number of constraints some offset satisfies together.
   Prints configs with depth >= THR and a depth histogram. usage: bookrk CARVED perms.bin texts.txt THR */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define N 97
static const char*KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static int ita2[26]={0x03,0x19,0x0E,0x09,0x01,0x0D,0x1A,0x14,0x06,0x0B,0x0F,0x12,0x1C,0x0C,0x18,0x16,0x17,0x0A,0x05,0x10,0x07,0x1E,0x13,0x1D,0x15,0x11};
int code[5][26],dec[5][32],kai[26];
int main(int argc,char**argv){
  const char*car=argv[1];FILE*f=fopen(argv[2],"rb");fseek(f,0,SEEK_END);long sz=ftell(f);fseek(f,0,SEEK_SET);
  int np=sz/(2*N);short*perms=malloc(sz);if(fread(perms,2,(size_t)np*N,f)!=(size_t)np*N)return 1;fclose(f);
  int THR=atoi(argv[4]);
  for(int l=0;l<26;l++)kai[l]=strchr(KA,'A'+l)-KA;
  for(int e=0;e<5;e++){for(int v=0;v<32;v++)dec[e][v]=-1;
    for(int l=0;l<26;l++){int c;if(e==0)c=ita2[l];else if(e==1)c=l;else if(e==2)c=l+1;else c=(e==3)?kai[l]:kai[l]+1;code[e][l]=c;dec[e][c]=l;}}
  const char*cr1="EASTNORTHEAST",*cr2="BERLINCLOCK";int cp[24],cl[24],nc=0;
  for(int i=0;i<13;i++){cp[nc]=21+i;cl[nc++]=cr1[i]-'A';}for(int i=0;i<11;i++){cp[nc]=63+i;cl[nc++]=cr2[i]-'A';}
  FILE*t=fopen(argv[3],"r");static char name[64];char*buf=malloc(1<<21);
  long hist[25]={0};int gbest=0;long full=0;
  while(fscanf(t,"%63s %2000000s",name,buf)==2){
    int T=strlen(buf);int W=(T+63)/64+4;int nofs=T-N+1;int WO=(nofs+63)/64;
    uint64_t*B=calloc((size_t)26*W,8);for(int i=0;i<T;i++)B[(size_t)(buf[i]-'A')*W+i/64]|=1ULL<<(i%64);
    uint64_t*R=malloc(8*(size_t)W);
    for(int p=0;p<np;p++){short*P=perms+(long)p*N;int inv[N];for(int k=0;k<N;k++)inv[P[k]]=k;
     for(int m=0;m<2;m++)for(int md=0;md<29;md++){
      int q[24],req[24],ok=1;
      for(int j=0;j<24;j++){int ci; if(m==0){q[j]=cp[j];ci=car[P[cp[j]]]-'A';}else{q[j]=inv[cp[j]];ci=car[inv[cp[j]]]-'A';}
        int pl=cl[j],k;
        if(md<24){int ty=md%3,ap=(md/3)&1,ac=(md/6)&1,ak=(md/12)&1;
          int c=ac?kai[ci]:ci, pp=ap?kai[pl]:pl;
          int kv= ty==0?(c-pp+26)%26: ty==1?(c+pp)%26:(pp-c+26)%26; k= ak? KA[kv]-'A':kv;}
        else{int e=md-24;int kc=code[e][ci]^code[e][pl];k=dec[e][kc];if(k<0){ok=0;break;}}
        req[j]=k;}
      if(!ok)continue;
      int depth=0;
      for(int j=0;j<24;j++){const uint64_t*Bl=B+(size_t)req[j]*W;int s=q[j]/64,b=q[j]%64;uint64_t any=0;
        for(int w=0;w<WO;w++){uint64_t v= b? (Bl[w+s]>>b)|(Bl[w+s+1]<<(64-b)) : Bl[w+s];
          if(j==0)R[w]=v;else R[w]&=v; any|=R[w];}
        if(nofs%64 && 1){ /* mask tail */ }
        if(!any)break; depth=j+1;}
      if(depth==24){ /* verify tail bits are real offsets */
        int real=0;for(int w=0;w<WO;w++){uint64_t v=R[w];while(v){int o=w*64+__builtin_ctzll(v);v&=v-1;if(o<nofs){real=1;
          printf("FULL perm=%d model=%c mode=%d text=%s offset=%d\n",p,m?'B':'A',md,name,o);}}}
        if(!real)depth=23; else full++;}
      hist[depth]++; if(depth>gbest)gbest=depth;
      if(depth>=THR&&depth<24)printf("CAND depth=%d perm=%d model=%c mode=%d text=%s\n",depth,p,m?'B':'A',md,name);
     }}
    free(B);free(R);}
  printf("SUMMARY perms=%d best=%d full=%ld hist:",np,gbest,full);for(int c=0;c<=24;c++)if(hist[c])printf(" %d:%ld",c,hist[c]);printf("\n");return 0;}
