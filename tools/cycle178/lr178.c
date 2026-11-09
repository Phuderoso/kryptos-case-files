/* Cycle 178 (IDEAS I-137): linear-recurrence key mod 26 behind the 165,782 K3-law decimations / routes (all.bin), both layer orders.
   Key k[i] = c1 k[i-1] + ... + cL k[i-L] + d (mod 26), ARBITRARY weights c and constant d, any seed. Tableau A-Z or KRYPTOS (pa),
   Vigenere k = ct - pt or Beaufort k = ct + pt (indices in the tableau alphabet); variant = -Vig maps the family onto itself.
   Perm convention as gm176/gm177: plaintext position i is carved at S[i].
   mode 0 (ix 0: key on the plaintext index, then transpose) - ALGEBRAIC: the 24 crib key values k[21..33], k[63..73] are known
     for each perm. The recurrence equations inside the blocks (i = 21+L..33 and 63+L..73) are LINEAR in x = (c1..cL, d). Solve
     them separately over GF(2) and GF(13) (Z26 = Z2 x Z13, CRT), enumerate the solution space of each, propagate k[34..73] from
     the 13 block-1 values mod p and require all 11 BERLINCLOCK key values mod p. A mod-26 fit exists iff a mod-2 AND a mod-13
     solution survive; #fits mod 26 = n2 * n13. (Seed upstream of 21 is not required to exist: superset of every seed, incl.
     vocabulary seeds.)
   mode 1 (ix 1: transpose first, key on the carved index, seed at carved 0..L-1, arbitrary) - CRT: mod 2, every stream
     (2^(2L+1)) is a 97-bit word; a perm passes iff some stream matches the 24 key bits at the crib slots' carved positions.
     Survivors go to GF(13): for every c mod 13 the stream is linear in (seed, d) (precomputed basis table), 24 equations solved
     by incremental elimination. Fit iff both moduli consistent.
   mode 2 (W: small weights c in {0,1}^L, c != 0, d in Z26, seed = first L letters of a vocabulary word, numbered A-Z or KRYPTOS;
     ix 0 seed at PT 0..L-1 -> exact 24-letter hash join; ix 1 seed at carved 0..L-1 -> decrypt + triple-position index).
   usage: lr178 CT perms.bin label qlo qhi mode Lmin Lmax [ix seedfile]
   output: H lines (counts), M lines (fits with solution lists), END                                                         */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define N 97
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char*PT="EASTNORTHEASTBERLINCLOCK",*KA="KRYPTOSABCDEFGHIJLMNQUVWXZ",*AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ";
static int pav[2][24],cidx[2][26];
static int inv13[13];
static int md(int a,int p){a%=p;return a<0?a+p:a;}
/* ---------- mode 0 ---------- */
#define MAXS 64
typedef struct{int n;int sol[MAXS][16];long tot;int ovf;}SolSet;
/* solve rows (A|b) mod p (n unknowns), enumerate solutions, keep those passing the link; returns count */
static void solve0(int p,int L,const int*kk /*k[21..73] mod p, index i-21*/,SolSet*S){
  int n=L+1,A[24][17],nr=0;S->n=0;S->tot=0;S->ovf=0;
  for(int i=21+L;i<=33;i++){for(int j=1;j<=L;j++)A[nr][j-1]=kk[i-j-21];A[nr][L]=1;A[nr][n]=kk[i-21];nr++;}
  for(int i=63+L;i<=73;i++){for(int j=1;j<=L;j++)A[nr][j-1]=kk[i-j-21];A[nr][L]=1;A[nr][n]=kk[i-21];nr++;}
  int piv[17],rk=0;for(int col=0;col<n&&rk<nr;col++){int r=-1;for(int i=rk;i<nr;i++)if(A[i][col]%p){r=i;break;}if(r<0)continue;
    if(r!=rk)for(int j=0;j<=n;j++){int t=A[r][j];A[r][j]=A[rk][j];A[rk][j]=t;}
    int iv=p==2?1:inv13[A[rk][col]%p];for(int j=0;j<=n;j++)A[rk][j]=(A[rk][j]*iv)%p;
    for(int i=0;i<nr;i++)if(i!=rk&&A[i][col]%p){int f=A[i][col];for(int j=0;j<=n;j++)A[i][j]=md(A[i][j]-f*A[rk][j],p);}
    piv[rk++]=col;}
  for(int i=rk;i<nr;i++)if(A[i][n]%p)return;           /* inconsistent */
  int isp[17]={0};for(int r=0;r<rk;r++)isp[piv[r]]=1;int fr[17],nf=0;for(int j=0;j<n;j++)if(!isp[j])fr[nf++]=j;
  long ns=1;for(int i=0;i<nf;i++){ns*=p;if(ns>5000000){S->ovf=1;return;}}
  for(long z=0;z<ns;z++){int x[17];long y=z;for(int i=0;i<nf;i++){x[fr[i]]=y%p;y/=p;}
    for(int r=0;r<rk;r++){int v=A[r][n];for(int i=0;i<nf;i++)v-=A[r][fr[i]]*x[fr[i]];x[piv[r]]=md(v,p);}
    int s[53];memcpy(s,kk,13*sizeof(int));int ok=1;
    for(int i=34;i<=73&&ok;i++){int v=x[L];for(int j=1;j<=L;j++)v+=x[j-1]*s[i-j-21];v%=p;s[i-21]=v;if(i>=63&&v!=kk[i-21])ok=0;}
    if(!ok)continue;S->tot++;if(S->n<MAXS){memcpy(S->sol[S->n],x,n*sizeof(int));S->n++;}}
}
/* ---------- mode 1 tables ---------- */
static unsigned char*T13; static long n13c;
static void build13(int L){n13c=1;for(int i=0;i<L;i++)n13c*=13;free(T13);T13=malloc(n13c*(L+1)*N);
  #pragma omp parallel for schedule(static)
  for(long z=0;z<n13c;z++){int c[16];long y=z;for(int i=L-1;i>=0;i--){c[i]=y%13;y/=13;}
    for(int m=0;m<=L;m++){unsigned char*s=T13+(z*(L+1)+m)*N;for(int j=0;j<L;j++)s[j]=(m==j);
      for(int j=L;j<N;j++){int v=(m==L);for(int a=1;a<=L;a++)v+=c[a-1]*s[j-a];s[j]=v%13;}}}}
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
    for(int L=Lmin;L<=Lmax;L++){long long fit[2][2]={{0}},sols[2][2]={{0}},ovf[2][2]={{0}},p2[2][2]={{0}};
      #pragma omp parallel for schedule(dynamic,256) reduction(+:fit[:2][:2],sols[:2][:2],ovf[:2][:2],p2[:2][:2])
      for(long q=qlo;q<qhi;q++){const short*S=P+q*N;
        for(int pa=0;pa<2;pa++)for(int fm=0;fm<2;fm++){int k[53];for(int i=21;i<=73;i++)k[i-21]=0;
          for(int t=0;t<24;t++){int ci=cidx[pa][C[S[CI[t]]]];k[CI[t]-21]=md(fm?ci+pav[pa][t]:ci-pav[pa][t],26);}
          int k2[53],k13[53];for(int i=0;i<53;i++){k2[i]=k[i]%2;k13[i]=k[i]%13;}
          SolSet A2,A13;solve0(2,L,k2,&A2);if(A2.ovf)ovf[pa][fm]++;if(!A2.tot&&!A2.ovf)continue;p2[pa][fm]++;
          solve0(13,L,k13,&A13);if(A13.ovf)ovf[pa][fm]++;if(!A13.tot)continue;
          if(A2.ovf||A13.ovf){
            #pragma omp critical
            printf("O %s 0 %d %s %s %ld ovf2 %d ovf13 %d\n",lab,L,pa?"ka":"az",fm?"beau":"vig",q,A2.ovf,A13.ovf);
            continue;}
          fit[pa][fm]++;sols[pa][fm]+=A2.tot*A13.tot;
          char buf[8192];int o=sprintf(buf,"M %s 0 %d %s %s %ld n2 %ld n13 %ld S2",lab,L,pa?"ka":"az",fm?"beau":"vig",q,A2.tot,A13.tot);
          for(int s=0;s<A2.n&&s<32;s++){o+=sprintf(buf+o," ");for(int j=0;j<=L;j++)o+=sprintf(buf+o,"%d%s",A2.sol[s][j],j<L?",":"");}
          o+=sprintf(buf+o," S13");for(int s=0;s<A13.n&&s<32;s++){o+=sprintf(buf+o," ");for(int j=0;j<=L;j++)o+=sprintf(buf+o,"%d%s",A13.sol[s][j],j<L?",":"");}
          #pragma omp critical
          printf("%s\n",buf);}
      }
      for(int pa=0;pa<2;pa++)for(int fm=0;fm<2;fm++)printf("H %s 0 %d %s %s cfg %ld pass2 %lld fits %lld sols %lld ovf %lld\n",lab,L,pa?"ka":"az",fm?"beau":"vig",qhi-qlo,p2[pa][fm],fit[pa][fm],sols[pa][fm],ovf[pa][fm]);
    }
  } else if(mode==1){
    for(int L=Lmin;L<=Lmax;L++){
      long n2=1L<<(2*L+1);uint64_t*S2=malloc(n2*16);
      for(long z=0;z<n2;z++){int c=z&((1<<L)-1),sd=(z>>L)&((1<<L)-1),d=(z>>(2*L))&1;int s[N];
        for(int j=0;j<L;j++)s[j]=(sd>>j)&1;for(int j=L;j<N;j++){int v=d;for(int a=1;a<=L;a++)if((c>>(a-1))&1)v^=s[j-a];s[j]=v;}
        uint64_t lo=0,hi=0;for(int j=0;j<N;j++)if(s[j]){if(j<64)lo|=1ULL<<j;else hi|=1ULL<<(j-64);}S2[2*z]=lo;S2[2*z+1]=hi;}
      build13(L);
      long long fit[2][2]={{0}},p2[2][2]={{0}},sols[2][2]={{0}};
      #pragma omp parallel for schedule(dynamic,64) reduction(+:fit[:2][:2],p2[:2][:2],sols[:2][:2])
      for(long q=qlo;q<qhi;q++){const short*S=P+q*N;int J[24];uint64_t Mlo=0,Mhi=0;
        for(int t=0;t<24;t++){J[t]=S[CI[t]];if(J[t]<64)Mlo|=1ULL<<J[t];else Mhi|=1ULL<<(J[t]-64);}
        for(int pa=0;pa<2;pa++)for(int fm=0;fm<2;fm++){int ko[24];uint64_t Vlo=0,Vhi=0;
          for(int t=0;t<24;t++){int ci=cidx[pa][C[J[t]]];ko[t]=md(fm?ci+pav[pa][t]:ci-pav[pa][t],26);
            if(ko[t]&1){if(J[t]<64)Vlo|=1ULL<<J[t];else Vhi|=1ULL<<(J[t]-64);}}
          long m2=0;long first2[32];for(long z=0;z<n2;z++)if(!((S2[2*z]^Vlo)&Mlo)&&!((S2[2*z+1]^Vhi)&Mhi)){if(m2<32)first2[m2]=z;m2++;}
          if(!m2)continue;p2[pa][fm]++;
          long m13=0;long f13[32];int fx[32][17];int fnul[32];
          for(long z=0;z<n13c;z++){const unsigned char*B=T13+z*(L+1)*N;int R[17][18],rk=0,pc[17],ok=1;
            for(int t=0;t<24&&ok;t++){int row[18];for(int m=0;m<=L;m++)row[m]=B[m*N+J[t]];row[L+1]=ko[t]%13;
              for(int r=0;r<rk;r++){int f=row[pc[r]];if(f)for(int m=0;m<=L+1;m++)row[m]=(row[m]+13*13-f*R[r][m])%13;}
              int cc=-1;for(int m=0;m<=L;m++)if(row[m]){cc=m;break;}
              if(cc<0){if(row[L+1])ok=0;continue;}
              int iv=inv13[row[cc]];for(int m=0;m<=L+1;m++)row[m]=row[m]*iv%13;
              for(int r=0;r<rk;r++){int f=R[r][cc];if(f)for(int m=0;m<=L+1;m++)R[r][m]=(R[r][m]+13*13-f*row[m])%13;}
              memcpy(R[rk],row,sizeof row);pc[rk++]=cc;}
            if(!ok)continue;
            long mult=1;for(int i=rk;i<=L;i++)mult*=13;
            if(m13<32){f13[m13]=z;int x[17]={0};for(int r=0;r<rk;r++)x[pc[r]]=R[r][L+1];memcpy(fx[m13],x,sizeof x);fnul[m13]=L+1-rk;}
            m13+=1;sols[pa][fm]+=0;(void)mult;}
          if(!m13)continue;fit[pa][fm]++;sols[pa][fm]+=m2*m13;
          char buf[16384];int o=sprintf(buf,"M %s 1 %d %s %s %ld n2 %ld n13c %ld S2",lab,L,pa?"ka":"az",fm?"beau":"vig",q,m2,m13);
          for(long i=0;i<m2&&i<32;i++){long z=first2[i];o+=sprintf(buf+o," c");for(int a=0;a<L;a++)o+=sprintf(buf+o,"%ld",(z>>a)&1);
            o+=sprintf(buf+o,"s");for(int a=0;a<L;a++)o+=sprintf(buf+o,"%ld",(z>>(L+a))&1);o+=sprintf(buf+o,"d%ld",(z>>(2*L))&1);}
          o+=sprintf(buf+o," S13");for(long i=0;i<m13&&i<32;i++){long z=f13[i];int c[16];long y=z;for(int a=L-1;a>=0;a--){c[a]=y%13;y/=13;}
            o+=sprintf(buf+o," c");for(int a=0;a<L;a++)o+=sprintf(buf+o,"%d%s",c[a],a<L-1?",":"");
            o+=sprintf(buf+o,"x");for(int m=0;m<=L;m++)o+=sprintf(buf+o,"%d%s",fx[i][m],m<L?",":"");o+=sprintf(buf+o,"n%d",fnul[i]);}
          #pragma omp critical
          printf("%s\n",buf);}
      }
      for(int pa=0;pa<2;pa++)for(int fm=0;fm<2;fm++)printf("H %s 1 %d %s %s cfg %ld pass2 %lld fits %lld sols %lld ovf 0\n",lab,L,pa?"ka":"az",fm?"beau":"vig",qhi-qlo,p2[pa][fm],fit[pa][fm],sols[pa][fm]);
      free(S2);
    }
  } else {
    int ix=atoi(argv[9]);char words[512][40];int nw=0;FILE*f=fopen(argv[10],"r");while(nw<512&&fscanf(f,"%39s",words[nw])==1)nw++;fclose(f);
    /* perm index */
    int*head=NULL,*nx=malloc(sizeof(int)*(qhi-qlo));uint64_t*KA_=NULL,*KB_=NULL;int HB=20;
    if(ix==1){head=malloc(sizeof(int)*N*N*N);for(long i=0;i<(long)N*N*N;i++)head[i]=-1;
      for(long q=qlo;q<qhi;q++){const short*S=P+q*N;long h=((long)S[CI[0]]*N+S[CI[1]])*N+S[CI[2]];nx[q-qlo]=head[h];head[h]=(int)(q-qlo);}}
    else{head=malloc(sizeof(int)<<HB);for(long i=0;i<(1L<<HB);i++)head[i]=-1;KA_=malloc(8*(qhi-qlo));KB_=malloc(8*(qhi-qlo));
      for(long q=qlo;q<qhi;q++){const short*S=P+q*N;uint64_t a=0,b=0;for(int t=0;t<12;t++)a|=(uint64_t)C[S[CI[t]]]<<(5*t);for(int t=12;t<24;t++)b|=(uint64_t)C[S[CI[t]]]<<(5*(t-12));
        KA_[q-qlo]=a;KB_[q-qlo]=b;uint64_t h=((a*0x9E3779B97F4A7C15ULL)^(b*0xC2B2AE3D27D4EB4FULL))>>(64-HB);nx[q-qlo]=head[h];head[h]=(int)(q-qlo);}}
    for(int L=Lmin;L<=Lmax;L++){long long tests[2][2]={{0}},fit[2][2]={{0}};
      #pragma omp parallel for schedule(dynamic,1) collapse(2) reduction(+:tests[:2][:2],fit[:2][:2])
      for(int w=0;w<nw;w++)for(int nb=0;nb<2;nb++){if((int)strlen(words[w])<L)continue;
        for(int cm=1;cm<(1<<L);cm++)for(int d=0;d<26;d++){int k[N];for(int j=0;j<L;j++)k[j]=cidx[nb][words[w][j]-'A'];
          for(int j=L;j<N;j++){int v=d;for(int a=1;a<=L;a++)if((cm>>(a-1))&1)v+=k[j-a];k[j]=v%26;}
          for(int pa=0;pa<2;pa++)for(int fm=0;fm<2;fm++){tests[pa][fm]++;const char*al=pa?KA:AZ;
            if(ix==0){uint64_t a=0,b=0;for(int t=0;t<24;t++){int e=md(fm?k[CI[t]]-pav[pa][t]:pav[pa][t]+k[CI[t]],26);uint64_t l=al[e]-'A';if(t<12)a|=l<<(5*t);else b|=l<<(5*(t-12));}
              uint64_t h=((a*0x9E3779B97F4A7C15ULL)^(b*0xC2B2AE3D27D4EB4FULL))>>(64-HB);
              for(int e=head[h];e>=0;e=nx[e])if(KA_[e]==a&&KB_[e]==b){fit[pa][fm]++;
                #pragma omp critical
                printf("M %s W0 %d %s %s %ld %s %s c%d d%d\n",lab,L,pa?"ka":"az",fm?"beau":"vig",qlo+e,words[w],nb?"kaN":"azN",cm,d);}}
            else{int D[N];for(int j=0;j<N;j++){int ci=cidx[pa][C[j]];D[j]=al[md(fm?k[j]-ci:ci-k[j],26)]-'A';}
              int p0[N],n0=0,p1[N],n1=0,p2_[N],n2_=0;for(int j=0;j<N;j++){if(D[j]==PT[0]-'A')p0[n0++]=j;if(D[j]==PT[1]-'A')p1[n1++]=j;if(D[j]==PT[2]-'A')p2_[n2_++]=j;}
              for(int x=0;x<n0;x++)for(int y=0;y<n1;y++)for(int z=0;z<n2_;z++){long h=((long)p0[x]*N+p1[y])*N+p2_[z];
                for(int e=head[h];e>=0;e=nx[e]){const short*S=P+(qlo+e)*N;int ok=1;for(int t=3;t<24&&ok;t++)if(D[S[CI[t]]]!=PT[t]-'A')ok=0;
                  if(ok){fit[pa][fm]++;
                    #pragma omp critical
                    printf("M %s W1 %d %s %s %ld %s %s c%d d%d\n",lab,L,pa?"ka":"az",fm?"beau":"vig",qlo+e,words[w],nb?"kaN":"azN",cm,d);}}}}}
        }}
      for(int pa=0;pa<2;pa++)for(int fm=0;fm<2;fm++)printf("H %s W%d %d %s %s streams %lld perms %ld fits %lld\n",lab,ix,L,pa?"ka":"az",fm?"beau":"vig",tests[pa][fm],qhi-qlo,fit[pa][fm]);
    }
  }
  printf("END %s %ld %ld\n",lab,qlo,qhi);return 0;}
