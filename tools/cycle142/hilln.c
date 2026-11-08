/* Cycle 142: Hill n x n (n = 6) direct, every alignment, A-Z/KRYPTOS numbering.
   Each row of the decryption matrix D meets only plaintext positions = o+r (mod n); the cribs
   give each row a small linear system, solved exactly mod 2 and mod 13 (CRT). Every row's full
   solution set is enumerated (<= 17576). The joint choice (no crib checks left) is searched by
   coordinate ascent on mean log10 quadgram (windows outside cribs), RESTARTS random starts.
   usage: hilln CT n o num label   env RESTARTS (default 300), SEED */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MX 8
#define RC 17600
static float *Q; static int ISCRIB[97]; static const char *CRIB="EASTNORTHEASTBERLINCLOCK"; static int cpos[24];
static const char *NUMS[2]={"ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"};
static int inv13[13], n;
static int solvep(int p,int m,int A[][MX],int *b,int *part,int basis[MX][MX]){
  int M[24][MX+1]; for(int i=0;i<m;i++){for(int j=0;j<n;j++)M[i][j]=((A[i][j]%p)+p)%p; M[i][n]=((b[i]%p)+p)%p;}
  int piv[MX],r=0; for(int c=0;c<n&&r<m;c++){int s=-1;for(int i=r;i<m;i++)if(M[i][c]){s=i;break;} if(s<0)continue;
    for(int j=0;j<=n;j++){int t=M[r][j];M[r][j]=M[s][j];M[s][j]=t;}
    int iv=(p==2)?1:inv13[M[r][c]]; for(int j=0;j<=n;j++)M[r][j]=M[r][j]*iv%p;
    for(int i=0;i<m;i++)if(i!=r&&M[i][c]){int f=M[i][c];for(int j=0;j<=n;j++)M[i][j]=((M[i][j]-f*M[r][j])%p+p)%p;}
    piv[r]=c;r++;}
  for(int i=r;i<m;i++)if(M[i][n])return -1;
  int isp[MX]={0};for(int i=0;i<r;i++)isp[piv[i]]=1;
  for(int j=0;j<n;j++)part[j]=0; for(int i=0;i<r;i++)part[piv[i]]=M[i][n];
  int d=0; for(int f=0;f<n;f++)if(!isp[f]){for(int j=0;j<n;j++)basis[d][j]=0;basis[d][f]=1;
    for(int i=0;i<r;i++)basis[d][piv[i]]=(p-M[i][f])%p; d++;}
  return d;}
static int detp(int p,int D[MX][MX]){int M[MX][MX];for(int i=0;i<n;i++)for(int j=0;j<n;j++)M[i][j]=D[i][j]%p;
  for(int c=0;c<n;c++){int s=-1;for(int i=c;i<n;i++)if(M[i][c]){s=i;break;} if(s<0)return 0;
    if(s!=c)for(int j=0;j<n;j++){int t=M[c][j];M[c][j]=M[s][j];M[s][j]=t;}
    int iv=(p==2)?1:inv13[M[c][c]]; for(int i=c+1;i<n;i++)if(M[i][c]){int f=M[i][c]*iv%p;for(int j=0;j<n;j++)M[i][j]=((M[i][j]-f*M[c][j])%p+p)%p;}}
  return 1;}
static int rows[MX][RC][MX]; static int nrow[MX];
static int enumrow(int m,int A[][MX],int *b,int r){
  int p2[MX],B2[MX][MX],p13[MX],B13[MX][MX]; int d2=solvep(2,m,A,b,p2,B2); if(d2<0)return -1; int d13=solvep(13,m,A,b,p13,B13); if(d13<0)return -1;
  long n2=1L<<d2,n13=1;for(int i=0;i<d13;i++)n13*=13; if(n2*n13>RC)return -2;
  int k=0; for(long a=0;a<n2;a++)for(long c=0;c<n13;c++){int x2[MX],x13[MX];for(int j=0;j<n;j++){x2[j]=p2[j];x13[j]=p13[j];}
    for(int t=0;t<d2;t++)if(a>>t&1)for(int j=0;j<n;j++)x2[j]^=B2[t][j];
    long cc=c;for(int t=0;t<d13;t++){int co=cc%13;cc/=13;for(int j=0;j<n;j++)x13[j]=(x13[j]+co*B13[t][j])%13;}
    for(int j=0;j<n;j++)rows[r][k][j]=(13*x2[j]+14*x13[j])%26; k++;}
  nrow[r]=k; return k;}
static unsigned long long rs=88172645463325252ULL; static unsigned long long rnd(){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs;}
static char pt[97]; static int L[97], o, nb; static const char *N;
static char dec[MX][RC][16];
static double score(){double t=0;int c=0;for(int i=0;i+4<=97;i++){int g=1,id=0;for(int z=0;z<4;z++){char ch=pt[i+z];if(!ch||ISCRIB[i+z]){g=0;break;}id=id*26+ch-'A';}if(g){t+=Q[id];c++;}}return c?t/c:-99;}
static void setrow(int r,int k){for(int b=0;b<nb;b++)pt[o+n*b+r]=dec[r][k][b];}
int main(int ac,char**av){
  if(ac<6)return 1; for(int i=1;i<13;i++)for(int j=1;j<13;j++)if(i*j%13==1)inv13[i]=j;
  Q=malloc(456976*4);{FILE*f=fopen("/home/box/kryptos_support_backup/quad.bin","rb");if(!f||fread(Q,4,456976,f)!=456976)return 2;fclose(f);}
  {int k=0;for(int i=21;i<=33;i++){ISCRIB[i]=1;cpos[k++]=i;}for(int i=63;i<=73;i++){ISCRIB[i]=1;cpos[k++]=i;}}
  const char*CT=av[1]; n=atoi(av[2]); o=atoi(av[3]); int nu=atoi(av[4]); const char*lab=av[5];
  int R=getenv("RESTARTS")?atoi(getenv("RESTARTS")):300; if(getenv("SEED"))rs^=strtoull(getenv("SEED"),0,10)*2654435761ULL;
  N=NUMS[nu]; int idx[26]; for(int i=0;i<26;i++)idx[N[i]-'A']=i; for(int i=0;i<97;i++)L[i]=idx[CT[i]-'A'];
  int kp[97]; for(int i=0;i<97;i++)kp[i]=-1; for(int k=0;k<24;k++)kp[cpos[k]]=idx[CRIB[k]-'A'];
  nb=(97-o)/n; int A[MX][24][MX],b[MX][24],m[MX]={0};
  for(int k=0;k<nb;k++){int bs=o+n*k;for(int r=0;r<n;r++){int q=bs+r;if(kp[q]<0)continue;for(int j=0;j<n;j++)A[r][m[r]][j]=L[bs+j];b[r][m[r]]=kp[q];m[r]++;}}
  double space=1; for(int r=0;r<n;r++){int e=enumrow(m[r],A[r],b[r],r); if(e==-1){printf("C %s n=%d o=%d num=%d inconsistent row %d\n",lab,n,o,nu,r);return 0;} if(e==-2){printf("C %s n=%d o=%d num=%d row %d too free\n",lab,n,o,nu,r);return 0;} space*=e;}
  for(int r=0;r<n;r++)for(int k=0;k<nrow[r];k++)for(int bb=0;bb<nb;bb++){int bs=o+n*bb,s=0;for(int j=0;j<n;j++)s+=rows[r][k][j]*L[bs+j];dec[r][k][bb]=N[s%26];}
  double gbest=-99,anyb=-99; int gc[MX]; long evals=0;
  for(int rr=0;rr<R;rr++){ memset(pt,0,97); int c[MX]; for(int r=0;r<n;r++){c[r]=rnd()%nrow[r];setrow(r,c[r]);}
    double cur=score(); int imp=1; while(imp){imp=0; for(int r=0;r<n;r++){int bk=c[r];double bs=cur; for(int k=0;k<nrow[r];k++){setrow(r,k);double s=score();evals++;if(s>bs+1e-9){bs=s;bk=k;}} setrow(r,bk); if(bk!=c[r]){c[r]=bk;cur=bs;imp=1;}}}
    {int D[MX][MX]; for(int r=0;r<n;r++)for(int j=0;j<n;j++)D[r][j]=rows[r][c[r]][j]; if(cur>anyb)anyb=cur; if(detp(2,D)&&detp(13,D)&&cur>gbest){gbest=cur;memcpy(gc,c,sizeof gc);}} }
  if(gbest<-90){printf("C %s n=%d o=%d num=%d no invertible endpoint best_any=%.3f\n",lab,n,o,nu,anyb);return 0;}
  memset(pt,0,97); for(int r=0;r<n;r++)setrow(r,gc[r]); int D[MX][MX]; for(int r=0;r<n;r++)for(int j=0;j<n;j++)D[r][j]=rows[r][gc[r]][j];
  int inv=detp(2,D)&&detp(13,D); char s[98]; for(int i=0;i<97;i++)s[i]=pt[i]?pt[i]:'.'; s[97]=0;
  printf("C %s n=%d o=%d num=%d eqs=",lab,n,o,nu); for(int r=0;r<n;r++)printf("%d%s",m[r],r<n-1?",":""); printf(" space=%.3g restarts=%d evals=%ld best=%.3f best_any=%.3f invertible=%d %s\n",space,R,evals,gbest,anyb,inv,s);
  return 0;}
