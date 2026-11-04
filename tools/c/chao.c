/* Cycle 14: Chaocipher (Byrne 1918; algorithm per Rubin 2010) as K4's layer, with and without a transposition.
   State: left (cipher) and right (plain) alphabets. Start = two themed keyword alphabets + relative offset 0..25.
   dir 0: carved = Chao-ENCRYPT(text) -> we DECRYPT carved. dir 1: carved = Chao-DECRYPT(text) -> we ENCRYPT carved.
   Modes:
     plain  : no transposition. Prints histogram of crib matches (0..24) and every run with >= THR matches.
     tb     : transpose then Chao  (decrypt carved once, then for every perm check T[perm[j]] at the 24 cribs)
     ta     : Chao then transpose  (intermediate I[j]=CT[perm[j]], decrypt sequentially, exit on first crib miss)
   Usage: ./chao test | ./chao plain alpha.bin CT M THR | ./chao tb alpha.bin perm.bin CT M | ./chao ta alpha.bin perm.bin CT M
   Alphabet file: n*26 bytes, values 0..25 (letter at position). perm file: n*97 int16, perm[j] = carved index for PT pos j. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PT="EASTNORTHEASTBERLINCLOCK";
static int CRIB[97];
typedef struct { unsigned char L[26],R[26]; } St;
static inline int idx(const unsigned char*a,int x){ for(int i=0;i<26;i++) if(a[i]==x) return i; return -1; }
static inline void permute(St*s,int i){ unsigned char t[26];
  /* left: rotate so position i at zenith; take letter at zenith+1 out, insert at nadir (13) */
  for(int k=0;k<26;k++) t[k]=s->L[(i+k)%26];
  { unsigned char x=t[1]; memmove(t+1,t+2,12); t[13]=x; } memcpy(s->L,t,26);
  /* right: rotate so position i at zenith, then one more (zenith = i+1); take letter at zenith+2, insert at nadir */
  for(int k=0;k<26;k++) t[k]=s->R[(i+1+k)%26];
  { unsigned char x=t[2]; memmove(t+2,t+3,11); t[13]=x; } memcpy(s->R,t,26); }
/* one step: input letter x; dir 0 = decrypt (x is cipher, look in L, output R), dir 1 = encrypt (x plain in R, out L) */
static inline int step(St*s,int x,int dir){ int i,o; if(dir==0){ i=idx(s->L,x); o=s->R[i]; } else { i=idx(s->R,x); o=s->L[i]; }
  permute(s,i); return o; }
static void init(St*s,const unsigned char*a,const unsigned char*b,int off){ for(int k=0;k<26;k++){ s->L[k]=a[(k+off)%26]; s->R[k]=b[k]; } }
static unsigned char*loadA(const char*fn,long*n){ FILE*f=fopen(fn,"rb"); fseek(f,0,2); *n=ftell(f)/26; fseek(f,0,0);
  unsigned char*A=malloc(*n*26); fread(A,26,*n,f); fclose(f); return A; }
static short*loadP(const char*fn,long*n){ FILE*f=fopen(fn,"rb"); fseek(f,0,2); *n=ftell(f)/194; fseek(f,0,0);
  short*P=malloc(*n*194); fread(P,194,*n,f); fclose(f); return P; }
int main(int argc,char**argv){
  for(int i=0;i<97;i++) CRIB[i]=-1; for(int i=0;i<24;i++) CRIB[CI[i]]=PT[i]-65;
  if(!strcmp(argv[1],"test")){ /* Rubin's published example */
    const char*L0="HXUCZVAMDSLKPEFJRIGTWOBNYQ",*R0="PTLNBQDEOYSFAVZKGJRIHWXUMC",*P="WELLDONEISBETTERTHANWELLSAID";
    unsigned char a[26],b[26]; for(int k=0;k<26;k++){a[k]=L0[k]-65;b[k]=R0[k]-65;}
    St s; init(&s,a,b,0); char out[64]; int n=strlen(P); for(int k=0;k<n;k++) out[k]=65+step(&s,P[k]-65,1); out[n]=0;
    printf("enc %s (expect OAHQHCNYNXTSZJRRHJBYHQKSOUJY)\n",out);
    init(&s,a,b,0); for(int k=0;k<n;k++) out[k]=65+step(&s,out[k]-65,0); printf("dec %s\n",out); return 0; }
  long na; unsigned char*A=loadA(argv[2],&na);
  if(!strcmp(argv[1],"plain")){ const char*CT=argv[3]; long M=atol(argv[4]); int THR=atoi(argv[5]);
    long long h[25]={0};
    #pragma omp parallel for schedule(dynamic) reduction(+:h[:25])
    for(long a=0;a<M;a++) for(long b=0;b<M;b++) for(int off=0;off<26;off++) for(int d=0;d<2;d++){
      St s; init(&s,A+a*26,A+b*26,off); char out[98]; int m=0;
      for(int j=0;j<97;j++){ int o=step(&s,CT[j]-65,d); out[j]=65+o; if(CRIB[j]==o) m++; } out[97]=0; h[m]++;
      if(m>=THR){
        #pragma omp critical
        printf("HIT m=%d a=%ld b=%ld off=%d dir=%d %s\n",m,a,b,off,d,out); } }
    printf("RUNS %lld HIST",(long long)M*M*52); for(int i=0;i<25;i++) if(h[i]) printf(" %d:%lld",i,h[i]); printf("\n"); return 0; }
  long nt; short*Pm=loadP(argv[3],&nt); const char*CT=argv[4]; long M=atol(argv[5]);
  long long first=0, full=0;
  if(!strcmp(argv[1],"tb")){
    #pragma omp parallel for schedule(dynamic) reduction(+:first,full)
    for(long a=0;a<M;a++) for(long b=0;b<M;b++) for(int off=0;off<26;off++) for(int d=0;d<2;d++){
      St s; init(&s,A+a*26,A+b*26,off); unsigned char T[97]; for(int j=0;j<97;j++) T[j]=step(&s,CT[j]-65,d);
      for(long t=0;t<nt;t++){ const short*p=Pm+t*97; int i=0; while(i<24 && T[p[CI[i]]]==PT[i]-65) i++;
        if(i>=13) first++; if(i==24){ full++;
          #pragma omp critical
          { printf("FULL tb t=%ld a=%ld b=%ld off=%d dir=%d PT=",t,a,b,off,d); for(int j=0;j<97;j++) putchar(65+T[p[j]]); putchar('\n'); } } } }
  } else { /* ta */
    #pragma omp parallel for schedule(dynamic,256) reduction(+:first,full)
    for(long t=0;t<nt;t++){ const short*p=Pm+t*97; unsigned char I[97]; for(int j=0;j<97;j++) I[j]=CT[p[j]]-65;
      for(long a=0;a<M;a++) for(long b=0;b<M;b++) for(int off=0;off<26;off++) for(int d=0;d<2;d++){
        St s; init(&s,A+a*26,A+b*26,off); int ok=1, j; unsigned char o[97];
        for(j=0;j<74&&ok;j++){ o[j]=step(&s,I[j],d); if(CRIB[j]>=0 && CRIB[j]!=o[j]) ok=0; }
        if(j>=34 && (ok||j>34)) first++;
        if(ok){ full++; for(;j<97;j++) o[j]=step(&s,I[j],d);
          #pragma omp critical
          { printf("FULL ta t=%ld a=%ld b=%ld off=%d dir=%d PT=",t,a,b,off,d); for(int k=0;k<97;k++) putchar(65+o[k]); putchar('\n'); } } } }
  }
  printf("MODE %s TRANSPOSITIONS %ld ALPHABETS %ld RUNS %lld PASS_FIRST_CRIB %lld FULL %lld\n",argv[1],nt,M,(long long)nt*M*M*52,first,full);
  return 0; }
