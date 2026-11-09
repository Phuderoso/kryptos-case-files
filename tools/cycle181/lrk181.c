/* Cycle 181 (IDEAS I-156): ONE-ERROR audit of case 168. Linear-recurrence key mod 26 over KEYED (Quagmire I/II/III) alphabets
   behind the 165,782 K3-law decimations / routes, with ONE of the 24 crib key values allowed to be wrong (a mis-carved letter at
   that slot's carved position, or a wrong crib letter): that slot's key value is a free unknown.
   Family, alphabets, types and forms exactly as lrk180.c (case 168): k[i] = c1 k[i-1] + ... + cL k[i-L] + d (mod 26), arbitrary c,
   d, seed; ty 0 q1 (A keyed, B = A-Z), ty 1 q2 (A = A-Z, B keyed), ty 2 q3 (A = B keyed); Vig k = B(c) - A(p), Beau k = B(c) + A(p).
   Exactness via CRT (case 167): slot t free fits mod 26 iff some v2 makes the GF(2) system pass AND some v13 makes the GF(13)
   system pass, for the SAME t.
   mode 0 (key on the plaintext index): the case-168 2^24 mod-2 table T (per L) is dilated to Hamming distance 1:
     T1[id] = T[id] | OR_t T[id ^ (1<<t)]. Per (perm, alphabet, type) one lookup in T1; survivors get their allowed slot set
     (all 24 if T[id] passes strictly, else {t : T[id^(1<<t)]}), then per form, per allowed slot, v13 in 0..12 through lr178's
     GF(13) solve0. A strict fit (mod 2 and mod 13 strict) is a fit at every slot and is reported once (t -1).
   mode 1 (key on the carved index, seed at carved 0..L-1): the 2^(2L+1) mod-2 streams projected on the 24 crib carved positions
     (pext) are inserted into a per-thread 2^24 bitset together with their 24 one-bit neighbours; per (alphabet, type) one lookup;
     survivors: allowed slots from the streams within distance 1; GF(13): for each c mod 13, the 24 rows (seed, d linear) are
     eliminated; if inconsistent, each allowed slot's row is left out in turn.
   usage: lrk181 CT perms.bin alphafile label qlo qhi mode Lmin Lmax
   output: H lines (per L x type x form: perms, pairs, mod-2 one-error passes, fits, strict fits, fitting slots), M lines (fits:
     slot t, wildcard value, solution lists), O (overflow), X (table/solve0 disagreement, must never appear), END            */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <immintrin.h>
#define N 97
#ifndef SAFE
#define SAFE 0   /* -DSAFE=1: no early-row shortcut in mode 1, no block-2 shortcut in mode 0 (audit build) */
#endif
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char*PT="EASTNORTHEASTBERLINCLOCK";
static int inv13[13];
static int md(int a,int p){a%=p;return a<0?a+p:a;}
static int NA; static int (*IDX)[26]; static char (*LAB)[64]; static uint32_t *PAR; static int *isAZ;
static const char*TY[3]={"q1","q2","q3"};
#define MAXS 16
typedef struct{int n;int sol[MAXS][16];long tot;int ovf;}SolSet;
/* lr178.c / lrk180.c solve0 algebra; skip = plaintext index (63..73) of a block-2 slot whose key value is free (-1 = none):
   the block-2 in-block rows that contain it are dropped and the propagation check ignores it (exact: propagation from block 1
   determines block 2, so 'free value at slot skip' <=> 'match the other block-2 slots'; the free value is then s[skip]) */
static void solve0s(int p,int L,const int*kk,SolSet*S,int skip){
  int n=L+1,A[24][17],nr=0;S->n=0;S->tot=0;S->ovf=0;
  for(int i=21+L;i<=33;i++){for(int j=1;j<=L;j++)A[nr][j-1]=kk[i-j-21];A[nr][L]=1;A[nr][n]=kk[i-21];nr++;}
  for(int i=63+L;i<=73;i++){if(skip>=0&&i>=skip&&i<=skip+L)continue;for(int j=1;j<=L;j++)A[nr][j-1]=kk[i-j-21];A[nr][L]=1;A[nr][n]=kk[i-21];nr++;}
  int piv[17],rk=0;for(int col=0;col<n&&rk<nr;col++){int r=-1;for(int i=rk;i<nr;i++)if(A[i][col]%p){r=i;break;}if(r<0)continue;
    if(r!=rk)for(int j=0;j<=n;j++){int t=A[r][j];A[r][j]=A[rk][j];A[rk][j]=t;}
    int iv=p==2?1:inv13[A[rk][col]%p];for(int j=0;j<=n;j++)A[rk][j]=(A[rk][j]*iv)%p;
    for(int i=0;i<nr;i++)if(i!=rk&&A[i][col]%p){int f=A[i][col];for(int j=0;j<=n;j++)A[i][j]=md(A[i][j]-f*A[rk][j],p);}
    piv[rk++]=col;}
  for(int i=rk;i<nr;i++)if(A[i][n]%p)return;
  int isp[17]={0};for(int r=0;r<rk;r++)isp[piv[r]]=1;int fr[17],nf=0;for(int j=0;j<n;j++)if(!isp[j])fr[nf++]=j;
  long ns=1;for(int i=0;i<nf;i++){ns*=p;if(ns>5000000){S->ovf=1;return;}}
  for(long z=0;z<ns;z++){int x[17];long y=z;for(int i=0;i<nf;i++){x[fr[i]]=y%p;y/=p;}
    for(int r=0;r<rk;r++){int v=A[r][n];for(int i=0;i<nf;i++)v-=A[r][fr[i]]*x[fr[i]];x[piv[r]]=md(v,p);}
    int s[53];memcpy(s,kk,13*sizeof(int));int ok=1;
    for(int i=34;i<=73&&ok;i++){int v=x[L];for(int j=1;j<=L;j++)v+=x[j-1]*s[i-j-21];v%=p;s[i-21]=v;if(i>=63&&i!=skip&&v!=kk[i-21])ok=0;}
    if(!ok)continue;S->tot++;if(S->n<MAXS){memcpy(S->sol[S->n],x,n*sizeof(int));if(skip>=0)S->sol[S->n][n]=s[skip-21];S->n++;}}
}
static void solve0(int p,int L,const int*kk,SolSet*S){solve0s(p,L,kk,S,-1);}
static unsigned char*T13; static long n13c;
static void build13(int L){n13c=1;for(int i=0;i<L;i++)n13c*=13;T13=malloc(n13c*(L+1)*N);
  #pragma omp parallel for schedule(static)
  for(long z=0;z<n13c;z++){int c[16];long y=z;for(int i=L-1;i>=0;i--){c[i]=y%13;y/=13;}
    for(int m=0;m<=L;m++){unsigned char*s=T13+(z*(L+1)+m)*N;for(int j=0;j<L;j++)s[j]=(m==j);
      for(int j=L;j<N;j++){int v=(m==L);for(int a=1;a<=L;a++)v+=c[a-1]*s[j-a];s[j]=v%13;}}}}
/* GF(13) consistency of the 24 rows (weight table B), leaving out row `skip` (-1 none); identical to lr179 cons13 */
static int cons13(const unsigned char*B,int L,const int*J,const int*ko13,int skip,int*xout,int*nul){
  int R[17][18],rk=0,pc[17];
  for(int t=0;t<24;t++){if(t==skip)continue;int row[18];for(int m=0;m<=L;m++)row[m]=B[m*N+J[t]];row[L+1]=ko13[t];
    for(int r=0;r<rk;r++){int f=row[pc[r]];if(f)for(int m=0;m<=L+1;m++)row[m]=(row[m]+169-f*R[r][m])%13;}
    int cc=-1;for(int m=0;m<=L;m++)if(row[m]){cc=m;break;}
    if(cc<0){if(row[L+1])return -1-t;continue;}
    int iv=inv13[row[cc]];for(int m=0;m<=L+1;m++)row[m]=row[m]*iv%13;
    for(int r=0;r<rk;r++){int f=R[r][cc];if(f)for(int m=0;m<=L+1;m++)R[r][m]=(R[r][m]+169-f*row[m])%13;}
    memcpy(R[rk],row,sizeof row);pc[rk++]=cc;}
  if(xout){for(int m=0;m<=L;m++)xout[m]=0;for(int r=0;r<rk;r++)xout[pc[r]]=R[r][L+1];*nul=L+1-rk;}
  return 1;}   /* returns 1 if consistent, else -1-(index of the first row that made it inconsistent): leaving out a later row
                  cannot repair it, so the one-error loop only tries slots up to that row (exact) */
static inline int kval(int a,int ty,int fm,int cl,int t){int pl=PT[t]-'A';
  int ci=(ty==0)?cl:IDX[a][cl], pi=(ty==1)?pl:IDX[a][pl]; return md(fm?ci+pi:ci-pi,26);}
static int crt(int a2,int a13){return (13*a2+14*a13)%26;}
static int prsol(char*b,const SolSet*S,int L,int cap){int o=0;for(int s=0;s<S->n&&s<cap;s++){o+=sprintf(b+o," ");for(int j=0;j<=L;j++)o+=sprintf(b+o,"%d%s",S->sol[s][j],j<L?",":"");}return o;}
int main(int argc,char**argv){
  setvbuf(stdout,NULL,_IOLBF,0);
  if(argc<10){fprintf(stderr,"usage\n");return 1;}
  const char*Cs=argv[1];if(strlen(Cs)!=N)return 1;int C[N];for(int i=0;i<N;i++)C[i]=Cs[i]-'A';
  const char*lab=argv[4];long qlo=atol(argv[5]),qhi=atol(argv[6]);int mode=atoi(argv[7]),Lmin=atoi(argv[8]),Lmax=atoi(argv[9]);
  if(Lmin<1||Lmax>8||(mode==1&&Lmax>4)){fprintf(stderr,"L range\n");return 1;}
  for(int a=1;a<13;a++)for(int b=1;b<13;b++)if(a*b%13==1)inv13[a]=b;
  {FILE*f=fopen(argv[3],"r");char al[64],lb[64];int cap=1024;IDX=malloc(cap*sizeof*IDX);LAB=malloc(cap*sizeof*LAB);NA=0;
   while(fscanf(f,"%63s %63s",al,lb)==2){if(NA==cap){cap*=2;IDX=realloc(IDX,cap*sizeof*IDX);LAB=realloc(LAB,cap*sizeof*LAB);}
     if(strlen(al)!=26){fprintf(stderr,"bad alphabet\n");return 1;}int seen=0;for(int i=0;i<26;i++){IDX[NA][al[i]-'A']=i;seen|=1<<(al[i]-'A');}
     if(seen!=(1<<26)-1){fprintf(stderr,"not a permutation\n");return 1;}strcpy(LAB[NA],lb);NA++;}fclose(f);
   PAR=malloc(NA*4);isAZ=malloc(NA*sizeof(int));
   for(int a=0;a<NA;a++){PAR[a]=0;isAZ[a]=1;for(int l=0;l<26;l++){if(IDX[a][l]&1)PAR[a]|=1u<<l;if(IDX[a][l]!=l)isAZ[a]=0;}}}
  FILE*pf=fopen(argv[2],"rb");fseek(pf,0,SEEK_END);long np=ftell(pf)/(2*N);rewind(pf);
  short*P=malloc(np*N*2);if(fread(P,2,np*N,pf)!=(size_t)(np*N))return 2;fclose(pf);if(qhi>np)qhi=np;
  long ncfg=0;for(int a=0;a<NA;a++)ncfg+=isAZ[a]?1:3;
  long long FIT[9][3][2]={{{0}}},STR[9][3][2]={{{0}}},SLF[9][3][2]={{{0}}},P2[9][3]={{0}},OVF=0,XM=0;
  if(mode==0){
    uint8_t*T=calloc(1<<24,1);
    for(int L=Lmin;L<=Lmax;L++){
      #pragma omp parallel for schedule(dynamic,64)
      for(int b1=0;b1<8192;b1++){int k[53];for(int i=0;i<13;i++)k[i]=(b1>>i)&1;
        for(int x=0;x<(1<<(L+1));x++){int d=(x>>L)&1,ok=1;
          for(int i=21+L;i<=33&&ok;i++){int v=d;for(int j=1;j<=L;j++)if((x>>(j-1))&1)v^=k[i-j-21];if(v!=k[i-21])ok=0;}
          if(!ok)continue;int s[53];memcpy(s,k,13*sizeof(int));int b2=0;
          for(int i=34;i<=73;i++){int v=d;for(int j=1;j<=L;j++)if((x>>(j-1))&1)v^=s[i-j-21];s[i-21]=v;if(i>=63&&v)b2|=1<<(i-63);}
          uint32_t id=(uint32_t)b1|((uint32_t)b2<<13);
          __atomic_fetch_or(&T[id],(uint8_t)(1<<(L-1)),__ATOMIC_RELAXED);}}}
    uint8_t*T1=malloc(1<<24);
    #pragma omp parallel for schedule(static)
    for(long id=0;id<(1L<<24);id++){uint8_t v=T[id];for(int t=0;t<24;t++)v|=T[id^(1u<<t)];T1[id]=v;}
    uint32_t ptpAZ=0;for(int t=0;t<24;t++)if((PT[t]-'A')&1)ptpAZ|=1u<<t;
    uint32_t*PTP=malloc(NA*4);for(int a=0;a<NA;a++){PTP[a]=0;for(int t=0;t<24;t++)if(IDX[a][PT[t]-'A']&1)PTP[a]|=1u<<t;}
    #pragma omp parallel
    { long long fit[9][3][2]={{{0}}},str[9][3][2]={{{0}}},slf[9][3][2]={{{0}}},p2[9][3]={{0}},ovf=0,xm=0;
      #pragma omp for schedule(dynamic,16)
      for(long q=qlo;q<qhi;q++){const short*S=P+q*N;int cl[24];uint32_t lm[26]={0};int dl[24],nd=0;
        for(int t=0;t<24;t++){cl[t]=C[S[CI[t]]];if(!lm[cl[t]])dl[nd++]=cl[t];lm[cl[t]]|=1u<<t;}
        uint32_t cpAZ=0;for(int j=0;j<nd;j++)if(dl[j]&1)cpAZ^=lm[dl[j]];
        for(int a=0;a<NA;a++){uint32_t pb=PAR[a],cp=0;for(int j=0;j<nd;j++)cp^=lm[dl[j]]&(0u-((pb>>dl[j])&1u));
          for(int ty=0;ty<3;ty++){if(isAZ[a]&&ty<2)continue;
            uint32_t bits=ty==0?cpAZ^PTP[a]:ty==1?cp^ptpAZ:cp^PTP[a];
            int lmask=T1[bits];if(!lmask)continue;
            for(int L=Lmin;L<=Lmax;L++){if(!((lmask>>(L-1))&1))continue;p2[L][ty]++;
              int st2=(T[bits]>>(L-1))&1;uint32_t A2=0;   /* slots whose bit may flip */
              for(int t=0;t<24;t++)if((T[bits^(1u<<t)]>>(L-1))&1)A2|=1u<<t;
              for(int fm=0;fm<2;fm++){int ko[24],k13[53]={0};
                for(int t=0;t<24;t++){ko[t]=kval(a,ty,fm,cl[t],t);k13[CI[t]-21]=ko[t]%13;}
                SolSet B;solve0(13,L,k13,&B);if(B.ovf)ovf++;int st13=B.tot>0;
                char buf[16384];int o=0,nslot=0,isstrict=0;
                if(st2&&st13){isstrict=1;nslot=24;
                  int k2[53]={0};for(int t=0;t<24;t++)k2[CI[t]-21]=ko[t]&1;SolSet A;solve0(2,L,k2,&A);
                  if(!A.tot){xm++;
                    #pragma omp critical
                    printf("X %s strict mismatch q %ld a %d ty %d L %d\n",lab,q,a,ty,L);}
                  o+=sprintf(buf+o,"M %s 0 %d %s %s %ld %s t -1 slot -1 V -1 n2 %ld n13 %ld S2",lab,L,TY[ty],fm?"beau":"vig",q,LAB[a],A.tot,B.tot);
                  o+=prsol(buf+o,&A,L,8);o+=sprintf(buf+o," S13");o+=prsol(buf+o,&B,L,8);o+=sprintf(buf+o,"\n");}
                else for(int t=0;t<24;t++){
                  int ok2[2];int ob=ko[t]&1;ok2[ob]=st2;ok2[ob^1]=(A2>>t)&1;if(!ok2[0]&&!ok2[1])continue;
                  int sl=CI[t]-21,orig=k13[sl],got=0;
                  if(t>=13&&!SAFE){SolSet Bv;solve0s(13,L,k13,&Bv,CI[t]);if(Bv.ovf)ovf++;if(!Bv.tot)continue;
                    int k2[53]={0};for(int u=0;u<24;u++)k2[CI[u]-21]=ko[u]&1;SolSet A;solve0s(2,L,k2,&A,CI[t]);
                    if(!A.tot){xm++;
                      #pragma omp critical
                      printf("X %s block2 mismatch q %ld a %d ty %d L %d t %d\n",lab,q,a,ty,L,t);continue;}
                    got=1;if(o<14000){o+=sprintf(buf+o,"M %s 0 %d %s %s %ld %s t %d slot %d V -2 n2 %ld n13 %ld S2",lab,L,TY[ty],fm?"beau":"vig",q,LAB[a],t,CI[t],A.tot,Bv.tot);
                      o+=prsol(buf+o,&A,L,8);o+=sprintf(buf+o," S13");o+=prsol(buf+o,&Bv,L,8);o+=sprintf(buf+o,"\n");}
                    nslot++;continue;}
                  for(int v=0;v<13;v++){SolSet Bv;if(v==orig){if(!st13)continue;Bv=B;}else{k13[sl]=v;solve0(13,L,k13,&Bv);k13[sl]=orig;if(Bv.ovf)ovf++;if(!Bv.tot)continue;}
                    for(int v2=0;v2<2;v2++){if(!ok2[v2])continue;if(v2==ob&&v==orig)continue;   /* = strict, handled above */
                      int k2[53]={0};for(int u=0;u<24;u++)k2[CI[u]-21]=ko[u]&1;k2[sl]=v2;SolSet A;solve0(2,L,k2,&A);
                      if(!A.tot){xm++;
                        #pragma omp critical
                        printf("X %s slot mismatch q %ld a %d ty %d L %d t %d\n",lab,q,a,ty,L,t);continue;}
                      got=1;if(o<14000){o+=sprintf(buf+o,"M %s 0 %d %s %s %ld %s t %d slot %d V %d n2 %ld n13 %ld S2",lab,L,TY[ty],fm?"beau":"vig",q,LAB[a],t,CI[t],crt(v2,v),A.tot,Bv.tot);
                        o+=prsol(buf+o,&A,L,8);o+=sprintf(buf+o," S13");o+=prsol(buf+o,&Bv,L,8);o+=sprintf(buf+o,"\n");}}}
                  nslot+=got;}
                if(nslot){fit[L][ty][fm]++;slf[L][ty][fm]+=nslot;str[L][ty][fm]+=isstrict;
                  #pragma omp critical
                  fputs(buf,stdout);}}}}}}
      #pragma omp critical
      {for(int L=0;L<9;L++)for(int ty=0;ty<3;ty++){P2[L][ty]+=p2[L][ty];for(int fm=0;fm<2;fm++){FIT[L][ty][fm]+=fit[L][ty][fm];STR[L][ty][fm]+=str[L][ty][fm];SLF[L][ty][fm]+=slf[L][ty][fm];}}OVF+=ovf;XM+=xm;}
    }
  } else {
    long n2[5]={0};uint64_t*S2[5]={0};
    for(int L=Lmin;L<=Lmax;L++){n2[L]=1L<<(2*L+1);S2[L]=malloc(n2[L]*16);
      for(long z=0;z<n2[L];z++){int c=z&((1<<L)-1),sd=(z>>L)&((1<<L)-1),d=(z>>(2*L))&1;int s[N];
        for(int j=0;j<L;j++)s[j]=(sd>>j)&1;for(int j=L;j<N;j++){int v=d;for(int a=1;a<=L;a++)if((c>>(a-1))&1)v^=s[j-a];s[j]=v;}
        uint64_t lo=0,hi=0;for(int j=0;j<N;j++)if(s[j]){if(j<64)lo|=1ULL<<j;else hi|=1ULL<<(j-64);}S2[L][2*z]=lo;S2[L][2*z+1]=hi;}}
    unsigned char*T13L[5]={0};long n13L[5]={0};
    for(int L=Lmin;L<=Lmax;L++){build13(L);T13L[L]=T13;n13L[L]=n13c;}
    #pragma omp parallel
    { long long fit[9][3][2]={{{0}}},str[9][3][2]={{{0}}},slf[9][3][2]={{{0}}},p2[9][3]={{0}};uint64_t*BS=calloc(1<<18,8);uint32_t*proj[5];
      for(int L=Lmin;L<=Lmax;L++)proj[L]=malloc(n2[L]*4);
      #pragma omp for schedule(dynamic,16)
      for(long q=qlo;q<qhi;q++){const short*S=P+q*N;int J[24],cl[24];uint64_t Mlo=0,Mhi=0;
        for(int t=0;t<24;t++){J[t]=S[CI[t]];cl[t]=C[J[t]];if(J[t]<64)Mlo|=1ULL<<J[t];else Mhi|=1ULL<<(J[t]-64);}
        int sh=__builtin_popcountll(Mlo);int r[24],rinv[24];
        for(int t=0;t<24;t++){r[t]=J[t]<64?__builtin_popcountll(Mlo&((1ULL<<J[t])-1)):sh+__builtin_popcountll(Mhi&((1ULL<<(J[t]-64))-1));rinv[r[t]]=t;}
        for(int L=Lmin;L<=Lmax;L++)for(long z=0;z<n2[L];z++){uint32_t v=(uint32_t)(_pext_u64(S2[L][2*z],Mlo)|(_pext_u64(S2[L][2*z+1],Mhi)<<sh));
          proj[L][z]=v;BS[v>>6]|=1ULL<<(v&63);for(int b=0;b<24;b++){uint32_t w=v^(1u<<b);BS[w>>6]|=1ULL<<(w&63);}}
        uint32_t lm[26]={0},pm[26]={0};int dl[24],nd=0;
        for(int t=0;t<24;t++){if(!lm[cl[t]])dl[nd++]=cl[t];lm[cl[t]]|=1u<<r[t];pm[PT[t]-'A']|=1u<<r[t];}
        static const int PL[13]={'E'-'A','A'-'A','S'-'A','T'-'A','N'-'A','O'-'A','R'-'A','H'-'A','B'-'A','L'-'A','I'-'A','C'-'A','K'-'A'};
        uint32_t cpAZ=0,ptpAZ=0;for(int j=0;j<nd;j++)if(dl[j]&1)cpAZ^=lm[dl[j]];for(int j=0;j<13;j++)if(PL[j]&1)ptpAZ^=pm[PL[j]];
        for(int a=0;a<NA;a++){uint32_t pb=PAR[a],cp=0,pp=0;for(int j=0;j<nd;j++)cp^=lm[dl[j]]&(0u-((pb>>dl[j])&1u));
          for(int j=0;j<13;j++)pp^=pm[PL[j]]&(0u-((pb>>PL[j])&1u));
          for(int ty=0;ty<3;ty++){if(isAZ[a]&&ty<2)continue;
            uint32_t bits=ty==0?cpAZ^pp:ty==1?cp^ptpAZ:cp^pp;
            if(!((BS[bits>>6]>>(bits&63))&1))continue;
            for(int L=Lmin;L<=Lmax;L++){uint32_t T2=0;int st2=0;long ex0=-1,ex2[24];for(int t=0;t<24;t++)ex2[t]=-1;
              for(long z=0;z<n2[L];z++){uint32_t x=proj[L][z]^bits;if(!x){st2=1;if(ex0<0)ex0=z;}
                else if(!(x&(x-1))){int t=rinv[__builtin_ctz(x)];T2|=1u<<t;if(ex2[t]<0)ex2[t]=z;}}
              if(st2)T2=0xFFFFFF;if(!T2)continue;p2[L][ty]++;
              for(int fm=0;fm<2;fm++){int ko13[24];for(int t=0;t<24;t++)ko13[t]=kval(a,ty,fm,cl[t],t)%13;
                uint32_t TT13=0;int st13=0;long nc13=0,exc[24],exs=-1;int exx[24][17],exn[24],exsx[17],exsn=0;for(int t=0;t<24;t++)exc[t]=-1;
                for(long z=0;z<n13L[L];z++){const unsigned char*Bt=T13L[L]+z*(L+1)*N;uint32_t got=0;int xx[17],nn;
                  int rc=cons13(Bt,L,J,ko13,-1,xx,&nn);
                  if(rc==1){got=0xFFFFFF;st13=1;if(exs<0){exs=z;memcpy(exsx,xx,sizeof xx);exsn=nn;}for(int t=0;t<24;t++)if(exc[t]<0){exc[t]=z;memcpy(exx[t],xx,sizeof xx);exn[t]=nn;}}
                  else{int lim=SAFE?23:-1-rc;for(int t=0;t<=lim;t++)if((T2>>t)&1){if(cons13(Bt,L,J,ko13,t,xx,&nn)==1){got|=1u<<t;if(exc[t]<0){exc[t]=z;memcpy(exx[t],xx,sizeof xx);exn[t]=nn;}}}}
                  if(got&T2){nc13++;TT13|=got;}}
                uint32_t F=T2&TT13;if(!F)continue;
                int isstrict=st2&&st13;fit[L][ty][fm]++;slf[L][ty][fm]+=__builtin_popcount(F);str[L][ty][fm]+=isstrict;
                char buf[16384];int o=0;
                if(isstrict){F=1;exc[0]=exs;memcpy(exx[0],exsx,sizeof exsx);exn[0]=exsn;ex2[0]=ex0;}   /* one line, t -1 */
                for(int t=0;t<24;t++)if((F>>t)&1){long z=ex2[t]>=0?ex2[t]:ex0;if(z<0)z=ex0;long c13=exc[t];int c[16];long y=c13;for(int b=L-1;b>=0;b--){c[b]=y%13;y/=13;}
                  o+=sprintf(buf+o,"M %s 1 %d %s %s %ld %s t %d slot %d carved %d strict %d nc13 %ld S2 c",lab,L,TY[ty],fm?"beau":"vig",q,LAB[a],isstrict?-1:t,isstrict?-1:CI[t],isstrict?-1:J[t],isstrict,nc13);
                  for(int b=0;b<L;b++)o+=sprintf(buf+o,"%ld",(z>>b)&1);o+=sprintf(buf+o,"s");for(int b=0;b<L;b++)o+=sprintf(buf+o,"%ld",(z>>(L+b))&1);o+=sprintf(buf+o,"d%ld",(z>>(2*L))&1);
                  o+=sprintf(buf+o," S13 c");for(int b=0;b<L;b++)o+=sprintf(buf+o,"%d%s",c[b],b<L-1?",":"");o+=sprintf(buf+o,"x");
                  for(int m=0;m<=L;m++)o+=sprintf(buf+o,"%d%s",exx[t][m],m<L?",":"");o+=sprintf(buf+o,"n%d\n",exn[t]);if(o>15000)break;}
                #pragma omp critical
                fputs(buf,stdout);}}}}
        for(int L=Lmin;L<=Lmax;L++)for(long z=0;z<n2[L];z++){uint32_t v=proj[L][z];BS[v>>6]=0;for(int b=0;b<24;b++){uint32_t w=v^(1u<<b);BS[w>>6]=0;}}}
      #pragma omp critical
      {for(int L=0;L<9;L++)for(int ty=0;ty<3;ty++){P2[L][ty]+=p2[L][ty];for(int fm=0;fm<2;fm++){FIT[L][ty][fm]+=fit[L][ty][fm];STR[L][ty][fm]+=str[L][ty][fm];SLF[L][ty][fm]+=slf[L][ty][fm];}}}
      free(BS);}
  }
  for(int L=Lmin;L<=Lmax;L++)for(int ty=0;ty<3;ty++)for(int fm=0;fm<2;fm++)
    printf("H %s %d %d %s %s perms %ld pairs %ld pass2 %lld fits %lld strict %lld slotfits %lld\n",lab,mode,L,TY[ty],fm?"beau":"vig",qhi-qlo,ncfg,P2[L][ty],FIT[L][ty][fm],STR[L][ty][fm],SLF[L][ty][fm]);
  printf("O %s overflow %lld mismatch %lld\n",lab,OVF,XM);
  printf("END %s %ld %ld\n",lab,qlo,qhi);return 0;}
