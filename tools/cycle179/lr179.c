/* Cycle 179 (IDEAS I-141): ONE-ERROR linear-recurrence key mod 26 behind the 165,782 K3-law decimations / routes (all.bin),
   the audit of case 166. Same family as lr178 (k[i] = c1 k[i-1] + ... + cL k[i-L] + d mod 26, arbitrary c, d, seed; tableau
   A-Z or KRYPTOS; Vigenere k = ct - pt or Beaufort k = ct + pt), but ONE of the 24 crib key values may be wrong (a mis-carved
   letter at that slot's carved position, or a wrong crib letter): the key value at that slot is a free unknown.
   Exactness via CRT: with slot t free, a mod-26 fit exists iff some v2 in Z2 makes the GF(2) system pass AND some v13 in Z13
   makes the GF(13) system pass (k[t] = CRT(v2, v13)); the error slot must be the SAME slot in both moduli.
   mode 0 (ix 0, key on the plaintext index): for every slot t, v2 in {0,1}: lr178's solve0 (equations inside the crib blocks +
     propagation across the gap) over GF(2); for every t that passes mod 2, v13 in 0..12 over GF(13).
   mode 1 (ix 1, key on the carved index, seed at carved 0..L-1): mod 2, every stream (2^(2L+1)) whose 24 crib bits mismatch
     in at most ONE slot gives the allowed slot set T2 (0 mismatches -> every slot); then for every c mod 13 the 24 equations
     linear in (seed, d) are eliminated with slot t left out, for t in T2 (all 24 rows first: consistent -> every slot).
   A strict fit (no error) counts as a fit for every slot; the H line separates strict fits and one-error-only fits.
   usage: lr179 CT perms.bin label qlo qhi mode Lmin Lmax
   output: H lines (counts per L, alphabet, form), M lines (fits: q, slot t, v2/v13 sets, solution lists), END               */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define N 97
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char*PT="EASTNORTHEASTBERLINCLOCK",*KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static int pav[2][24],cidx[2][26],inv13[13];
static int md(int a,int p){a%=p;return a<0?a+p:a;}
#define MAXS 16
typedef struct{int n;int sol[MAXS][16];long tot;int ovf;}SolSet;
static void solve0(int p,int L,const int*kk,SolSet*S){            /* identical algebra to lr178 solve0 */
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
static unsigned char*T13;static long n13c;
static void build13(int L){n13c=1;for(int i=0;i<L;i++)n13c*=13;free(T13);T13=malloc(n13c*(L+1)*N);
  #pragma omp parallel for schedule(static)
  for(long z=0;z<n13c;z++){int c[16];long y=z;for(int i=L-1;i>=0;i--){c[i]=y%13;y/=13;}
    for(int m=0;m<=L;m++){unsigned char*s=T13+(z*(L+1)+m)*N;for(int j=0;j<L;j++)s[j]=(m==j);
      for(int j=L;j<N;j++){int v=(m==L);for(int a=1;a<=L;a++)v+=c[a-1]*s[j-a];s[j]=v%13;}}}}
/* GF(13) consistency of the 24 rows for weight table B, skipping row `skip` (-1 = none); returns 1 if consistent */
static int cons13(const unsigned char*B,int L,const int*J,const int*ko13,int skip,int*xout,int*nul){
  int R[17][18],rk=0,pc[17];
  for(int t=0;t<24;t++){if(t==skip)continue;int row[18];for(int m=0;m<=L;m++)row[m]=B[m*N+J[t]];row[L+1]=ko13[t];
    for(int r=0;r<rk;r++){int f=row[pc[r]];if(f)for(int m=0;m<=L+1;m++)row[m]=(row[m]+169-f*R[r][m])%13;}
    int cc=-1;for(int m=0;m<=L;m++)if(row[m]){cc=m;break;}
    if(cc<0){if(row[L+1])return 0;continue;}
    int iv=inv13[row[cc]];for(int m=0;m<=L+1;m++)row[m]=row[m]*iv%13;
    for(int r=0;r<rk;r++){int f=R[r][cc];if(f)for(int m=0;m<=L+1;m++)R[r][m]=(R[r][m]+169-f*row[m])%13;}
    memcpy(R[rk],row,sizeof row);pc[rk++]=cc;}
  if(xout){for(int m=0;m<=L;m++)xout[m]=0;for(int r=0;r<rk;r++)xout[pc[r]]=R[r][L+1];*nul=L+1-rk;}
  return 1;}
int main(int argc,char**argv){
  setvbuf(stdout,NULL,_IOLBF,0);
  if(argc<9){fprintf(stderr,"usage\n");return 1;}
  const char*Cs=argv[1];if(strlen(Cs)!=N)return 1;int C[N];for(int i=0;i<N;i++)C[i]=Cs[i]-'A';
  const char*lab=argv[3];long qlo=atol(argv[4]),qhi=atol(argv[5]);int mode=atoi(argv[6]),Lmin=atoi(argv[7]),Lmax=atoi(argv[8]);
  for(int a=1;a<13;a++)for(int b=1;b<13;b++)if(a*b%13==1)inv13[a]=b;
  for(int t=0;t<24;t++){pav[0][t]=PT[t]-'A';pav[1][t]=strchr(KA,PT[t])-KA;}
  for(int l=0;l<26;l++){cidx[0][l]=l;cidx[1][l]=strchr(KA,'A'+l)-KA;}
  FILE*pf=fopen(argv[2],"rb");fseek(pf,0,SEEK_END);long np=ftell(pf)/(2*N);rewind(pf);
  short*P=malloc(np*N*2);if(fread(P,2,np*N,pf)!=(size_t)(np*N))return 2;fclose(pf);if(qhi>np)qhi=np;
  if(mode==0){
    for(int L=Lmin;L<=Lmax;L++){long long fit[2][2]={{0}},strict[2][2]={{0}},slotfits[2][2]={{0}},ovf[2][2]={{0}},p2[2][2]={{0}};
      #pragma omp parallel for schedule(dynamic,128) reduction(+:fit[:2][:2],strict[:2][:2],slotfits[:2][:2],ovf[:2][:2],p2[:2][:2])
      for(long q=qlo;q<qhi;q++){const short*S=P+q*N;
        for(int pa=0;pa<2;pa++){int kf[2][53];
          for(int fm=0;fm<2;fm++){for(int i=0;i<53;i++)kf[fm][i]=0;
            for(int t=0;t<24;t++){int ci=cidx[pa][C[S[CI[t]]]];kf[fm][CI[t]-21]=md(fm?ci+pav[pa][t]:ci-pav[pa][t],26);}}
          /* mod 2 is the same for Vigenere and Beaufort (they differ by 2p) */
          int k2[53];for(int i=0;i<53;i++)k2[i]=kf[0][i]&1;
          int ok2[24][2];int any2=0;int st2;SolSet A;
          solve0(2,L,k2,&A);st2=(A.tot>0)||A.ovf;
          for(int t=0;t<24;t++){int sl=CI[t]-21,orig=k2[sl];
            for(int v=0;v<2;v++){if(v==orig){ok2[t][v]=st2;continue;}k2[sl]=v;solve0(2,L,k2,&A);ok2[t][v]=(A.tot>0)||A.ovf;if(A.ovf)ovf[pa][0]++;k2[sl]=orig;}
            any2|=ok2[t][0]|ok2[t][1];}
          if(!any2)continue;
          for(int fm=0;fm<2;fm++){p2[pa][fm]++;int k13[53];for(int i=0;i<53;i++)k13[i]=kf[fm][i]%13;
            SolSet B;solve0(13,L,k13,&B);int st13=(B.tot>0)||B.ovf;
            if(st2&&st13){strict[pa][fm]++;}
            int nslot=0;char buf[16384];int o=0;
            for(int t=0;t<24;t++){if(!(ok2[t][0]|ok2[t][1]))continue;int sl=CI[t]-21,orig=k13[sl];int m13=0;long tot13=0;int o13=0;char b13[4096];
              for(int v=0;v<13;v++){int pass;if(v==orig){pass=st13;if(pass)tot13+=B.tot;}else{k13[sl]=v;SolSet Bv;solve0(13,L,k13,&Bv);pass=(Bv.tot>0)||Bv.ovf;if(Bv.ovf)ovf[pa][fm]++;
                  if(pass&&o13<3500){o13+=sprintf(b13+o13," v%d:",v);for(int s=0;s<Bv.n&&s<4;s++){for(int j=0;j<=L;j++)o13+=sprintf(b13+o13,"%d%s",Bv.sol[s][j],j<L?",":"");o13+=sprintf(b13+o13,";");}}
                  tot13+=Bv.tot;k13[sl]=orig;}
                if(pass&&v==orig&&o13<3500){o13+=sprintf(b13+o13," v%d:",v);for(int s=0;s<B.n&&s<4;s++){for(int j=0;j<=L;j++)o13+=sprintf(b13+o13,"%d%s",B.sol[s][j],j<L?",":"");o13+=sprintf(b13+o13,";");}}
                m13+=pass;}
              if(!m13)continue;nslot++;
              /* mod-2 solutions for the passing v2 values */
              char b2[2048];int o2=0;int k2b[53];memcpy(k2b,k2,sizeof k2b);
              for(int v=0;v<2;v++)if(ok2[t][v]){k2b[sl]=v;SolSet A2;solve0(2,L,k2b,&A2);o2+=sprintf(b2+o2," v%d:",v);
                for(int s=0;s<A2.n&&s<6;s++){for(int j=0;j<=L;j++)o2+=sprintf(b2+o2,"%d%s",A2.sol[s][j],j<L?",":"");o2+=sprintf(b2+o2,";");}}
              if(o<12000)o+=sprintf(buf+o,"M %s 0 %d %s %s %ld t %d slot %d obs %d S2%s S13%s\n",lab,L,pa?"ka":"az",fm?"beau":"vig",q,t,CI[t],kf[fm][sl],b2,b13);}
            if(nslot){fit[pa][fm]++;slotfits[pa][fm]+=nslot;
              #pragma omp critical
              fputs(buf,stdout);}
          }}}
      for(int pa=0;pa<2;pa++)for(int fm=0;fm<2;fm++)printf("H %s 0 %d %s %s cfg %ld pass2any %lld fits %lld strict %lld slotfits %lld ovf %lld\n",lab,L,pa?"ka":"az",fm?"beau":"vig",qhi-qlo,p2[pa][fm],fit[pa][fm],strict[pa][fm],slotfits[pa][fm],ovf[pa][fm]);
    }
  } else {
    for(int L=Lmin;L<=Lmax;L++){
      long n2=1L<<(2*L+1);uint64_t*S2=malloc(n2*16);
      for(long z=0;z<n2;z++){int c=z&((1<<L)-1),sd=(z>>L)&((1<<L)-1),d=(z>>(2*L))&1;int s[N];
        for(int j=0;j<L;j++)s[j]=(sd>>j)&1;for(int j=L;j<N;j++){int v=d;for(int a=1;a<=L;a++)if((c>>(a-1))&1)v^=s[j-a];s[j]=v;}
        uint64_t lo=0,hi=0;for(int j=0;j<N;j++)if(s[j]){if(j<64)lo|=1ULL<<j;else hi|=1ULL<<(j-64);}S2[2*z]=lo;S2[2*z+1]=hi;}
      build13(L);
      long long fit[2][2]={{0}},p2[2][2]={{0}},strict[2][2]={{0}},slotfits[2][2]={{0}};
      #pragma omp parallel for schedule(dynamic,64) reduction(+:fit[:2][:2],p2[:2][:2],strict[:2][:2],slotfits[:2][:2])
      for(long q=qlo;q<qhi;q++){const short*S=P+q*N;int J[24];uint64_t Mlo=0,Mhi=0;int slotof[N];
        for(int t=0;t<24;t++){J[t]=S[CI[t]];slotof[J[t]]=t;if(J[t]<64)Mlo|=1ULL<<J[t];else Mhi|=1ULL<<(J[t]-64);}
        for(int pa=0;pa<2;pa++){int ko[2][24];uint64_t Vlo=0,Vhi=0;
          for(int fm=0;fm<2;fm++)for(int t=0;t<24;t++){int ci=cidx[pa][C[J[t]]];ko[fm][t]=md(fm?ci+pav[pa][t]:ci-pav[pa][t],26);}
          for(int t=0;t<24;t++)if(ko[0][t]&1){if(J[t]<64)Vlo|=1ULL<<J[t];else Vhi|=1ULL<<(J[t]-64);}
          uint32_t T2=0;int st2=0;long ex2[24];for(int t=0;t<24;t++)ex2[t]=-1;long ex0=-1;
          for(long z=0;z<n2;z++){uint64_t a=(S2[2*z]^Vlo)&Mlo,b=(S2[2*z+1]^Vhi)&Mhi;int pc=__builtin_popcountll(a)+__builtin_popcountll(b);
            if(pc==0){st2=1;T2=0xFFFFFF;if(ex0<0)ex0=z;}
            else if(pc==1){int pos=a?__builtin_ctzll(a):64+__builtin_ctzll(b);int t=slotof[pos];T2|=1u<<t;if(ex2[t]<0)ex2[t]=z;}}
          if(!T2)continue;
          for(int fm=0;fm<2;fm++){p2[pa][fm]++;int ko13[24];for(int t=0;t<24;t++)ko13[t]=ko[fm][t]%13;
            uint32_t TT13=0;long nc13=0;int st13=0;long exc[24];int exx[24][17],exn[24];for(int t=0;t<24;t++)exc[t]=-1;
            for(long z=0;z<n13c;z++){const unsigned char*B=T13+z*(L+1)*N;uint32_t got=0;
              int xx[17],nn;if(cons13(B,L,J,ko13,-1,xx,&nn)){got=0xFFFFFF;st13=1;for(int t=0;t<24;t++)if(exc[t]<0){exc[t]=z;memcpy(exx[t],xx,sizeof xx);exn[t]=nn;}}
              else for(int t=0;t<24;t++)if((T2>>t)&1){if(cons13(B,L,J,ko13,t,xx,&nn)){got|=1u<<t;if(exc[t]<0){exc[t]=z;memcpy(exx[t],xx,sizeof xx);exn[t]=nn;}}}
              if(got&T2){nc13++;TT13|=got;}}
            uint32_t F=T2&TT13;if(!F)continue;
            if(st2&&st13)strict[pa][fm]++;
            fit[pa][fm]++;slotfits[pa][fm]+=__builtin_popcount(F);
            char buf[16384];int o=0;
            for(int t=0;t<24;t++)if((F>>t)&1){long z=ex2[t]>=0?ex2[t]:ex0;long c13=exc[t];int c[16];long y=c13;for(int a=L-1;a>=0;a--){c[a]=y%13;y/=13;}
              o+=sprintf(buf+o,"M %s 1 %d %s %s %ld t %d slot %d carved %d nc13 %ld S2 c",lab,L,pa?"ka":"az",fm?"beau":"vig",q,t,CI[t],J[t],nc13);
              for(int a=0;a<L;a++)o+=sprintf(buf+o,"%ld",(z>>a)&1);o+=sprintf(buf+o,"s");for(int a=0;a<L;a++)o+=sprintf(buf+o,"%ld",(z>>(L+a))&1);o+=sprintf(buf+o,"d%ld",(z>>(2*L))&1);
              o+=sprintf(buf+o," S13 c");for(int a=0;a<L;a++)o+=sprintf(buf+o,"%d%s",c[a],a<L-1?",":"");o+=sprintf(buf+o,"x");
              for(int m=0;m<=L;m++)o+=sprintf(buf+o,"%d%s",exx[t][m],m<L?",":"");o+=sprintf(buf+o,"n%d\n",exn[t]);if(o>15000)break;}
            #pragma omp critical
            fputs(buf,stdout);}
        }}
      for(int pa=0;pa<2;pa++)for(int fm=0;fm<2;fm++)printf("H %s 1 %d %s %s cfg %ld pass2any %lld fits %lld strict %lld slotfits %lld ovf 0\n",lab,L,pa?"ka":"az",fm?"beau":"vig",qhi-qlo,p2[pa][fm],fit[pa][fm],strict[pa][fm],slotfits[pa][fm]);
      free(S2);}
  }
  printf("END %s %ld %ld\n",lab,qlo,qhi);return 0;}
