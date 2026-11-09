/* Cycle 175 (IDEAS I-113): Hill n = 2, 3, 4 (linear P = D·Z and affine P = D·Z + e, decryption form) behind the 165,782
   K3-law decimations / spiral-diagonal routes of all.bin.  Same models and conventions as tools/cycle174/hill174.c:
     ix 0: CT = T(Hill(P)): Hill on plaintext order, Z[i] = C[S[i]], known P at the crib indices.
     ix 1: CT = Hill(T(P)): Hill on carved order, Z = C, known intermediate X[S[i]] = P[i].
   Block offset 0..n-1 (letters outside whole blocks free; crib letters outside whole blocks ignored); numbering A-Z / KRYPTOS.
   New solver (replaces hill174's brute-force row enumeration, needed for n 4 / u 5): each row's system A x = z is put in
   reduced row-echelon form mod 2 and mod 13; inconsistent -> no fit; otherwise particular solution + kernel basis per prime,
   the row solution set mod 26 = CRT of the two affine spaces (2^f2 * 13^f13 vectors, enumerated up to CAP).
   Consistent configs are checked for an invertible D (det != 0 mod 2 and mod 13) and decoded with the first invertible key.
   checks(config) = sum_r max(0, m_r - u) (equations beyond unknowns; I-115 information filter, counted as 'consistent_k').
   Analytic chance per config ~ prod_r 26^-(max(0, m_r - u)) (generic rank).
   usage: hill175 CT perms.bin label qlo qhi nmin nmax KMIN
   Output: H lab n aff num ix off configs consistent invertible consistent_k expected expected_k
           K lab q n aff num ix off ninv checks PT                                                          */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define N 97
#define CAP 4096
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PT="EASTNORTHEASTBERLINCLOCK";
static const char *KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static int inv_mod(int a,int p){a%=p;if(a<0)a+=p;for(int x=1;x<p;x++) if(a*x%p==1) return x; return -1;}
/* RREF mod p of [A|z] (m x u). Returns -1 if inconsistent, else number of free vars; fills x0 (particular) and kernel basis K[f][u]. */
static int affsol(int m,int u,int A0[][5],const int*z,int p,int x0[5],int K[5][5]){
  int A[24][6]; for(int i=0;i<m;i++){for(int j=0;j<u;j++){A[i][j]=A0[i][j]%p;} A[i][u]=z[i]%p;}
  int r=0, pc[5], ispiv[5]={0,0,0,0,0};
  for(int c=0;c<u&&r<m;c++){int piv=-1;for(int i=r;i<m;i++) if(A[i][c]){piv=i;break;}
    if(piv<0)continue; for(int k=0;k<=u;k++){int t=A[r][k];A[r][k]=A[piv][k];A[piv][k]=t;}
    int iv=inv_mod(A[r][c],p); for(int k=0;k<=u;k++)A[r][k]=A[r][k]*iv%p;
    for(int i=0;i<m;i++) if(i!=r&&A[i][c]){int f=A[i][c];for(int k=0;k<=u;k++)A[i][k]=((A[i][k]-f*A[r][k])%p+p)%p;}
    pc[r]=c; ispiv[c]=1; r++;}
  for(int i=r;i<m;i++) if(A[i][u]) return -1;
  for(int j=0;j<u;j++) x0[j]=0; for(int i=0;i<r;i++) x0[pc[i]]=A[i][u];
  int nf=0; for(int c=0;c<u;c++) if(!ispiv[c]){ for(int j=0;j<u;j++) K[nf][j]=0; K[nf][c]=1;
      for(int i=0;i<r;i++) K[nf][pc[i]]=(p-A[i][c])%p; nf++; }
  return nf;}
/* all solutions mod 26 of one row (up to cap); returns total count (may exceed cap) or 0 if none */
static long rowsols(int m,int u,int A[][5],const int*z,int sols[][5],int cap){
  int x2[5],K2[5][5],x13[5],K13[5][5];
  int f2=affsol(m,u,A,z,2,x2,K2); if(f2<0) return 0;
  int f13=affsol(m,u,A,z,13,x13,K13); if(f13<0) return 0;
  long n2=1L<<f2, n13=1; for(int i=0;i<f13;i++) n13*=13; long tot=n2*n13, ns=0;
  for(long a=0;a<n2&&ns<cap;a++){ int v2[5]; for(int j=0;j<u;j++){int s=x2[j]; for(int f=0;f<f2;f++) if(a>>f&1) s+=K2[f][j]; v2[j]=s%2;}
    for(long b=0;b<n13&&ns<cap;b++){ int v13[5]; long t=b; int co[5]; for(int f=0;f<f13;f++){co[f]=t%13;t/=13;}
      for(int j=0;j<u;j++){int s=x13[j]; for(int f=0;f<f13;f++) s+=co[f]*K13[f][j]; v13[j]=s%13;}
      for(int j=0;j<u;j++) sols[ns][j]=(v2[j]*13+v13[j]*14)%26; ns++; } }
  return tot;}
static int det_nz_mod(int n,int D[4][5],int p){int A[4][4]; for(int i=0;i<n;i++)for(int j=0;j<n;j++)A[i][j]=D[i][j]%p;
  for(int c=0;c<n;c++){int piv=-1;for(int i=c;i<n;i++) if(A[i][c]){piv=i;break;} if(piv<0) return 0;
    for(int k=0;k<n;k++){int t=A[c][k];A[c][k]=A[piv][k];A[piv][k]=t;} int iv=inv_mod(A[c][c],p);
    for(int i=c+1;i<n;i++) if(A[i][c]){int f=A[i][c]*iv%p; for(int k=0;k<n;k++) A[i][k]=((A[i][k]-f*A[c][k])%p+p)%p;}}
  return 1;}
static int SOL[4][CAP][5];
int main(int argc,char**argv){
  if(argc<9){fprintf(stderr,"usage: hill175 CT perms.bin label qlo qhi nmin nmax KMIN\n");return 1;}
  const char*Cs=argv[1]; if(strlen(Cs)!=N){fprintf(stderr,"CT len\n");return 1;}
  const char*lab=argv[3]; long qlo=atol(argv[4]),qhi=atol(argv[5]); int nmin=atoi(argv[6]),nmax=atoi(argv[7]),KMIN=atoi(argv[8]);
  FILE*pf=fopen(argv[2],"rb"); if(!pf){perror(argv[2]);return 1;} fseek(pf,0,SEEK_END); long np=ftell(pf)/(2*N); rewind(pf);
  short*Perm=malloc(np*N*2); if(fread(Perm,2,np*N,pf)!=(size_t)(np*N))return 2; fclose(pf); if(qhi>np)qhi=np;
  int numtab[2][26]; for(int i=0;i<26;i++){numtab[0][i]=i;numtab[1][KA[i]-'A']=i;}
  static long long H[3][2][2][2][4][4]; static double E[3][2][2][2][4][2]; memset(H,0,sizeof H); memset(E,0,sizeof E);
  for(long q=qlo;q<qhi;q++){const short*S=Perm+q*N;
   for(int num=0;num<2;num++){const int*nm=numtab[num];int Cn[N];for(int i=0;i<N;i++)Cn[i]=nm[Cs[i]-'A'];
    for(int ix=0;ix<2;ix++){int Z[N],kp[24],kv[24];
      if(ix==0){for(int i=0;i<N;i++)Z[i]=Cn[S[i]];for(int t=0;t<24;t++){kp[t]=CI[t];kv[t]=nm[PT[t]-'A'];}}
      else{for(int i=0;i<N;i++)Z[i]=Cn[i];for(int t=0;t<24;t++){kp[t]=S[CI[t]];kv[t]=nm[PT[t]-'A'];}}
      for(int n=nmin;n<=nmax;n++) for(int off=0;off<n;off++) for(int aff=0;aff<2;aff++){
        int u=n+aff; int A[4][24][5],z[4][24],m[4]={0,0,0,0};
        for(int t=0;t<24;t++){int j=kp[t]; if(j<off)continue; int b=(j-off)/n, r=(j-off)%n; if(off+n*(b+1)>N)continue;
          int*row=A[r][m[r]]; for(int c=0;c<n;c++)row[c]=Z[off+n*b+c]; if(aff)row[n]=1; z[r][m[r]]=kv[t]; m[r]++;}
        long long*h=H[n-2][aff][num][ix][off]; h[0]++;
        int chk=0; for(int r=0;r<n;r++){int ex=m[r]-u; if(ex>0) chk+=ex;}
        double e=pow(26.0,-chk); E[n-2][aff][num][ix][off][0]+=e; if(chk>=KMIN) E[n-2][aff][num][ix][off][1]+=e;
        long ns[4]; int ok=1;
        for(int r=0;r<n&&ok;r++){ ns[r]=rowsols(m[r],u,A[r],z[r],SOL[r],CAP); if(!ns[r]) ok=0; }
        if(!ok)continue; h[1]++; if(chk>=KMIN) h[3]++;
        long c[4]; int trunc=0; for(int r=0;r<n;r++){c[r]=ns[r]; if(c[r]>CAP){c[r]=CAP;trunc=1;}}
        for(int r=n;r<4;r++) c[r]=1;
        long ninv=0, lim=20000000L; int best[4][5];
        for(long a0=0;a0<c[0]&&lim>0;a0++)for(long a1=0;a1<c[1]&&lim>0;a1++)for(long a2=0;a2<c[2]&&lim>0;a2++)for(long a3=0;a3<c[3]&&lim>0;a3++){lim--;
          int D[4][5]; long ai[4]={a0,a1,a2,a3}; for(int r=0;r<n;r++) memcpy(D[r],SOL[r][ai[r]],sizeof D[r]);
          if(det_nz_mod(n,D,2)&&det_nz_mod(n,D,13)){ if(!ninv) memcpy(best,D,sizeof best); ninv++; } }
        if(!ninv)continue; h[2]++;
        int inv[26]; for(int i=0;i<26;i++)inv[nm[i]]=i; char out[N+1]; out[N]=0; int X[N]; for(int i=0;i<N;i++)X[i]=-1;
        for(int b=0;off+n*(b+1)<=N;b++) for(int r=0;r<n;r++){int s=aff?best[r][n]:0; for(int cc=0;cc<n;cc++)s+=best[r][cc]*Z[off+n*b+cc]; X[off+n*b+r]=s%26;}
        for(int i=0;i<N;i++){int v= ix==0? X[i] : X[S[i]]; out[i]= v<0?'?':(char)('A'+inv[v]);}
        printf("K %s %ld %d %d %s %d %d %ld%s %d %s\n",lab,q,n,aff,num?"KA":"AZ",ix,off,ninv,(trunc||lim<=0)?"+":"",chk,out);
      }}}}
  for(int n=nmin;n<=nmax;n++)for(int aff=0;aff<2;aff++)for(int num=0;num<2;num++)for(int ix=0;ix<2;ix++)for(int off=0;off<n;off++){
    long long*h=H[n-2][aff][num][ix][off]; double*e=E[n-2][aff][num][ix][off];
    printf("H %s %d %d %s %d %d %lld %lld %lld %lld %.4g %.4g\n",lab,n,aff,num?"KA":"AZ",ix,off,h[0],h[1],h[2],h[3],e[0],e[1]);}
  printf("END %s\n",lab); return 0;}
