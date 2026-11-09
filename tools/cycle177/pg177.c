/* Cycle 177 (IDEAS I-128): ACA Periodic Gromark (vocabulary keywords, fixed alphabets; cycle 176's cfg) behind the 165,782
   K3-law decimations / routes with AT MOST ONE wrong letter among the 24 crib slots (>= 23/24 exact predictions).
   Fixed alphabets make every crib letter an exact prediction, so one wrong carved letter and one wrong crib letter are the
   same event: one mismatching slot.
   ix 0: key on the plaintext index, then transpose -> join on the 24 predicted letters with slot t masked (24 keys per perm)
   ix 1: transpose first, key on the carved index -> per config, perms bucketed by the carved slot of crib 0 and of crib 1
         (a >= 23/24 fit matches crib 0 or crib 1); bucket-1 hits are taken only where crib 0 misses (no double count).
   usage: pg177 CT perms.bin cfg.txt label ix
   output: H label ix form configs tests strict onlyone ; M label ix form q cfglabel missslot(-1 = strict) ; END */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define N 97
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char*PT="EASTNORTHEASTBERLINCLOCK";
#define HB 23
static uint64_t *HA,*HBk;static int *Hhead,*nxt;static unsigned char*used;
static long hslot(uint64_t a,uint64_t b){uint64_t h=((a*0x9E3779B97F4A7C15ULL)^(b*0xC2B2AE3D27D4EB4FULL))>>(64-HB);
  while(used[h]&&!(HA[h]==a&&HBk[h]==b))h=(h+1)&((1u<<HB)-1);return (long)h;}
static void pack(const int*x,int drop,uint64_t*a,uint64_t*b){uint64_t A=0,B=0;for(int t=0;t<24;t++){uint64_t v=(t==drop)?31:x[t];if(t<12)A|=v<<(5*t);else B|=v<<(5*(t-12));}*a=A;*b=B;}
int main(int argc,char**argv){
  setvbuf(stdout,NULL,_IOLBF,0);if(argc<6)return 1;
  const char*Cs=argv[1];int C[N];for(int i=0;i<N;i++)C[i]=Cs[i]-'A';const char*lab=argv[4];int ix=atoi(argv[5]);
  FILE*pf=fopen(argv[2],"rb");fseek(pf,0,SEEK_END);long np=ftell(pf)/(2*N);rewind(pf);short*P=malloc(np*N*2);
  if(fread(P,2,np*N,pf)!=(size_t)(np*N))return 2;fclose(pf);
  int nc=0,cap=0;char(*cl)[64]=NULL;unsigned char(*CA)[26]=NULL,(*CAI)[26]=NULL,(*PAI)[26]=NULL,(*K)[N]=NULL;
  FILE*f=fopen(argv[3],"r");char l[64],a[64],b[64],k[128];
  while(fscanf(f,"%63s %63s %63s %127s",l,a,b,k)==4){if(nc==cap){cap=cap?cap*2:4096;cl=realloc(cl,cap*64);CA=realloc(CA,cap*26);CAI=realloc(CAI,cap*26);PAI=realloc(PAI,cap*26);K=realloc(K,cap*N);}
    strcpy(cl[nc],l);for(int i=0;i<26;i++){CA[nc][i]=a[i]-'A';CAI[nc][a[i]-'A']=i;PAI[nc][b[i]-'A']=i;}for(int i=0;i<N;i++)K[nc][i]=k[i]-'A';nc++;}
  fclose(f);
  long long fs[2]={0},fo[2]={0};
  unsigned char*TC=malloc(np*24);for(long q=0;q<np;q++)for(int t=0;t<24;t++)TC[q*24+t]=P[q*N+CI[t]];
  if(ix==0){HA=malloc(sizeof(uint64_t)<<HB);HBk=malloc(sizeof(uint64_t)<<HB);Hhead=malloc(sizeof(int)<<HB);used=calloc(1u<<HB,1);nxt=malloc(np*24*sizeof(int));
    for(long q=0;q<np;q++){int x[24];for(int t=0;t<24;t++)x[t]=C[TC[q*24+t]];
      for(int t=0;t<24;t++){uint64_t A,B;pack(x,t,&A,&B);long h=hslot(A,B);if(!used[h]){used[h]=1;HA[h]=A;HBk[h]=B;Hhead[h]=-1;}int id=(int)(q*24+t);nxt[id]=Hhead[h];Hhead[h]=id;}}
    #pragma omp parallel for schedule(dynamic,256) reduction(+:fs[:2],fo[:2])
    for(int c=0;c<nc;c++)for(int fm=0;fm<2;fm++){int x[24];
      for(int t=0;t<24;t++){int p=PAI[c][PT[t]-'A'],kk=K[c][CI[t]];int v=fm?kk-p:p+kk;v=((v%26)+26)%26;x[t]=CA[c][v];}
      int hq[2048],ht[2048],nh=0;
      for(int t=0;t<24;t++){uint64_t A,B;pack(x,t,&A,&B);long h=hslot(A,B);if(!used[h])continue;for(int e=Hhead[h];e>=0;e=nxt[e])if(nh<2048){hq[nh]=e/24;ht[nh]=e%24;nh++;}}
      /* a perm hit under all 24 masks is strict; under exactly one mask t it is a one-error fit with miss t */
      for(int i=0;i<nh;i++){int q=hq[i],cnt=0,first=1;for(int j=0;j<nh;j++)if(hq[j]==q){cnt++;if(j<i)first=0;}
        if(!first)continue;int miss=cnt==24?-1:ht[i];if(cnt!=24&&cnt!=1){fprintf(stderr,"odd count %d\n",cnt);}
        if(miss<0)fs[fm]++;else fo[fm]++;
        #pragma omp critical
        printf("M %s 0 %s %d %s %d\n",lab,fm?"beau":"vig",q,cl[c],miss);}}
  } else {
    int *ord[2],*bst[2];for(int s=0;s<2;s++){bst[s]=calloc(N+1,sizeof(int));ord[s]=malloc(np*sizeof(int));for(long q=0;q<np;q++)bst[s][TC[q*24+s]+1]++;
      for(int j=0;j<N;j++)bst[s][j+1]+=bst[s][j];int fill[N];memcpy(fill,bst[s],N*sizeof(int));for(long q=0;q<np;q++)ord[s][fill[TC[q*24+s]]++]=(int)q;}
    #pragma omp parallel for schedule(dynamic,256) reduction(+:fs[:2],fo[:2])
    for(int c=0;c<nc;c++)for(int fm=0;fm<2;fm++){unsigned char Z[N];int pv[24];
      for(int j=0;j<N;j++){int v=fm?K[c][j]-CAI[c][C[j]]:CAI[c][C[j]]-K[c][j];Z[j]=((v%26)+26)%26;}
      for(int t=0;t<24;t++)pv[t]=PAI[c][PT[t]-'A'];
      for(int s=0;s<2;s++)for(int j=0;j<N;j++){if(Z[j]!=pv[s])continue;
        for(int u=bst[s][j];u<bst[s][j+1];u++){int q=ord[s][u];const unsigned char*tc=TC+(long)q*24;
          if(s==1&&Z[tc[0]]==pv[0])continue;            /* counted in bucket 0 */
          int miss=-1,nm=0;for(int t=0;t<24;t++)if(Z[tc[t]]!=pv[t]){miss=t;if(++nm>1)break;}
          if(nm>1)continue;
          if(nm==0)fs[fm]++;else fo[fm]++;
          #pragma omp critical
          printf("M %s 1 %s %d %s %d\n",lab,fm?"beau":"vig",q,cl[c],miss);}}}
  }
  for(int fm=0;fm<2;fm++)printf("H %s %d %s %d %lld %lld %lld\n",lab,ix,fm?"beau":"vig",nc,(long long)nc*np,fs[fm],fo[fm]);
  printf("END %s\n",lab);return 0;}
