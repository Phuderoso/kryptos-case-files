/* Cycle 214 (PREREG214 Part A, I-295): digit-keyed polyalphabetic on two keyed alphabets, key-agnostic crib filter.
   Model Q: substitution-layer letter at plaintext position i is carved at S[i]; S = family row (dir 0) or its inverse (dir 1);
   'x' = identity. Forms: 0 Vig c=Y[x(p)+k] (k=y-x), 1 variant c=Y[x(p)-k] (k=x-y), 2 Beau c=Y[k-x(p)] (k=y+x), mod 26.
   Survivor <=> all 24 crib digits k in 0..9 (any digit key stream; order-free).
   usage: gron214 CT perms.bin|x alphabets.bin rowstride rowoff xstride xoff [maxprint]
   output: 'S perm dir X Y form digits' lines, 'T rows pairs survivors' line. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char *C1="EASTNORTHEAST",*C2="BERLINCLOCK";
int main(int argc,char**argv){
  if(argc<8){fprintf(stderr,"usage\n");return 1;}
  int C[N]; for(int i=0;i<N;i++)C[i]=argv[1][i]-'A';
  int rs=atoi(argv[4]),ro=atoi(argv[5]),xs=atoi(argv[6]),xo=atoi(argv[7]); long maxprint=argc>8?atol(argv[8]):1000;
  int POS[24],PT[24]; for(int j=0;j<13;j++){POS[j]=21+j;PT[j]=C1[j]-'A';} for(int j=0;j<11;j++){POS[13+j]=63+j;PT[13+j]=C2[j]-'A';}
  FILE*fa=fopen(argv[3],"rb"); fseek(fa,0,SEEK_END); long na=ftell(fa)/26; rewind(fa);
  unsigned char *A=malloc(na*26); if(fread(A,1,na*26,fa)!=(size_t)(na*26))return 1; fclose(fa);
  unsigned char *INV=malloc(na*26); for(long a=0;a<na;a++)for(int i=0;i<26;i++)INV[a*26+A[a*26+i]]=i;
  int direct=!strcmp(argv[2],"x"); long np=1; short*Perm=NULL;
  if(!direct){FILE*pf=fopen(argv[2],"rb");fseek(pf,0,SEEK_END);np=ftell(pf)/(2*N);rewind(pf);
    Perm=malloc(np*N*2); if(fread(Perm,2,np*N,pf)!=(size_t)(np*N))return 1; fclose(pf);}
  unsigned char *XP=malloc(na*24); for(long a=0;a<na;a++)for(int j=0;j<24;j++)XP[a*24+j]=INV[a*26+PT[j]];
  long long tot=0,printed=0,rows=0,pairs=0;
  int ndir=direct?1:2;
  if(direct){
    unsigned char *YC=malloc(na*24); for(long a=0;a<na;a++)for(int j=0;j<24;j++)YC[a*24+j]=INV[a*26+C[POS[j]]];
    #pragma omp parallel for schedule(dynamic,64) reduction(+:tot,pairs)
    for(long x=xo;x<na;x+=xs){ const unsigned char*xp=XP+x*24;
      for(long y=0;y<na;y++){ const unsigned char*yc=YC+y*24; pairs++;
        for(int f=0;f<3;f++){ int j;
          for(j=0;j<24;j++){int k= f==0?(yc[j]-xp[j]+26)%26: f==1?(xp[j]-yc[j]+26)%26:(yc[j]+xp[j])%26; if(k>9)break;}
          if(j==24){ tot++;
            #pragma omp critical
            { if(printed<maxprint){printed++; printf("S perm=-1 dir=0 X=%ld Y=%ld form=%d k=",x,y,f);
                for(int t=0;t<24;t++){int k= f==0?(yc[t]-xp[t]+26)%26: f==1?(xp[t]-yc[t]+26)%26:(yc[t]+xp[t])%26; printf("%d",k);} printf("\n");} } } } } }
    rows=1;
  } else {
    #pragma omp parallel for schedule(dynamic,64) reduction(+:tot,pairs,rows)
    for(long q=ro;q<np;q+=rs){ short*P=Perm+q*N; int inv[N]; for(int i=0;i<N;i++)inv[P[i]]=i; rows++;
      for(int dir=0;dir<2;dir++){ int cc[24]; for(int j=0;j<24;j++)cc[j]=C[dir==0?P[POS[j]]:inv[POS[j]]];
        unsigned char yc[24];
        for(long y=0;y<na;y++){ for(int j=0;j<24;j++)yc[j]=INV[y*26+cc[j]];
          for(long x=xo;x<na;x+=xs){ const unsigned char*xp=XP+x*24; pairs++;
            for(int f=0;f<3;f++){ int j;
              for(j=0;j<24;j++){int k= f==0?(yc[j]-xp[j]+26)%26: f==1?(xp[j]-yc[j]+26)%26:(yc[j]+xp[j])%26; if(k>9)break;}
              if(j==24){ tot++;
                #pragma omp critical
                { if(printed<maxprint){printed++; printf("S perm=%ld dir=%d X=%ld Y=%ld form=%d k=",q,dir,x,y,f);
                    for(int t=0;t<24;t++){int k= f==0?(yc[t]-xp[t]+26)%26: f==1?(xp[t]-yc[t]+26)%26:(yc[t]+xp[t])%26; printf("%d",k);} printf("\n");} } } } } } } }
  }
  printf("T rows=%lld dirs=%d pairforms=%lld survivors=%lld\n",rows,ndir,pairs*3,tot);
  return 0;}
