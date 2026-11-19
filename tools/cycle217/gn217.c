/* Cycle 217 (PREREG217 Part A, I-304): named two-digit-group numeric keys on two keyed alphabets.
   Model Q (as case 200): layer letter at plaintext position i is carved at S[i]; S = family row (dir 0) or inverse (dir 1); 'x' = identity.
   Forms: 0 Vig c=Y[x(p)+k], 1 variant c=Y[x(p)-k], 2 Beau c=Y[k-x(p)], mod 26. Key value at crib seat j:
   ix 0: K[w][POS[j]] (plaintext index); ix 1: K[w][S[POS[j]]] (carved index). Direct: ix 0 == ix 1.
   Hit <=> >= 23 of the 24 crib seats agree with window w (exact = 24). Two 4-seat indexes (seats 0-3 and 13-16) make one error anywhere
   recoverable; a cell found via both indexes is counted once.
   usage: gn217 CT perms.bin|x Xalpha.bin Yalpha.bin keys.bin rowstride rowoff [maxprint]
   output: 'H perm dir ix X Y form w agree' lines; 'T rows pairforms windows hits24 hits23' line. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
#define T4 (26*26*26*26)
static const char *C1="EASTNORTHEAST",*C2="BERLINCLOCK";
static int POS[24],PT[24];
static unsigned char* rd(const char*fn,long*n,int rec){FILE*f=fopen(fn,"rb");if(!f){perror(fn);exit(1);}fseek(f,0,SEEK_END);long s=ftell(f);rewind(f);
  unsigned char*b=malloc(s);if(fread(b,1,s,f)!=(size_t)s)exit(1);fclose(f);*n=s/rec;return b;}
static inline int t4(const int*v){return ((v[0]*26+v[1])*26+v[2])*26+v[3];}
int main(int argc,char**argv){
  if(argc<8){fprintf(stderr,"usage\n");return 1;}
  int C[N]; for(int i=0;i<N;i++)C[i]=argv[1][i]-'A';
  for(int j=0;j<13;j++){POS[j]=21+j;PT[j]=C1[j]-'A';} for(int j=0;j<11;j++){POS[13+j]=63+j;PT[13+j]=C2[j]-'A';}
  int rs=atoi(argv[6]),ro=atoi(argv[7]); long maxprint=argc>8?atol(argv[8]):1000;
  long nx,ny,nw; unsigned char*XA=rd(argv[3],&nx,26),*YA=rd(argv[4],&ny,26),*K=rd(argv[5],&nw,N);
  unsigned char*XI=malloc(nx*26),*YI=malloc(ny*26);
  for(long a=0;a<nx;a++)for(int i=0;i<26;i++)XI[a*26+XA[a*26+i]]=i;
  for(long a=0;a<ny;a++)for(int i=0;i<26;i++)YI[a*26+YA[a*26+i]]=i;
  unsigned char*XP=malloc(nx*24); for(long a=0;a<nx;a++)for(int j=0;j<24;j++)XP[a*24+j]=XI[a*26+PT[j]];
  int direct=!strcmp(argv[2],"x"); long np=1; short*Perm=NULL;
  if(!direct){long b; Perm=(short*)rd(argv[2],&b,2*N); np=b;}
  long long h24=0,h23=0,pf=0,rows=0,printed=0;
  if(direct){ /* join: index X by u at seats 0-3 (A) and 13-16 (B); per window, form, Y compute required u */
    int *headA=malloc(T4*sizeof(int)),*headB=malloc(T4*sizeof(int)),*nxA=malloc(nx*sizeof(int)),*nxB=malloc(nx*sizeof(int));
    for(int i=0;i<T4;i++)headA[i]=headB[i]=-1;
    for(long x=0;x<nx;x++){int v[4]; for(int j=0;j<4;j++)v[j]=XP[x*24+j]; int a=t4(v); nxA[x]=headA[a]; headA[a]=x;
      for(int j=0;j<4;j++)v[j]=XP[x*24+13+j]; a=t4(v); nxB[x]=headB[a]; headB[a]=x;}
    unsigned char*YC=malloc(ny*24); for(long y=0;y<ny;y++)for(int j=0;j<24;j++)YC[y*24+j]=YI[y*26+C[POS[j]]];
    #pragma omp parallel for schedule(dynamic,16) reduction(+:h24,h23,pf)
    for(long y=ro;y<ny;y+=rs){ const unsigned char*yc=YC+y*24;
      for(long w=0;w<nw;w++){ int kk[24]; for(int j=0;j<24;j++)kk[j]=K[w*N+POS[j]];
        for(int f=0;f<3;f++){ int u[24]; pf+=nx;
          for(int j=0;j<24;j++)u[j]= f==0?(yc[j]-kk[j]+26)%26: f==1?(yc[j]+kk[j])%26:(kk[j]-yc[j]+26)%26;
          for(int pass=0;pass<2;pass++){ long x= pass==0?headA[t4(u)]:headB[t4(u+13)];
            for(;x>=0;x= pass==0?nxA[x]:nxB[x]){ const unsigned char*xp=XP+x*24; int ag=0,a4=1;
              for(int j=0;j<24;j++)ag+=(xp[j]==u[j]); if(pass==1){for(int j=0;j<4;j++)if(xp[j]!=u[j])a4=0; if(a4)continue;}
              if(ag>=23){ if(ag==24)h24++; else h23++;
                #pragma omp critical
                { if(printed<maxprint){printed++; printf("H perm=-1 dir=0 ix=0 X=%ld Y=%ld form=%d w=%ld agree=%d\n",x,y,f,w,ag);} } } } } } } }
    rows=1;
  } else { /* pair loop with per-(S,dir,ix) window index on seats 0-3 / 13-16 */
    #pragma omp parallel reduction(+:h24,h23,pf,rows)
    { int *headA=malloc(T4*sizeof(int)),*headB=malloc(T4*sizeof(int)),*nxA=malloc(nw*sizeof(int)),*nxB=malloc(nw*sizeof(int));
      for(int i=0;i<T4;i++)headA[i]=headB[i]=-1;
      unsigned char*KS=malloc(nw*24); int *tA=malloc(nw*sizeof(int)),*tB=malloc(nw*sizeof(int));
      #pragma omp for schedule(dynamic,32)
      for(long q=ro;q<np;q+=rs){ short*P=Perm+q*N; int inv[N]; for(int i=0;i<N;i++)inv[P[i]]=i; rows++;
        for(int dir=0;dir<2;dir++){ int cp[24],cc[24]; for(int j=0;j<24;j++){cp[j]= dir==0?P[POS[j]]:inv[POS[j]]; cc[j]=C[cp[j]];}
          for(int ix=0;ix<2;ix++){
            for(long w=0;w<nw;w++){ unsigned char*ks=KS+w*24; for(int j=0;j<24;j++)ks[j]=K[w*N+(ix==0?POS[j]:cp[j])];
              int v[4]; for(int j=0;j<4;j++)v[j]=ks[j]; tA[w]=t4(v); nxA[w]=headA[tA[w]]; headA[tA[w]]=w;
              for(int j=0;j<4;j++)v[j]=ks[13+j]; tB[w]=t4(v); nxB[w]=headB[tB[w]]; headB[tB[w]]=w; }
            for(long y=0;y<ny;y++){ int yc[24]; for(int j=0;j<24;j++)yc[j]=YI[y*26+cc[j]];
              for(long x=0;x<nx;x++){ const unsigned char*xp=XP+x*24;
                for(int f=0;f<3;f++){ int k[24]; pf++;
                  for(int j=0;j<24;j++)k[j]= f==0?(yc[j]-xp[j]+26)%26: f==1?(xp[j]-yc[j]+26)%26:(yc[j]+xp[j])%26;
                  for(int pass=0;pass<2;pass++){ long w= pass==0?headA[t4(k)]:headB[t4(k+13)];
                    for(;w>=0;w= pass==0?nxA[w]:nxB[w]){ const unsigned char*ks=KS+w*24; int ag=0,a4=1;
                      for(int j=0;j<24;j++)ag+=(ks[j]==k[j]); if(pass==1){for(int j=0;j<4;j++)if(ks[j]!=k[j])a4=0; if(a4)continue;}
                      if(ag>=23){ if(ag==24)h24++; else h23++;
                        #pragma omp critical
                        { if(printed<maxprint){printed++; printf("H perm=%ld dir=%d ix=%d X=%ld Y=%ld form=%d w=%ld agree=%d\n",q,dir,ix,x,y,f,w,ag);} } } } } } } }
            for(long w=0;w<nw;w++){headA[tA[w]]=-1; headB[tB[w]]=-1;} } } } }
  }
  printf("T rows=%lld pairforms=%lld windows=%ld hits24=%lld hits23=%lld\n",rows,pf,nw,h24,h23);
  return 0;}
