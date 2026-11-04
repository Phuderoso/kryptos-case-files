/* Cycle 24: the one-letter anomaly model (K1-K3 each carry one planted single-letter error).
   True ciphertext C' (n letters) = periodic substitution + transposition of an n-letter plaintext;
   the carved K4 (97) differs from C' by ONE letter:
     model del : a letter of C' (index d, 0..97) was left off the copper    -> n = 98
     model ins : an extra letter was carved at carved index d (0..96)        -> n = 96
     model chg : one carved letter was changed (only visible if under a crib) -> n = 97, one crib dropped
     model swp : two adjacent carved letters swapped (carved d <-> d+1, d=0..95) -> n = 97
     model none: no anomaly (baseline)                                         -> n = 97
   perm[j] = index in C' paired with plaintext position j (family includes inverses, so both directions).
   Cribs at the official plaintext positions 21-33, 63-73 (0-indexed).
   Tableaux: (PA,CA) in {AZ,KA}^2 ; modes vig (k=C-P, same test as variant Beaufort) and beau (k=C+P);
   key indexed by plaintext position (substitute then transpose) or by C' index (transpose then substitute).
   Exact test: the 24 (or 23) crib key values must agree within each residue class mod p, p=1..PMAX.
   Build: gcc -O3 -fopenmp anomaly_periodic.c -o anomaly_periodic
   Run:   ./anomaly_periodic perms.bin n model CT PMAX PPRINT                                              */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PT="EASTNORTHEASTBERLINCLOCK";
static const char *AL[2]={"ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"};
int main(int argc,char**argv){
  const char*fn=argv[1]; int n=atoi(argv[2]); const char*model=argv[3]; const char*CT=argv[4];
  int PMAX=atoi(argv[5]), PPRINT=atoi(argv[6]);
  FILE*f=fopen(fn,"rb"); fseek(f,0,2); long nt=ftell(f)/(2*n); fseek(f,0,0);
  short*Pm=malloc(nt*2*n); if(fread(Pm,2*n,nt,f)!=(size_t)nt) return 1; fclose(f);
  int INV[2][26]; for(int a=0;a<2;a++) for(int j=0;j<26;j++) INV[a][AL[a][j]-65]=j;
  int md = !strcmp(model,"del")?0: !strcmp(model,"ins")?1: !strcmp(model,"chg")?2: !strcmp(model,"swp")?4:3;
  int nd = md==0?98: md==1?97: md==2?24: md==4?96:1;
  long long hist[100]; memset(hist,0,sizeof hist); long long tests=0;
  #pragma omp parallel
  { long long h[100]; memset(h,0,sizeof h); long long tl=0;
    #pragma omp for schedule(dynamic,16)
    for(long t=0;t<nt;t++){ const short*p=Pm+t*n;
      for(int d=0;d<nd;d++){
        int u[24],c[24],use[24],m=0;
        for(int i=0;i<24;i++){ int uu=p[CI[i]], cc; use[i]=1;
          if(md==0){ if(uu==d) {use[i]=0; cc=-1;} else cc= uu<d?uu:uu-1; }
          else if(md==1){ cc = uu<d?uu:uu+1; }
          else if(md==4){ cc = uu==d?d+1: uu==d+1?d: uu; }
          else { cc=uu; if(md==2&&i==d) use[i]=0; }
          u[i]=uu; c[i]=cc; if(use[i]) m++; }
        for(int pa=0;pa<2;pa++) for(int ca=0;ca<2;ca++){
          int Pv[24],Cv[24]; for(int i=0;i<24;i++){Pv[i]=INV[pa][PT[i]-65]; Cv[i]=use[i]?INV[ca][CT[c[i]]-65]:0;}
          for(int mo=0;mo<2;mo++){ int kv[24]; for(int i=0;i<24;i++) kv[i]=mo?(Cv[i]+Pv[i])%26:(Cv[i]-Pv[i]+26)%26;
            for(int ix=0;ix<2;ix++) for(int per=1;per<=PMAX;per++){ int key[100]; memset(key,-1,sizeof(int)*per); int ok=1; tl++;
              for(int i=0;i<24&&ok;i++){ if(!use[i]) continue; int r=(ix?u[i]:CI[i])%per; if(key[r]<0) key[r]=kv[i]; else if(key[r]!=kv[i]) ok=0;}
              if(!ok) continue; h[per]++;
              if(per<=PPRINT){
              #pragma omp critical
              { printf("HIT t=%ld d=%d PA=%s CA=%s mode=%s idx=%s p=%d key=",t,d,pa?"KA":"AZ",ca?"KA":"AZ",mo?"beau":"vig",ix?"ct":"pt",per);
                for(int r=0;r<per;r++) printf("%c",key[r]<0?'?':AL[ca][0]=='A'?'A'+key[r]:'A'+key[r]); printf("\n"); } } } } } } }
    #pragma omp critical
    { for(int i=0;i<100;i++) hist[i]+=h[i]; tests+=tl; }
  }
  printf("MODEL %s n=%d TRANSPOSITIONS %ld ANOMALY_SLOTS %d PMAX %d TESTS %lld\nHIST",model,n,nt,nd,PMAX,tests);
  for(int i=1;i<=PMAX;i++) printf(" %d:%lld",i,hist[i]); printf("\n"); return 0;}
