/* Cycle 206 (I-258, PREREG206 Part A): word-restart key R1 behind the transposition bank, model Q.
   Layer letter i (plaintext order) = C[S[i]]; S = bank entry (dir 0) or its inverse (dir 1); 'x' = identity.
   Key index of a crib letter = its position inside its plaintext word mod L (case 190 segmentations, free offsets).
   Tableaux AZ / KA, Vigenere (= variant for consistency) and Beaufort. Survivor = equal index -> equal key value.
   usage: wrbank CT perms.bin|x LMIN LMAX [maxprint]
   output: 'S' survivor lines, 'H tm L count' histogram (tm: 0 AZvig 1 AZbeau 2 KAvig 3 KAbeau), 'T' totals. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char *KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static const char *C1="EASTNORTHEAST", *C2="BERLINCLOCK";
static const int P1=21, P2=63;
static const int SE[4][3]={{0},{1,4},{1,9},{2,4,9}}; /* n, boundaries */
static const char *SEN[4]={"EASTNORTHEAST","EAST|NORTHEAST","EASTNORTH|EAST","EAST|NORTH|EAST"};
static const int SB[2][2]={{0},{1,6}};
static const char *SBN[2]={"BERLINCLOCK","BERLIN|CLOCK"};
static int cls1[27][4][26][13], cls2[27][2][26][11];
static int cidx(const int *b,int nb,int j,int o,int L){int pb=-1;for(int k=0;k<nb;k++)if(b[k]<=j)pb=b[k];return ((pb>=0)?(j-pb):(o+j))%L;}
int main(int argc,char**argv){
  if(argc<5){fprintf(stderr,"usage\n");return 1;}
  int C[N]; for(int i=0;i<N;i++)C[i]=argv[1][i]-'A';
  int LMIN=atoi(argv[3]),LMAX=atoi(argv[4]); int maxprint=argc>5?atoi(argv[5]):100;
  int kai[26]; for(int i=0;i<26;i++)kai[KA[i]-'A']=i;
  int direct=!strcmp(argv[2],"x"); long np=1; short*Perm=NULL;
  if(!direct){FILE*pf=fopen(argv[2],"rb");fseek(pf,0,SEEK_END);np=ftell(pf)/(2*N);rewind(pf);
    Perm=malloc(np*N*2); if(fread(Perm,2,np*N,pf)!=(size_t)(np*N))return 1; fclose(pf);}
  for(int L=1;L<=26;L++){
    for(int s=0;s<4;s++)for(int o=0;o<L;o++)for(int j=0;j<13;j++)cls1[L][s][o][j]=cidx(SE[s]+1,SE[s][0],j,o,L);
    for(int s=0;s<2;s++)for(int o=0;o<L;o++)for(int j=0;j<11;j++)cls2[L][s][o][j]=cidx(SB[s]+1,SB[s][0],j,o,L);}
  long long hist[4][27]; memset(hist,0,sizeof hist); long long printed=0;
  int nd=direct?1:2;
  #pragma omp parallel for schedule(dynamic,64) reduction(+:printed)
  for(long q=0;q<np;q++){
   long long lh[4][27]; memset(lh,0,sizeof lh);
   for(int dir=0;dir<nd;dir++){
    short S[N];
    if(direct){for(int i=0;i<N;i++)S[i]=i;}
    else{const short*s=Perm+q*N; if(dir){for(int i=0;i<N;i++)S[s[i]]=i;} else memcpy(S,s,2*N);}
    int c1[13],c2[11];
    for(int j=0;j<13;j++)c1[j]=C[S[P1+j]]; for(int j=0;j<11;j++)c2[j]=C[S[P2+j]];
    for(int tm=0;tm<4;tm++){
      int v1[13],v2[11];
      for(int j=0;j<13;j++){int c=c1[j],p=C1[j]-'A'; if(tm>=2){c=kai[c];p=kai[p];} v1[j]=(tm&1)?(c+p)%26:(c-p+26)%26;}
      for(int j=0;j<11;j++){int c=c2[j],p=C2[j]-'A'; if(tm>=2){c=kai[c];p=kai[p];} v2[j]=(tm&1)?(c+p)%26:(c-p+26)%26;}
      for(int L=LMIN;L<=LMAX;L++){
        unsigned char m1[4*26][26]; int ok1[4*26];
        for(int s=0;s<4;s++)for(int o=0;o<L;o++){unsigned char*m=m1[s*26+o]; memset(m,255,26); int ok=1;
          for(int j=0;j<13&&ok;j++){int k=cls1[L][s][o][j]; if(m[k]==255)m[k]=v1[j]; else if(m[k]!=v1[j])ok=0;} ok1[s*26+o]=ok;}
        for(int s=0;s<2;s++)for(int o=0;o<L;o++){unsigned char m[26]; memset(m,255,26); int ok=1;
          for(int j=0;j<11&&ok;j++){int k=cls2[L][s][o][j]; if(m[k]==255)m[k]=v2[j]; else if(m[k]!=v2[j])ok=0;}
          if(!ok)continue;
          for(int s1=0;s1<4;s1++)for(int o1=0;o1<L;o1++){ if(!ok1[s1*26+o1])continue; const unsigned char*a=m1[s1*26+o1]; int good=1;
            for(int k=0;k<L;k++) if(m[k]!=255&&a[k]!=255&&m[k]!=a[k]){good=0;break;}
            if(good){ lh[tm][L]++;
              int doprint; 
              #pragma omp atomic capture
              doprint=++printed;
              if(doprint<=maxprint){
                char key[27]; for(int k=0;k<L;k++){int v=a[k]!=255?a[k]:m[k]; key[k]=v==255?'?':(tm>=2?KA[v]:'A'+v);} key[L]=0;
                #pragma omp critical
                printf("S perm=%ld dir=%d tm=%d L=%d segE=%s segB=%s o1=%d o2=%d key=%s\n",q,dir,tm,L,SEN[s1],SBN[s],o1,o,key);
              }}}}
      }}}
   #pragma omp critical
   for(int a=0;a<4;a++)for(int L=0;L<27;L++)hist[a][L]+=lh[a][L];
  }
  for(int tm=0;tm<4;tm++)for(int L=LMIN;L<=LMAX;L++)printf("H %d %d %lld\n",tm,L,hist[tm][L]);
  long long tot=0; for(int tm=0;tm<4;tm++)for(int L=LMIN;L<=LMAX;L++)tot+=hist[tm][L];
  printf("T perms=%ld dirs=%d L=%d..%d survivors(cells, vig counted once)=%lld\n",np,nd,LMIN,LMAX,tot);
  return 0;}
