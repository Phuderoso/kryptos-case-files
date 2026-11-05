/* Cycle 34: running keys the artist already carved (K0-K3 plaintexts/ciphertexts, KA tableau),
   exact crib test, with and without a transposition, both layer orders.
   Modes 0-5: {AZ,KA} x {Vigenere K=C-P, Beaufort K=C+P, variant K=P-C}; modes 6-10: 5-bit XOR codes (as cycle 33).
   Model A: substitute in plaintext order then transpose (key index = plaintext position).
   Model B: transpose then substitute in carved order (key index = carved position).
   Key = text[(o + keyindex) mod T], every offset o, text cyclic. Reports configs with >= THR crib matches
   and the global max. usage: carved_rk CARVED perms.bin texts.txt THR
   WARNING (cycle 74 audit): key texts longer than 8191 letters are chopped by the %8191s read; use bookrk for books. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char*KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static int ita2[26]={0x03,0x19,0x0E,0x09,0x01,0x0D,0x1A,0x14,0x06,0x0B,0x0F,0x12,0x1C,0x0C,0x18,0x16,0x17,0x0A,0x05,0x10,0x07,0x1E,0x13,0x1D,0x15,0x11};
int code[5][26],dec[5][32],kai[26];
char*tx[256];int tl[256];char tn[256][256];int nt=0; int*pos[256][26];int npos[256][26];
int main(int argc,char**argv){
  const char*car=argv[1];FILE*f=fopen(argv[2],"rb");fseek(f,0,SEEK_END);long sz=ftell(f);fseek(f,0,SEEK_SET);
  int np=sz/(2*N);short*perms=malloc(sz);if(fread(perms,2,(size_t)np*N,f)!=(size_t)np*N)return 1;fclose(f);
  int THR=atoi(argv[4]);
  FILE*t=fopen(argv[3],"r");char buf[8192];
  while(fscanf(t,"%63s %8191s",tn[nt],buf)==2){tl[nt]=strlen(buf);tx[nt]=strdup(buf);
    for(int l=0;l<26;l++){pos[nt][l]=malloc(sizeof(int)*tl[nt]);npos[nt][l]=0;}
    for(int i=0;i<tl[nt];i++){int l=buf[i]-'A';pos[nt][l][npos[nt][l]++]=i;} nt++;}
  for(int l=0;l<26;l++)kai[l]=strchr(KA,'A'+l)-KA;
  for(int e=0;e<5;e++){for(int v=0;v<32;v++)dec[e][v]=-1;
    for(int l=0;l<26;l++){int c;if(e==0)c=ita2[l];else if(e==1)c=l;else if(e==2)c=l+1;else c=(e==3)?kai[l]:kai[l]+1;code[e][l]=c;dec[e][c]=l;}}
  const char*cr1="EASTNORTHEAST",*cr2="BERLINCLOCK";int cp[24],cl[24],nc=0;
  for(int i=0;i<13;i++){cp[nc]=21+i;cl[nc++]=cr1[i]-'A';}for(int i=0;i<11;i++){cp[nc]=63+i;cl[nc++]=cr2[i]-'A';}
  int gbest=0; long hist[25]={0}; long full=0;
  for(int p=0;p<np;p++){short*P=perms+(long)p*N;int inv[N];for(int k=0;k<N;k++)inv[P[k]]=k;
   for(int m=0;m<2;m++)for(int md=0;md<11;md++){
    int kidx[24],req[24],okc=1;
    for(int j=0;j<24;j++){int ci; /* carved letter that encodes crib j */
      if(m==0){kidx[j]=cp[j]; ci=car[P[cp[j]]]-'A';} else {kidx[j]=inv[cp[j]]; ci=car[inv[cp[j]]]-'A';}
      /* model A: C'_i=car[P[i]] is the substituted text in plaintext order; model B: carved position k=inv[i] */
      int pl=cl[j],k;
      if(md<6){int a=md/3,ty=md%3; int c= a?kai[ci]:ci, pp= a?kai[pl]:pl;
        int kv= ty==0? (c-pp+26)%26 : ty==1? (c+pp)%26 : (pp-c+26)%26; k= a? KA[kv]-'A' : kv;}
      else {int e=md-6; int kc=code[e][ci]^code[e][pl]; k=dec[e][kc]; if(k<0){okc=0;break;}}
      req[j]=k;}
    if(!okc)continue;
    for(int ti=0;ti<nt;ti++){int T=tl[ti];const char*s=tx[ti];
      for(int q=0;q<npos[ti][req[0]];q++){int o=((pos[ti][req[0]][q]-kidx[0])%T+T)%T;int c=1;
        for(int j=1;j<24;j++) if(s[(o+kidx[j])%T]-'A'==req[j])c++;
        hist[c]++; if(c>gbest)gbest=c;
        if(c>=THR){printf("CAND matches=%d perm=%d model=%c mode=%d text=%s offset=%d\n",c,p,m?'B':'A',md,tn[ti],o);
          if(c==24)full++;}}}
   }}
  printf("SUMMARY perms=%d texts=%d best=%d full=%ld hist:",np,nt,gbest,full);for(int c=1;c<=24;c++)if(hist[c])printf(" %d:%ld",c,hist[c]);printf("\n");return 0;}
