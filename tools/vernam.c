/* Cycle 33: 5-bit Vernam (XOR) behind/without transposition.
   Encodings: 0=ITA2 letters, 1=A0 binary, 2=A1 binary, 3=KA0, 4=KA1.
   Model A: XOR key on plaintext order, then transposition (C'_i = carved[perm[i]], key index i).
   Model B: transposition then XOR (key index k = inv[i], ct = carved[k]).
   Per config: periodic key L=1..26 consistency + all derivable plaintext codes must be letters.
   Also dumps 24 key codes (as letters) when all are letter codes, for running-key scoring (model A).
   usage: vernam CARVED perms.bin dumpfile */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char*KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static int ita2[26]={0x03,0x19,0x0E,0x09,0x01,0x0D,0x1A,0x14,0x06,0x0B,0x0F,0x12,0x1C,0x0C,0x18,0x16,0x17,0x0A,0x05,0x10,0x07,0x1E,0x13,0x1D,0x15,0x11};
int code[5][26], dec[5][32];
int main(int argc,char**argv){
  const char*car=argv[1]; FILE*f=fopen(argv[2],"rb"); fseek(f,0,SEEK_END); long sz=ftell(f); fseek(f,0,SEEK_SET);
  int np=sz/(2*N); short*perms=malloc(sz); if(fread(perms,2,(size_t)np*N,f)!=(size_t)np*N)return 1; fclose(f);
  FILE*dump=fopen(argv[3],"w");
  for(int e=0;e<5;e++){for(int v=0;v<32;v++)dec[e][v]=-1;
    for(int l=0;l<26;l++){int c; if(e==0)c=ita2[l]; else if(e==1)c=l; else if(e==2)c=l+1;
      else {int idx=strchr(KA,'A'+l)-KA; c=(e==3)?idx:idx+1;} code[e][l]=c; dec[e][c]=l;}}
  const char*cr1="EASTNORTHEAST",*cr2="BERLINCLOCK"; int cp[24],cl[24],nc=0;
  for(int i=0;i<13;i++){cp[nc]=21+i;cl[nc++]=cr1[i]-'A';} for(int i=0;i<11;i++){cp[nc]=63+i;cl[nc++]=cr2[i]-'A';}
  long hits=0, cons[27]={0}, letterkeys=0;
  for(int p=0;p<np;p++){short*P=perms+(long)p*N; int inv[N]; for(int k=0;k<N;k++)inv[P[k]]=k;
    for(int e=0;e<5;e++)for(int m=0;m<2;m++){
      int ct[N]; /* ct in key-index order */ int kidx[24], kc[24];
      for(int k=0;k<N;k++) ct[k]= code[e][ (m==0? car[P[k]] : car[k]) -'A'];
      int allL=1;
      for(int j=0;j<24;j++){kidx[j]= m==0? cp[j] : inv[cp[j]]; kc[j]=ct[kidx[j]]^code[e][cl[j]]; if(dec[e][kc[j]]<0)allL=0;}
      if(allL){letterkeys++; if(m==0){fprintf(dump,"%d %d ",p,e); for(int j=0;j<24;j++)fputc('A'+dec[e][kc[j]],dump); fputc('\n',dump);}}
      for(int L=1;L<=26;L++){int key[26]; for(int r=0;r<L;r++)key[r]=-1; int ok=1;
        for(int j=0;j<24&&ok;j++){int r=kidx[j]%L; if(key[r]<0)key[r]=kc[j]; else if(key[r]!=kc[j])ok=0;}
        if(!ok)continue; cons[L]++;
        int bad=0,known=0; for(int k=0;k<N;k++){int r=k%L; if(key[r]<0)continue; known++; if(dec[e][ct[k]^key[r]]<0){bad=1;break;}}
        if(bad)continue; hits++;
        char pt[N+1]; for(int k=0;k<N;k++){int r=k%L; pt[k]= key[r]<0?'.':'A'+dec[e][ct[k]^key[r]];} pt[N]=0;
        /* return plaintext to plaintext order for model B */
        char po[N+1]; if(m==1){for(int i=0;i<N;i++)po[i]=pt[inv[i]]; po[N]=0;} else strcpy(po,pt);
        printf("HIT perm=%d enc=%d model=%c L=%d known=%d pt=%s\n",p,e,m?'B':'A',L,known,po);
      }}}
  printf("SUMMARY perms=%d hits=%ld letterkeys=%ld",np,hits,letterkeys); for(int L=1;L<=26;L++)printf(" c%d=%ld",L,cons[L]); printf("\n");
  return 0;}
