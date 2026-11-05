/* Cycle 94: Chaocipher with ONE wheel enumerated and the OTHER wheel ARBITRARY.
   Lemma: both wheels move by position permutations that depend only on the index k_i where the input letter sat.
   So the input-side wheel + the carved text fix k_i and the output stream u_i (an index into the arbitrary output
   wheel's starting order); plaintext = mono-substitution of u. Rotations of the input wheel are irrelevant.
   Crib test: u at the 24 crib positions must map consistently and injectively to EASTNORTHEAST/BERLINCLOCK.
   dir 0: carved = Chao-encrypt(pt) (input wheel = left). dir 1: carved = Chao-decrypt(pt) (input wheel = right).
   Usage: ./chaoarb CT alphabets.bin [random N seed]  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PT="EASTNORTHEASTBERLINCLOCK";
static void opL(unsigned char*w,int i){unsigned char t[26];for(int k=0;k<26;k++)t[k]=w[(i+k)%26];unsigned char x=t[1];memmove(t+1,t+2,12);t[13]=x;memcpy(w,t,26);}
static void opR(unsigned char*w,int i){unsigned char t[26];for(int k=0;k<26;k++)t[k]=w[(i+1+k)%26];unsigned char x=t[2];memmove(t+2,t+3,11);t[13]=x;memcpy(w,t,26);}
/* returns score: satisfied equal-pairs (max 13) and conflicts; fills u[0..n) */
static void stream(const char*CT,int n,const unsigned char*A,int dir,unsigned char*u){
  unsigned char in[26],out[26]; memcpy(in,A,26); for(int k=0;k<26;k++) out[k]=k;
  for(int j=0;j<n;j++){ int x=CT[j]-65,i=0; while(in[i]!=x) i++; u[j]=out[i];
    if(dir==0){opL(in,i);opR(out,i);} else {opR(in,i);opL(out,i);} } }
static void score(const unsigned char*u,int*sat,int*conf){ *sat=0;*conf=0;
  for(int a=0;a<24;a++)for(int b=a+1;b<24;b++){ int same=PT[a]==PT[b], eq=u[CI[a]]==u[CI[b]];
    if(same&&eq)(*sat)++; if(same!=eq)(*conf)++; } }
int main(int argc,char**argv){ const char*CT=argv[1]; int n=strlen(CT);
  long na; unsigned char*A; long R=0; unsigned long long seed=1;
  if(argc>3&&!strcmp(argv[3],"random")){ R=atol(argv[4]); seed=strtoull(argv[5],0,10); na=R; A=0; }
  else { FILE*f=fopen(argv[2],"rb"); fseek(f,0,2); na=ftell(f)/26; fseek(f,0,0); A=malloc(na*26); fread(A,26,na,f); fclose(f); }
  long long hist[2][80]={{0}}; long hits=0; int best[2]={999,999};
  #pragma omp parallel for schedule(dynamic,1024) reduction(+:hits)
  for(long a=0;a<na;a++){ unsigned char al[26];
    if(R){ unsigned long long s=seed*0x9E3779B97F4A7C15ULL+a*0xBF58476D1CE4E5B9ULL; for(int k=0;k<26;k++)al[k]=k;
      for(int k=25;k>0;k--){ s^=s>>31; s*=0x94D049BB133111EBULL; s^=s>>29; int r=s%(k+1); unsigned char t=al[k];al[k]=al[r];al[r]=t; } }
    else memcpy(al,A+a*26,26);
    for(int d=0;d<2;d++){ unsigned char u[97]; stream(CT,n,al,d,u); int s,c; score(u,&s,&c);
      #pragma omp atomic
      hist[d][c]++;
      if(c==0){ hits++;
        #pragma omp critical
        { printf("HIT a=%ld dir=%d alpha=",a,d); for(int k=0;k<26;k++)putchar(65+al[k]); printf(" u="); for(int j=0;j<n;j++)printf("%c",u[j]<26?'a'+u[j]:'?'); printf("\n"); } } } }
  for(int d=0;d<2;d++){ printf("dir%d conflicts-hist:",d); for(int c=0;c<80;c++) if(hist[d][c]) printf(" %d:%lld",c,hist[d][c]); printf("\n"); }
  printf("ALPHABETS %ld HITS %ld\n",na,hits); return 0; }
