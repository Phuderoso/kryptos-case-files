/* Cycle 174 (IDEAS I-108): Hill n = 2, 3 (linear P = D·Z and affine P = D·Z + e, decryption form) behind each of the
   165,782 K3-law decimations / spiral-diagonal routes of all.bin (perm and inverse are both entries).
   Convention as tools/cycle172/q4d172.c: plaintext index i <-> carved index S[i].
     ix 0: CT = T(Hill(P)): Hill on plaintext order, Hill ciphertext Z[i] = C[S[i]], known P at the crib indices.
     ix 1: CT = Hill(T(P)): Hill on carved order, Z = C, known intermediate X[S[i]] = P[i].
   Block offset off = 0..n-1 (letters outside whole blocks are left free; a crib letter outside a whole block is ignored).
   Numbering: A-Z (A=0) and KRYPTOS-keyed (KA).  Affine covers any cyclic shift of the numbering (A=1 etc.).
   Exact per row: every crib letter gives one linear equation on one row of D; solvable mod 2 and mod 13
   (Gaussian elimination, CRT) <=> solvable mod 26.  Configs where every row is solvable are then enumerated
   (brute force over each row's solution set mod 26) for an invertible D (det a unit mod 26), and decoded.
   Chance expectation (approx, generic rank): prod_r 26^-(max(0, m_r - u)), u = n (+1 if affine).
   usage: hill174 CT perms.bin label qlo qhi
   Output: H lab n aff num ix off configs consistent invertible expected
           K lab q n aff num ix off ninv  PT   (first invertible key's decryption)  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define N 97
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PT="EASTNORTHEASTBERLINCLOCK";
static const char *KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static int inv_mod(int a,int p){a%=p;if(a<0)a+=p;for(int x=1;x<p;x++) if(a*x%p==1) return x; return -1;}
/* is A x = z solvable mod p ; A is m x u */
static int solvable(int m,int u,int A0[][5],const int*z,int p){
  int A[24][6]; for(int i=0;i<m;i++){for(int j=0;j<u;j++)A[i][j]=A0[i][j]%p; A[i][u]=z[i]%p;}
  int r=0;
  for(int c=0;c<u&&r<m;c++){int piv=-1;for(int i=r;i<m;i++) if(A[i][c]){piv=i;break;}
    if(piv<0)continue; for(int k=0;k<=u;k++){int t=A[r][k];A[r][k]=A[piv][k];A[piv][k]=t;}
    int iv=inv_mod(A[r][c],p); for(int k=0;k<=u;k++)A[r][k]=A[r][k]*iv%p;
    for(int i=0;i<m;i++) if(i!=r&&A[i][c]){int f=A[i][c];for(int k=0;k<=u;k++)A[i][k]=((A[i][k]-f*A[r][k])%p+p)%p;}
    r++;}
  for(int i=r;i<m;i++) if(A[i][u]) return 0; return 1;}
/* enumerate solutions mod 26 of one row (brute force), up to cap */
static int rowsols(int m,int u,int A[][5],const int*z,int sols[][4],int cap){
  int tot=1;for(int i=0;i<u;i++)tot*=26; int ns=0;
  for(int v=0;v<tot;v++){int x[4],t=v;for(int i=0;i<u;i++){x[i]=t%26;t/=26;}
    int ok=1;for(int e=0;e<m&&ok;e++){int s=0;for(int i=0;i<u;i++)s+=A[e][i]*x[i];if(s%26!=z[e])ok=0;}
    if(ok){if(ns<cap)memcpy(sols[ns],x,sizeof x);ns++;}}
  return ns;}
static int det_unit(int n,int D[3][3]){long d; if(n==2)d=D[0][0]*D[1][1]-D[0][1]*D[1][0];
  else d=(long)D[0][0]*(D[1][1]*D[2][2]-D[1][2]*D[2][1])-(long)D[0][1]*(D[1][0]*D[2][2]-D[1][2]*D[2][0])+(long)D[0][2]*(D[1][0]*D[2][1]-D[1][1]*D[2][0]);
  d%=26;if(d<0)d+=26; return (d%2)&&(d%13);}
#define CAP 4096
static int S1[CAP][4],S2[CAP][4],S3[CAP][4];
int main(int argc,char**argv){
  if(argc<6){fprintf(stderr,"usage\n");return 1;}
  const char*Cs=argv[1]; if(strlen(Cs)!=N){fprintf(stderr,"CT len\n");return 1;}
  const char*lab=argv[3]; long qlo=atol(argv[4]),qhi=atol(argv[5]);
  FILE*pf=fopen(argv[2],"rb"); fseek(pf,0,SEEK_END); long np=ftell(pf)/(2*N); rewind(pf);
  short*Perm=malloc(np*N*2); if(fread(Perm,2,np*N,pf)!=(size_t)(np*N))return 2; fclose(pf); if(qhi>np)qhi=np;
  int numtab[2][26]; for(int i=0;i<26;i++){numtab[0][i]=i;numtab[1][KA[i]-'A']=i;}
  static long long H[2][2][2][2][3][3]; static double E[2][2][2][2][3]; memset(H,0,sizeof H);
  for(long q=qlo;q<qhi;q++){const short*S=Perm+q*N;
   for(int num=0;num<2;num++){const int*nm=numtab[num];int Cn[N];for(int i=0;i<N;i++)Cn[i]=nm[Cs[i]-'A'];
    for(int ix=0;ix<2;ix++){int Z[N],kp[24],kv[24];
      if(ix==0){for(int i=0;i<N;i++)Z[i]=Cn[S[i]];for(int t=0;t<24;t++){kp[t]=CI[t];kv[t]=nm[PT[t]-'A'];}}
      else{for(int i=0;i<N;i++)Z[i]=Cn[i];for(int t=0;t<24;t++){kp[t]=S[CI[t]];kv[t]=nm[PT[t]-'A'];}}
      for(int n=2;n<=3;n++) for(int off=0;off<n;off++) for(int aff=0;aff<2;aff++){
        int u=n+aff; int A[3][24][5],z[3][24],m[3]={0,0,0};
        for(int t=0;t<24;t++){int j=kp[t]; if(j<off)continue; int b=(j-off)/n, r=(j-off)%n; if(off+n*(b+1)>N)continue;
          int*row=A[r][m[r]]; for(int c=0;c<n;c++)row[c]=Z[off+n*b+c]; if(aff)row[n]=1; z[r][m[r]]=kv[t]; m[r]++;}
        long long*h=H[n-2][aff][num][ix][off]; h[0]++;
        double e=1; for(int r=0;r<n;r++){int ex=m[r]-u; if(ex>0)e*=pow(26.0,-ex);} E[n-2][aff][num][ix][off]+=e;
        int ok=1; for(int r=0;r<n&&ok;r++) if(!solvable(m[r],u,A[r],z[r],2)||!solvable(m[r],u,A[r],z[r],13)) ok=0;
        if(!ok)continue; h[1]++;
        int n1=rowsols(m[0],u,A[0],z[0],S1,CAP),n2=rowsols(m[1],u,A[1],z[1],S2,CAP),n3=n==3?rowsols(m[2],u,A[2],z[2],S3,CAP):1;
        if(n1>CAP)n1=CAP; if(n2>CAP)n2=CAP; if(n3>CAP)n3=CAP;
        long ninv=0; int best[3][4]; long lim=20000000L;
        for(int a=0;a<n1&&lim>0;a++)for(int b=0;b<n2&&lim>0;b++)for(int c=0;c<n3&&lim>0;c++){lim--;
          int D[3][3]; for(int k=0;k<n;k++){D[0][k]=S1[a][k];D[1][k]=S2[b][k];if(n==3)D[2][k]=S3[c][k];}
          if(det_unit(n,D)){if(!ninv){memcpy(best[0],S1[a],16);memcpy(best[1],S2[b],16);if(n==3)memcpy(best[2],S3[c],16);}ninv++;}}
        if(!ninv)continue; h[2]++;
        /* decode with the first invertible key */
        int inv[26]; for(int i=0;i<26;i++)inv[nm[i]]=i; char out[N+1]; for(int i=0;i<N;i++)out[i]='?'; out[N]=0;
        int X[N]; for(int i=0;i<N;i++)X[i]=-1;
        for(int b=0;off+n*(b+1)<=N;b++) for(int r=0;r<n;r++){int s=aff?best[r][n]:0; for(int c=0;c<n;c++)s+=best[r][c]*Z[off+n*b+c]; X[off+n*b+r]=s%26;}
        for(int i=0;i<N;i++){int v= ix==0? X[i] : X[S[i]]; out[i]= v<0?'?':(char)('A'+inv[v]);}
        printf("K %s %ld %d %d %s %d %d %ld%s %s\n",lab,q,n,aff,num?"KA":"AZ",ix,off,ninv,(n1>=CAP||n2>=CAP||n3>=CAP||lim<=0)?"+":"",out);
      }}}}
  for(int n=2;n<=3;n++)for(int aff=0;aff<2;aff++)for(int num=0;num<2;num++)for(int ix=0;ix<2;ix++)for(int off=0;off<n;off++){
    long long*h=H[n-2][aff][num][ix][off];
    printf("H %s %d %d %s %d %d %lld %lld %lld %.4g\n",lab,n,aff,num?"KA":"AZ",ix,off,h[0],h[1],h[2],E[n-2][aff][num][ix][off]);}
  printf("END %s\n",lab); return 0;}
