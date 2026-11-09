/* Cycle 188 (IDEAS I-185): ONE-ERROR audit of case 174. Quagmire IV (plaintext-side alphabet A, ciphertext-side alphabet B) with an
   affine linear-recurrence key mod 26 on the CARVED index (M1: transpose first, then key; seed at carved positions 0..L-1), behind the
   165,782 K3-law decimations / routes (all.bin), with ONE of the 24 crib key values allowed to be wrong (a mis-carved letter at that
   slot's carved position, or a wrong crib letter): that slot's key value is a free unknown. k[j] = c1 k[j-1] + ... + cL k[j-L] + d.
   Vig k = B(c) - A(p), Beau k = B(c) + A(p) (as lrk186; variant / rotations only change d). Perm convention as lrk186.
   Exact by CRT (case 167/169/171): slot t free fits mod 26 iff the 23 other slots are consistent mod 2 AND mod 13 (same t).
   Mod 2 (lrk186's projected streams, bit = rank of the carved position among the 24): w = cp_B ^ pp_A; one-error = Hamming-1 dilation
   (I-161 / lrk183): V1 = V_Lmax u {v ^ e_r}. st2(L) = w in V_L (then every t is allowed mod 2); A2(L) = {t : w ^ e_r[t] in V_L}.
   method 1 (join): per perm hash the larger side's words, probe u ^ (small-side word) for every u in V1 (deduplicated), candidates
     deduplicated per perm (sort/unique).   method 2 (audit): every (A, B) pair looked up in a per-perm 2^24 bitset of V1.
   Every candidate is re-checked by linear scan of the stream list (X line if not within distance 1 of V_Lmax).
   GF(13), per c in Z13^L (lrk186's basis table: seed, d linear): rows = the 24 slots (coefficients of seed_0..seed_{L-1}, d at J[t]).
     allowed slots = all 24 if st2, else A2. Strict (t = -1) = all 24 rows consistent and st2. Slot t = rows except t consistent.
     Prefilter (off with -DSAFE=1; exact, necessary): if st2, rows 0..11 consistent OR rows 12..23 consistent (one bad row cannot
     sit in both halves). Shortcut (off in SAFE): GF(13) at Lmax first, lower L only if Lmax fits (exact by nesting: an order-L
     stream is an order-(L+1) stream with c_{L+1} = 0, for any fixed free slot).
   usage: lrk188 CT perms.bin alphaA alphaB label qlo qhi method Lmin Lmax tylabel
   output: H (per L, form: perms, pairs, one-error mod-2 passes, fits, strict fits, slot fits), M (fits), O, X, END                */
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
/* consistency mod 13 of the rows in `rows` (bit t = slot t) for basis Bt; early exit; on success x (particular solution, free = 0)
   and nullity */
static int cons13(int L,const unsigned char*Bt,const int*J,const int*ko,uint32_t rows,int*x,int*nul){
  int R[5][6],pc[5],rk=0;
  for(int t=0;t<24;t++){if(!((rows>>t)&1))continue;int row[6];for(int m=0;m<=L;m++)row[m]=Bt[m*N+J[t]];row[L+1]=ko[t];
    for(int r=0;r<rk;r++){int f=row[pc[r]];if(f)for(int m=0;m<=L+1;m++)row[m]=(row[m]+169-f*R[r][m])%13;}
    int cc=-1;for(int m=0;m<=L;m++)if(row[m]){cc=m;break;}
    if(cc<0){if(row[L+1])return 0;continue;}
    int iv=inv13[row[cc]];for(int m=0;m<=L+1;m++)row[m]=row[m]*iv%13;
    for(int r=0;r<rk;r++){int f=R[r][cc];if(f)for(int m=0;m<=L+1;m++)R[r][m]=(R[r][m]+169-f*row[m])%13;}
    memcpy(R[rk],row,sizeof row);pc[rk++]=cc;}
  if(x){for(int m=0;m<=L;m++)x[m]=0;for(int r=0;r<rk;r++)x[pc[r]]=R[r][L+1];*nul=L+1-rk;}
  return 1;}
#define ALL24 0xFFFFFFu
/* does (L, ko, st2, A2) fit for some c and some slot? (early return) */
static int any13(int L,const int*J,const int*ko,int st2,uint32_t A2){
  for(long z=0;z<n13L[L];z++){const unsigned char*Bt=T13L[L]+z*(L+1)*N;
    if(st2){if(!SAFE&&!cons13(L,Bt,J,ko,0xFFFu,NULL,NULL)&&!cons13(L,Bt,J,ko,0xFFF000u,NULL,NULL))continue;
      if(cons13(L,Bt,J,ko,ALL24,NULL,NULL))return 1;for(int t=0;t<24;t++)if(cons13(L,Bt,J,ko,ALL24&~(1u<<t),NULL,NULL))return 1;}
    else for(int t=0;t<24;t++)if(((A2>>t)&1)&&cons13(L,Bt,J,ko,ALL24&~(1u<<t),NULL,NULL))return 1;}
  return 0;}
int main(int argc,char**argv){
  setvbuf(stdout,NULL,_IOLBF,0);
  if(argc<12){fprintf(stderr,"usage\n");return 1;}
  const char*Cs=argv[1];if(strlen(Cs)!=N)return 1;int C[N];for(int i=0;i<N;i++)C[i]=Cs[i]-'A';
  AL A,B;load(argv[3],&A);load(argv[4],&B);const char*lab=argv[5];long qlo=atol(argv[6]),qhi=atol(argv[7]);
  int meth=atoi(argv[8]),Lmin=atoi(argv[9]),Lmax=atoi(argv[10]);const char*TYL=argv[11];
  if(Lmin<1||Lmax>3||Lmin>Lmax){fprintf(stderr,"L range\n");return 1;}
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
  long long FIT[9][2]={{0}},STR[9][2]={{0}},SLF[9][2]={{0}},P2[9]={0},XX=0,NCAND=0;long npairs=(long)A.n*B.n;
  static const int PLd[13]={'E'-'A','A'-'A','S'-'A','T'-'A','N'-'A','O'-'A','R'-'A','H'-'A','B'-'A','L'-'A','I'-'A','C'-'A','K'-'A'};
  #pragma omp parallel
  { long long fit[9][2]={{0}},str[9][2]={{0}},slf[9][2]={{0}},p2[9]={0},xx=0,ncand=0;uint32_t*proj[5];for(int L=1;L<=Lmax;L++)proj[L]=malloc(n2[L]*4);
    uint32_t*cpB=malloc(B.n*4),*ppA=malloc(A.n*4);int HB=1<<16;int*head=malloc(HB*sizeof(int));int*nxt=malloc(nLg*sizeof(int));
    uint64_t*BS=(meth==2)?calloc(1<<18,8):NULL;uint32_t*V1=malloc(4*25*128);long cap=4000000;long*cand=malloc(sizeof(long)*cap);
    char*buf=malloc(1<<17);
    #pragma omp for schedule(dynamic,8)
    for(long q=qlo;q<qhi;q++){const short*S=P+q*N;int J[24],cl[24];uint64_t Mlo=0,Mhi=0;
      for(int t=0;t<24;t++){J[t]=S[CI[t]];cl[t]=C[J[t]];if(J[t]<64)Mlo|=1ULL<<J[t];else Mhi|=1ULL<<(J[t]-64);}
      int sh=__builtin_popcountll(Mlo);int r[24];
      for(int t=0;t<24;t++)r[t]=J[t]<64?__builtin_popcountll(Mlo&((1ULL<<J[t])-1)):sh+__builtin_popcountll(Mhi&((1ULL<<(J[t]-64))-1));
      for(int L=1;L<=Lmax;L++)for(long z=0;z<n2[L];z++)proj[L][z]=(uint32_t)(_pext_u64(S2[L][2*z],Mlo)|(_pext_u64(S2[L][2*z+1],Mhi)<<sh));
      int nV=0;for(long z=0;z<n2[Lmax];z++)for(int e=-1;e<24;e++){uint32_t v=proj[Lmax][z]^(e<0?0u:1u<<e);int dup=0;for(int i=0;i<nV;i++)if(V1[i]==v){dup=1;break;}if(!dup)V1[nV++]=v;}
      uint32_t lm[26]={0},pm[26]={0};int dl[24],nd=0;
      for(int t=0;t<24;t++){if(!lm[cl[t]])dl[nd++]=cl[t];lm[cl[t]]|=1u<<r[t];pm[PT[t]-'A']|=1u<<r[t];}
      for(int b=0;b<B.n;b++){uint32_t pb=B.PAR[b],cp=0;for(int j=0;j<nd;j++)cp^=lm[dl[j]]&(0u-((pb>>dl[j])&1u));cpB[b]=cp;}
      for(int a=0;a<A.n;a++){uint32_t pa=A.PAR[a],pp=0;for(int j=0;j<13;j++)pp^=pm[PLd[j]]&(0u-((pa>>PLd[j])&1u));ppA[a]=pp;}
      long ns=0;
      if(meth==1){uint32_t*Lw=smallA?cpB:ppA,*Sw=smallA?ppA:cpB;
        for(int h=0;h<HB;h++)head[h]=-1;
        for(int i=0;i<nLg;i++){int h=(Lw[i]*0x9E3779B1u)>>16;nxt[i]=head[h];head[h]=i;}
        for(int vi=0;vi<nV;vi++)for(int s=0;s<nS;s++){uint32_t tg=V1[vi]^Sw[s];int h=(tg*0x9E3779B1u)>>16;
          for(int i=head[h];i>=0;i=nxt[i])if(Lw[i]==tg){long id=smallA?(long)s*B.n+i:(long)i*B.n+s;if(ns>=cap){fprintf(stderr,"cand overflow\n");exit(4);}cand[ns++]=id;}}
        /* dedupe */
        if(ns>1){for(long i=1;i<ns;i++){long v=cand[i];long j=i-1;while(j>=0&&cand[j]>v){cand[j+1]=cand[j];j--;}cand[j+1]=v;}
          long m=1;for(long i=1;i<ns;i++)if(cand[i]!=cand[m-1])cand[m++]=cand[i];ns=m;}}
      else {for(int i=0;i<nV;i++)BS[V1[i]>>6]|=1ULL<<(V1[i]&63);
        for(int a=0;a<A.n;a++)for(int b=0;b<B.n;b++){uint32_t w=cpB[b]^ppA[a];if((BS[w>>6]>>(w&63))&1){if(ns>=cap){fprintf(stderr,"cand overflow\n");exit(4);}cand[ns++]=(long)a*B.n+b;}}
        for(int i=0;i<nV;i++)BS[V1[i]>>6]=0;}
      ncand+=ns;
      for(long i=0;i<ns;i++){int a=cand[i]/B.n,b=cand[i]%B.n;uint32_t w=cpB[b]^ppA[a];
        int st2[5]={0};uint32_t A2[5]={0};int dil[5]={0};
        for(int L=1;L<=Lmax;L++)for(long z=0;z<n2[L];z++){uint32_t x=proj[L][z]^w;if(!x)st2[L]=1;else if(!(x&(x-1))){int rr=__builtin_ctz(x);for(int t=0;t<24;t++)if(r[t]==rr)A2[L]|=1u<<t;}}
        for(int L=1;L<=Lmax;L++)dil[L]=st2[L]||A2[L];
        if(!dil[Lmax]){xx++;
          #pragma omp critical
          printf("X %s method/stream mismatch q %ld a %d b %d\n",lab,q,a,b);
          continue;}
        for(int L=Lmin;L<=Lmax;L++)if(dil[L])p2[L]++;
        for(int fm=0;fm<2;fm++){int ko[24];
          for(int t=0;t<24;t++){int ci=B.IDX[b][cl[t]],pi=A.IDX[a][PT[t]-'A'];ko[t]=md(fm?ci+pi:ci-pi,26)%13;}
          if(!SAFE&&!any13(Lmax,J,ko,st2[Lmax],A2[Lmax]))continue;
          for(int L=Lmin;L<=Lmax;L++){if(!dil[L])continue;
            /* exact enumeration: slot list (t = -1 strict, else t), per slot up to 32 mod-13 solutions */
            int o=0,nslot=0,isstr=0;
            for(int t=-1;t<24;t++){
              if(t<0&&!st2[L])continue;if(t>=0&&!st2[L]&&!((A2[L]>>t)&1))continue;
              uint32_t rows=t<0?ALL24:(ALL24&~(1u<<t));long m13=0;long f13[32];int fx[32][6],fnul[32];
              for(long z=0;z<n13L[L];z++){const unsigned char*Bt=T13L[L]+z*(L+1)*N;
                if(!SAFE&&st2[L]&&t>=0&&t!=12&&t!=0){ /* cheap necessary check: the half without t */
                  if(!cons13(L,Bt,J,ko,t<12?0xFFF000u:0xFFFu,NULL,NULL))continue;}
                int x[6],nl;if(!cons13(L,Bt,J,ko,rows,x,&nl))continue;
                if(m13<32){f13[m13]=z;memcpy(fx[m13],x,sizeof x);fnul[m13]=nl;}m13++;}
              if(!m13)continue;
              /* when t >= 0 and the strict system already fits, slot t is implied by the strict fit: report strict only */
              if(t>=0&&isstr)continue;
              /* mod-2 streams agreeing with w except possibly at rank r[t] */
              long m2=0,first2[32];uint32_t km=t<0?0xFFFFFFFFu:~(1u<<r[t]);
              for(long z=0;z<n2[L];z++)if(((proj[L][z]^w)&km)==0){if(m2<32)first2[m2]=z;m2++;}
              if(!m2){xx++;
                #pragma omp critical
                printf("X %s mod2 slot mismatch q %ld a %d b %d L %d t %d\n",lab,q,a,b,L,t);continue;}
              if(t<0)isstr=1;nslot++;
              if(o<100000){o+=sprintf(buf+o,"M %s 1 %d %s %s %ld %s %s t %d slot %d n2 %ld n13c %ld S2",lab,L,TYL,fm?"beau":"vig",q,A.LAB[a],B.LAB[b],t,t<0?-1:J[t],m2,m13);
                for(long u=0;u<m2&&u<32;u++){long z=first2[u];o+=sprintf(buf+o," c");for(int bb=0;bb<L;bb++)o+=sprintf(buf+o,"%ld",(z>>bb)&1);
                  o+=sprintf(buf+o,"s");for(int bb=0;bb<L;bb++)o+=sprintf(buf+o,"%ld",(z>>(L+bb))&1);o+=sprintf(buf+o,"d%ld",(z>>(2*L))&1);}
                o+=sprintf(buf+o," S13");for(long u=0;u<m13&&u<32;u++){long z=f13[u];int c[16];long y=z;for(int bb=L-1;bb>=0;bb--){c[bb]=y%13;y/=13;}
                  o+=sprintf(buf+o," c");for(int bb=0;bb<L;bb++)o+=sprintf(buf+o,"%d%s",c[bb],bb<L-1?",":"");
                  o+=sprintf(buf+o,"x");for(int m=0;m<=L;m++)o+=sprintf(buf+o,"%d%s",fx[u][m],m<L?",":"");o+=sprintf(buf+o,"n%d",fnul[u]);}
                o+=sprintf(buf+o,"\n");}}
            if(nslot){fit[L][fm]++;str[L][fm]+=isstr;slf[L][fm]+=nslot-isstr;
              #pragma omp critical
              fputs(buf,stdout);}}}}}
    #pragma omp critical
    {for(int L=0;L<9;L++){P2[L]+=p2[L];for(int fm=0;fm<2;fm++){FIT[L][fm]+=fit[L][fm];STR[L][fm]+=str[L][fm];SLF[L][fm]+=slf[L][fm];}}XX+=xx;NCAND+=ncand;}
    free(cand);free(cpB);free(ppA);free(head);free(nxt);free(V1);free(buf);if(BS)free(BS);}
  for(int L=Lmin;L<=Lmax;L++)for(int fm=0;fm<2;fm++)
    printf("H %s 1 %d %s %s perms %ld pairs %ld pass2 %lld fits %lld strict %lld slotfits %lld\n",lab,L,TYL,fm?"beau":"vig",qhi-qlo,npairs,P2[L],FIT[L][fm],STR[L][fm],SLF[L][fm]);
  printf("O %s mismatch %lld cand %lld method %d safe %d\n",lab,XX,NCAND,meth,SAFE);
  printf("END %s %ld %ld\n",lab,qlo,qhi);return 0;}
