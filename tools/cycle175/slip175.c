/* Cycle 175 (IDEAS I-111): two slips behind K3-law decimations = one dropped/extra carved letter AND one wrong crib letter.
   Built on tools/cycle173/anom173.c (same conventions, case 23 / cycle 24):
     delx : one letter of the true ciphertext C' (index d = 0..97) left off the copper (n = 98) + any ONE used crib dropped
     insx : one extra letter carved at carved index d (0..96) (n = 96)                      + any ONE used crib dropped
   perm[j] = index in C' paired with plaintext position j. Cribs at plaintext positions 21-33, 63-73 (0-indexed).
   Tableaux (PA,CA) in {AZ,KA}^2; vig (k = C - P; = variant Beaufort test) and beau (k = C + P);
   ix pt: key at plaintext index; ix ct: key at C' index.  Periodic key, p = 1..PMAX, exact on the 23 (or 22) remaining crib letters.
   Method: for every (perm, d, ix, tableau, mode) the bad crib pairs (equal residue mod p, different key value) are found once;
   per p, cand[p] = intersection over bad pairs of {a, b}.  Dropping crib i makes the config consistent at p iff i is in cand[p]
   (no bad pair at all: every drop is consistent).  A configuration = (perm, d, dropped crib, ix, PA, CA, mode, p).
   Information filter (I-115): checks(config) = (#used cribs after the drop) - (#residue classes they occupy).  Configs with
   checks >= KMIN are counted separately (HISTK) and are the only ones scored on the grid.
   Prints per p: all consistent configs (HIST), filtered (HISTK), distinct perms with any hit (DPERM), analytic chance expectation
   sum 26^-checks over all configs (EXPECT) and over the filtered ones (EXPECTK).
   Build: gcc -O3 -march=native -fopenmp slip175.c -o slip175 -lm
   Run:   ./slip175 perms.bin n model CT PMAX PPRINT KMIN lo hi                                                       */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PT="EASTNORTHEASTBERLINCLOCK";
static const char *AL[2]={"ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"};
int main(int argc,char**argv){
  if(argc<10){fprintf(stderr,"usage: slip175 perms.bin n delx|insx CT PMAX PPRINT KMIN lo hi\n");return 1;}
  const char*fn=argv[1]; int n=atoi(argv[2]); const char*model=argv[3]; const char*CT=argv[4];
  int PMAX=atoi(argv[5]), PPRINT=atoi(argv[6]), KMIN=atoi(argv[7]); long lo=atol(argv[8]), hi=atol(argv[9]);
  if(strlen(CT)!=97){fprintf(stderr,"CT must be 97\n");return 1;}
  if(PMAX>30){fprintf(stderr,"PMAX<=30\n");return 1;}
  int md = !strcmp(model,"delx")?0: !strcmp(model,"insx")?1: -1; if(md<0){fprintf(stderr,"model\n");return 1;}
  if((md==0&&n!=98)||(md==1&&n!=96)){fprintf(stderr,"n mismatch\n");return 1;}
  FILE*f=fopen(fn,"rb"); if(!f){perror(fn);return 1;} fseek(f,0,2); long nt=ftell(f)/(2*n); fseek(f,0,0);
  short*Pm=malloc(nt*2*n); if(fread(Pm,2*n,nt,f)!=(size_t)nt) return 1; fclose(f);
  if(hi>nt) hi=nt;
  int INV[2][26]; for(int a=0;a<2;a++) for(int j=0;j<26;j++) INV[a][AL[a][j]-65]=j;
  int nd = md==0?98:97;
  unsigned divm[256]; for(int df=0;df<256;df++){ divm[df]=0; for(int p=1;p<=PMAX;p++) if(df%p==0) divm[df]|=1u<<p; }
  double P26[40]; for(int i=0;i<40;i++) P26[i]=pow(26.0,-(double)i);
  long long hist[32]={0}, histk[32]={0}, dperm[32]={0}; double expc[32]={0}, expk[32]={0}; long long tests=0;
  #pragma omp parallel
  { long long h[32]={0}, hk[32]={0}, dp[32]={0}; double ex[32]={0}, exk[32]={0}; long long tl=0;
    #pragma omp for schedule(dynamic,64)
    for(long t=lo;t<hi;t++){ const short*p=Pm+t*n; unsigned anyp=0;
      for(int d=0;d<nd;d++){
        int u[24],c[24],ui[24],nu=0;
        for(int i=0;i<24;i++){ int uu=p[CI[i]], cc, use=1;
          if(md==0){ if(uu==d){use=0; cc=-1;} else cc= uu<d?uu:uu-1; }
          else { cc = uu<d?uu:uu+1; }
          u[i]=uu; c[i]=cc; if(use) ui[nu++]=i; }
        int Pv[2][24],Cv[2][24];
        for(int a=0;a<2;a++) for(int q=0;q<nu;q++){int i=ui[q]; Pv[a][q]=INV[a][PT[i]-65]; Cv[a][q]=INV[a][CT[c[i]]-65];}
        unsigned allq=(nu==32)?0xffffffffu:((1u<<nu)-1);
        for(int ix=0;ix<2;ix++){
          int id[24]; for(int q=0;q<nu;q++) id[q]= ix?u[ui[q]]:CI[ui[q]];
          unsigned pm[300]; unsigned ab[300]; int np=0; int pa_[300],pb_[300];
          for(int a=0;a<nu;a++) for(int b=a+1;b<nu;b++){ int df=id[a]-id[b]; if(df<0) df=-df; unsigned mk=divm[df]; if(mk){pm[np]=mk;pa_[np]=a;pb_[np]=b;ab[np]=(1u<<a)|(1u<<b);np++;} }
          /* per p: which drops pass the information filter; expectation */
          unsigned okk[32];
          for(int per=1;per<=PMAX;per++){ unsigned char cnt[32]={0}; int cls=0;
            for(int q=0;q<nu;q++){int r=id[q]%per; if(!cnt[r]) cls++; cnt[r]++;}
            unsigned m=0;
            for(int q=0;q<nu;q++){ int cl= cls - (cnt[id[q]%per]==1); int chk=(nu-1)-cl;
              ex[per]+=8.0*P26[chk]; if(chk>=KMIN){ m|=1u<<q; exk[per]+=8.0*P26[chk]; } }
            okk[per]=m; }
          for(int pa=0;pa<2;pa++) for(int ca=0;ca<2;ca++) for(int mo=0;mo<2;mo++){
            int kv[24]; for(int q=0;q<nu;q++) kv[q]= mo?(Cv[ca][q]+Pv[pa][q])%26:(Cv[ca][q]-Pv[pa][q]+26)%26;
            unsigned cand[32]; for(int per=0;per<=PMAX;per++) cand[per]=allq;
            for(int e=0;e<np;e++) if(kv[pa_[e]]!=kv[pb_[e]]){ unsigned mk=pm[e]; while(mk){ int per=__builtin_ctz(mk); mk&=mk-1; cand[per]&=ab[e]; } }
            tl+=(long long)PMAX*nu;
            for(int per=1;per<=PMAX;per++){ unsigned cm=cand[per]; if(!cm) continue;
              anyp|=1u<<per; h[per]+=__builtin_popcount(cm); hk[per]+=__builtin_popcount(cm&okk[per]);
              if(per<=PPRINT){ unsigned w=cm; while(w){ int dq=__builtin_ctz(w); w&=w-1;
                  int key[32]; for(int r=0;r<per;r++) key[r]=-1; for(int q=0;q<nu;q++) if(q!=dq) key[id[q]%per]=kv[q];
                  char ks[33]; for(int r=0;r<per;r++) ks[r]=key[r]<0?'?':'A'+key[r]; ks[per]=0;
                  #pragma omp critical
                  printf("HIT t=%ld d=%d drop=%d PA=%s CA=%s mode=%s idx=%s p=%d info=%d key=%s\n",t,d,ui[dq],pa?"KA":"AZ",ca?"KA":"AZ",mo?"beau":"vig",ix?"ct":"pt",per,(okk[per]>>dq)&1,ks); } } }
          } } }
      for(int per=1;per<=PMAX;per++) if(anyp>>per&1) dp[per]++; }
    #pragma omp critical
    { for(int i=0;i<32;i++){hist[i]+=h[i]; histk[i]+=hk[i]; dperm[i]+=dp[i]; expc[i]+=ex[i]; expk[i]+=exk[i];} tests+=tl; }
  }
  printf("MODEL %s n=%d PERMS %ld..%ld SLOTS %d PMAX %d KMIN %d TESTS %lld\nHIST",model,n,lo,hi,nd,PMAX,KMIN,tests);
  for(int i=1;i<=PMAX;i++) printf(" %d:%lld",i,hist[i]); printf("\nHISTK");
  for(int i=1;i<=PMAX;i++) printf(" %d:%lld",i,histk[i]); printf("\nDPERM");
  for(int i=1;i<=PMAX;i++) printf(" %d:%lld",i,dperm[i]); printf("\nEXPECT");
  for(int i=1;i<=PMAX;i++) printf(" %d:%.4g",i,expc[i]); printf("\nEXPECTK");
  for(int i=1;i<=PMAX;i++) printf(" %d:%.4g",i,expk[i]); printf("\nEND\n"); return 0;}
