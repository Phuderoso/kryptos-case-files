/* Cycle 210 (I-270 + I-276): word-restart key R1 with a Quagmire tableau built from two keyword alphabets (K1/K2 construction),
   behind a transposition family (model Q: R1 in plaintext order, then transposition; layer letter i = C[S[i]]).
   Generalises cycle 206's wrbank.c: tableau-form = (plain alphabet X, cipher alphabet Y, form) with
     Vigenere-form  c = Y[x(p) + k]  ->  k = y(c) - x(p)   (variant Beaufort is the dual: same consistency, counted once)
     Beaufort-form  c = Y[k - x(p)]  ->  k = y(c) + x(p)
   X = Y = AZ / KA reproduces wrbank tm 0..3 exactly (gate G0').
   usage: wrq CT perms.bin|x LMIN LMAX alphabets.txt pairs.txt stride offset [maxprint]
     alphabets.txt: one 26-letter alphabet per line (name after a space); pairs.txt: lines "ix iy" (0-based indices into alphabets)
     stride/offset: use rows q with q % stride == offset (sampling); both directions always.
   output: 'S' survivor lines, 'H L count' (all pair-forms), 'P pairidx form L count' per pair, 'T' totals. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char *C1="EASTNORTHEAST", *C2="BERLINCLOCK";
static const int P1=21, P2=63;
static const int SE[4][3]={{0},{1,4},{1,9},{2,4,9}};
static const char *SEN[4]={"EASTNORTHEAST","EAST|NORTHEAST","EASTNORTH|EAST","EAST|NORTH|EAST"};
static const int SB[2][2]={{0},{1,6}};
static const char *SBN[2]={"BERLINCLOCK","BERLIN|CLOCK"};
static int cls1[27][4][26][13], cls2[27][2][26][11];
static int cidx(const int *b,int nb,int j,int o,int L){int pb=-1;for(int k=0;k<nb;k++)if(b[k]<=j)pb=b[k];return ((pb>=0)?(j-pb):(o+j))%L;}
static char AL[400][27]; static int INV[400][26]; static int PX[20000],PY[20000];
int main(int argc,char**argv){
  if(argc<9){fprintf(stderr,"usage\n");return 1;}
  int C[N]; for(int i=0;i<N;i++)C[i]=argv[1][i]-'A';
  int LMIN=atoi(argv[3]),LMAX=atoi(argv[4]); int stride=atoi(argv[7]),off=atoi(argv[8]); long maxprint=argc>9?atol(argv[9]):100;
  FILE*fa=fopen(argv[5],"r"); int na=0; char line[256];
  while(fgets(line,sizeof line,fa)){ if(strlen(line)<26)continue; memcpy(AL[na],line,26); AL[na][26]=0;
    int seen=0; for(int i=0;i<26;i++){int v=AL[na][i]-'A'; if(v<0||v>25||(seen>>v&1)){fprintf(stderr,"bad alphabet %d\n",na);return 1;} seen|=1<<v; INV[na][v]=i;} na++; }
  fclose(fa);
  FILE*fp=fopen(argv[6],"r"); int npair=0; while(fscanf(fp,"%d %d",&PX[npair],&PY[npair])==2)npair++; fclose(fp);
  int direct=!strcmp(argv[2],"x"); long np=1; short*Perm=NULL;
  if(!direct){FILE*pf=fopen(argv[2],"rb");fseek(pf,0,SEEK_END);np=ftell(pf)/(2*N);rewind(pf);
    Perm=malloc(np*N*2); if(fread(Perm,2,np*N,pf)!=(size_t)(np*N))return 1; fclose(pf);}
  for(int L=1;L<=26;L++){
    for(int s=0;s<4;s++)for(int o=0;o<L;o++)for(int j=0;j<13;j++)cls1[L][s][o][j]=cidx(SE[s]+1,SE[s][0],j,o,L);
    for(int s=0;s<2;s++)for(int o=0;o<L;o++)for(int j=0;j<11;j++)cls2[L][s][o][j]=cidx(SB[s]+1,SB[s][0],j,o,L);}
  long long *ph=calloc((size_t)npair*2*27,sizeof(long long)); long long printed=0, rows=0;
  int nd=direct?1:2;
  #pragma omp parallel for schedule(dynamic,16) reduction(+:printed,rows)
  for(long q=0;q<np;q++){
   if(!direct && q%stride!=off) continue; rows++;
   long long *lh=calloc((size_t)npair*2*27,sizeof(long long));
   for(int dir=0;dir<nd;dir++){
    short S[N];
    if(direct){for(int i=0;i<N;i++)S[i]=i;}
    else{const short*s=Perm+q*N; if(dir){for(int i=0;i<N;i++)S[s[i]]=i;} else memcpy(S,s,2*N);}
    int c1[13],c2[11];
    for(int j=0;j<13;j++)c1[j]=C[S[P1+j]]; for(int j=0;j<11;j++)c2[j]=C[S[P2+j]];
    for(int pi=0;pi<npair;pi++)for(int fm=0;fm<2;fm++){
      const int *xi=INV[PX[pi]], *yi=INV[PY[pi]];
      int v1[13],v2[11];
      for(int j=0;j<13;j++){int c=yi[c1[j]],p=xi[C1[j]-'A']; v1[j]=fm?(c+p)%26:(c-p+26)%26;}
      for(int j=0;j<11;j++){int c=yi[c2[j]],p=xi[C2[j]-'A']; v2[j]=fm?(c+p)%26:(c-p+26)%26;}
      for(int L=LMIN;L<=LMAX;L++){
        unsigned char m1[4*26][26]; int ok1[4*26];
        for(int s=0;s<4;s++)for(int o=0;o<L;o++){unsigned char*m=m1[s*26+o]; memset(m,255,26); int ok=1;
          for(int j=0;j<13&&ok;j++){int k=cls1[L][s][o][j]; if(m[k]==255)m[k]=v1[j]; else if(m[k]!=v1[j])ok=0;} ok1[s*26+o]=ok;}
        for(int s=0;s<2;s++)for(int o=0;o<L;o++){unsigned char m[26]; memset(m,255,26); int ok=1;
          for(int j=0;j<11&&ok;j++){int k=cls2[L][s][o][j]; if(m[k]==255)m[k]=v2[j]; else if(m[k]!=v2[j])ok=0;}
          if(!ok)continue;
          for(int s1=0;s1<4;s1++)for(int o1=0;o1<L;o1++){ if(!ok1[s1*26+o1])continue; const unsigned char*a=m1[s1*26+o1]; int good=1;
            for(int k=0;k<L;k++) if(m[k]!=255&&a[k]!=255&&m[k]!=a[k]){good=0;break;}
            if(good){ lh[((size_t)pi*2+fm)*27+L]++;
              long long doprint;
              #pragma omp atomic capture
              doprint=++printed;
              if(doprint<=maxprint){
                char key[27]; for(int k=0;k<L;k++){int v=a[k]!=255?a[k]:m[k]; key[k]=v==255?'?':AL[PY[pi]][v];} key[L]=0;
                #pragma omp critical
                printf("S perm=%ld dir=%d pair=%d X=%s Y=%s form=%s L=%d segE=%s segB=%s o1=%d o2=%d key=%s\n",q,dir,pi,AL[PX[pi]],AL[PY[pi]],fm?"beau":"vig",L,SEN[s1],SBN[s],o1,o,key);
              }}}}
      }}}
   #pragma omp critical
   for(size_t a=0;a<(size_t)npair*2*27;a++)ph[a]+=lh[a];
   free(lh);
  }
  for(int L=LMIN;L<=LMAX;L++){long long t=0; for(int a=0;a<npair*2;a++)t+=ph[a*27+L]; printf("H %d %lld\n",L,t);}
  for(int a=0;a<npair*2;a++)for(int L=LMIN;L<=LMAX;L++) if(ph[a*27+L]) printf("P %d %d %d %lld\n",a/2,a%2,L,ph[a*27+L]);
  long long tot=0; for(int a=0;a<npair*2*27;a++)tot+=ph[a];
  printf("T rows=%lld dirs=%d pairs=%d L=%d..%d survivors(cells, vig=variant counted once)=%lld printed=%lld\n",rows,nd,npair,LMIN,LMAX,tot,printed);
  return 0;}
