/* Cycle 13 (fixed cycle 57: perm entries of -1 = omitted letter are now skipped; before, CT[-1] was read): transposition undone, then a PERIODIC key of any letters (generic, not a word list).
   For each transposition t (perm[j] = carved index paired with PT position j; only crib positions used),
   alphabet pair (PA,CA) in {(a,a) Quagmire III, (AZ,a) Quagmire II, (a,AZ) Quagmire I} over the first M alphabets,
   mode vig (k = C-P, also covers variant Beaufort) or beau (k = C+P), key index by PT position j (substitute,
   then transpose) or by carved position t(j) (transpose, then substitute), and period p = 1..PMAX:
   the 24 crib key values must agree within each residue class. Prints every survivor; histogram per period.
   Build: gcc -O3 -fopenmp periodic_perm.c -o periodic_perm ; Run: ./periodic_perm alpha.bin perm.bin CT M PMAX */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PT="EASTNORTHEASTBERLINCLOCK";
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"rb"); fseek(f,0,2); long na=ftell(f)/26; fseek(f,0,0);
  unsigned char*A=malloc(na*26); fread(A,26,na,f); fclose(f);
  f=fopen(argv[2],"rb"); fseek(f,0,2); long nt=ftell(f)/194; fseek(f,0,0);
  short*Pm=malloc(nt*194); fread(Pm,194,nt,f); fclose(f);
  const char*CT=argv[3]; long M=atol(argv[4]); int PMAX=atoi(argv[5]);
  unsigned char*INV=malloc(na*26);
  for(long a=0;a<na;a++) for(int j=0;j<26;j++) INV[a*26+A[a*26+j]]=j;
  long long hist[64]; memset(hist,0,sizeof hist);
  #pragma omp parallel
  { long long h[64]; memset(h,0,sizeof h);
    #pragma omp for schedule(dynamic,64)
    for(long t=0;t<nt;t++){ const short*p=Pm+t*97; int tc[24]; for(int i=0;i<24;i++) tc[i]=p[CI[i]];
      for(long a=0;a<M;a++) for(int pr=0;pr<3;pr++){
        const unsigned char*ip=INV+(pr==1?0:a)*26, *ic=INV+(pr==2?0:a)*26;   /* alphabet 0 = AZ */
        if(pr&&a==0) continue;
        int Pv[24],Cv[24]; for(int i=0;i<24;i++){Pv[i]=ip[PT[i]-65]; Cv[i]= tc[i]<0? 0 : ic[CT[tc[i]]-65];}
        for(int m=0;m<2;m++){ int kv[24]; for(int i=0;i<24;i++) kv[i]=m?(Cv[i]+Pv[i])%26:(Cv[i]-Pv[i]+26)%26;
          for(int ix=0;ix<2;ix++) for(int per=1;per<=PMAX;per++){ int key[64]; memset(key,-1,sizeof key); int ok=1;
            for(int i=0;i<24&&ok;i++){ if(tc[i]<0) continue; int r=(ix?tc[i]:CI[i])%per; if(key[r]<0) key[r]=kv[i]; else if(key[r]!=kv[i]) ok=0;}
            if(!ok) continue; h[per]++;
            #pragma omp critical
            { printf("HIT t=%ld a=%ld pair=%s %s idx=%s p=%d key=",t,a,pr==0?"QIII":pr==1?"QII(AZ,a)":"QI(a,AZ)",
                m?"beau":"vig",ix?"carved":"pt",per);
              for(int r=0;r<per;r++) printf("%c",key[r]<0?'?':'A'+key[r]); printf("\n"); } } } } }
    #pragma omp critical
    for(int i=0;i<64;i++) hist[i]+=h[i];
  }
  printf("TRANSPOSITIONS %ld ALPHABETS_USED %ld PMAX %d\nHIST",nt,M,PMAX);
  for(int i=1;i<=PMAX;i++) printf(" %d:%lld",i,hist[i]); printf("\n"); return 0;}
