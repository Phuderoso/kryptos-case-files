/* Cycle 144: Hill n x n + Vigenere-style additive key of period k (k independent of n) on the Hill output stream:
   out[t] = sum_j D[r][j] * L[b*n+o+j] + e[t mod k]   (t = b*n+o+r), then plaintext (model Q: pt = out; carved: pt[p] = out[S[p]]).
   All n*n + k unknowns are solved JOINTLY and exactly from the 24 crib letters, mod 2 and mod 13 (CRT);
   shift residues never hit by a crib are dropped (their letters stay undecided '.').
   Consistent systems with <= COMBOCAP solutions are enumerated; invertible D decoded and ranked by mean log10 quadgram
   over windows of decided, non-crib letters.  usage: hillvk CT perms.bin|- label lo hi stride n k
   env THR (-4.6), COMBOCAP (20000) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MU 24
static float *Q; static int ISCRIB[97]; static const char *CRIB="EASTNORTHEASTBERLINCLOCK";
static int cpos[24]; static double THR=-4.6; static long COMBOCAP=20000;
static const char *NUMS[2]={"ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"};
static int inv13[13]; static int n,K,U;
static int solvep(int p,int m,int A[][MU],int *b,int *part,int basis[MU][MU]){
  int M[24][MU+1]; for(int i=0;i<m;i++){for(int j=0;j<U;j++)M[i][j]=A[i][j]%p; M[i][U]=b[i]%p;}
  int piv[MU],r=0; for(int c=0;c<U&&r<m;c++){int s=-1;for(int i=r;i<m;i++)if(M[i][c]){s=i;break;} if(s<0)continue;
    for(int j=0;j<=U;j++){int t=M[r][j];M[r][j]=M[s][j];M[s][j]=t;}
    int iv=(p==2)?1:inv13[M[r][c]]; for(int j=0;j<=U;j++)M[r][j]=M[r][j]*iv%p;
    for(int i=0;i<m;i++)if(i!=r&&M[i][c]){int f=M[i][c];for(int j=0;j<=U;j++)M[i][j]=((M[i][j]-f*M[r][j])%p+p)%p;}
    piv[r]=c;r++;}
  for(int i=r;i<m;i++)if(M[i][U])return -1;
  int isp[MU]={0};for(int i=0;i<r;i++)isp[piv[i]]=1;
  for(int j=0;j<U;j++)part[j]=0; for(int i=0;i<r;i++)part[piv[i]]=M[i][U];
  int d=0; for(int f=0;f<U;f++)if(!isp[f]){for(int j=0;j<U;j++)basis[d][j]=0;basis[d][f]=1;
    for(int i=0;i<r;i++)basis[d][piv[i]]=(p-M[i][f])%p; d++;}
  return d;}
static int detp(int p,int D[4][4]){int M[4][4];for(int i=0;i<n;i++)for(int j=0;j<n;j++)M[i][j]=D[i][j]%p;
  for(int c=0;c<n;c++){int s=-1;for(int i=c;i<n;i++)if(M[i][c]){s=i;break;} if(s<0)return 0;
    if(s!=c)for(int j=0;j<n;j++){int t=M[c][j];M[c][j]=M[s][j];M[s][j]=t;}
    int iv=(p==2)?1:inv13[M[c][c]]; for(int i=c+1;i<n;i++)if(M[i][c]){int f=M[i][c]*iv%p;for(int j=0;j<n;j++)M[i][j]=((M[i][j]-f*M[c][j])%p+p)%p;}}
  return 1;}
int main(int ac,char**av){
  if(ac<9)return 1; n=atoi(av[7]); K=atoi(av[8]); if(n>4||n*n+K>MU)return 4;
  for(int i=1;i<13;i++)for(int j=1;j<13;j++)if(i*j%13==1)inv13[i]=j;
  if(getenv("THR"))THR=atof(getenv("THR")); if(getenv("COMBOCAP"))COMBOCAP=atol(getenv("COMBOCAP"));
  Q=malloc(456976*4);{FILE*f=fopen(getenv("QUAD")?getenv("QUAD"):"/home/box/kryptos_support_backup/quad.bin","rb");if(!f||fread(Q,4,456976,f)!=456976)return 2;fclose(f);}
  {int k=0;for(int i=21;i<=33;i++){ISCRIB[i]=1;cpos[k++]=i;}for(int i=63;i<=73;i++){ISCRIB[i]=1;cpos[k++]=i;}}
  const char*CT=av[1]; const char*lab=av[3]; long lo=atol(av[4]),hi=atol(av[5]),st=atol(av[6]);
  long np=1; short *bank=NULL; if(strcmp(av[2],"-")){FILE*f=fopen(av[2],"rb");fseek(f,0,2);np=ftell(f)/194;fseek(f,0,0);bank=malloc(np*194);if(fread(bank,194,np,f)!=(size_t)np)return 3;fclose(f);}
  if(hi>np)hi=np; long tests=0,incons=0,under=0,scored=0,combos=0; double gbest=-99;
  for(long q=lo;q<hi;q+=st)for(int dir=0;dir<(bank?2:1);dir++){
    int S[97]; if(bank){for(int i=0;i<97;i++)S[i]=bank[q*97+i]; if(dir){int T[97];for(int i=0;i<97;i++)T[S[i]]=i;memcpy(S,T,sizeof S);}} else for(int i=0;i<97;i++)S[i]=i;
    for(int ix=0;ix<(bank?2:1);ix++)for(int nu=0;nu<2;nu++){
      const char*N=NUMS[nu]; int idx[26]; for(int i=0;i<26;i++)idx[N[i]-'A']=i;
      int L[97],kp[97]; for(int i=0;i<97;i++)kp[i]=-1;
      if(ix==0){for(int i=0;i<97;i++)L[i]=idx[CT[S[i]]-'A']; for(int k=0;k<24;k++)kp[cpos[k]]=idx[CRIB[k]-'A'];}
      else{for(int i=0;i<97;i++)L[i]=idx[CT[i]-'A']; for(int k=0;k<24;k++)kp[S[cpos[k]]]=idx[CRIB[k]-'A'];}
      for(int o=0;o<n;o++){ tests++;
        int nb=(97-o)/n; int hit[24]={0};
        for(int t=o;t<o+nb*n;t++)if(kp[t]>=0)hit[t%K]=1;
        int col[24],nc=0; for(int s=0;s<K;s++)col[s]=hit[s]?nc++:-1; U=n*n+nc;
        int A[24][MU],b[24],m=0;
        for(int t=o;t<o+nb*n;t++)if(kp[t]>=0){int bs=o+((t-o)/n)*n,r=(t-o)%n; memset(A[m],0,sizeof A[m]);
          for(int j=0;j<n;j++)A[m][r*n+j]=L[bs+j]; A[m][n*n+col[t%K]]=1; b[m]=kp[t]; m++;}
        int p2[MU],B2[MU][MU],p13[MU],B13[MU][MU]; int d2=solvep(2,m,A,b,p2,B2); if(d2<0){incons++;continue;}
        int d13=solvep(13,m,A,b,p13,B13); if(d13<0){incons++;continue;}
        double n2=1,n13=1; for(int i=0;i<d2;i++)n2*=2; for(int i=0;i<d13;i++)n13*=13;
        if(n2*n13>COMBOCAP){under++;continue;}
        scored++; double best=-99; char bpt[98]; bpt[97]=0;
        for(long a=0;a<(long)n2;a++)for(long c=0;c<(long)n13;c++){int x2[MU],x13[MU],x[MU];for(int j=0;j<U;j++){x2[j]=p2[j];x13[j]=p13[j];}
          for(int t=0;t<d2;t++)if(a>>t&1)for(int j=0;j<U;j++)x2[j]^=B2[t][j];
          long cc=c;for(int t=0;t<d13;t++){int co=cc%13;cc/=13;for(int j=0;j<U;j++)x13[j]=(x13[j]+co*B13[t][j])%13;}
          for(int j=0;j<U;j++)x[j]=(13*x2[j]+14*x13[j])%26;
          int D[4][4]; for(int r=0;r<n;r++)for(int j=0;j<n;j++)D[r][j]=x[r*n+j];
          if(!detp(2,D)||!detp(13,D))continue; combos++;
          char out[97]; memset(out,0,97);
          for(int t=o;t<o+nb*n;t++){if(col[t%K]<0)continue; int bs=o+((t-o)/n)*n,r=(t-o)%n; int s=x[n*n+col[t%K]]; for(int j=0;j<n;j++)s+=D[r][j]*L[bs+j]; out[t]=N[s%26];}
          char pt[97]; if(ix==0)memcpy(pt,out,97); else for(int p=0;p<97;p++)pt[p]=out[S[p]];
          double tot=0;int w=0; for(int i=0;i+4<=97;i++){int g=1,id=0;for(int z=0;z<4;z++){char ch=pt[i+z];if(!ch||ISCRIB[i+z]){g=0;break;}id=id*26+ch-'A';} if(g){tot+=Q[id];w++;}}
          double sc=w>=20?tot/w:-99; if(sc>best){best=sc;for(int i=0;i<97;i++)bpt[i]=pt[i]?pt[i]:'.';}
        }
        if(best<-90)continue; if(best>gbest)gbest=best;
        if(best>THR){printf("S %s n=%d k=%d perm=%ld dir=%d ix=%d num=%d o=%d sols=%.0f meanQ=%.3f %s\n",lab,n,K,q,dir,ix,nu,o,n2*n13,best,bpt);fflush(stdout);}
      }}}
  printf("C %s n=%d k=%d tests=%ld incons=%ld underdet=%ld scored=%ld invertible_combos=%ld best=%.3f range=%ld..%ld/%ld\n",lab,n,K,tests,incons,under,scored,combos,gbest,lo,hi,st);
  return 0;}
