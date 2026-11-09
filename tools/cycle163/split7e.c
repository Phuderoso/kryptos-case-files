/* Cycle 163 (IDEAS I-069): split period-7 key (cycle 162 model, IDEAS I-013) under ONE error, in a single pass.
   Same model as tools/cycle162/split7.c: two period-P keys (default 7), phase from position 0 of the chosen index, key 1
   on positions < b, key 2 on positions >= b, b free 0..97; Quagmire III on every alphabet of alpha.bin; Vigenere or
   Beaufort per segment; direct or behind every bank permutation, both directions, key at plaintext (ix 0) or carved (ix 1)
   index.  One error = leave one of the 24 cribs out (a wrong crib letter or a wrong carved letter under a crib).
   Drop-aware exact method (no 24x loop):
     prefix scan: cribs in increasing x, each compared with the first member of its residue class; the first conflict
     (crib i vs reference f) gives B1s = x_i (b <= B1s).  Any single removal that repairs the prefix must remove i or f,
     so the one-error bound is B1e = max(B1s, first-conflict(list without i), first-conflict(list without f)).
     suffix scan mirrored (reference = last member): B2s = x_i + 1, B2e = min(B2s, ...without i, ...without f).
     Since the dropped crib lies in one segment only, one-error consistent  <=>  B2s <= B1e  or  B2e <= B1s.
   Alphabet-free prefilter: the strict prefilter of split7.c after removing some crib d (or none) must pass.
   usage: split7e CT alpha.bin perms.bin label qlo qhi [P [idonly]]
   Output: S lab q dir ix a m1 m2 B1s B1e B2s B2e   (model S one-error; m 0 Vig, 1 Beau)
           Z lab q dir ix a1 m1 a2 m2 B1s B1e B2s B2e (AZ (0) / KRYPTOS (1) cross, one-error)
           X lab q dir ix maxB1s maxB1e minB2s minB2e (model X one-error, alphabet free per segment)
           H lab ix configs prefilter_pass S_strict_cfg S1e_cfg S1e_hits Z1e_cfg Xstrict_cfg X1e_cfg */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define N 97
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PTS="EASTNORTHEASTBERLINCLOCK";
static int NA,P; static uint8_t *IVT;
typedef struct{int x1,x2,y1,y2,pos,ci,cf;}chk;
static int n,X[24],CC[24],PP[24],R[24];
/* build check list for mode m, direction dirn (0 prefix ascending, 1 suffix descending), excluding crib ex (-1 none) */
static int build(chk*L,int m,int dirn,int ex){int ref[32],nl=0;for(int r=0;r<P;r++)ref[r]=-1;
  for(int s=0;s<n;s++){int i=dirn?n-1-s:s;if(i==ex)continue;int f0=ref[R[i]];if(f0<0){ref[R[i]]=i;continue;}
    if(m==0)L[nl]=(chk){CC[i],PP[f0],CC[f0],PP[i],X[i]+dirn,i,f0};else L[nl]=(chk){CC[i],PP[i],CC[f0],PP[f0],X[i]+dirn,i,f0};nl++;}
  return nl;}
static inline int bad(const chk*c,int a){int d=(int)IVT[c->x1*NA+a]+IVT[c->x2*NA+a]-IVT[c->y1*NA+a]-IVT[c->y2*NA+a];return !(d==0||d==26||d==-26);}
static int *alive;
/* all alphabets: B[a], K[a] = index of conflicting check (255 none) */
static void scan_all(const chk*L,int nl,uint8_t*B,uint8_t*K,uint8_t none){
  if(nl==0){memset(B,none,NA);memset(K,255,NA);return;}
  const uint8_t *a1=IVT+L[0].x1*NA,*a2=IVT+L[0].x2*NA,*b1=IVT+L[0].y1*NA,*b2=IVT+L[0].y2*NA; uint8_t p0=L[0].pos;
  for(int a=0;a<NA;a++){uint8_t s1=a1[a]+a2[a],s2=b1[a]+b2[a];uint8_t ok=(s1==s2)|(s1==(uint8_t)(s2+26))|(s2==(uint8_t)(s1+26));B[a]=ok?none:p0;K[a]=ok?255:0;}
  int na=0;for(int a=0;a<NA;a++)if(K[a]==255)alive[na++]=a;
  for(int k=0;k<na;k++){int a=alive[k];for(int l=1;l<nl;l++)if(bad(&L[l],a)){B[a]=L[l].pos;K[a]=l;break;}}
}
/* subset: returns first-conflict bound into Bo[a] for a in list G */
static void scan_sub(const chk*L,int nl,const int*G,int ng,uint8_t*Bo,uint8_t none){
  if(nl==0){for(int g=0;g<ng;g++)Bo[G[g]]=none;return;}
  if(ng*8>NA){ /* large group: first check vectorised over all alphabets, survivors scalar */
    const uint8_t *a1=IVT+L[0].x1*NA,*a2=IVT+L[0].x2*NA,*b1=IVT+L[0].y1*NA,*b2=IVT+L[0].y2*NA; uint8_t p0=L[0].pos;
    for(int a=0;a<NA;a++){uint8_t s1=a1[a]+a2[a],s2=b1[a]+b2[a];uint8_t ok=(s1==s2)|(s1==(uint8_t)(s2+26))|(s2==(uint8_t)(s1+26));Bo[a]=ok?none:p0;}
    for(int g=0;g<ng;g++){int a=G[g];if(Bo[a]!=none)continue;for(int l=1;l<nl;l++)if(bad(&L[l],a)){Bo[a]=L[l].pos;break;}}
    return;}
  for(int g=0;g<ng;g++){int a=G[g];uint8_t b=none;for(int l=0;l<nl;l++)if(bad(&L[l],a)){b=L[l].pos;break;}Bo[a]=b;}}
static uint8_t *Bs[2][2],*Be[2][2],*Kc,*Tmp; static int *grp,*gcnt,*gst;
/* dirn 0: prefix (none 97, combine max); 1: suffix (none 0, combine min) */
static void onee(int m,int dirn){chk L[24],L2[24];uint8_t none=dirn?0:97;
  int nl=build(L,m,dirn,-1);scan_all(L,nl,Bs[m][dirn],Kc,none);uint8_t*E=Be[m][dirn];memcpy(E,Bs[m][dirn],NA);
  if(nl==0)return;
  /* group 0 (conflict at the first check, ~25/26 of alphabets): vectorised over all alphabets, masked combine */
  for(int w=0;w<2;w++){int ex=w?L[0].cf:L[0].ci;int n2=build(L2,m,dirn,ex);
    if(n2==0){for(int a=0;a<NA;a++)if(Kc[a]==0)E[a]=none;continue;}
    const uint8_t *a1=IVT+L2[0].x1*NA,*a2=IVT+L2[0].x2*NA,*b1=IVT+L2[0].y1*NA,*b2=IVT+L2[0].y2*NA; uint8_t p0=L2[0].pos;
    int na=0;
    for(int a=0;a<NA;a++){uint8_t s1=a1[a]+a2[a],s2=b1[a]+b2[a];uint8_t ok=(s1==s2)|(s1==(uint8_t)(s2+26))|(s2==(uint8_t)(s1+26));
      uint8_t better=dirn?(p0<E[a]):(p0>E[a]);E[a]=(Kc[a]==0&&!ok&&better)?p0:E[a];}
    for(int a=0;a<NA;a++){uint8_t s1=a1[a]+a2[a],s2=b1[a]+b2[a];if(Kc[a]==0&&((s1==s2)|(s1==(uint8_t)(s2+26))|(s2==(uint8_t)(s1+26))))alive[na++]=a;}
    for(int g=0;g<na;g++){int a=alive[g];uint8_t t=none;for(int l=1;l<n2;l++)if(bad(&L2[l],a)){t=L2[l].pos;break;}
      if(dirn?(t<E[a]):(t>E[a]))E[a]=t;}}
  /* groups k >= 1: gathered scalar */
  int ng=0;for(int a=0;a<NA;a++)if(Kc[a]!=255&&Kc[a]!=0)grp[ng++]=a;
  if(!ng)return;
  memset(gcnt,0,sizeof(int)*32);for(int g=0;g<ng;g++)gcnt[Kc[grp[g]]]++;
  gst[0]=0;for(int k=0;k<nl;k++)gst[k+1]=gst[k]+gcnt[k];int pos[32];memcpy(pos,gst,sizeof(int)*nl);
  for(int g=0;g<ng;g++){int a=grp[g];alive[pos[Kc[a]]++]=a;}
  for(int k=1;k<nl;k++){int n_=gst[k+1]-gst[k];if(!n_)continue;const int*G=alive+gst[k];
    for(int w=0;w<2;w++){int ex=w?L[k].cf:L[k].ci;int n2=build(L2,m,dirn,ex);
      for(int g=0;g<n_;g++){int a=G[g];uint8_t t=none;for(int l=0;l<n2;l++)if(bad(&L2[l],a)){t=L2[l].pos;break;}
        if(dirn?(t<E[a]):(t>E[a]))E[a]=t;}}}
}
static int prefilt(int ex){int Bf1=97,Bf2=-1;
  for(int i=0;i<n&&Bf1==97;i++){if(i==ex)continue;for(int j=0;j<i;j++)if(j!=ex&&R[j]==R[i]&&((CC[j]==CC[i])!=(PP[j]==PP[i]))){Bf1=X[i];break;}}
  for(int i=n-1;i>=0&&Bf2==-1;i--){if(i==ex)continue;for(int j=n-1;j>i;j--)if(j!=ex&&R[j]==R[i]&&((CC[j]==CC[i])!=(PP[j]==PP[i]))){Bf2=X[i];break;}}
  return Bf2<Bf1;}
int main(int argc,char**argv){
  if(argc<7){fprintf(stderr,"usage\n");return 1;}
  int C[N];for(int i=0;i<N;i++)C[i]=argv[1][i]-'A';
  FILE*f=fopen(argv[2],"rb");fseek(f,0,2);NA=ftell(f)/26;rewind(f);uint8_t*AL=malloc(NA*26);if(fread(AL,26,NA,f)!=(size_t)NA)return 1;fclose(f);
  IVT=malloc(26*NA);for(int a=0;a<NA;a++)for(int i=0;i<26;i++)IVT[AL[a*26+i]*NA+a]=i;
  for(int m=0;m<2;m++)for(int d=0;d<2;d++){Bs[m][d]=malloc(NA);Be[m][d]=malloc(NA);}
  Kc=malloc(NA);Tmp=malloc(NA);alive=malloc(NA*sizeof(int));grp=malloc(NA*sizeof(int));gcnt=malloc(32*sizeof(int));gst=malloc(32*sizeof(int));
  const char*lab=argv[4];long qlo=atol(argv[5]),qhi=atol(argv[6]);P=argc>7?atoi(argv[7]):7;int idonly=argc>8&&atoi(argv[8]);
  short*Perm;long np;
  if(idonly){np=1;Perm=malloc(N*2);for(int i=0;i<N;i++)Perm[i]=i;qlo=0;qhi=1;}
  else{f=fopen(argv[3],"rb");fseek(f,0,2);np=ftell(f)/(2*N);rewind(f);Perm=malloc(np*N*2);if(fread(Perm,2,np*N,f)!=(size_t)(np*N))return 2;fclose(f);}
  if(qhi>np)qhi=np;
  int pt[24];for(int i=0;i<24;i++)pt[i]=PTS[i]-'A';
  long long H[2][8];memset(H,0,sizeof H);
  for(long q=qlo;q<qhi;q++){const short*s=Perm+q*N;short u[N];for(int i=0;i<N;i++)u[s[i]]=i;
   for(int dir=0;dir<(idonly?1:2);dir++){const short*S=dir?u:s;
    for(int ix=0;ix<(idonly?1:2);ix++){
      int tx[24],tc[24],tp[24];n=24;
      for(int t=0;t<24;t++){int cpos=S[CI[t]];tx[t]=ix?cpos:CI[t];tc[t]=C[cpos];tp[t]=pt[t];}
      int ord[24];for(int i=0;i<n;i++)ord[i]=i;
      for(int i=1;i<n;i++){int k=ord[i],j=i-1;while(j>=0&&tx[ord[j]]>tx[k]){ord[j+1]=ord[j];j--;}ord[j+1]=k;}
      for(int i=0;i<n;i++){X[i]=tx[ord[i]];CC[i]=tc[ord[i]];PP[i]=tp[ord[i]];R[i]=X[i]%P;}
      H[ix][0]++;
      int pass=prefilt(-1);for(int d=0;d<n&&!pass;d++)pass=prefilt(d);
      if(!pass)continue;
      H[ix][1]++;
      for(int m=0;m<2;m++){onee(m,0);onee(m,1);}
      int mx1s=0,mx1e=0,mn2s=255,mn2e=255,sc=0,ss=0,zc=0;
      for(int m=0;m<2;m++){uint8_t x1=0,x2=0,y1=255,y2=255;const uint8_t*p1=Bs[m][0],*p2=Be[m][0],*p3=Bs[m][1],*p4=Be[m][1];
        for(int a=0;a<NA;a++){x1=p1[a]>x1?p1[a]:x1;x2=p2[a]>x2?p2[a]:x2;y1=p3[a]<y1?p3[a]:y1;y2=p4[a]<y2?p4[a]:y2;}
        if(x1>mx1s)mx1s=x1;if(x2>mx1e)mx1e=x2;if(y1<mn2s)mn2s=y1;if(y2<mn2e)mn2e=y2;}
      {int na=0;for(int a=0;a<NA;a++){uint8_t e0=Be[0][1][a],e1=Be[1][1][a],f0=Be[0][0][a],f1=Be[1][0][a];
         uint8_t lo=e0<e1?e0:e1,hi=f0>f1?f0:f1;if(lo<=hi)alive[na++]=a;}
       for(int g=0;g<na;g++){int a=alive[g];
        for(int m1=0;m1<2;m1++)for(int m2=0;m2<2;m2++){
          if(Bs[m2][1][a]<=Bs[m1][0][a])ss++;
          if(Bs[m2][1][a]<=Be[m1][0][a]||Be[m2][1][a]<=Bs[m1][0][a]){sc++;H[ix][4]++;
            printf("S %s %ld %d %d %d %d %d %d %d %d %d\n",lab,q,dir,ix,a,m1,m2,Bs[m1][0][a],Be[m1][0][a],Bs[m2][1][a],Be[m2][1][a]);}}}}
      for(int a1=0;a1<2;a1++)for(int a2=0;a2<2;a2++)if(a1!=a2)for(int m1=0;m1<2;m1++)for(int m2=0;m2<2;m2++)
        if(Bs[m2][1][a2]<=Be[m1][0][a1]||Be[m2][1][a2]<=Bs[m1][0][a1]){zc++;
          printf("Z %s %ld %d %d %d %d %d %d %d %d %d %d\n",lab,q,dir,ix,a1,m1,a2,m2,Bs[m1][0][a1],Be[m1][0][a1],Bs[m2][1][a2],Be[m2][1][a2]);}
      if(ss)H[ix][2]++; if(sc)H[ix][3]++; if(zc)H[ix][5]++; if(mn2s<=mx1s)H[ix][6]++;
      if(mn2s<=mx1e||mn2e<=mx1s){H[ix][7]++;printf("X %s %ld %d %d %d %d %d %d\n",lab,q,dir,ix,mx1s,mx1e,mn2s,mn2e);}
    }}}
  for(int ix=0;ix<2;ix++)if(H[ix][0])printf("H %s %d %lld %lld %lld %lld %lld %lld %lld %lld\n",lab,ix,H[ix][0],H[ix][1],H[ix][2],H[ix][3],H[ix][4],H[ix][5],H[ix][6],H[ix][7]);
  return 0;}
