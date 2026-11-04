/* Cycle 26: interrupted-key (X-reset) Vigenere/Beaufort/variant with dictionary key words.
   Usage: xreset <ciphertext97> <wordlist> [maxshow]
   Rules: 0 plain periodic, 1 key restarts after each plaintext X, 2 key restarts after each ciphertext X,
          3 key does not advance on plaintext X. Tableaux: AZ, KA (same alphabet both sides, K1/K2 style).
   Every key phase 0..L-1 tried. Reports best crib-match count and full matches. */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
static const char *ALPH[2]={"ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"};
static const char *CRIB1="EASTNORTHEAST", *CRIB2="BERLINCLOCK";
int main(int argc,char**argv){
  const char*ct=argv[1]; int n=strlen(ct); FILE*f=fopen(argv[2],"r"); int maxshow=argc>3?atoi(argv[3]):20;
  char crib[128]; memset(crib,0,sizeof crib);
  for(int i=0;i<13;i++)crib[21+i]=CRIB1[i]; for(int i=0;i<11;i++)crib[63+i]=CRIB2[i];
  int idx[2][26]; for(int t=0;t<2;t++)for(int i=0;i<26;i++)idx[t][ALPH[t][i]-'A']=i;
  int c[128]; char w[64]; long tests=0; int best[4]={0}; int hist[4][25]; memset(hist,0,sizeof hist); int shown=0;
  while(fgets(w,64,f)){ int L=0; int k[64]; for(char*p=w;*p;p++){ if(*p>='a'&&*p<='z')*p-=32; if(*p>='A'&&*p<='Z')k[L++]=*p-'A'; }
    if(L<3||L>20) continue;
    for(int t=0;t<2;t++){ int ki[64]; for(int i=0;i<L;i++)ki[i]=idx[t][k[i]]; for(int i=0;i<n;i++)c[i]=idx[t][ct[i]-'A'];
     for(int m=0;m<3;m++) for(int r=0;r<4;r++) for(int ph=0;ph<L;ph++){ tests++;
      int j=ph, hits=0, miss=0; char pt[128];
      for(int i=0;i<n;i++){ int kk=ki[j%L], p;
        if(m==0)p=(c[i]-kk+26)%26; else if(m==1)p=(kk-c[i]+26)%26; else p=(c[i]+kk)%26;
        pt[i]=ALPH[t][p];
        if(crib[i]){ if(pt[i]==crib[i])hits++; else miss++; }
        if(r==1 && pt[i]=='X') j=0; else if(r==2 && ct[i]=='X') j=0; else if(r==3 && pt[i]=='X') ; else j++;
      }
      pt[n]=0; hist[r][hits]++; if(hits>best[r])best[r]=hits;
      if(hits>=20 && shown<maxshow){ shown++; printf("HIT %d/24 rule%d tab%s mode%d key=%.*s ph%d %s\n",hits,r,t?"KA":"AZ",m,L,w,ph,pt);} 
     }}
  }
  printf("tests=%ld\n",tests);
  for(int r=0;r<4;r++){ printf("rule%d best=%d  tail:",r,best[r]); for(int h=8;h<=24;h++) if(hist[r][h])printf(" %d:%d",h,hist[r][h]); printf("\n"); }
}
