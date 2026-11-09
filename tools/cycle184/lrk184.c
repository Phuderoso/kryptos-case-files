/* Cycle 184 (IDEAS I-163; lrk182.c verbatim apart from this header line): Quagmire IV (two DIFFERENT keyed alphabets, here both from the 18,776 vocabulary) with an affine linear-recurrence key mod 26, key on the
   plaintext index (M0), behind the 165,782 K3-law decimations / routes (all.bin). k[i] = c1 k[i-1] + ... + cL k[i-L] + d (mod 26).
   A = plaintext-side alphabet (list file 1), B = ciphertext-side alphabet (list file 2), every (A, B) pair.
   Vigenere: c = B[(A.index(p) + k) % 26] -> k = B(c) - A(p);  Beaufort: c = B[(k - A.index(p)) % 26] -> k = B(c) + A(p).
   Rotations of A or B (k -> k + e) and the variant form map the affine family onto itself (case 168), so they are covered.
   Perm convention as lr178 / lrk180: plaintext position i is carved at S[i].
   Mod 2 the test depends only on the 24 key bits w = parity_B(carved) XOR parity_A(crib) (case 168). w = cp_B (per perm) ^ pa_A
   (constant). Lmax-table T as lrk180 (bit L-1: some (c, d) mod 2 fits at order L). The pass sets are NESTED in L (an order-L
   solution is an order-(L+1) solution with c_{L+1} = 0; fewer in-block equations, same propagation), mod 2 and mod 13 alike.
   method 0 (A list small): U = union over A of (W_Lmax ^ pa_A), a 2^24 CSR map word -> A list; per perm one lookup per B.
   method 1 (A list large): for each (c, d) mod 2 at order Lmax the words form an affine space w0 + span(w_j), whose low Lmax bits are
     the free seed (crib slots 21..), so x in V <=> sigma(x) = w0>>Lmax with sigma(x) = (x ^ sum_j x_j w_j) >> Lmax (linear). Hash join
     per (c, d): sigma(pa_A) ^ (w0>>Lmax) precomputed for every A; per perm one sigma(cp_B) lookup per (B, (c, d)).
   method 2 (audit): every (A, B) pair looked up in T directly.
   Every mod-2 pass is re-checked against T (X line if not set). GF(13): lrk180's solve0; shortcut (off with -DSAFE=1): solve at Lmax
   first, lower L only if Lmax has a mod-13 solution (exact by nesting). Fit iff mod 2 and mod 13 both solvable at that L.
   usage: lrk182 CT perms.bin alphaA alphaB label qlo qhi method Lmin Lmax tylabel
   output: H lines (per L, form: perms, pairs, mod-2 passes, fits), M lines, O, X, END                                         */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#ifndef SAFE
#define SAFE 0
#endif
#define N 97
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char*PT="EASTNORTHEASTBERLINCLOCK";
static int inv13[13];
static int md(int a,int p){a%=p;return a<0?a+p:a;}
#include "solve0.inc"
typedef struct{int n;int (*IDX)[26];char (*LAB)[64];uint32_t*PAR;}AL;
static void load(const char*fn,AL*a){FILE*f=fopen(fn,"r");if(!f){fprintf(stderr,"open %s\n",fn);exit(1);}char al[64],lb[64];int cap=1024;
  a->IDX=malloc(cap*sizeof*a->IDX);a->LAB=malloc(cap*sizeof*a->LAB);a->n=0;
  while(fscanf(f,"%63s %63s",al,lb)==2){if(a->n==cap){cap*=2;a->IDX=realloc(a->IDX,cap*sizeof*a->IDX);a->LAB=realloc(a->LAB,cap*sizeof*a->LAB);}
    if(strlen(al)!=26){fprintf(stderr,"bad alphabet\n");exit(1);}int seen=0;for(int i=0;i<26;i++){a->IDX[a->n][al[i]-'A']=i;seen|=1<<(al[i]-'A');}
    if(seen!=(1<<26)-1){fprintf(stderr,"not a permutation\n");exit(1);}strcpy(a->LAB[a->n],lb);a->n++;}fclose(f);
  a->PAR=malloc(a->n*4);for(int i=0;i<a->n;i++){a->PAR[i]=0;for(int l=0;l<26;l++)if(a->IDX[i][l]&1)a->PAR[i]|=1u<<l;}}
static int cmp64(const void*x,const void*y){uint64_t a=*(const uint64_t*)x,b=*(const uint64_t*)y;return a<b?-1:a>b;}
int main(int argc,char**argv){
  setvbuf(stdout,NULL,_IOLBF,0);
  if(argc<12){fprintf(stderr,"usage\n");return 1;}
  const char*Cs=argv[1];if(strlen(Cs)!=N)return 1;int C[N];for(int i=0;i<N;i++)C[i]=Cs[i]-'A';
  AL A,B;load(argv[3],&A);load(argv[4],&B);const char*lab=argv[5];long qlo=atol(argv[6]),qhi=atol(argv[7]);
  int meth=atoi(argv[8]),Lmin=atoi(argv[9]),Lmax=atoi(argv[10]);const char*TYL=argv[11];
  if(Lmin<1||Lmax>7||Lmin>Lmax){fprintf(stderr,"L range\n");return 1;}
  for(int a=1;a<13;a++)for(int b=1;b<13;b++)if(a*b%13==1)inv13[a]=b;
  FILE*pf=fopen(argv[2],"rb");fseek(pf,0,SEEK_END);long np=ftell(pf)/(2*N);rewind(pf);
  short*P=malloc(np*N*2);if(fread(P,2,np*N,pf)!=(size_t)(np*N))return 2;fclose(pf);if(qhi>np)qhi=np;if(qlo>qhi)qlo=qhi;
  /* mod-2 table (identical construction to lrk180) */
  uint8_t*T=calloc(1<<24,1);
  for(int L=1;L<=Lmax;L++){
    #pragma omp parallel for schedule(dynamic,64)
    for(int b1=0;b1<8192;b1++){int k[53];for(int i=0;i<13;i++)k[i]=(b1>>i)&1;
      for(int x=0;x<(1<<(L+1));x++){int d=(x>>L)&1,ok=1;
        for(int i=21+L;i<=33&&ok;i++){int v=d;for(int j=1;j<=L;j++)if((x>>(j-1))&1)v^=k[i-j-21];if(v!=k[i-21])ok=0;}
        if(!ok)continue;int s[53];memcpy(s,k,13*sizeof(int));int b2=0;
        for(int i=34;i<=73;i++){int v=d;for(int j=1;j<=L;j++)if((x>>(j-1))&1)v^=s[i-j-21];s[i-21]=v;if(i>=63&&v)b2|=1<<(i-63);}
        uint32_t id=(uint32_t)b1|((uint32_t)b2<<13);__atomic_fetch_or(&T[id],(uint8_t)(1<<(L-1)),__ATOMIC_RELAXED);}}}
  long nW=0,nest_bad=0;for(uint32_t w=0;w<(1u<<24);w++){if((T[w]>>(Lmax-1))&1)nW++;else if(T[w])nest_bad++;}
  if(nest_bad){printf("X %s nesting violated %ld\n",lab,nest_bad);return 3;}
  uint32_t*W=malloc(nW*4);{long i=0;for(uint32_t w=0;w<(1u<<24);w++)if((T[w]>>(Lmax-1))&1)W[i++]=w;}
  uint32_t*PA=malloc(A.n*4);for(int a=0;a<A.n;a++){PA[a]=0;for(int t=0;t<24;t++)if(A.IDX[a][PT[t]-'A']&1)PA[a]|=1u<<t;}
  /* method structures */
  uint32_t*Uoff=NULL,*Ulist=NULL;                                  /* method 0 */
  int ncd=1<<(Lmax+1);uint32_t (*G)[128]=NULL;uint32_t*W0s=NULL;uint64_t**SK=NULL;uint64_t**SB=NULL;int sbits=24-Lmax;  /* method 1 */
  if(meth==0){long ne=(long)A.n*nW;uint64_t*E=malloc(ne*8);long i=0;for(int a=0;a<A.n;a++)for(long j=0;j<nW;j++)E[i++]=((uint64_t)(W[j]^PA[a])<<24)|a;
    qsort(E,ne,8,cmp64);Uoff=calloc((1u<<24)+1,4);Ulist=malloc(ne*4);for(long j=0;j<ne;j++){Uoff[(E[j]>>24)+1]++;Ulist[j]=E[j]&0xFFFFFF;}
    for(uint32_t w=0;w<(1u<<24);w++)Uoff[w+1]+=Uoff[w];free(E);}
  else if(meth==1){G=malloc(ncd*sizeof*G);W0s=malloc(ncd*4);SK=malloc(ncd*sizeof*SK);SB=malloc(ncd*sizeof*SB);int L=Lmax;
    for(int cd=0;cd<ncd;cd++){uint32_t wv[8];
      for(int sv=-1;sv<L;sv++){int s[53]={0};if(sv>=0)s[sv]=1;int d=(cd>>L)&1;
        for(int i=21+L;i<=73;i++){int v=d;for(int j=1;j<=L;j++)if((cd>>(j-1))&1)v^=s[i-j-21];s[i-21]=v;}
        uint32_t w=0;for(int t=0;t<24;t++)if(s[CI[t]-21])w|=1u<<t;if(sv<0)W0s[cd]=w;else wv[sv]=w^W0s[cd];}
      for(int u=0;u<(1<<L);u++){uint32_t g=0;for(int j=0;j<L;j++)if((u>>j)&1)g^=wv[j];G[cd][u]=g>>L;}
      SK[cd]=malloc((size_t)A.n*8);SB[cd]=calloc(((size_t)1<<sbits)/64+1,8);
      for(int a=0;a<A.n;a++){uint32_t x=PA[a];uint32_t key=((x>>L)^G[cd][x&((1u<<L)-1)])^(W0s[cd]>>L);SK[cd][a]=((uint64_t)key<<24)|a;SB[cd][key>>6]|=1ULL<<(key&63);}
      qsort(SK[cd],A.n,8,cmp64);}}
  long long FIT[9][2]={{0}},P2[9]={0},OVF=0,XX=0,PASSL=0;long npairs=(long)A.n*B.n;
  #pragma omp parallel
  { long long fit[9][2]={{0}},p2[9]={0},ovf=0,xx=0,passl=0;uint64_t*seen=calloc(npairs/64+1,8);long*sl=malloc(sizeof(long)*4000000);
    uint32_t*cpB=malloc(B.n*4);
    #pragma omp for schedule(dynamic,8)
    for(long q=qlo;q<qhi;q++){const short*S=P+q*N;int cl[24];uint32_t lm[26]={0};int dl[24],nd=0;long ns=0;
      for(int t=0;t<24;t++){cl[t]=C[S[CI[t]]];if(!lm[cl[t]])dl[nd++]=cl[t];lm[cl[t]]|=1u<<t;}
      for(int b=0;b<B.n;b++){uint32_t pb=B.PAR[b],cp=0;for(int j=0;j<nd;j++)cp^=lm[dl[j]]&(0u-((pb>>dl[j])&1u));cpB[b]=cp;}
      /* collect mod-2 candidate pairs (index a*B.n+b) */
      if(meth==0){for(int b=0;b<B.n;b++){uint32_t cp=cpB[b];for(uint32_t j=Uoff[cp];j<Uoff[cp+1];j++){long id=(long)Ulist[j]*B.n+b;sl[ns++]=id;}}}
      else if(meth==1){int L=Lmax;for(int b=0;b<B.n;b++){uint32_t x=cpB[b];for(int cd=0;cd<ncd;cd++){uint32_t key=(x>>L)^G[cd][x&((1u<<L)-1)];
            if(!((SB[cd][key>>6]>>(key&63))&1))continue;
            long lo=0,hi=A.n;uint64_t k0=(uint64_t)key<<24;while(lo<hi){long m=(lo+hi)/2;if(SK[cd][m]<k0)lo=m+1;else hi=m;}
            for(long m=lo;m<A.n&&(SK[cd][m]>>24)==key;m++){long id=(long)(SK[cd][m]&0xFFFFFF)*B.n+b;if((seen[id>>6]>>(id&63))&1)continue;seen[id>>6]|=1ULL<<(id&63);sl[ns++]=id;}}}
        for(long i=0;i<ns;i++)seen[sl[i]>>6]=0;}
      else {for(int a=0;a<A.n;a++)for(int b=0;b<B.n;b++){uint32_t bits=cpB[b]^PA[a];if((T[bits]>>(Lmax-1))&1)sl[ns++]=(long)a*B.n+b;}}
      if(ns>3900000){fprintf(stderr,"sl overflow\n");exit(4);}
      for(long i=0;i<ns;i++){int a=sl[i]/B.n,b=sl[i]%B.n;uint32_t bits=cpB[b]^PA[a];int lmk=T[bits];
        if(!((lmk>>(Lmax-1))&1)){xx++;
          #pragma omp critical
          printf("X %s method/table mismatch q %ld a %d b %d\n",lab,q,a,b);
          continue;}
        passl++;for(int L=Lmin;L<=Lmax;L++)if((lmk>>(L-1))&1)p2[L]++;
        for(int fm=0;fm<2;fm++){int k13[53]={0},k2[53]={0};
          for(int t=0;t<24;t++){int ci=B.IDX[b][cl[t]],pi=A.IDX[a][PT[t]-'A'];int v=md(fm?ci+pi:ci-pi,26);k13[CI[t]-21]=v%13;k2[CI[t]-21]=v&1;}
          if(!SAFE){SolSet Z;solve0(13,Lmax,k13,&Z);if(Z.ovf)ovf++;if(!Z.tot)continue;}
          for(int L=Lmin;L<=Lmax;L++){if(!((lmk>>(L-1))&1))continue;
            SolSet A13;solve0(13,L,k13,&A13);if(A13.ovf)ovf++;if(!A13.tot)continue;
            SolSet A2;solve0(2,L,k2,&A2);if(!A2.tot){xx++;
              #pragma omp critical
              printf("X %s table/solve0 mismatch q %ld a %d b %d L %d\n",lab,q,a,b,L);
              continue;}
            fit[L][fm]++;
            char buf[8192];int o=sprintf(buf,"M %s 0 %d %s %s %ld %s %s n2 %ld n13 %ld S2",lab,L,TYL,fm?"beau":"vig",q,A.LAB[a],B.LAB[b],A2.tot,A13.tot);
            for(int s=0;s<A2.n&&s<32;s++){o+=sprintf(buf+o," ");for(int j=0;j<=L;j++)o+=sprintf(buf+o,"%d%s",A2.sol[s][j],j<L?",":"");}
            o+=sprintf(buf+o," S13");for(int s=0;s<A13.n&&s<32;s++){o+=sprintf(buf+o," ");for(int j=0;j<=L;j++)o+=sprintf(buf+o,"%d%s",A13.sol[s][j],j<L?",":"");}
            #pragma omp critical
            printf("%s\n",buf);}}}}
    #pragma omp critical
    {for(int L=0;L<9;L++){P2[L]+=p2[L];for(int fm=0;fm<2;fm++)FIT[L][fm]+=fit[L][fm];}OVF+=ovf;XX+=xx;PASSL+=passl;}
    free(seen);free(sl);free(cpB);}
  for(int L=Lmin;L<=Lmax;L++)for(int fm=0;fm<2;fm++)
    printf("H %s 0 %d %s %s perms %ld pairs %ld pass2 %lld fits %lld\n",lab,L,TYL,fm?"beau":"vig",qhi-qlo,npairs,P2[L],FIT[L][fm]);
  printf("O %s overflow %lld mismatch %lld passLmax %lld method %d safe %d nW %ld\n",lab,OVF,XX,PASSL,meth,SAFE,nW);
  printf("END %s %ld %ld\n",lab,qlo,qhi);return 0;}
