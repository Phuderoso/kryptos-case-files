/* Cycle 216 (PREREG216 Part A, I-297): one-error robustness of the cycle 214 digit-key filter (gron214.c, case 200).
   Same model Q, same three forms, same alphabets/families; survivor <=> at least 23 of the 24 crib digits k lie in 0..9
   (one crib position - a wrong crib letter or a wrong carved letter - is allowed to fail). Early exit at the 2nd failure.
   usage: gron216 CT perms.bin|x alphabets.bin rowstride rowoff xstride xoff [maxprint]
   output: 'S perm dir X Y form bad=j badk=v k=d0,..,d23' (bad=-1: all 24 in 0..9), then 'T rows dirs pairforms survivors s24 s23'. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char *C1="EASTNORTHEAST",*C2="BERLINCLOCK";
static inline int kf(int f,int y,int x){return f==0?(y-x+26)%26: f==1?(x-y+26)%26:(y+x)%26;}
static long long printed=0,maxprint=1000;
static void emit(long q,int dir,long x,long y,int f,const unsigned char*yc,const unsigned char*xp){
  int bad=-1,badk=-1; for(int t=0;t<24;t++){int k=kf(f,yc[t],xp[t]); if(k>9){bad=t;badk=k;}}
  #pragma omp critical
  { if(printed<maxprint){printed++; printf("S perm=%ld dir=%d X=%ld Y=%ld form=%d bad=%d badk=%d k=",q,dir,x,y,f,bad,badk);
      for(int t=0;t<24;t++){printf(t?",%d":"%d",kf(f,yc[t],xp[t]));} printf("\n");} } }
int main(int argc,char**argv){
  if(argc<8){fprintf(stderr,"usage\n");return 1;}
  int C[N]; for(int i=0;i<N;i++)C[i]=argv[1][i]-'A';
  int rs=atoi(argv[4]),ro=atoi(argv[5]),xs=atoi(argv[6]),xo=atoi(argv[7]); if(argc>8)maxprint=atol(argv[8]);
  int POS[24],PT[24]; for(int j=0;j<13;j++){POS[j]=21+j;PT[j]=C1[j]-'A';} for(int j=0;j<11;j++){POS[13+j]=63+j;PT[13+j]=C2[j]-'A';}
  FILE*fa=fopen(argv[3],"rb"); fseek(fa,0,SEEK_END); long na=ftell(fa)/26; rewind(fa);
  unsigned char *A=malloc(na*26); if(fread(A,1,na*26,fa)!=(size_t)(na*26))return 1; fclose(fa);
  unsigned char *INV=malloc(na*26); for(long a=0;a<na;a++)for(int i=0;i<26;i++)INV[a*26+A[a*26+i]]=i;
  int direct=!strcmp(argv[2],"x"); long np=1; short*Perm=NULL;
  if(!direct){FILE*pf=fopen(argv[2],"rb");fseek(pf,0,SEEK_END);np=ftell(pf)/(2*N);rewind(pf);
    Perm=malloc(np*N*2); if(fread(Perm,2,np*N,pf)!=(size_t)(np*N))return 1; fclose(pf);}
  unsigned char *XP=malloc(na*24); for(long a=0;a<na;a++)for(int j=0;j<24;j++)XP[a*24+j]=INV[a*26+PT[j]];
  long long s24=0,s23=0,rows=0,pairs=0;
  if(direct){
    unsigned char *YC=malloc(na*24); for(long a=0;a<na;a++)for(int j=0;j<24;j++)YC[a*24+j]=INV[a*26+C[POS[j]]];
    #pragma omp parallel for schedule(dynamic,64) reduction(+:s24,s23,pairs)
    for(long x=xo;x<na;x+=xs){ const unsigned char*xp=XP+x*24;
      for(long y=0;y<na;y++){ const unsigned char*yc=YC+y*24; pairs++;
        for(int f=0;f<3;f++){ int j,nb=0;
          for(j=0;j<24;j++){ if(kf(f,yc[j],xp[j])>9){ if(++nb>1)break; } }
          if(j==24){ if(nb==0)s24++; else s23++; emit(-1,0,x,y,f,yc,xp);} } } }
    rows=1;
  } else {
    #pragma omp parallel for schedule(dynamic,64) reduction(+:s24,s23,pairs,rows)
    for(long q=ro;q<np;q+=rs){ short*P=Perm+q*N; int inv[N]; for(int i=0;i<N;i++)inv[P[i]]=i; rows++;
      for(int dir=0;dir<2;dir++){ int cc[24]; for(int j=0;j<24;j++)cc[j]=C[dir==0?P[POS[j]]:inv[POS[j]]];
        unsigned char yc[24];
        for(long y=0;y<na;y++){ for(int j=0;j<24;j++)yc[j]=INV[y*26+cc[j]];
          for(long x=xo;x<na;x+=xs){ const unsigned char*xp=XP+x*24; pairs++;
            for(int f=0;f<3;f++){ int j,nb=0;
              for(j=0;j<24;j++){ if(kf(f,yc[j],xp[j])>9){ if(++nb>1)break; } }
              if(j==24){ if(nb==0)s24++; else s23++; emit(q,dir,x,y,f,yc,xp);} } } } } }
  }
  printf("T rows=%lld dirs=%d pairforms=%lld survivors=%lld s24=%lld s23=%lld\n",rows,direct?1:2,pairs*3,s24+s23,s24,s23);
  return 0;}
