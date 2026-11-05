/* Cycle 106: Alberti cipher-disk screen (piecewise-constant shift, irregular disk turns).
   Model A: plaintext letter j is enciphered with disk setting s_j, then lands at ciphertext position t[j].
   Disk: outer ring O (plaintext order) and inner ring I (cipher order); C = I^-1[(O(p)+s) mod 26] (Vig)
   or reversed inner ring (Beau: s = I(c)+O(p)). Modes: 0 QIII Vig (O=I=A), 1 QIII Beau, 2 QI Vig (O=AZ,I=A),
   3 QI Beau, 4 QII Vig (O=A,I=AZ), 5 QII Beau.
   Statistic E = number of adjacent crib pairs (12 in EASTNORTHEAST, 10 in BERLINCLOCK) with equal setting
   = 22 - (disk turns inside the crib spans).
   usage: alberti CT perm.bin nperm alpha.bin nalpha thresh  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const char *CR1="EASTNORTHEAST", *CR2="BERLINCLOCK";
int main(int argc,char**argv){
  const char*ct=argv[1]; int np=atoi(argv[3]), na=atoi(argv[5]), th=atoi(argv[6]);
  FILE*f=fopen(argv[2],"rb"); short*P=malloc((size_t)np*97*2); if(fread(P,2,(size_t)np*97,f)!=(size_t)np*97){fprintf(stderr,"short perm\n");}
  fclose(f);
  f=fopen(argv[4],"rb"); unsigned char*A=malloc((size_t)na*26); if(fread(A,1,(size_t)na*26,f)!=(size_t)na*26)fprintf(stderr,"short alpha\n"); fclose(f);
  int cpos[24],pl[24]; for(int k=0;k<13;k++){cpos[k]=21+k;pl[k]=CR1[k]-65;} for(int k=0;k<11;k++){cpos[13+k]=63+k;pl[13+k]=CR2[k]-65;}
  int C[97]; for(int i=0;i<97;i++)C[i]=ct[i]-65;
  long hist[23]={0}; long nhit=0; int best=0;
  unsigned char (*pos)[26]=malloc((size_t)na*26);
  for(int a=0;a<na;a++)for(int k=0;k<26;k++)pos[a][A[a*26+k]]=k;
  for(int p=0;p<np;p++){
    short*t=P+(size_t)p*97; int cc[24]; for(int k=0;k<24;k++)cc[k]=C[t[cpos[k]]];
    for(int a=0;a<na;a++){ unsigned char*q=pos[a];
      for(int m=0;m<6;m++){ int s[24];
        for(int k=0;k<24;k++){ int c=cc[k],x=pl[k],v;
          switch(m){case 0:v=q[c]-q[x];break;case 1:v=q[c]+q[x];break;case 2:v=q[c]-x;break;case 3:v=q[c]+x;break;case 4:v=c-q[x];break;default:v=c+q[x];}
          s[k]=((v%26)+26)%26;}
        int E=0; for(int k=0;k<12;k++)E+=(s[k]==s[k+1]); for(int k=13;k<23;k++)E+=(s[k]==s[k+1]);
        hist[E]++; if(E>best)best=E;
        if(E>=th){nhit++; if(nhit<=200){printf("HIT E=%d perm=%d alpha=%d mode=%d s=",E,p,a,m); for(int k=0;k<24;k++)printf("%c",65+s[k]); printf("\n");}}
      }}
  }
  printf("best %d hits>=%d: %ld\nhist:",best,th,nhit); for(int e=0;e<=22;e++)if(hist[e])printf(" %d:%ld",e,hist[e]); printf("\n");
}
