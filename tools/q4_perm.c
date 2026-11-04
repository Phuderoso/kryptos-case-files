/* Cycle 28: Quagmire IV (two DIFFERENT keyed alphabets, PA != CA, neither A-Z) with a periodic key of ANY
   letters, behind or in front of a transposition. Extends cycle 13's periodic_perm.c (which covered QI/QII/QIII).
   perm[j] = carved index paired with PT position j. Modes: vig (k=C-P; same test as variant Beaufort), beau (k=C+P).
   Key indexed by PT position (substitute then transpose) or carved position (transpose then substitute).
   Exact: the 24 crib key values must agree within each residue class mod p, p = 1..PMAX.
   Build: gcc -O3 -march=native -fopenmp q4_perm.c -o q4_perm ; Run: ./q4_perm alpha.bin perm.bin CT PMAX [maxperms] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PT="EASTNORTHEASTBERLINCLOCK";
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"rb"); fseek(f,0,2); long na=ftell(f)/26; fseek(f,0,0);
  unsigned char*A=malloc(na*26); if(fread(A,26,na,f)!=(size_t)na) return 1; fclose(f);
  f=fopen(argv[2],"rb"); fseek(f,0,2); long nt=ftell(f)/194; fseek(f,0,0);
  short*Pm=malloc(nt*194); if(fread(Pm,194,nt,f)!=(size_t)nt) return 1; fclose(f);
  const char*CT=argv[3]; int PMAX=atoi(argv[4]); if(argc>5){long m=atol(argv[5]); if(m<nt) nt=m;}
  unsigned char*INV=malloc(na*26);
  for(long a=0;a<na;a++) for(int j=0;j<26;j++) INV[a*26+A[a*26+j]]=j;
  int PV[300][24]; for(long a=0;a<na;a++) for(int i=0;i<24;i++) PV[a][i]=INV[a*26+PT[i]-65];
  long long hist[64]; memset(hist,0,sizeof hist); long long tested=0;
  #pragma omp parallel reduction(+:tested)
  { long long h[64]; memset(h,0,sizeof h);
    #pragma omp for schedule(dynamic,16)
    for(long t=0;t<nt;t++){ const short*p=Pm+t*97; int tc[24]; for(int i=0;i<24;i++) tc[i]=p[CI[i]];
      /* constraint pairs per (ix,period): consecutive members of each residue class */
      int np[2][64]; unsigned char pi[2][64][24], pj[2][64][24];
      for(int ix=0;ix<2;ix++) for(int per=1;per<=PMAX;per++){ int last[64]; memset(last,-1,sizeof last); int n=0;
        for(int i=0;i<24;i++){ int r=(ix?tc[i]:CI[i])%per; if(last[r]>=0){pi[ix][per][n]=last[r]; pj[ix][per][n]=i; n++;} last[r]=i; }
        np[ix][per]=n; }
      for(long b=1;b<na;b++){ int Cv[24]; for(int i=0;i<24;i++) Cv[i]=INV[b*26+CT[tc[i]]-65];
        for(long a=1;a<na;a++){ if(a==b) continue; const int*Pv=PV[a];
          for(int m=0;m<2;m++){ int kv[24]; for(int i=0;i<24;i++) kv[i]=m?(Cv[i]+Pv[i])%26:(Cv[i]-Pv[i]+26)%26;
            for(int ix=0;ix<2;ix++) for(int per=1;per<=PMAX;per++){ tested++; int n=np[ix][per], ok=1;
              for(int k=0;k<n;k++) if(kv[pi[ix][per][k]]!=kv[pj[ix][per][k]]){ok=0;break;}
              if(!ok) continue; h[per]++;
              int key[64]; memset(key,-1,sizeof key); for(int i=0;i<24;i++) key[(ix?tc[i]:CI[i])%per]=kv[i];
              #pragma omp critical
              { printf("HIT t=%ld PA=%ld CA=%ld %s idx=%s p=%d key=",t,a,b,m?"beau":"vig",ix?"carved":"pt",per);
                for(int r=0;r<per;r++) printf("%c",key[r]<0?'?':'A'+key[r]); printf("\n"); fflush(stdout);} } } } } }
    #pragma omp critical
    for(int i=0;i<64;i++) hist[i]+=h[i];
  }
  printf("TRANSPOSITIONS %ld ALPHABETS %ld PMAX %d TESTS %lld\nHIST",nt,na,PMAX,tested);
  for(int i=1;i<=PMAX;i++) printf(" %d:%lld",i,hist[i]); printf("\n"); return 0;}
