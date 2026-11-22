/* Cycle 235 (PREREG235, I-364 / I-356 audit): gn217 (cycle 217, sha 97bae55f...) with a hit-rich crib-SUBSET surrogate.
   Same model Q, forms, alphabets, permutations, windows and index seats as gn217. A surrogate hit <=> all 8 index seats
   (crib seats 0-3 = EAST at 21-24 and 13-16 = BERL at 63-66) agree with window w (8/8). Each hit is decrypted in full
   (97 letters; the window is a full key) and scored with NC = mean log10 quadgram (qg.bin) over quadgrams that touch no crib
   position (21-33, 63-73): nq = 64 always. agree24 (all 24 crib seats) is also printed.
   Forms: 0 Vig c=Y[x(p)+k], 1 variant c=Y[x(p)-k], 2 Beau c=Y[k-x(p)]. ix 0: K[w][i]; ix 1: K[w][S[i]] (carved index).
   usage: gn235 CT perms.bin|x Xalpha.bin Yalpha.bin keys.bin rowstride rowoff qg.bin [maxprint]
   output: 'H perm dir ix X Y form w agree8 agree24 nc pt' lines (at most maxprint), then
           'Y nq=64 n=COUNT max=NC' and 'T rows pairforms windows hits8 hits24ge23'. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
#define T4 (26*26*26*26)
static const char *C1="EASTNORTHEAST",*C2="BERLINCLOCK";
static int POS[24],PT[24],CRIB[N]; static float*QG;
static unsigned char* rd(const char*fn,long*n,int rec){FILE*f=fopen(fn,"rb");if(!f){perror(fn);exit(1);}fseek(f,0,SEEK_END);long s=ftell(f);rewind(f);
  unsigned char*b=malloc(s);if(fread(b,1,s,f)!=(size_t)s)exit(1);fclose(f);*n=s/rec;return b;}
static inline int t4(const int*v){return ((v[0]*26+v[1])*26+v[2])*26+v[3];}
static double nc(const char*t){double s=0;int n=0;for(int i=0;i+3<N;i++){if(CRIB[i]||CRIB[i+1]||CRIB[i+2]||CRIB[i+3])continue;
  s+=QG[(((t[i]-65)*26+t[i+1]-65)*26+t[i+2]-65)*26+t[i+3]-65];n++;} return s/n;}
int main(int argc,char**argv){
  if(argc<9){fprintf(stderr,"usage\n");return 1;}
  int C[N]; for(int i=0;i<N;i++)C[i]=argv[1][i]-'A';
  for(int j=0;j<13;j++){POS[j]=21+j;PT[j]=C1[j]-'A';} for(int j=0;j<11;j++){POS[13+j]=63+j;PT[13+j]=C2[j]-'A';}
  for(int j=0;j<24;j++)CRIB[POS[j]]=1;
  int rs=atoi(argv[6]),ro=atoi(argv[7]); long maxprint=argc>9?atol(argv[9]):1000;
  long nx,ny,nw,nq4; unsigned char*XA=rd(argv[3],&nx,26),*YA=rd(argv[4],&ny,26),*K=rd(argv[5],&nw,N);
  QG=(float*)rd(argv[8],&nq4,4); if(nq4!=T4){fprintf(stderr,"qg size\n");return 1;}
  unsigned char*XI=malloc(nx*26),*YI=malloc(ny*26);
  for(long a=0;a<nx;a++)for(int i=0;i<26;i++)XI[a*26+XA[a*26+i]]=i;
  for(long a=0;a<ny;a++)for(int i=0;i<26;i++)YI[a*26+YA[a*26+i]]=i;
  unsigned char*XP=malloc(nx*24); for(long a=0;a<nx;a++)for(int j=0;j<24;j++)XP[a*24+j]=XI[a*26+PT[j]];
  int direct=!strcmp(argv[2],"x"); long np=1; short*Perm=NULL;
  if(!direct){long b; Perm=(short*)rd(argv[2],&b,2*N); np=b;}
  long long h8=0,h23=0,pf=0,rows=0,printed=0; double mx=-99;
  if(direct){
    int *headA=malloc(T4*sizeof(int)),*nxA=malloc(nx*sizeof(int));
    for(int i=0;i<T4;i++)headA[i]=-1;
    for(long x=0;x<nx;x++){int v[4]; for(int j=0;j<4;j++)v[j]=XP[x*24+j]; int a=t4(v); nxA[x]=headA[a]; headA[a]=x;}
    unsigned char*YC=malloc(ny*24); for(long y=0;y<ny;y++)for(int j=0;j<24;j++)YC[y*24+j]=YI[y*26+C[POS[j]]];
    #pragma omp parallel for schedule(dynamic,16) reduction(+:h8,h23,pf) reduction(max:mx)
    for(long y=ro;y<ny;y+=rs){ const unsigned char*yc=YC+y*24;
      for(long w=0;w<nw;w++){ int kk[24]; for(int j=0;j<24;j++)kk[j]=K[w*N+POS[j]];
        for(int f=0;f<3;f++){ int u[24]; pf+=nx;
          for(int j=0;j<24;j++)u[j]= f==0?(yc[j]-kk[j]+26)%26: f==1?(yc[j]+kk[j])%26:(kk[j]-yc[j]+26)%26;
          for(long x=headA[t4(u)];x>=0;x=nxA[x]){ const unsigned char*xp=XP+x*24; int ok=1;
            for(int j=13;j<17;j++)if(xp[j]!=u[j])ok=0; if(!ok)continue;
            int ag=0; for(int j=0;j<24;j++)ag+=(xp[j]==u[j]);
            char t[N+1]; for(int i=0;i<N;i++){int k=K[w*N+i],yy=YI[y*26+C[i]]; int xx= f==0?(yy-k+26)%26: f==1?(yy+k)%26:(k-yy+26)%26; t[i]='A'+XA[x*26+xx];} t[N]=0;
            double s=nc(t); h8++; if(ag>=23)h23++; if(s>mx)mx=s;
            #pragma omp critical
            { if(printed<maxprint){printed++; printf("H perm=-1 dir=0 ix=0 X=%ld Y=%ld form=%d w=%ld agree8=8 agree24=%d nc=%.4f pt=%s\n",x,y,f,w,ag,s,t);} } } } } }
    rows=1;
  } else {
    #pragma omp parallel reduction(+:h8,h23,pf,rows) reduction(max:mx)
    { int *headA=malloc(T4*sizeof(int)),*nxA=malloc(nw*sizeof(int));
      for(int i=0;i<T4;i++)headA[i]=-1;
      unsigned char*KS=malloc(nw*24); int *tA=malloc(nw*sizeof(int));
      #pragma omp for schedule(dynamic,32)
      for(long q=ro;q<np;q+=rs){ short*P=Perm+q*N; int inv[N]; for(int i=0;i<N;i++)inv[P[i]]=i; rows++;
        for(int dir=0;dir<2;dir++){ int cp[N],cc[24]; for(int i=0;i<N;i++)cp[i]= dir==0?P[i]:inv[i]; for(int j=0;j<24;j++)cc[j]=C[cp[POS[j]]];
          for(int ix=0;ix<2;ix++){
            for(long w=0;w<nw;w++){ unsigned char*ks=KS+w*24; for(int j=0;j<24;j++)ks[j]=K[w*N+(ix==0?POS[j]:cp[POS[j]])];
              int v[4]; for(int j=0;j<4;j++)v[j]=ks[j]; tA[w]=t4(v); nxA[w]=headA[tA[w]]; headA[tA[w]]=w; }
            for(long y=0;y<ny;y++){ int yc[24]; for(int j=0;j<24;j++)yc[j]=YI[y*26+cc[j]];
              for(long x=0;x<nx;x++){ const unsigned char*xp=XP+x*24;
                for(int f=0;f<3;f++){ int k[24]; pf++;
                  for(int j=0;j<24;j++)k[j]= f==0?(yc[j]-xp[j]+26)%26: f==1?(xp[j]-yc[j]+26)%26:(yc[j]+xp[j])%26;
                  for(long w=headA[t4(k)];w>=0;w=nxA[w]){ const unsigned char*ks=KS+w*24; int ok=1;
                    for(int j=13;j<17;j++)if(ks[j]!=k[j])ok=0; if(!ok)continue;
                    int ag=0; for(int j=0;j<24;j++)ag+=(ks[j]==k[j]);
                    char t[N+1]; for(int i=0;i<N;i++){int kv=K[w*N+(ix==0?i:cp[i])],yy=YI[y*26+C[cp[i]]];
                      int xx= f==0?(yy-kv+26)%26: f==1?(yy+kv)%26:(kv-yy+26)%26; t[i]='A'+XA[x*26+xx];} t[N]=0;
                    double s=nc(t); h8++; if(ag>=23)h23++; if(s>mx)mx=s;
                    #pragma omp critical
                    { if(printed<maxprint){printed++; printf("H perm=%ld dir=%d ix=%d X=%ld Y=%ld form=%d w=%ld agree8=8 agree24=%d nc=%.4f pt=%s\n",q,dir,ix,x,y,f,w,ag,s,t);} } } } } }
            for(long w=0;w<nw;w++)headA[tA[w]]=-1; } } } }
  }
  printf("Y nq=64 n=%lld max=%.4f\n",h8,h8?mx:-99.0);
  printf("T rows=%lld pairforms=%lld windows=%ld hits8=%lld hits24ge23=%lld\n",rows,pf,nw,h8,h23);
  return 0;}
