// M-209 / C-38 pin-and-lug annealer. usage: m209a CT qg.bin mode(0=Beaufort M-209,1=Vig) restarts iters seed cribw
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define N 97
static const int PER[6]={26,25,23,21,19,17};
static int TY[21]; // bitmask of wheels
static float *QG; static int ct[N], crib[N];
static unsigned long long rs;
static inline unsigned rnd(){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return (unsigned)rs;}
static inline double urand(){return (rnd()&0xffffff)/16777216.0;}
typedef struct{unsigned char pin[6][26]; int n[21];} St;
static int mode;
static void dec(St*s,int*pt){for(int i=0;i<N;i++){int m=0;for(int w=0;w<6;w++) if(s->pin[w][i%PER[w]]) m|=1<<w;
  int k=0;for(int t=0;t<21;t++) if(TY[t]&m) k+=s->n[t];
  int c=ct[i]; pt[i]= mode==0? ((25+k-c)%26+26)%26 : ((c-k)%26+26)%26;}}
static double cribw, QW=1;
static double score(St*s,int*mis){int pt[N];dec(s,pt);double q=0;for(int i=0;i+3<N;i++)q+=QG[((pt[i]*26+pt[i+1])*26+pt[i+2])*26+pt[i+3]];
  int m=0;for(int i=0;i<N;i++) if(crib[i]>=0&&pt[i]!=crib[i]) m++; *mis=m; return QW*q/(N-3)-cribw*m;}
int main(int c,char**v){
  int t=0;for(int w=0;w<6;w++)TY[t++]=1<<w;for(int a=0;a<6;a++)for(int b=a+1;b<6;b++)TY[t++]=(1<<a)|(1<<b);
  for(int i=0;i<N;i++){ct[i]=v[1][i]-65;crib[i]=-1;}
  const char*E="EASTNORTHEAST",*B="BERLINCLOCK";for(int i=0;i<13;i++)crib[21+i]=E[i]-65;for(int i=0;i<11;i++)crib[63+i]=B[i]-65;
  QG=malloc(4*456976);FILE*f=fopen(v[2],"rb");if(fread(QG,4,456976,f)!=456976)return 1;fclose(f);
  mode=atoi(v[3]);int R=atoi(v[4]);long IT=atol(v[5]);rs=atoll(v[6])*2654435761ULL+1;cribw=atof(v[7]); if(c>8)QW=atof(v[8]);
  double gbest=-1e9;St gb;int gm=99;
  for(int r=0;r<R;r++){St s;for(int w=0;w<6;w++)for(int j=0;j<26;j++)s.pin[w][j]=rnd()&1;
    memset(s.n,0,sizeof s.n);for(int b=0;b<27;b++){int tt=rnd()%22; if(tt<21)s.n[tt]++;}
    int mis;double cur=score(&s,&mis),T0=0.3;
    for(long it=0;it<IT;it++){double T=T0*(1-(double)it/IT)+1e-4;St o=s;
      int mv=rnd()%3;
      if(mv==0){int w=rnd()%6;s.pin[w][rnd()%PER[w]]^=1;}
      else if(mv==1){int a=rnd()%21,b=rnd()%22; if(s.n[a]>0){s.n[a]--; if(b<21)s.n[b]++;}}
      else {int a=rnd()%21; int tot=0;for(int k=0;k<21;k++)tot+=s.n[k]; if(tot<27)s.n[a]++; else continue;}
      int m2;double nw=score(&s,&m2);
      if(nw>=cur||urand()<exp((nw-cur)/T)){cur=nw;mis=m2;}else s=o;}
    if(cur>gbest){gbest=cur;gb=s;gm=mis;}
  }
  int pt[N];dec(&gb,pt);char o[N+1];for(int i=0;i<N;i++)o[i]=pt[i]+65;o[N]=0;
  int lug=0;for(int k=0;k<21;k++)lug+=gb.n[k];
  printf("best %.3f crib_mismatch %d quad %.3f lugs %d %s\n",gbest,gm,gbest+cribw*gm,lug,o);
  return 0;}
