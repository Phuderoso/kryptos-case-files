/* Cycle 183 (IDEAS I-165): ONE-ERROR audit of case 170. Quagmire IV (plaintext-side alphabet A, ciphertext-side alphabet B) with an
   affine linear-recurrence key mod 26 on the plaintext index (M0), behind the 165,782 K3-law decimations / routes (all.bin), with ONE
   of the 24 crib key values allowed to be wrong (a mis-carved letter at that slot's carved position, or a wrong crib letter): that
   slot's key value is a free unknown. k[i] = c1 k[i-1] + ... + cL k[i-L] + d (mod 26).
   Vig k = B(c) - A(p), Beau k = B(c) + A(p) (as lrk182). Exact by CRT (case 167/169): slot t free fits mod 26 iff some v2 passes GF(2)
   AND some v13 passes GF(13) with slot t free (the strict/strict combination is reported once as a strict fit, t -1).
   Mod 2: w = cp_B ^ pa_A as lrk182; strict table T (bit L-1) as lrk180/182; one-error = Hamming-1 dilation (I-161):
     SM[x] bits 0..23 = {t : T[x ^ 1<<t] has bit Lmax}, bits 24.. = dilated L mask (T[x] | OR_t T[x ^ 1<<t]).
   method 0 (A small): U = union over A of (W1_Lmax ^ pa_A), CSR map word -> A list (W1 = dilated pass set).
   method 1 (A large): per (c, d) mod 2 at Lmax, x within distance 1 of V_cd <=> sigma(x) ^ (w0>>Lmax) in {0} u {sigma(e_t)}; hash
     join on sigma(pa_A) ^ (w0>>Lmax), up to 25 probes per (B, (c, d)); duplicates removed per perm.
   method 2 (audit): every (A, B) pair looked up in SM.
   Every candidate is re-checked against SM (X line if the dilated Lmax bit is not set).
   GF(13), per (candidate, form, L with a dilated bit): strict = lrk180 solve0. Otherwise per allowed slot t (all 24 if strict mod 2,
   else {t : T[x^e_t] bit L}): prefilter = consistency of the in-block rows (both blocks) that do not contain slot t (a necessary
   condition: the true key satisfies every such row); then exact: block-1 slot -> v13 in 0..12 through solve0; block-2 slot ->
   solve0s (block-2 rows containing it dropped, propagation check ignores it; exact as lrk181, block 2 is determined by propagation).
   -DSAFE=1: no prefilter, 13-value loop for every slot (block 2 too). The mod-2 side is confirmed with solve0 / solve0s (X if not).
   usage: lrk183 CT perms.bin alphaA alphaB label qlo qhi method Lmin Lmax tylabel
   output: H (per L, form: perms, pairs, one-error mod-2 passes, fits, strict fits, slot fits), M (fits), O, X, END            */
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
#define MAXS 16
typedef struct{int n;int sol[MAXS][16];long tot;int ovf;}SolSet;
/* lrk181 solve0s verbatim (skip = plaintext index of a free block-2 slot, -1 none) */
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
/* prefilter: GF(13) consistency of the order-L in-block rows that do not contain plaintext index `skip` (-1: all rows), early exit */
static int pre13(int L,const int*kk,int skip){
  int R[8][9],pc[8],rk=0;
  for(int b=0;b<2;b++){int lo=b?63:21,hi=b?73:33;
    for(int i=lo+L;i<=hi;i++){if(skip>=i-L&&skip<=i)continue;int row[9];for(int j=1;j<=L;j++)row[j-1]=kk[i-j-21];row[L]=1;row[L+1]=kk[i-21];
      for(int r=0;r<rk;r++){int f=row[pc[r]];if(f)for(int m=0;m<=L+1;m++)row[m]=(row[m]+169-f*R[r][m])%13;}
      int cc=-1;for(int m=0;m<=L;m++)if(row[m]){cc=m;break;}
      if(cc<0){if(row[L+1])return 0;continue;}
      int iv=inv13[row[cc]];for(int m=0;m<=L+1;m++)row[m]=row[m]*iv%13;
      for(int r=0;r<rk;r++){int f=R[r][cc];if(f)for(int m=0;m<=L+1;m++)R[r][m]=(R[r][m]+169-f*row[m])%13;}
      memcpy(R[rk],row,sizeof row);pc[rk++]=cc;}}
  return 1;}
typedef struct{int n;int (*IDX)[26];char (*LAB)[64];uint32_t*PAR;}AL;
static void load(const char*fn,AL*a){FILE*f=fopen(fn,"r");if(!f){fprintf(stderr,"open %s\n",fn);exit(1);}char al[64],lb[64];int cap=1024;
  a->IDX=malloc(cap*sizeof*a->IDX);a->LAB=malloc(cap*sizeof*a->LAB);a->n=0;
  while(fscanf(f,"%63s %63s",al,lb)==2){if(a->n==cap){cap*=2;a->IDX=realloc(a->IDX,cap*sizeof*a->IDX);a->LAB=realloc(a->LAB,cap*sizeof*a->LAB);}
    if(strlen(al)!=26){fprintf(stderr,"bad alphabet\n");exit(1);}int seen=0;for(int i=0;i<26;i++){a->IDX[a->n][al[i]-'A']=i;seen|=1<<(al[i]-'A');}
    if(seen!=(1<<26)-1){fprintf(stderr,"not a permutation\n");exit(1);}strcpy(a->LAB[a->n],lb);a->n++;}fclose(f);
  a->PAR=malloc(a->n*4);for(int i=0;i<a->n;i++){a->PAR[i]=0;for(int l=0;l<26;l++)if(a->IDX[i][l]&1)a->PAR[i]|=1u<<l;}}
static int cmp64(const void*x,const void*y){uint64_t a=*(const uint64_t*)x,b=*(const uint64_t*)y;return a<b?-1:a>b;}
static int crt(int a2,int a13){return (13*a2+14*a13)%26;}
static int prsol(char*b,const SolSet*S,int L,int cap){int o=0;for(int s=0;s<S->n&&s<cap;s++){o+=sprintf(b+o," ");for(int j=0;j<=L;j++)o+=sprintf(b+o,"%d%s",S->sol[s][j],j<L?",":"");}return o;}
int main(int argc,char**argv){
  setvbuf(stdout,NULL,_IOLBF,0);
  if(argc<12){fprintf(stderr,"usage\n");return 1;}
  const char*Cs=argv[1];if(strlen(Cs)!=N)return 1;int C[N];for(int i=0;i<N;i++)C[i]=Cs[i]-'A';
  AL A,B;load(argv[3],&A);load(argv[4],&B);const char*lab=argv[5];long qlo=atol(argv[6]),qhi=atol(argv[7]);
  int meth=atoi(argv[8]),Lmin=atoi(argv[9]),Lmax=atoi(argv[10]);const char*TYL=argv[11];
  if(Lmin<1||Lmax>6||Lmin>Lmax){fprintf(stderr,"L range\n");return 1;}
  for(int a=1;a<13;a++)for(int b=1;b<13;b++)if(a*b%13==1)inv13[a]=b;
  FILE*pf=fopen(argv[2],"rb");fseek(pf,0,SEEK_END);long np=ftell(pf)/(2*N);rewind(pf);
  short*P=malloc(np*N*2);if(fread(P,2,np*N,pf)!=(size_t)(np*N))return 2;fclose(pf);if(qhi>np)qhi=np;if(qlo>qhi)qlo=qhi;
  /* strict mod-2 table (identical construction to lrk180/182) */
  uint8_t*T=calloc(1<<24,1);
  for(int L=1;L<=Lmax;L++){
    #pragma omp parallel for schedule(dynamic,64)
    for(int b1=0;b1<8192;b1++){int k[53];for(int i=0;i<13;i++)k[i]=(b1>>i)&1;
      for(int x=0;x<(1<<(L+1));x++){int d=(x>>L)&1,ok=1;
        for(int i=21+L;i<=33&&ok;i++){int v=d;for(int j=1;j<=L;j++)if((x>>(j-1))&1)v^=k[i-j-21];if(v!=k[i-21])ok=0;}
        if(!ok)continue;int s[53];memcpy(s,k,13*sizeof(int));int b2=0;
        for(int i=34;i<=73;i++){int v=d;for(int j=1;j<=L;j++)if((x>>(j-1))&1)v^=s[i-j-21];s[i-21]=v;if(i>=63&&v)b2|=1<<(i-63);}
        uint32_t id=(uint32_t)b1|((uint32_t)b2<<13);__atomic_fetch_or(&T[id],(uint8_t)(1<<(L-1)),__ATOMIC_RELAXED);}}}
  long nest_bad=0;for(uint32_t w=0;w<(1u<<24);w++)if(T[w]&&!((T[w]>>(Lmax-1))&1))nest_bad++;
  if(nest_bad){printf("X %s nesting violated %ld\n",lab,nest_bad);return 3;}
  /* dilation */
  uint32_t*SM=calloc(1u<<24,4);
  for(uint32_t w=0;w<(1u<<24);w++){if(!T[w])continue;uint32_t lm=(uint32_t)T[w]<<24;SM[w]|=lm;int top=(T[w]>>(Lmax-1))&1;
    for(int t=0;t<24;t++){uint32_t y=w^(1u<<t);SM[y]|=lm|((uint32_t)top<<t);}}
  uint32_t DB=1u<<(24+Lmax-1);long nW1=0;for(uint32_t w=0;w<(1u<<24);w++)if(SM[w]&DB)nW1++;
  uint32_t*W1=malloc(nW1*4);{long i=0;for(uint32_t w=0;w<(1u<<24);w++)if(SM[w]&DB)W1[i++]=w;}
  uint32_t*PA=malloc(A.n*4);for(int a=0;a<A.n;a++){PA[a]=0;for(int t=0;t<24;t++)if(A.IDX[a][PT[t]-'A']&1)PA[a]|=1u<<t;}
  uint32_t*Uoff=NULL,*Ulist=NULL;
  int ncd=1<<(Lmax+1);uint32_t (*G)[64]=NULL;uint32_t*W0s=NULL;uint64_t**SK=NULL;uint64_t**SB=NULL;int sbits=24-Lmax;uint32_t (*DL)[25]=NULL;int*nDL=NULL;
  if(meth==0){long ne=(long)A.n*nW1;uint64_t*E=malloc(ne*8);long i=0;for(int a=0;a<A.n;a++)for(long j=0;j<nW1;j++)E[i++]=((uint64_t)(W1[j]^PA[a])<<24)|a;
    qsort(E,ne,8,cmp64);Uoff=calloc((1u<<24)+1,4);Ulist=malloc(ne*4);for(long j=0;j<ne;j++){Uoff[(E[j]>>24)+1]++;Ulist[j]=E[j]&0xFFFFFF;}
    for(uint32_t w=0;w<(1u<<24);w++)Uoff[w+1]+=Uoff[w];free(E);}
  else if(meth==1){G=malloc(ncd*sizeof*G);W0s=malloc(ncd*4);SK=malloc(ncd*sizeof*SK);SB=malloc(ncd*sizeof*SB);DL=malloc(ncd*sizeof*DL);nDL=malloc(ncd*sizeof(int));int L=Lmax;
    for(int cd=0;cd<ncd;cd++){uint32_t wv[8];
      for(int sv=-1;sv<L;sv++){int s[53]={0};if(sv>=0)s[sv]=1;int d=(cd>>L)&1;
        for(int i=21+L;i<=73;i++){int v=d;for(int j=1;j<=L;j++)if((cd>>(j-1))&1)v^=s[i-j-21];s[i-21]=v;}
        uint32_t w=0;for(int t=0;t<24;t++)if(s[CI[t]-21])w|=1u<<t;if(sv<0)W0s[cd]=w;else wv[sv]=w^W0s[cd];}
      for(int u=0;u<(1<<L);u++){uint32_t g=0;for(int j=0;j<L;j++)if((u>>j)&1)g^=wv[j];G[cd][u]=g>>L;}
      /* distinct offsets sigma(e_t) and 0 */
      nDL[cd]=0;for(int t=-1;t<24;t++){uint32_t x=t<0?0:1u<<t;uint32_t s=(x>>L)^G[cd][x&((1u<<L)-1)];int dup=0;for(int k=0;k<nDL[cd];k++)if(DL[cd][k]==s)dup=1;if(!dup)DL[cd][nDL[cd]++]=s;}
      SK[cd]=malloc((size_t)A.n*8);SB[cd]=calloc(((size_t)1<<sbits)/64+1,8);
      for(int a=0;a<A.n;a++){uint32_t x=PA[a];uint32_t key=((x>>L)^G[cd][x&((1u<<L)-1)])^(W0s[cd]>>L);SK[cd][a]=((uint64_t)key<<24)|a;SB[cd][key>>6]|=1ULL<<(key&63);}
      qsort(SK[cd],A.n,8,cmp64);}}
  long long FIT[9][2]={{0}},STR[9][2]={{0}},SLF[9][2]={{0}},P2[9]={0},OVF=0,XX=0,NCAND=0;long npairs=(long)A.n*B.n;
  #pragma omp parallel
  { long long fit[9][2]={{0}},str[9][2]={{0}},slf[9][2]={{0}},p2[9]={0},ovf=0,xx=0,ncand=0;uint64_t*seen=calloc(npairs/64+1,8);long cap=8000000;long*sl=malloc(sizeof(long)*cap);
    uint32_t*cpB=malloc(B.n*4);char*buf=malloc(1<<16);
    #pragma omp for schedule(dynamic,8)
    for(long q=qlo;q<qhi;q++){const short*S=P+q*N;int cl[24];uint32_t lm[26]={0};int dl[24],nd=0;long ns=0;
      for(int t=0;t<24;t++){cl[t]=C[S[CI[t]]];if(!lm[cl[t]])dl[nd++]=cl[t];lm[cl[t]]|=1u<<t;}
      for(int b=0;b<B.n;b++){uint32_t pb=B.PAR[b],cp=0;for(int j=0;j<nd;j++)cp^=lm[dl[j]]&(0u-((pb>>dl[j])&1u));cpB[b]=cp;}
      if(meth==0){for(int b=0;b<B.n;b++){uint32_t cp=cpB[b];for(uint32_t j=Uoff[cp];j<Uoff[cp+1];j++){if(ns>=cap){fprintf(stderr,"sl overflow\n");exit(4);}sl[ns++]=(long)Ulist[j]*B.n+b;}}}
      else if(meth==1){int L=Lmax;for(int b=0;b<B.n;b++){uint32_t x=cpB[b];for(int cd=0;cd<ncd;cd++){uint32_t key0=(x>>L)^G[cd][x&((1u<<L)-1)];
            for(int k=0;k<nDL[cd];k++){uint32_t key=key0^DL[cd][k];
              if(!((SB[cd][key>>6]>>(key&63))&1))continue;
              long lo=0,hi=A.n;uint64_t k0=(uint64_t)key<<24;while(lo<hi){long m=(lo+hi)/2;if(SK[cd][m]<k0)lo=m+1;else hi=m;}
              for(long m=lo;m<A.n&&(SK[cd][m]>>24)==key;m++){long id=(long)(SK[cd][m]&0xFFFFFF)*B.n+b;if((seen[id>>6]>>(id&63))&1)continue;seen[id>>6]|=1ULL<<(id&63);
                if(ns>=cap){fprintf(stderr,"sl overflow\n");exit(4);}sl[ns++]=id;}}}}
        for(long i=0;i<ns;i++)seen[sl[i]>>6]=0;}
      else {for(int a=0;a<A.n;a++)for(int b=0;b<B.n;b++){uint32_t bits=cpB[b]^PA[a];if(SM[bits]&DB){if(ns>=cap){fprintf(stderr,"sl overflow\n");exit(4);}sl[ns++]=(long)a*B.n+b;}}}
      ncand+=ns;
      for(long i=0;i<ns;i++){int a=sl[i]/B.n,b=sl[i]%B.n;uint32_t x=cpB[b]^PA[a];uint32_t sm=SM[x];
        if(!(sm&DB)){xx++;
          #pragma omp critical
          printf("X %s method/table mismatch q %ld a %d b %d\n",lab,q,a,b);
          continue;}
        int ko[24];for(int fm=0;fm<2;fm++){
          for(int t=0;t<24;t++){int ci=B.IDX[b][cl[t]],pi=A.IDX[a][PT[t]-'A'];ko[t]=md(fm?ci+pi:ci-pi,26);}
          int k13[53]={0},k2[53]={0};for(int t=0;t<24;t++){k13[CI[t]-21]=ko[t]%13;k2[CI[t]-21]=ko[t]&1;}
          for(int L=Lmin;L<=Lmax;L++){if(!((sm>>(24+L-1))&1))continue;if(fm==0)p2[L]++;
            int st2=(T[x]>>(L-1))&1;uint32_t A2;
            if(L==Lmax)A2=sm&0xFFFFFF;else{A2=0;for(int t=0;t<24;t++)if((T[x^(1u<<t)]>>(L-1))&1)A2|=1u<<t;}
            int o=0,nslot=0,isstrict=0;
            int st13=0;SolSet B13;B13.tot=0;
            if(SAFE||pre13(L,k13,-1)){solve0(13,L,k13,&B13);if(B13.ovf)ovf++;st13=B13.tot>0;}
            if(st2&&st13){isstrict=1;nslot=24;SolSet A2s;solve0(2,L,k2,&A2s);
              if(!A2s.tot){xx++;
                #pragma omp critical
                printf("X %s strict mismatch q %ld a %d b %d L %d\n",lab,q,a,b,L);continue;}
              o+=sprintf(buf+o,"M %s 0 %d %s %s %ld %s %s t -1 slot -1 V -1 n2 %ld n13 %ld S2",lab,L,TYL,fm?"beau":"vig",q,A.LAB[a],B.LAB[b],A2s.tot,B13.tot);
              o+=prsol(buf+o,&A2s,L,8);o+=sprintf(buf+o," S13");o+=prsol(buf+o,&B13,L,8);o+=sprintf(buf+o,"\n");}
            else for(int t=0;t<24;t++){int ob=ko[t]&1,ok2[2];ok2[ob]=st2;ok2[ob^1]=(A2>>t)&1;if(!ok2[0]&&!ok2[1])continue;
              int sl_=CI[t]-21,orig=k13[sl_],got=0;
              if(!SAFE&&!pre13(L,k13,CI[t]))continue;
              if(t>=13&&!SAFE){SolSet Bv;solve0s(13,L,k13,&Bv,CI[t]);if(Bv.ovf)ovf++;if(!Bv.tot)continue;
                SolSet As;solve0s(2,L,k2,&As,CI[t]);
                if(!As.tot){xx++;
                  #pragma omp critical
                  printf("X %s block2 mismatch q %ld a %d b %d L %d t %d\n",lab,q,a,b,L,t);continue;}
                got=1;if(o<60000){o+=sprintf(buf+o,"M %s 0 %d %s %s %ld %s %s t %d slot %d V -2 n2 %ld n13 %ld S2",lab,L,TYL,fm?"beau":"vig",q,A.LAB[a],B.LAB[b],t,CI[t],As.tot,Bv.tot);
                  o+=prsol(buf+o,&As,L,8);o+=sprintf(buf+o," S13");o+=prsol(buf+o,&Bv,L,8);o+=sprintf(buf+o,"\n");}
                nslot++;continue;}
              for(int v=0;v<13;v++){SolSet Bv;if(v==orig){if(!st13)continue;Bv=B13;}else{k13[sl_]=v;solve0(13,L,k13,&Bv);k13[sl_]=orig;if(Bv.ovf)ovf++;if(!Bv.tot)continue;}
                for(int v2=0;v2<2;v2++){if(!ok2[v2])continue;if(v2==ob&&v==orig)continue;
                  int k2v[53];memcpy(k2v,k2,sizeof k2v);k2v[sl_]=v2;SolSet As;solve0(2,L,k2v,&As);
                  if(!As.tot){xx++;
                    #pragma omp critical
                    printf("X %s slot mismatch q %ld a %d b %d L %d t %d\n",lab,q,a,b,L,t);continue;}
                  got=1;if(o<60000){o+=sprintf(buf+o,"M %s 0 %d %s %s %ld %s %s t %d slot %d V %d n2 %ld n13 %ld S2",lab,L,TYL,fm?"beau":"vig",q,A.LAB[a],B.LAB[b],t,CI[t],crt(v2,v),As.tot,Bv.tot);
                    o+=prsol(buf+o,&As,L,8);o+=sprintf(buf+o," S13");o+=prsol(buf+o,&Bv,L,8);o+=sprintf(buf+o,"\n");}}}
              nslot+=got;}
            if(nslot){fit[L][fm]++;slf[L][fm]+=nslot;str[L][fm]+=isstrict;
              #pragma omp critical
              fputs(buf,stdout);}}}}}
    #pragma omp critical
    {for(int L=0;L<9;L++){P2[L]+=p2[L];for(int fm=0;fm<2;fm++){FIT[L][fm]+=fit[L][fm];STR[L][fm]+=str[L][fm];SLF[L][fm]+=slf[L][fm];}}OVF+=ovf;XX+=xx;NCAND+=ncand;}
    free(seen);free(sl);free(cpB);free(buf);}
  for(int L=Lmin;L<=Lmax;L++)for(int fm=0;fm<2;fm++)
    printf("H %s 0 %d %s %s perms %ld pairs %ld pass2 %lld fits %lld strict %lld slotfits %lld\n",lab,L,TYL,fm?"beau":"vig",qhi-qlo,npairs,P2[L],FIT[L][fm],STR[L][fm],SLF[L][fm]);
  printf("O %s overflow %lld mismatch %lld cand %lld method %d safe %d nW1 %ld\n",lab,OVF,XX,NCAND,meth,SAFE,nW1);
  printf("END %s %ld %ld\n",lab,qlo,qhi);return 0;}
