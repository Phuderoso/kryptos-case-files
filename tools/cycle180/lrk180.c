/* Cycle 180 (IDEAS I-142): linear-recurrence key mod 26 over KEYED (Quagmire) alphabets behind the 165,782 K3-law decimations /
   routes (all.bin). Key k[i] = c1 k[i-1] + ... + cL k[i-L] + d (mod 26), arbitrary weights c, constant d, any seed.
   Alphabet file: one keyed alphabet per line ("ALPHABET label"; tools/cycle172/mkalpha172.py, 18,776 alphabets = every vocabulary
   word keyed on A-Z (K1/K2 construction) and on the KRYPTOS order, plus A-Z and KA).
   Tableau types (A = plaintext-side alphabet, B = ciphertext-side alphabet; key value = index difference):
     ty 0 Q1: A keyed, B = A-Z      ty 1 Q2: A = A-Z, B keyed      ty 2 Q3: A = B = keyed (the K1/K2 construction)
   Vigenere: c = B[(A.index(p) + k) % 26]  ->  k = B(c) - A(p);  Beaufort: c = B[(k - A.index(p)) % 26]  ->  k = B(c) + A(p).
   Variant (= -Vigenere) and any rotation of either alphabet (k -> k + e) map the affine family onto itself, so they are covered.
   Perm convention as lr178: plaintext position i is carved at S[i].
   mode 0 (ix 0, key on the plaintext index, then transpose; arbitrary seed upstream of 21): CRT. Mod 2 the whole test depends only on
     the 24 key bits; a precomputed 2^24 table (bit 0..12 = k[21..33] mod 2, bit 13..23 = k[63..73] mod 2) holds, per L, whether some
     (c,d) mod 2 satisfies the in-block equations AND propagates block 1 through the gap onto block 2. Bits are built per perm from
     letter masks (24-bit) and per alphabet from its parity mask. Survivors: lr178's GF(13) solve0 (block equations + propagation)
     for each form; fit iff mod 2 and mod 13 both survive (then solve0 mod 2 is rerun to list the solutions).
   mode 1 (ix 1, transpose first, key on the carved index, seed at carved 0..L-1): mod 2, the 2^(2L+1) streams are projected onto the
     24 crib slots' carved positions (pext), stored in a per-thread 2^24 bitset; each (alphabet, type) is one lookup. Survivors: lr178's
     GF(13) loop over c mod 13 with the precomputed basis table (seed, d linear).
   usage: lrk180 CT perms.bin alphafile label qlo qhi mode Lmin Lmax
   output: H lines (per L, type, form: configs, mod-2 passes, fits), M lines (fits), END                                      */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <immintrin.h>
#define N 97
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char*PT="EASTNORTHEASTBERLINCLOCK";
static int inv13[13];
static int md(int a,int p){a%=p;return a<0?a+p:a;}
static int NA; static int (*IDX)[26]; static char (*LAB)[64]; static uint32_t *PAR; static int *isAZ;
static const char*TY[3]={"q1","q2","q3"};
#define MAXS 64
typedef struct{int n;int sol[MAXS][16];long tot;int ovf;}SolSet;
static void solve0(int p,int L,const int*kk,SolSet*S){          /* identical algebra to lr178.c solve0 */
  int n=L+1,A[24][17],nr=0;S->n=0;S->tot=0;S->ovf=0;
  for(int i=21+L;i<=33;i++){for(int j=1;j<=L;j++)A[nr][j-1]=kk[i-j-21];A[nr][L]=1;A[nr][n]=kk[i-21];nr++;}
  for(int i=63+L;i<=73;i++){for(int j=1;j<=L;j++)A[nr][j-1]=kk[i-j-21];A[nr][L]=1;A[nr][n]=kk[i-21];nr++;}
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
    for(int i=34;i<=73&&ok;i++){int v=x[L];for(int j=1;j<=L;j++)v+=x[j-1]*s[i-j-21];v%=p;s[i-21]=v;if(i>=63&&v!=kk[i-21])ok=0;}
    if(!ok)continue;S->tot++;if(S->n<MAXS){memcpy(S->sol[S->n],x,n*sizeof(int));S->n++;}}
}
static unsigned char*T13; static long n13c;
static void build13(int L){n13c=1;for(int i=0;i<L;i++)n13c*=13;free(T13);T13=malloc(n13c*(L+1)*N);
  #pragma omp parallel for schedule(static)
  for(long z=0;z<n13c;z++){int c[16];long y=z;for(int i=L-1;i>=0;i--){c[i]=y%13;y/=13;}
    for(int m=0;m<=L;m++){unsigned char*s=T13+(z*(L+1)+m)*N;for(int j=0;j<L;j++)s[j]=(m==j);
      for(int j=L;j<N;j++){int v=(m==L);for(int a=1;a<=L;a++)v+=c[a-1]*s[j-a];s[j]=v%13;}}}}
/* key value at slot t for alphabet a, type ty, form fm, carved letter cl */
static inline int kval(int a,int ty,int fm,int cl,int t){int pl=PT[t]-'A';
  int ci=(ty==0)?cl:IDX[a][cl], pi=(ty==1)?pl:IDX[a][pl]; return md(fm?ci+pi:ci-pi,26);}
int main(int argc,char**argv){
  setvbuf(stdout,NULL,_IOLBF,0);
  if(argc<10){fprintf(stderr,"usage\n");return 1;}
  const char*Cs=argv[1];if(strlen(Cs)!=N)return 1;int C[N];for(int i=0;i<N;i++)C[i]=Cs[i]-'A';
  const char*lab=argv[4];long qlo=atol(argv[5]),qhi=atol(argv[6]);int mode=atoi(argv[7]),Lmin=atoi(argv[8]),Lmax=atoi(argv[9]);
  if(Lmin<1||Lmax>8||(mode==1&&Lmax>4)){fprintf(stderr,"L range\n");return 1;}
  for(int a=1;a<13;a++)for(int b=1;b<13;b++)if(a*b%13==1)inv13[a]=b;
  /* alphabets */
  {FILE*f=fopen(argv[3],"r");char al[64],lb[64];int cap=1024;IDX=malloc(cap*sizeof*IDX);LAB=malloc(cap*sizeof*LAB);NA=0;
   while(fscanf(f,"%63s %63s",al,lb)==2){if(NA==cap){cap*=2;IDX=realloc(IDX,cap*sizeof*IDX);LAB=realloc(LAB,cap*sizeof*LAB);}
     if(strlen(al)!=26){fprintf(stderr,"bad alphabet\n");return 1;}int seen=0;for(int i=0;i<26;i++){IDX[NA][al[i]-'A']=i;seen|=1<<(al[i]-'A');}
     if(seen!=(1<<26)-1){fprintf(stderr,"not a permutation\n");return 1;}strcpy(LAB[NA],lb);NA++;}fclose(f);
   PAR=malloc(NA*4);isAZ=malloc(NA*sizeof(int));
   for(int a=0;a<NA;a++){PAR[a]=0;isAZ[a]=1;for(int l=0;l<26;l++){if(IDX[a][l]&1)PAR[a]|=1u<<l;if(IDX[a][l]!=l)isAZ[a]=0;}}}
  FILE*pf=fopen(argv[2],"rb");fseek(pf,0,SEEK_END);long np=ftell(pf)/(2*N);rewind(pf);
  short*P=malloc(np*N*2);if(fread(P,2,np*N,pf)!=(size_t)(np*N))return 2;fclose(pf);if(qhi>np)qhi=np;
  long ncfg=0;for(int a=0;a<NA;a++)ncfg+=isAZ[a]?1:3;   /* (alphabet,type) pairs per perm; A-Z counted once (all types coincide) */
  uint32_t PARAZ=0;for(int l=0;l<26;l++)if(l&1)PARAZ|=1u<<l;
  long long FIT[9][3][2]={{{0}}},P2[9][3]={{0}},OVF=0;
  if(mode==0){
    uint8_t*T=calloc(1<<24,1);uint64_t*B=calloc(1<<18,8);
    for(int L=Lmin;L<=Lmax;L++){
      #pragma omp parallel for schedule(dynamic,64)
      for(int b1=0;b1<8192;b1++){int k[53];for(int i=0;i<13;i++)k[i]=(b1>>i)&1;
        for(int x=0;x<(1<<(L+1));x++){int d=(x>>L)&1,ok=1;
          for(int i=21+L;i<=33&&ok;i++){int v=d;for(int j=1;j<=L;j++)if((x>>(j-1))&1)v^=k[i-j-21];if(v!=k[i-21])ok=0;}
          if(!ok)continue;int s[53];memcpy(s,k,13*sizeof(int));int b2=0;
          for(int i=34;i<=73;i++){int v=d;for(int j=1;j<=L;j++)if((x>>(j-1))&1)v^=s[i-j-21];s[i-21]=v;if(i>=63&&v)b2|=1<<(i-63);}
          uint32_t id=(uint32_t)b1|((uint32_t)b2<<13);
          __atomic_fetch_or(&T[id],(uint8_t)(1<<(L-1)),__ATOMIC_RELAXED);__atomic_fetch_or(&B[id>>6],1ULL<<(id&63),__ATOMIC_RELAXED);}}}
    uint32_t ptpAZ=0;for(int t=0;t<24;t++)if((PT[t]-'A')&1)ptpAZ|=1u<<t;
    uint32_t*PTP=malloc(NA*4);for(int a=0;a<NA;a++){PTP[a]=0;for(int t=0;t<24;t++)if(IDX[a][PT[t]-'A']&1)PTP[a]|=1u<<t;}
    #pragma omp parallel
    { long long fit[9][3][2]={{{0}}},p2[9][3]={{0}},ovf=0;
      #pragma omp for schedule(dynamic,16)
      for(long q=qlo;q<qhi;q++){const short*S=P+q*N;int cl[24];uint32_t lm[26]={0};int dl[24],nd=0;
        for(int t=0;t<24;t++){cl[t]=C[S[CI[t]]];if(!lm[cl[t]])dl[nd++]=cl[t];lm[cl[t]]|=1u<<t;}
        uint32_t cpAZ=0;for(int j=0;j<nd;j++)if(dl[j]&1)cpAZ^=lm[dl[j]];
        for(int a=0;a<NA;a++){uint32_t pb=PAR[a],cp=0;for(int j=0;j<nd;j++)cp^=lm[dl[j]]&(0u-((pb>>dl[j])&1u));
          for(int ty=0;ty<3;ty++){if(isAZ[a]&&ty<2)continue;
            uint32_t bits=ty==0?cpAZ^PTP[a]:ty==1?cp^ptpAZ:cp^PTP[a];
            if(!((B[bits>>6]>>(bits&63))&1))continue;int lmask=T[bits];
            for(int L=Lmin;L<=Lmax;L++){if(!((lmask>>(L-1))&1))continue;p2[L][ty]++;
              for(int fm=0;fm<2;fm++){int k13[53]={0},k2[53]={0};
                for(int t=0;t<24;t++){int v=kval(a,ty,fm,cl[t],t);k13[CI[t]-21]=v%13;k2[CI[t]-21]=v&1;}
                SolSet A13;solve0(13,L,k13,&A13);if(A13.ovf)ovf++;if(!A13.tot)continue;
                SolSet A2;solve0(2,L,k2,&A2);if(!A2.tot){
                  #pragma omp critical
                  printf("X %s table/solve0 mismatch q %ld a %d ty %d L %d\n",lab,q,a,ty,L);
                  continue;}
                fit[L][ty][fm]++;
                char buf[8192];int o=sprintf(buf,"M %s 0 %d %s %s %ld %s %s n2 %ld n13 %ld S2",lab,L,TY[ty],fm?"beau":"vig",q,LAB[a],"-",A2.tot,A13.tot);
                for(int s=0;s<A2.n&&s<32;s++){o+=sprintf(buf+o," ");for(int j=0;j<=L;j++)o+=sprintf(buf+o,"%d%s",A2.sol[s][j],j<L?",":"");}
                o+=sprintf(buf+o," S13");for(int s=0;s<A13.n&&s<32;s++){o+=sprintf(buf+o," ");for(int j=0;j<=L;j++)o+=sprintf(buf+o,"%d%s",A13.sol[s][j],j<L?",":"");}
                #pragma omp critical
                printf("%s\n",buf);}}}}}
      #pragma omp critical
      {for(int L=0;L<9;L++)for(int ty=0;ty<3;ty++){P2[L][ty]+=p2[L][ty];for(int fm=0;fm<2;fm++)FIT[L][ty][fm]+=fit[L][ty][fm];}OVF+=ovf;}
    }
    for(int L=Lmin;L<=Lmax;L++)for(int ty=0;ty<3;ty++)for(int fm=0;fm<2;fm++)
      printf("H %s 0 %d %s %s perms %ld pairs %ld pass2 %lld fits %lld\n",lab,L,TY[ty],fm?"beau":"vig",qhi-qlo,ncfg,P2[L][ty],FIT[L][ty][fm]);
    printf("O %s overflow %lld\n",lab,OVF);
  } else {
    /* streams mod 2 for each L */
    int nL=Lmax-Lmin+1;long n2[5]={0};uint64_t*S2[5]={0};
    for(int L=Lmin;L<=Lmax;L++){n2[L]=1L<<(2*L+1);S2[L]=malloc(n2[L]*16);
      for(long z=0;z<n2[L];z++){int c=z&((1<<L)-1),sd=(z>>L)&((1<<L)-1),d=(z>>(2*L))&1;int s[N];
        for(int j=0;j<L;j++)s[j]=(sd>>j)&1;for(int j=L;j<N;j++){int v=d;for(int a=1;a<=L;a++)if((c>>(a-1))&1)v^=s[j-a];s[j]=v;}
        uint64_t lo=0,hi=0;for(int j=0;j<N;j++)if(s[j]){if(j<64)lo|=1ULL<<j;else hi|=1ULL<<(j-64);}S2[L][2*z]=lo;S2[L][2*z+1]=hi;}}
    (void)nL;
    unsigned char*T13L[5]={0};long n13L[5]={0};
    for(int L=Lmin;L<=Lmax;L++){T13=NULL;build13(L);T13L[L]=T13;n13L[L]=n13c;}
    #pragma omp parallel
    { long long fit[9][3][2]={{{0}}},p2[9][3]={{0}};uint64_t*BS=calloc(1<<18,8);uint32_t*proj[5];
      for(int L=Lmin;L<=Lmax;L++)proj[L]=malloc(n2[L]*4);
      #pragma omp for schedule(dynamic,16)
      for(long q=qlo;q<qhi;q++){const short*S=P+q*N;int J[24],cl[24];uint64_t Mlo=0,Mhi=0;
        for(int t=0;t<24;t++){J[t]=S[CI[t]];cl[t]=C[J[t]];if(J[t]<64)Mlo|=1ULL<<J[t];else Mhi|=1ULL<<(J[t]-64);}
        int sh=__builtin_popcountll(Mlo);int r[24];
        for(int t=0;t<24;t++)r[t]=J[t]<64?__builtin_popcountll(Mlo&((1ULL<<J[t])-1)):sh+__builtin_popcountll(Mhi&((1ULL<<(J[t]-64))-1));
        for(int L=Lmin;L<=Lmax;L++)for(long z=0;z<n2[L];z++){uint32_t v=(uint32_t)(_pext_u64(S2[L][2*z],Mlo)|(_pext_u64(S2[L][2*z+1],Mhi)<<sh));
          proj[L][z]=v;BS[v>>6]|=1ULL<<(v&63);}
        uint32_t lm[26]={0},pm[26]={0};int dl[24],nd=0;
        for(int t=0;t<24;t++){if(!lm[cl[t]])dl[nd++]=cl[t];lm[cl[t]]|=1u<<r[t];pm[PT[t]-'A']|=1u<<r[t];}
        static const int PL[13]={'E'-'A','A'-'A','S'-'A','T'-'A','N'-'A','O'-'A','R'-'A','H'-'A','B'-'A','L'-'A','I'-'A','C'-'A','K'-'A'};
        uint32_t cpAZ=0,ptpAZ=0;for(int j=0;j<nd;j++)if(dl[j]&1)cpAZ^=lm[dl[j]];for(int j=0;j<13;j++)if(PL[j]&1)ptpAZ^=pm[PL[j]];
        for(int a=0;a<NA;a++){uint32_t pb=PAR[a],cp=0,pp=0;for(int j=0;j<nd;j++)cp^=lm[dl[j]]&(0u-((pb>>dl[j])&1u));
          for(int j=0;j<13;j++)pp^=pm[PL[j]]&(0u-((pb>>PL[j])&1u));
          for(int ty=0;ty<3;ty++){if(isAZ[a]&&ty<2)continue;
            uint32_t bits=ty==0?cpAZ^pp:ty==1?cp^ptpAZ:cp^pp;
            if(!((BS[bits>>6]>>(bits&63))&1))continue;
            for(int L=Lmin;L<=Lmax;L++){long m2=0,first2[32];for(long z=0;z<n2[L];z++)if(proj[L][z]==bits){if(m2<32)first2[m2]=z;m2++;}
              if(!m2)continue;p2[L][ty]++;
              for(int fm=0;fm<2;fm++){int ko[24];for(int t=0;t<24;t++)ko[t]=kval(a,ty,fm,cl[t],t);
                long m13=0;long f13[32];int fx[32][17];int fnul[32];
                for(long z=0;z<n13L[L];z++){const unsigned char*Bt=T13L[L]+z*(L+1)*N;int R[17][18],rk=0,pc[17],ok=1;
                  for(int t=0;t<24&&ok;t++){int row[18];for(int m=0;m<=L;m++)row[m]=Bt[m*N+J[t]];row[L+1]=ko[t]%13;
                    for(int rr=0;rr<rk;rr++){int f=row[pc[rr]];if(f)for(int m=0;m<=L+1;m++)row[m]=(row[m]+13*13-f*R[rr][m])%13;}
                    int cc=-1;for(int m=0;m<=L;m++)if(row[m]){cc=m;break;}
                    if(cc<0){if(row[L+1])ok=0;continue;}
                    int iv=inv13[row[cc]];for(int m=0;m<=L+1;m++)row[m]=row[m]*iv%13;
                    for(int rr=0;rr<rk;rr++){int f=R[rr][cc];if(f)for(int m=0;m<=L+1;m++)R[rr][m]=(R[rr][m]+13*13-f*row[m])%13;}
                    memcpy(R[rk],row,sizeof row);pc[rk++]=cc;}
                  if(!ok)continue;
                  if(m13<32){f13[m13]=z;int x[17]={0};for(int rr=0;rr<rk;rr++)x[pc[rr]]=R[rr][L+1];memcpy(fx[m13],x,sizeof x);fnul[m13]=L+1-rk;}
                  m13++;}
                if(!m13)continue;fit[L][ty][fm]++;
                char buf[16384];int o=sprintf(buf,"M %s 1 %d %s %s %ld %s - n2 %ld n13c %ld S2",lab,L,TY[ty],fm?"beau":"vig",q,LAB[a],m2,m13);
                for(long i=0;i<m2&&i<32;i++){long z=first2[i];o+=sprintf(buf+o," c");for(int b=0;b<L;b++)o+=sprintf(buf+o,"%ld",(z>>b)&1);
                  o+=sprintf(buf+o,"s");for(int b=0;b<L;b++)o+=sprintf(buf+o,"%ld",(z>>(L+b))&1);o+=sprintf(buf+o,"d%ld",(z>>(2*L))&1);}
                o+=sprintf(buf+o," S13");for(long i=0;i<m13&&i<32;i++){long z=f13[i];int c[16];long y=z;for(int b=L-1;b>=0;b--){c[b]=y%13;y/=13;}
                  o+=sprintf(buf+o," c");for(int b=0;b<L;b++)o+=sprintf(buf+o,"%d%s",c[b],b<L-1?",":"");
                  o+=sprintf(buf+o,"x");for(int m=0;m<=L;m++)o+=sprintf(buf+o,"%d%s",fx[i][m],m<L?",":"");o+=sprintf(buf+o,"n%d",fnul[i]);}
                #pragma omp critical
                printf("%s\n",buf);}}}}
        for(int L=Lmin;L<=Lmax;L++)for(long z=0;z<n2[L];z++){uint32_t v=proj[L][z];BS[v>>6]=0;}}
      #pragma omp critical
      {for(int L=0;L<9;L++)for(int ty=0;ty<3;ty++){P2[L][ty]+=p2[L][ty];for(int fm=0;fm<2;fm++)FIT[L][ty][fm]+=fit[L][ty][fm];}}
      free(BS);}
    for(int L=Lmin;L<=Lmax;L++)for(int ty=0;ty<3;ty++)for(int fm=0;fm<2;fm++)
      printf("H %s 1 %d %s %s perms %ld pairs %ld pass2 %lld fits %lld\n",lab,L,TY[ty],fm?"beau":"vig",qhi-qlo,ncfg,P2[L][ty],FIT[L][ty][fm]);
  }
  printf("END %s %ld %ld\n",lab,qlo,qhi);return 0;}
