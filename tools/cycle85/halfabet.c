/* Cycle 85: HALFABET behind themed transpositions (new family).
   Alphabet A (any ordering) is split into two 13-letter halves, either
   split 0: H1=A[0..12], H2=A[13..25]  or  split 1: H1=even positions, H2=odd positions.
   Each key value k in 0..12 maps a letter at half-index i to the SAME half:
   var 0 (additive):   c = H[(i+k)%13]      var 1 (reflective): c = H[(k-i)%13]
   Necessary, key-free: every crib pair (P,C) lies in the same half.
   Model (as cycle 32): plaintext letter j pairs with ciphertext letter ct[t[j]].
   Key index = j (mode 0, substitute-then-transpose) or t[j] (mode 1, transpose-then-substitute).
   Prints hits with a consistent periodic key of period <= MAXL.
   usage: halfabet perms.bin alpha.bin ct.txt MAXL [a0 a1]  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char *CR1="EASTNORTHEAST", *CR2="BERLINCLOCK";
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"rb"); fseek(f,0,2); long np=ftell(f)/(2*N); rewind(f);
  short*P=malloc(np*N*2); if(fread(P,2,np*N,f)){} fclose(f);
  f=fopen(argv[2],"rb"); fseek(f,0,2); long na=ftell(f)/26; rewind(f);
  unsigned char*A=malloc(na*26); if(fread(A,1,na*26,f)){} fclose(f);
  char ct[200]; f=fopen(argv[3],"r"); if(fscanf(f,"%s",ct)){} fclose(f);
  int MAXL=atoi(argv[4]);
  long a0=0,a1=na; if(argc>6){a0=atol(argv[5]);a1=atol(argv[6]); if(a1>na)a1=na;}
  int cj[24],cp[24],nc=0;
  for(int i=0;i<13;i++){cj[nc]=21+i;cp[nc++]=CR1[i]-'A';}
  for(int i=0;i<11;i++){cj[nc]=63+i;cp[nc++]=CR2[i]-'A';}
  long halfpass[2]={0,0}, hits[64]={0};
  int pos[26], hf[26], hi_[26];
  for(long a=a0;a<a1;a++){
    for(int i=0;i<26;i++)pos[A[a*26+i]]=i;
    for(int sp=0;sp<2;sp++){
      for(int x=0;x<26;x++){int q=pos[x]; if(sp==0){hf[x]=q>=13; hi_[x]=q%13;} else {hf[x]=q&1; hi_[x]=q>>1;}}
      for(long p=0;p<np;p++){
        short*t=P+p*N; int ok=1;
        for(int c=0;c<24;c++){int cl=ct[t[cj[c]]]-'A'; if(hf[cp[c]]!=hf[cl]){ok=0;break;}}
        if(!ok)continue; halfpass[sp]++;
        for(int var=0;var<2;var++){
          int k[24];
          for(int c=0;c<24;c++){int i=hi_[cp[c]], o=hi_[ct[t[cj[c]]]-'A'];
            k[c]= var==0 ? ((o-i)%13+13)%13 : (o+i)%13;}
          for(int mode=0;mode<2;mode++){
            int idx[24]; for(int c=0;c<24;c++)idx[c]= mode==0?cj[c]:t[cj[c]];
            for(int L=1;L<=MAXL;L++){
              int key[128]; for(int r=0;r<L;r++)key[r]=-1; int good=1;
              for(int c=0;c<24&&good;c++){int r=idx[c]%L; if(key[r]<0)key[r]=k[c]; else if(key[r]!=k[c])good=0;}
              if(good){hits[L]++;
                printf("HIT a=%ld p=%ld sp=%d var=%d mode=%d L=%d key=",a,p,sp,var,mode,L);
                for(int r=0;r<L;r++)printf("%d,",key[r]); printf("\n"); break;}
            }
          }
        }
      }
    }
  }
  printf("SUMMARY perms=%ld alphas=%ld..%ld halfpass_split0=%ld halfpass_split1=%ld",np,a0,a1,halfpass[0],halfpass[1]);
  for(int L=1;L<=MAXL;L++)printf(" L%d=%ld",L,hits[L]); printf("\n");
}
