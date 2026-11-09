/* Cycle 176 (IDEAS I-125, I-053 transposition part, strict): ACA Periodic Gromark with vocabulary keywords behind the 165,782
   K3-law decimations / routes. Config = (keyword, CA variant, PA) from mkcfg176.py cfg: full key stream k[0..96] (group offset +
   chain-added digit, mod 26) and fully specified alphabets, so every crib letter is an exact prediction.
     vig (ACA): ct = CA[(PA(p) + k) mod 26]      beau: ct = CA[(k - PA(p)) mod 26]
   ix 0: key on the plaintext index, then transpose (ct of crib t carved at S[CI[t]])  -> exact 24-letter join
   ix 1: transpose first, key on the carved index j = S[CI[t]]                        -> per config, perms bucketed by S[CI[0]]
   usage: pg176 CT perms.bin cfg.txt label ix     output: H label ix form configs tests fits ; M label ix form q cfglabel ; END */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define N 97
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char*PT="EASTNORTHEASTBERLINCLOCK";
#define HB 20
static uint64_t HA[1<<HB],HBk[1<<HB];static int Hhead[1<<HB],used[1<<HB],*nxt;
static int hslot(uint64_t a,uint64_t b){uint64_t h=((a*0x9E3779B97F4A7C15ULL)^(b*0xC2B2AE3D27D4EB4FULL))>>(64-HB);
  while(used[h]&&!(HA[h]==a&&HBk[h]==b))h=(h+1)&((1u<<HB)-1);return (int)h;}
static void pack(const int*x,uint64_t*a,uint64_t*b){uint64_t A=0,B=0;for(int t=0;t<24;t++){uint64_t v=x[t];if(t<12)A|=v<<(5*t);else B|=v<<(5*(t-12));}*a=A;*b=B;}
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
  long long fits[2]={0};
  unsigned char*TC=malloc(np*24);for(long q=0;q<np;q++)for(int t=0;t<24;t++)TC[q*24+t]=P[q*N+CI[t]];
  if(ix==0){nxt=malloc(np*sizeof(int));
    for(long q=0;q<np;q++){int x[24];for(int t=0;t<24;t++)x[t]=C[TC[q*24+t]];uint64_t A,B;pack(x,&A,&B);int h=hslot(A,B);
      if(!used[h]){used[h]=1;HA[h]=A;HBk[h]=B;Hhead[h]=-1;}nxt[q]=Hhead[h];Hhead[h]=(int)q;}
    for(int c=0;c<nc;c++)for(int fm=0;fm<2;fm++){int x[24];
      for(int t=0;t<24;t++){int p=PAI[c][PT[t]-'A'],kk=K[c][CI[t]];int v=fm?kk-p:p+kk;v=((v%26)+26)%26;x[t]=CA[c][v];}
      uint64_t A,B;pack(x,&A,&B);int h=hslot(A,B);if(!used[h])continue;
      for(int e=Hhead[h];e>=0;e=nxt[e]){fits[fm]++;printf("M %s 0 %s %d %s\n",lab,fm?"beau":"vig",e,cl[c]);}}
  } else {
    /* bucket perms by carved position of crib 0 */
    int *bst=calloc(N+1,sizeof(int)),*ord=malloc(np*sizeof(int));for(long q=0;q<np;q++)bst[TC[q*24]+1]++;
    for(int j=0;j<N;j++)bst[j+1]+=bst[j];int*fill=malloc(N*sizeof(int));memcpy(fill,bst,N*sizeof(int));for(long q=0;q<np;q++)ord[fill[TC[q*24]]++]=(int)q;
    #pragma omp parallel for schedule(dynamic,256) reduction(+:fits[:2])
    for(int c=0;c<nc;c++)for(int fm=0;fm<2;fm++){unsigned char Z[N];int pv[24];
      for(int j=0;j<N;j++){int v=fm?K[c][j]-CAI[c][C[j]]:CAI[c][C[j]]-K[c][j];Z[j]=((v%26)+26)%26;}
      for(int t=0;t<24;t++)pv[t]=PAI[c][PT[t]-'A'];
      for(int j=0;j<N;j++){if(Z[j]!=pv[0])continue;
        for(int u=bst[j];u<bst[j+1];u++){const unsigned char*tc=TC+(long)ord[u]*24;int ok=1;for(int t=1;t<24;t++)if(Z[tc[t]]!=pv[t]){ok=0;break;}
          if(ok){fits[fm]++;
            #pragma omp critical
            printf("M %s 1 %s %d %s\n",lab,fm?"beau":"vig",ord[u],cl[c]);}}}}
  }
  for(int fm=0;fm<2;fm++)printf("H %s %d %s %d %lld %lld\n",lab,ix,fm?"beau":"vig",nc,(long long)nc*np,fits[fm]);
  printf("END %s\n",lab);return 0;}
