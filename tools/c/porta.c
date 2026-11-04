/* Cycle 32: Porta / generalized half-split reciprocal cipher behind themed transpositions.
   Model: plaintext letter j pairs with ciphertext letter ct[t[j]] (perm file already holds both directions).
   Alphabet A (any themed ordering) is split into halves H1=A[0..12], H2=A[13..25].
   Porta: each key value k in 0..12 is an involution swapping H1[i] <-> H2[(i+k)%13] (variant 0)
   or H1[i] <-> H2[(k-i)%13] (variant 1). Necessary: every crib pair crosses halves.
   Key index = j (substitute-then-transpose) or t[j] (transpose-then-substitute).
   Output: hits with a consistent periodic key of period <= MAXL.
   usage: porta perms.bin alpha.bin ct.txt MAXL */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char *CR1="EASTNORTHEAST", *CR2="BERLINCLOCK";
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"rb"); fseek(f,0,2); long np=ftell(f)/(2*N); rewind(f);
  short*P=malloc(np*N*2); fread(P,2,np*N,f); fclose(f);
  f=fopen(argv[2],"rb"); fseek(f,0,2); long na=ftell(f)/26; rewind(f);
  unsigned char*A=malloc(na*26); fread(A,1,na*26,f); fclose(f);
  char ct[200]; f=fopen(argv[3],"r"); fscanf(f,"%s",ct); fclose(f);
  int MAXL=atoi(argv[4]);
  int cj[24],cp[24],nc=0;
  for(int i=0;i<13;i++){cj[nc]=21+i;cp[nc++]=CR1[i]-'A';}
  for(int i=0;i<11;i++){cj[nc]=63+i;cp[nc++]=CR2[i]-'A';}
  long halfpass=0, hits[64]={0};
  int pos[26];
  for(long a=0;a<na;a++){
    for(int i=0;i<26;i++)pos[A[a*26+i]]=i;
    int pp[24]; for(int c=0;c<24;c++)pp[c]=pos[cp[c]];
    for(long p=0;p<np;p++){
      short*t=P+p*N; int cc[24],ok=1;
      for(int c=0;c<24;c++){int b=pos[ct[t[cj[c]]]-'A']; if((pp[c]<13)==(b<13)){ok=0;break;} cc[c]=b;}
      if(!ok)continue; halfpass++; printf("HALF a=%ld p=%ld\n",a,p);
      for(int var=0;var<2;var++){
        int k[24];
        for(int c=0;c<24;c++){int lo=pp[c]<13?pp[c]:cc[c], hi=(pp[c]<13?cc[c]:pp[c])-13;
          k[c]= var==0 ? ((hi-lo)%13+13)%13 : ((hi+lo)%13);}
        for(int mode=0;mode<2;mode++){
          int idx[24]; for(int c=0;c<24;c++)idx[c]= mode==0?cj[c]:t[cj[c]];
          for(int L=1;L<=MAXL;L++){
            int key[128]; for(int r=0;r<L;r++)key[r]=-1; int good=1;
            for(int c=0;c<24&&good;c++){int r=idx[c]%L; if(key[r]<0)key[r]=k[c]; else if(key[r]!=k[c])good=0;}
            if(good){hits[L]++;
              printf("HIT a=%ld p=%ld var=%d mode=%d L=%d key=",a,p,var,mode,L);
              for(int r=0;r<L;r++)printf("%d,",key[r]); printf("\n"); break;}
          }
        }
      }
    }
  }
  printf("SUMMARY perms=%ld alphas=%ld halfpass=%ld",np,na,halfpass);
  for(int L=1;L<=MAXL;L++)printf(" L%d=%ld",L,hits[L]); printf("\n");
}
