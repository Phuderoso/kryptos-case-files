/* Cycle 186 (IDEAS I-164): Quagmire IV (two DIFFERENT keyed alphabets) with an affine linear-recurrence key mod 26 on the CARVED
   index (M1: transpose first, then key; seed at carved positions 0..L-1), behind the 165,782 K3-law decimations / routes (all.bin).
   k[j] = c1 k[j-1] + ... + cL k[j-L] + d (mod 26), j = carved position, arbitrary weights, constant and seed.
   A = plaintext-side alphabet (list 1), B = ciphertext-side alphabet (list 2), every (A, B) pair.
   Vigenere: c = B[(A.index(p) + k) % 26] -> k = B(c) - A(p);  Beaufort: k = B(c) + A(p). Variant and rotations of A or B map the
   affine family onto itself (k -> k + e changes only d), so they are covered.  Perm convention as lr178: plaintext i carved at S[i].
   Mod 2 (as lrk180 mode 1): the 2^(2L+1) mod-2 streams projected (pext) on the 24 crib slots' carved positions (bit = rank of the
   carved position among the 24) give the per-perm word set V_L; the key-bit word of a pair is w = cp_B ^ pp_A, with cp_B = parity of
   B at the carved crib letters and pp_A = parity of A at the crib letters, both in rank order (both per perm).
   V_L is nested in L (an order-L stream is an order-(L+1) stream with c_{L+1} = 0), mod 2 and mod 13 alike.
   method 1 (join): per perm hash the larger side's words, probe v ^ (small-side word) for every v in V_Lmax (exact, each pair once).
   method 2 (audit): every (A, B) pair looked up in the per-perm 2^24 bitset of V_Lmax directly.
   Every candidate is re-checked by linear scan of the stream list (X line if not found). GF(13): lrk180's loop over c mod 13 with the
   precomputed basis table (seed, d linear), identical code. Shortcut (off with -DSAFE=1): GF(13) at Lmax first, lower L only if Lmax
   fits (exact by nesting). Fit iff mod 2 and mod 13 both solvable at that L.
   usage: lrk186 CT perms.bin alphaA alphaB label qlo qhi method Lmin Lmax tylabel
   output: H (per L, form: perms, pairs, mod-2 passes, fits), M (fits), O, X, END                                               */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <immintrin.h>
#ifndef SAFE
#define SAFE 0
#endif
#define N 97
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char*PT="EASTNORTHEASTBERLINCLOCK";
static int inv13[13];
static int md(int a,int p){a%=p;return a<0?a+p:a;}
typedef struct{int n;int (*IDX)[26];char (*LAB)[64];uint32_t*PAR;}AL;
static void load(const char*fn,AL*a){FILE*f=fopen(fn,"r");if(!f){fprintf(stderr,"open %s\n",fn);exit(1);}char al[64],lb[64];int cap=1024;
  a->IDX=malloc(cap*sizeof*a->IDX);a->LAB=malloc(cap*sizeof*a->LAB);a->n=0;
  while(fscanf(f,"%63s %63s",al,lb)==2){if(a->n==cap){cap*=2;a->IDX=realloc(a->IDX,cap*sizeof*a->IDX);a->LAB=realloc(a->LAB,cap*sizeof*a->LAB);}
    if(strlen(al)!=26){fprintf(stderr,"bad alphabet\n");exit(1);}int seen=0;for(int i=0;i<26;i++){a->IDX[a->n][al[i]-'A']=i;seen|=1<<(al[i]-'A');}
    if(seen!=(1<<26)-1){fprintf(stderr,"not a permutation\n");exit(1);}strcpy(a->LAB[a->n],lb);a->n++;}fclose(f);
  a->PAR=malloc(a->n*4);for(int i=0;i<a->n;i++){a->PAR[i]=0;for(int l=0;l<26;l++)if(a->IDX[i][l]&1)a->PAR[i]|=1u<<l;}}
static unsigned char*T13L[8];static long n13L[8];
static void build13(int L){long n=1;for(int i=0;i<L;i++)n*=13;n13L[L]=n;unsigned char*T=malloc(n*(L+1)*N);
  #pragma omp parallel for schedule(static)
  for(long z=0;z<n;z++){int c[16];long y=z;for(int i=L-1;i>=0;i--){c[i]=y%13;y/=13;}
    for(int m=0;m<=L;m++){unsigned char*s=T+(z*(L+1)+m)*N;for(int j=0;j<L;j++)s[j]=(m==j);
      for(int j=L;j<N;j++){int v=(m==L);for(int a=1;a<=L;a++)v+=c[a-1]*s[j-a];s[j]=v%13;}}}
  T13L[L]=T;}
/* lrk180's mod-13 loop: number of c (mod 13) for which (seed, d) solves all 24 slots; first solutions in f13/fx/fnul */
static long gf13(int L,const int*J,const int*ko,long*f13,int fx[][17],int*fnul){long m13=0;
  for(long z=0;z<n13L[L];z++){const unsigned char*Bt=T13L[L]+z*(L+1)*N;int R[17][18],rk=0,pc[17],ok=1;
    for(int t=0;t<24&&ok;t++){int row[18];for(int m=0;m<=L;m++)row[m]=Bt[m*N+J[t]];row[L+1]=ko[t]%13;
      for(int rr=0;rr<rk;rr++){int f=row[pc[rr]];if(f)for(int m=0;m<=L+1;m++)row[m]=(row[m]+13*13-f*R[rr][m])%13;}
      int cc=-1;for(int m=0;m<=L;m++)if(row[m]){cc=m;break;}
      if(cc<0){if(row[L+1])ok=0;continue;}
      int iv=inv13[row[cc]];for(int m=0;m<=L+1;m++)row[m]=row[m]*iv%13;
      for(int rr=0;rr<rk;rr++){int f=R[rr][cc];if(f)for(int m=0;m<=L+1;m++)R[rr][m]=(R[rr][m]+13*13-f*row[m])%13;}
      memcpy(R[rk],row,sizeof row);pc[rk++]=cc;}
    if(!ok)continue;
    if(f13&&m13<32){f13[m13]=z;int x[17]={0};for(int rr=0;rr<rk;rr++)x[pc[rr]]=R[rr][L+1];memcpy(fx[m13],x,sizeof x);fnul[m13]=L+1-rk;}
    m13++;if(!f13)return m13;}
  return m13;}
int main(int argc,char**argv){
  setvbuf(stdout,NULL,_IOLBF,0);
  if(argc<12){fprintf(stderr,"usage\n");return 1;}
  const char*Cs=argv[1];if(strlen(Cs)!=N)return 1;int C[N];for(int i=0;i<N;i++)C[i]=Cs[i]-'A';
  AL A,B;load(argv[3],&A);load(argv[4],&B);const char*lab=argv[5];long qlo=atol(argv[6]),qhi=atol(argv[7]);
  int meth=atoi(argv[8]),Lmin=atoi(argv[9]),Lmax=atoi(argv[10]);const char*TYL=argv[11];
  if(Lmin<1||Lmax>4||Lmin>Lmax){fprintf(stderr,"L range\n");return 1;}
  for(int a=1;a<13;a++)for(int b=1;b<13;b++)if(a*b%13==1)inv13[a]=b;
  FILE*pf=fopen(argv[2],"rb");fseek(pf,0,SEEK_END);long np=ftell(pf)/(2*N);rewind(pf);
  short*P=malloc(np*N*2);if(fread(P,2,np*N,pf)!=(size_t)(np*N))return 2;fclose(pf);if(qhi>np)qhi=np;if(qlo>qhi)qlo=qhi;
  long n2[5]={0};uint64_t*S2[5]={0};
  for(int L=1;L<=Lmax;L++){n2[L]=1L<<(2*L+1);S2[L]=malloc(n2[L]*16);
    for(long z=0;z<n2[L];z++){int c=z&((1<<L)-1),sd=(z>>L)&((1<<L)-1),d=(z>>(2*L))&1;int s[N];
      for(int j=0;j<L;j++)s[j]=(sd>>j)&1;for(int j=L;j<N;j++){int v=d;for(int a=1;a<=L;a++)if((c>>(a-1))&1)v^=s[j-a];s[j]=v;}
      uint64_t lo=0,hi=0;for(int j=0;j<N;j++)if(s[j]){if(j<64)lo|=1ULL<<j;else hi|=1ULL<<(j-64);}S2[L][2*z]=lo;S2[L][2*z+1]=hi;}}
  for(int L=Lmin;L<=Lmax;L++)build13(L);
  int smallA=A.n<=B.n;int nS=smallA?A.n:B.n,nLg=smallA?B.n:A.n;
  long long FIT[9][2]={{0}},P2[9]={0},XX=0,PASSL=0;long npairs=(long)A.n*B.n;
  static const int PLd[13]={'E'-'A','A'-'A','S'-'A','T'-'A','N'-'A','O'-'A','R'-'A','H'-'A','B'-'A','L'-'A','I'-'A','C'-'A','K'-'A'};
  #pragma omp parallel
  { long long fit[9][2]={{0}},p2[9]={0},xx=0,passl=0;uint32_t*proj[5];for(int L=1;L<=Lmax;L++)proj[L]=malloc(n2[L]*4);
    uint32_t*cpB=malloc(B.n*4),*ppA=malloc(A.n*4);int HB=1<<16;int*head=malloc(HB*sizeof(int));int*nxt=malloc(nLg*sizeof(int));
    uint64_t*BS=(meth==2)?calloc(1<<18,8):NULL;uint32_t V[512];long*cand=malloc(sizeof(long)*8000000);
    #pragma omp for schedule(dynamic,8)
    for(long q=qlo;q<qhi;q++){const short*S=P+q*N;int J[24],cl[24];uint64_t Mlo=0,Mhi=0;
      for(int t=0;t<24;t++){J[t]=S[CI[t]];cl[t]=C[J[t]];if(J[t]<64)Mlo|=1ULL<<J[t];else Mhi|=1ULL<<(J[t]-64);}
      int sh=__builtin_popcountll(Mlo);int r[24];
      for(int t=0;t<24;t++)r[t]=J[t]<64?__builtin_popcountll(Mlo&((1ULL<<J[t])-1)):sh+__builtin_popcountll(Mhi&((1ULL<<(J[t]-64))-1));
      for(int L=1;L<=Lmax;L++)for(long z=0;z<n2[L];z++)proj[L][z]=(uint32_t)(_pext_u64(S2[L][2*z],Mlo)|(_pext_u64(S2[L][2*z+1],Mhi)<<sh));
      int nV=0;for(long z=0;z<n2[Lmax];z++){uint32_t v=proj[Lmax][z];int dup=0;for(int i=0;i<nV;i++)if(V[i]==v){dup=1;break;}if(!dup)V[nV++]=v;}
      uint32_t lm[26]={0},pm[26]={0};int dl[24],nd=0;
      for(int t=0;t<24;t++){if(!lm[cl[t]])dl[nd++]=cl[t];lm[cl[t]]|=1u<<r[t];pm[PT[t]-'A']|=1u<<r[t];}
      for(int b=0;b<B.n;b++){uint32_t pb=B.PAR[b],cp=0;for(int j=0;j<nd;j++)cp^=lm[dl[j]]&(0u-((pb>>dl[j])&1u));cpB[b]=cp;}
      for(int a=0;a<A.n;a++){uint32_t pa=A.PAR[a],pp=0;for(int j=0;j<13;j++)pp^=pm[PLd[j]]&(0u-((pa>>PLd[j])&1u));ppA[a]=pp;}
      long ns=0;
      if(meth==1){uint32_t*Lw=smallA?cpB:ppA,*Sw=smallA?ppA:cpB;
        for(int h=0;h<HB;h++)head[h]=-1;
        for(int i=0;i<nLg;i++){int h=(Lw[i]*0x9E3779B1u)>>16;nxt[i]=head[h];head[h]=i;}
        for(int vi=0;vi<nV;vi++)for(int s=0;s<nS;s++){uint32_t tg=V[vi]^Sw[s];int h=(tg*0x9E3779B1u)>>16;
          for(int i=head[h];i>=0;i=nxt[i])if(Lw[i]==tg){long id=smallA?(long)s*B.n+i:(long)i*B.n+s;cand[ns++]=id;}
          if(ns>7900000){fprintf(stderr,"cand overflow\n");exit(4);}}}
      else {for(int i=0;i<nV;i++)BS[V[i]>>6]|=1ULL<<(V[i]&63);
        for(int a=0;a<A.n;a++)for(int b=0;b<B.n;b++){uint32_t w=cpB[b]^ppA[a];if((BS[w>>6]>>(w&63))&1){cand[ns++]=(long)a*B.n+b;if(ns>7900000){fprintf(stderr,"cand overflow\n");exit(4);}}}
        for(int i=0;i<nV;i++)BS[V[i]>>6]=0;}
      for(long i=0;i<ns;i++){int a=cand[i]/B.n,b=cand[i]%B.n;uint32_t w=cpB[b]^ppA[a];int lmk=0;
        for(int L=Lmin;L<=Lmax;L++)for(long z=0;z<n2[L];z++)if(proj[L][z]==w){lmk|=1<<(L-1);break;}
        if(!((lmk>>(Lmax-1))&1)){xx++;
          #pragma omp critical
          printf("X %s method/stream mismatch q %ld a %d b %d\n",lab,q,a,b);
          continue;}
        passl++;for(int L=Lmin;L<=Lmax;L++)if((lmk>>(L-1))&1)p2[L]++;
        for(int fm=0;fm<2;fm++){int ko[24];
          for(int t=0;t<24;t++){int ci=B.IDX[b][cl[t]],pi=A.IDX[a][PT[t]-'A'];ko[t]=md(fm?ci+pi:ci-pi,26);}
          if(!SAFE){if(!gf13(Lmax,J,ko,NULL,NULL,NULL))continue;}
          for(int L=Lmin;L<=Lmax;L++){if(!((lmk>>(L-1))&1))continue;
            long f13[32];int fx[32][17];int fnul[32];long m13=gf13(L,J,ko,f13,fx,fnul);if(!m13)continue;
            long m2=0,first2[32];for(long z=0;z<n2[L];z++)if(proj[L][z]==w){if(m2<32)first2[m2]=z;m2++;}
            fit[L][fm]++;
            char buf[16384];int o=sprintf(buf,"M %s 1 %d %s %s %ld %s %s n2 %ld n13c %ld S2",lab,L,TYL,fm?"beau":"vig",q,A.LAB[a],B.LAB[b],m2,m13);
            for(long u=0;u<m2&&u<32;u++){long z=first2[u];o+=sprintf(buf+o," c");for(int bb=0;bb<L;bb++)o+=sprintf(buf+o,"%ld",(z>>bb)&1);
              o+=sprintf(buf+o,"s");for(int bb=0;bb<L;bb++)o+=sprintf(buf+o,"%ld",(z>>(L+bb))&1);o+=sprintf(buf+o,"d%ld",(z>>(2*L))&1);}
            o+=sprintf(buf+o," S13");for(long u=0;u<m13&&u<32;u++){long z=f13[u];int c[16];long y=z;for(int bb=L-1;bb>=0;bb--){c[bb]=y%13;y/=13;}
              o+=sprintf(buf+o," c");for(int bb=0;bb<L;bb++)o+=sprintf(buf+o,"%d%s",c[bb],bb<L-1?",":"");
              o+=sprintf(buf+o,"x");for(int m=0;m<=L;m++)o+=sprintf(buf+o,"%d%s",fx[u][m],m<L?",":"");o+=sprintf(buf+o,"n%d",fnul[u]);}
            #pragma omp critical
            printf("%s\n",buf);}}}}
    #pragma omp critical
    {for(int L=0;L<9;L++){P2[L]+=p2[L];for(int fm=0;fm<2;fm++)FIT[L][fm]+=fit[L][fm];}XX+=xx;PASSL+=passl;}
    free(cand);free(cpB);free(ppA);free(head);free(nxt);if(BS)free(BS);}
  for(int L=Lmin;L<=Lmax;L++)for(int fm=0;fm<2;fm++)
    printf("H %s 1 %d %s %s perms %ld pairs %ld pass2 %lld fits %lld\n",lab,L,TYL,fm?"beau":"vig",qhi-qlo,npairs,P2[L],FIT[L][fm]);
  printf("O %s mismatch %lld passLmax %lld method %d safe %d\n",lab,XX,PASSL,meth,SAFE);
  printf("END %s %ld %ld\n",lab,qlo,qhi);return 0;}
