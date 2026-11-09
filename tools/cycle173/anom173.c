/* Cycle 173 (IDEAS I-105): the one-letter anomaly behind K3-law decimations.
   Derived from cycle 24's tools/c/anomaly_periodic.c (case 23), same models and conventions:
     del : one letter of the true ciphertext C' (index d = 0..97) was left off the copper -> n = 98
     ins : one extra letter was carved at carved index d (0..96)                          -> n = 96
     chg : one carved letter changed, visible only under a crib -> crib d (0..23) dropped    -> n = 97
     swp : carved letters d and d+1 swapped (d = 0..95)                                     -> n = 97
     none: baseline (reproduces case 57)                                                    -> n = 97
   perm[j] = index in C' paired with plaintext position j. Cribs at plaintext positions 21-33, 63-73 (0-indexed).
   Tableaux (PA,CA) in {AZ,KA}^2; vig (k = C - P, same test as variant Beaufort) and beau (k = C + P);
   ix pt: key at plaintext index (substitute, then transpose); ix ct: key at C' index (transpose, then substitute).
   Exact: the used crib key values must agree inside every residue class mod p, p = 1..PMAX (pairwise bad-period masks).
   Also prints, per p, the analytic chance expectation sum over configs of 26^-(used - classes) (I-097 known-answer check)
   and the number of distinct perms with any hit (I-101 cluster-aware).
   Build: gcc -O3 -march=native -fopenmp anom173.c -o anom173
   Run:   ./anom173 perms.bin n model CT PMAX PPRINT lo hi                                                  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PT="EASTNORTHEASTBERLINCLOCK";
static const char *AL[2]={"ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"};
int main(int argc,char**argv){
  if(argc<9){fprintf(stderr,"usage\n");return 1;}
  const char*fn=argv[1]; int n=atoi(argv[2]); const char*model=argv[3]; const char*CT=argv[4];
  int PMAX=atoi(argv[5]), PPRINT=atoi(argv[6]); long lo=atol(argv[7]), hi=atol(argv[8]);
  if(strlen(CT)!=97){fprintf(stderr,"CT must be 97\n");return 1;}
  FILE*f=fopen(fn,"rb"); fseek(f,0,2); long nt=ftell(f)/(2*n); fseek(f,0,0);
  short*Pm=malloc(nt*2*n); if(fread(Pm,2*n,nt,f)!=(size_t)nt) return 1; fclose(f);
  if(hi>nt) hi=nt;
  int INV[2][26]; for(int a=0;a<2;a++) for(int j=0;j<26;j++) INV[a][AL[a][j]-65]=j;
  int md = !strcmp(model,"del")?0: !strcmp(model,"ins")?1: !strcmp(model,"chg")?2: !strcmp(model,"swp")?4:3;
  int nd = md==0?98: md==1?97: md==2?24: md==4?96:1;
  unsigned divm[256]; for(int df=0;df<256;df++){ divm[df]=0; for(int p=1;p<=PMAX;p++) if(df%p==0) divm[df]|=1u<<p; }
  unsigned full=0; for(int p=1;p<=PMAX;p++) full|=1u<<p;
  long long hist[40]={0}, dperm[40]={0}; double expc[40]={0}; long long tests=0;
  #pragma omp parallel
  { long long h[40]={0}, dp[40]={0}; double ex[40]={0}; long long tl=0;
    #pragma omp for schedule(dynamic,64)
    for(long t=lo;t<hi;t++){ const short*p=Pm+t*n; unsigned anyp=0;
      for(int d=0;d<nd;d++){
        int u[24],c[24],use[24],m=0;
        for(int i=0;i<24;i++){ int uu=p[CI[i]], cc; use[i]=1;
          if(md==0){ if(uu==d){use[i]=0; cc=-1;} else cc= uu<d?uu:uu-1; }
          else if(md==1){ cc = uu<d?uu:uu+1; }
          else if(md==4){ cc = uu==d?d+1: uu==d+1?d: uu; }
          else { cc=uu; if(md==2&&i==d) use[i]=0; }
          u[i]=uu; c[i]=cc; if(use[i]) m++; }
        int ui[24],nu=0; for(int i=0;i<24;i++) if(use[i]) ui[nu++]=i;
        int Pv[2][24],Cv[2][24];
        for(int a=0;a<2;a++) for(int q=0;q<nu;q++){int i=ui[q]; Pv[a][q]=INV[a][PT[i]-65]; Cv[a][q]=INV[a][CT[c[i]]-65];}
        for(int ix=0;ix<2;ix++){
          int id[24]; for(int q=0;q<nu;q++) id[q]= ix?u[ui[q]]:CI[ui[q]];
          unsigned pm[300]; int np=0; int pa_[300],pb_[300];
          for(int a=0;a<nu;a++) for(int b=a+1;b<nu;b++){ int df=id[a]-id[b]; if(df<0) df=-df; unsigned mk=divm[df]; if(mk){pm[np]=mk;pa_[np]=a;pb_[np]=b;np++;} }
          /* chance expectation per p: classes among used cribs */
          for(int per=1;per<=PMAX;per++){ unsigned char seen[40]={0}; int cls=0; for(int q=0;q<nu;q++){int r=id[q]%per; if(!seen[r]){seen[r]=1;cls++;}}
            ex[per]+=8.0*pow(26.0,-(double)(nu-cls)); }
          for(int pa=0;pa<2;pa++) for(int ca=0;ca<2;ca++) for(int mo=0;mo<2;mo++){
#ifdef SAME
            if(pa!=ca) continue;
#endif
            int kv[24]; for(int q=0;q<nu;q++) kv[q]= mo?(Cv[ca][q]+Pv[pa][q])%26:(Cv[ca][q]-Pv[pa][q]+26)%26;
            unsigned bad=0; for(int e=0;e<np;e++) if(kv[pa_[e]]!=kv[pb_[e]]) bad|=pm[e];
            tl+=PMAX; unsigned good=full&~bad; if(!good) continue;
            anyp|=good;
            for(int per=1;per<=PMAX;per++) if(good>>per&1){ h[per]++;
              if(per<=PPRINT){ int key[40]; for(int r=0;r<per;r++) key[r]=-1; for(int q=0;q<nu;q++) key[id[q]%per]=kv[q];
                char ks[41]; for(int r=0;r<per;r++) ks[r]=key[r]<0?'?':'A'+key[r]; ks[per]=0;
                #pragma omp critical
                printf("HIT t=%ld d=%d PA=%s CA=%s mode=%s idx=%s p=%d key=%s\n",t,d,pa?"KA":"AZ",ca?"KA":"AZ",mo?"beau":"vig",ix?"ct":"pt",per,ks); } }
          } } }
      for(int per=1;per<=PMAX;per++) if(anyp>>per&1) dp[per]++; }
    #pragma omp critical
    { for(int i=0;i<40;i++){hist[i]+=h[i]; dperm[i]+=dp[i]; expc[i]+=ex[i];} tests+=tl; }
  }
  printf("MODEL %s n=%d PERMS %ld..%ld SLOTS %d PMAX %d TESTS %lld\nHIST",model,n,lo,hi,nd,PMAX,tests);
  for(int i=1;i<=PMAX;i++) printf(" %d:%lld",i,hist[i]); printf("\nDPERM");
  for(int i=1;i<=PMAX;i++) printf(" %d:%lld",i,dperm[i]); printf("\nEXPECT");
  for(int i=1;i<=PMAX;i++) printf(" %d:%.4g",i,expc[i]); printf("\nEND\n"); return 0;}
