/* Cycle 230 (PREREG230): bounded-shift keys on two keyed alphabets, key-agnostic crib filter (I-299 generalised; gron214.c skeleton).
   Model Q as gron214 (layer letter i carved at S[i]; S = family row (dir 0) or its inverse (dir 1)); forms 0 Vig k=y-x, 1 variant k=x-y,
   2 Beau k=y+x (mod 26). The 24 crib shifts k_j are order-free. Survivor <=> (A) all k_j lie in one circular window of <= WMAX values
   (any offset: a digit key with offset, any base <= WMAX) or (B) the k_j take <= DMAX distinct values (a key alphabet of <= DMAX shifts).
   usage: bsk230 CT perms.bin|x alphabets.bin rowstride rowoff xstride xoff maxprint [WMAX DMAX]
   output: 'S perm dir X Y form width pop k=letters' ; 'T rows pairforms survivors' */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char *C1="EASTNORTHEAST",*C2="BERLINCLOCK";
static inline int pc(unsigned m){return __builtin_popcount(m);}
int main(int argc,char**argv){
  if(argc<9){fprintf(stderr,"usage\n");return 1;}
  int C[N]; for(int i=0;i<N;i++)C[i]=argv[1][i]-'A';
  int rs=atoi(argv[4]),ro=atoi(argv[5]),xs=atoi(argv[6]),xo=atoi(argv[7]); long maxprint=atol(argv[8]);
  int WMAX=argc>9?atoi(argv[9]):10, DMAX=argc>10?atoi(argv[10]):7;
  int POS[24],PT[24]; for(int j=0;j<13;j++){POS[j]=21+j;PT[j]=C1[j]-'A';} for(int j=0;j<11;j++){POS[13+j]=63+j;PT[13+j]=C2[j]-'A';}
  FILE*fa=fopen(argv[3],"rb"); fseek(fa,0,SEEK_END); long na=ftell(fa)/26; rewind(fa);
  unsigned char *A=malloc(na*26); if(fread(A,1,na*26,fa)!=(size_t)(na*26))return 1; fclose(fa);
  unsigned char *INV=malloc(na*26); for(long a=0;a<na;a++)for(int i=0;i<26;i++)INV[a*26+A[a*26+i]]=i;
  int direct=!strcmp(argv[2],"x"); long np=1; short*Perm=NULL;
  if(!direct){FILE*pf=fopen(argv[2],"rb");fseek(pf,0,SEEK_END);np=ftell(pf)/(2*N);rewind(pf);
    Perm=malloc(np*N*2); if(fread(Perm,2,np*N,pf)!=(size_t)(np*N))return 1; fclose(pf);}
  unsigned char *XP=malloc(na*24); for(long a=0;a<na;a++)for(int j=0;j<24;j++)XP[a*24+j]=INV[a*26+PT[j]];
  long long tot=0,printed=0,rows=0,pairs=0; int ndir=direct?1:2;
#define KOF(f,yc,xp) ({int _k=(f)==0?(int)(yc)-(int)(xp):(f)==1?(int)(xp)-(int)(yc):(int)(yc)+(int)(xp); _k<0?_k+26:(_k>=26?_k-26:_k);})
#define TEST(yc,xp,x,y,q,dir) \
  for(int f=0;f<3;f++){ int k0=KOF(f,yc[0],xp[0]); int mn=0,mx=0; unsigned m=1u<<k0; int wa=1,da=1,j; \
    for(j=1;j<24;j++){ int k=KOF(f,yc[j],xp[j]); int d=k-k0; if(d>12)d-=26; if(d<-13)d+=26; \
      if(d<mn)mn=d; if(d>mx)mx=d; m|=1u<<k; if(mx-mn+1>WMAX)wa=0; if(pc(m)>DMAX)da=0; if(!wa&&!da)break; } \
    if(j==24 && (wa||da)){ tot++; \
      _Pragma("omp critical") \
      { if(printed<maxprint){printed++; printf("S perm=%ld dir=%d X=%ld Y=%ld form=%d w=%d pop=%d k=",(long)(q),dir,(long)(x),(long)(y),f,mx-mn+1,pc(m)); \
          for(int t=0;t<24;t++){int k=KOF(f,yc[t],xp[t]); printf("%c",'A'+k);} printf("\n");} } } }
  if(direct){
    unsigned char *YC=malloc(na*24); for(long a=0;a<na;a++)for(int j=0;j<24;j++)YC[a*24+j]=INV[a*26+C[POS[j]]];
    #pragma omp parallel for schedule(dynamic,64) reduction(+:tot,pairs)
    for(long x=xo;x<na;x+=xs){ const unsigned char*xp=XP+x*24;
      for(long y=0;y<na;y++){ const unsigned char*yc=YC+y*24; pairs++; TEST(yc,xp,x,y,-1,0) } }
    rows=1;
  } else {
    #pragma omp parallel for schedule(dynamic,64) reduction(+:tot,pairs,rows)
    for(long q=ro;q<np;q+=rs){ short*P=Perm+q*N; int inv[N]; for(int i=0;i<N;i++)inv[P[i]]=i; rows++;
      for(int dir=0;dir<2;dir++){ int cc[24]; for(int j=0;j<24;j++)cc[j]=C[dir==0?P[POS[j]]:inv[POS[j]]];
        unsigned char yc[24];
        for(long y=0;y<na;y++){ for(int j=0;j<24;j++)yc[j]=INV[y*26+cc[j]];
          for(long x=xo;x<na;x+=xs){ const unsigned char*xp=XP+x*24; pairs++; TEST(yc,xp,x,y,q,dir) } } } }
  }
  printf("T rows=%lld dirs=%d pairforms=%lld survivors=%lld\n",rows,ndir,pairs*3,tot);
  return 0;}
