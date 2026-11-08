/* Cycle 143: AFFINE Hill n x n (p_block = D c_block + e mod 26, e a per-row shift = Hill + period-n additive key), n given on the command line. Adapted from cycle 141's Hill 5x5 (any invertible decryption matrix mod 26), every block alignment,
   direct and behind bank permutations (model Q and carved order), A-Z or KRYPTOS numbering.
   Per row the cribs give linear equations in n+1 unknowns (row of D plus shift): solved exactly mod 2 and
   mod 13 (CRT). Underdetermined rows are enumerated (<= ROWCAP solutions); every invertible
   combination is decrypted and ranked by mean quadgram log10 over windows outside the cribs.
   usage: hillaff CT perms.bin|- label lo hi stride n
   env THR (mean-Q print threshold, default -4.6), ROWCAP (default 676), COMBOCAP (200000) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static float *Q; static int ISCRIB[97]; static const char *CRIB="EASTNORTHEASTBERLINCLOCK";
static int cpos[24]; static double THR=-4.6; static long ROWCAP=676, COMBOCAP=200000;
static const char *NUMS[2]={"ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"};
static int inv13[13]; static int n, U;
/* solve A x = b over GF(p), m eqs, U = n+1 unknowns; returns -1 inconsistent, else nullity; part, basis */
static int solvep(int p,int m,int A[][8],int *b,int *part,int basis[8][8]){
  int M[40][9]; for(int i=0;i<m;i++){for(int j=0;j<U;j++)M[i][j]=((A[i][j]%p)+p)%p; M[i][U]=((b[i]%p)+p)%p;}
  int piv[8],r=0; for(int c=0;c<U&&r<m;c++){int s=-1;for(int i=r;i<m;i++)if(M[i][c]){s=i;break;} if(s<0)continue;
    for(int j=0;j<=U;j++){int t=M[r][j];M[r][j]=M[s][j];M[s][j]=t;}
    int iv=(p==2)?1:inv13[M[r][c]]; for(int j=0;j<=U;j++)M[r][j]=M[r][j]*iv%p;
    for(int i=0;i<m;i++)if(i!=r&&M[i][c]){int f=M[i][c];for(int j=0;j<=U;j++)M[i][j]=((M[i][j]-f*M[r][j])%p+p)%p;}
    piv[r]=c;r++;}
  for(int i=r;i<m;i++)if(M[i][U])return -1;
  int isp[8]={0};for(int i=0;i<r;i++)isp[piv[i]]=1;
  for(int j=0;j<U;j++)part[j]=0; for(int i=0;i<r;i++)part[piv[i]]=M[i][U];
  int d=0; for(int f=0;f<U;f++)if(!isp[f]){for(int j=0;j<U;j++)basis[d][j]=0;basis[d][f]=1;
    for(int i=0;i<r;i++)basis[d][piv[i]]=(p-M[i][f])%p; d++;}
  return d;}
static int detp(int p,int D[8][8]){int M[8][8];for(int i=0;i<n;i++)for(int j=0;j<n;j++)M[i][j]=D[i][j]%p;
  for(int c=0;c<n;c++){int s=-1;for(int i=c;i<n;i++)if(M[i][c]){s=i;break;} if(s<0)return 0;
    if(s!=c)for(int j=0;j<n;j++){int t=M[c][j];M[c][j]=M[s][j];M[s][j]=t;}
    int iv=(p==2)?1:inv13[M[c][c]]; for(int i=c+1;i<n;i++)if(M[i][c]){int f=M[i][c]*iv%p;for(int j=0;j<n;j++)M[i][j]=((M[i][j]-f*M[c][j])%p+p)%p;}}
  return 1;}
static int rows[8][17600][8]; static int nrow[8];
static int enumrow(int m,int A[][8],int *b,int r){
  int p2[8],B2[8][8],p13[8],B13[8][8]; int d2=solvep(2,m,A,b,p2,B2); if(d2<0)return -1; int d13=solvep(13,m,A,b,p13,B13); if(d13<0)return -1;
  long n2=1L<<d2, n13=1; for(int i=0;i<d13;i++)n13*=13; if(n2*n13>ROWCAP||n2*n13>17600)return -2;
  int k=0; for(long a=0;a<n2;a++)for(long c=0;c<n13;c++){int x2[8],x13[8];for(int j=0;j<U;j++){x2[j]=p2[j];x13[j]=p13[j];}
    for(int t=0;t<d2;t++)if(a>>t&1)for(int j=0;j<U;j++)x2[j]^=B2[t][j];
    long cc=c;for(int t=0;t<d13;t++){int co=cc%13;cc/=13;for(int j=0;j<U;j++)x13[j]=(x13[j]+co*B13[t][j])%13;}
    for(int j=0;j<U;j++)rows[r][k][j]=(13*x2[j]+14*x13[j])%26; k++;}
  nrow[r]=k; return k;}
int main(int ac,char**av){
  if(ac<8)return 1; n=atoi(av[7]); U=n+1; for(int i=1;i<13;i++)for(int j=1;j<13;j++)if(i*j%13==1)inv13[i]=j;
  if(getenv("THR"))THR=atof(getenv("THR")); if(getenv("ROWCAP"))ROWCAP=atol(getenv("ROWCAP")); if(getenv("COMBOCAP"))COMBOCAP=atol(getenv("COMBOCAP"));
  Q=malloc(456976*4);{FILE*f=fopen(getenv("QUAD")?getenv("QUAD"):"/home/box/kryptos_support_backup/quad.bin","rb");if(!f||fread(Q,4,456976,f)!=456976)return 2;fclose(f);}
  {int k=0;for(int i=21;i<=33;i++){ISCRIB[i]=1;cpos[k++]=i;}for(int i=63;i<=73;i++){ISCRIB[i]=1;cpos[k++]=i;}}
  const char*CT=av[1]; const char*lab=av[3]; long lo=atol(av[4]),hi=atol(av[5]),st=atol(av[6]);
  long np=1; short *bank=NULL; if(strcmp(av[2],"-")){FILE*f=fopen(av[2],"rb");fseek(f,0,2);np=ftell(f)/194;fseek(f,0,0);bank=malloc(np*194);if(fread(bank,194,np,f)!=(size_t)np)return 3;fclose(f);} 
  if(hi>np)hi=np; long tests=0,incons=0,under=0,scored=0,combos=0; long hist[40]={0}; double gbest=-99;
  for(long q=lo;q<hi;q+=st)for(int dir=0;dir<(bank?2:1);dir++){
    int S[97]; if(bank){for(int i=0;i<97;i++)S[i]=bank[q*97+i]; if(dir){int T[97];for(int i=0;i<97;i++)T[S[i]]=i;memcpy(S,T,sizeof S);}} else for(int i=0;i<97;i++)S[i]=i;
    for(int ix=0;ix<(bank?2:1);ix++)for(int nu=0;nu<2;nu++){
      const char*N=NUMS[nu]; int idx[26]; for(int i=0;i<26;i++)idx[N[i]-'A']=i;
      int L[97],kp[97]; for(int i=0;i<97;i++)kp[i]=-1;
      if(ix==0){for(int i=0;i<97;i++)L[i]=idx[CT[S[i]]-'A']; for(int k=0;k<24;k++)kp[cpos[k]]=idx[CRIB[k]-'A'];}
      else{for(int i=0;i<97;i++)L[i]=idx[CT[i]-'A']; for(int k=0;k<24;k++)kp[S[cpos[k]]]=idx[CRIB[k]-'A'];}
      for(int o=0;o<n;o++){ tests++;
        int nb=(97-o)/n; int A[8][40][8],b[8][40],m[8]={0}; int ok=1;
        for(int k=0;k<nb;k++){int bs=o+n*k;for(int r=0;r<n;r++){int qq=bs+r;if(kp[qq]<0)continue; if(m[r]>=40){continue;} for(int j=0;j<n;j++)A[r][m[r]][j]=L[bs+j]; A[r][m[r]][n]=1; b[r][m[r]]=kp[qq]; m[r]++;}}
        long prod=1; for(int r=0;r<n&&ok;r++){int e=enumrow(m[r],A[r],b[r],r); if(e==-1){ok=0;incons++;} else if(e==-2){ok=-1;} else prod*=e;}
        if(ok==0)continue; if(ok<0||prod>COMBOCAP){under++;continue;} if(prod==0){incons++;continue;}
        scored++; double best=-99; int bestc[8]={0};
        int c[8]={0}; for(long t=0;t<prod;t++){
          long tt=t; for(int r=0;r<n;r++){c[r]=tt%nrow[r];tt/=nrow[r];}
          int D[8][8]; for(int r=0;r<n;r++)for(int j=0;j<n;j++)D[r][j]=rows[r][c[r]][j];
          if(!detp(2,D)||!detp(13,D))continue; combos++;
          char out[97]; for(int i=0;i<97;i++)out[i]=0;
          for(int k=0;k<nb;k++){int bs=o+n*k;for(int r=0;r<n;r++){int s=rows[r][c[r]][n];for(int j=0;j<n;j++)s+=D[r][j]*L[bs+j];out[bs+r]=N[s%26];}}
          char pt[97]; if(ix==0)memcpy(pt,out,97); else for(int p=0;p<97;p++)pt[p]=out[S[p]];
          double tot=0;int n=0; for(int i=0;i+4<=97;i++){int g=1,id=0;for(int z=0;z<4;z++){char ch=pt[i+z];if(!ch||ISCRIB[i+z]){g=0;break;}id=id*26+ch-'A';} if(g){tot+=Q[id];n++;}}
          double sc=n?tot/n:-99; if(sc>best){best=sc;memcpy(bestc,c,sizeof c);}
        }
        if(best<-90)continue; int h=(int)((best+8)*5); if(h<0)h=0; if(h>39)h=39; hist[h]++; if(best>gbest)gbest=best;
        if(best>THR){ int D[8][8]; memcpy(c,bestc,sizeof c); for(int r=0;r<n;r++)for(int j=0;j<n;j++)D[r][j]=rows[r][c[r]][j];
          char out[98]; memset(out,'.',97); out[97]=0;
          for(int k=0;k<nb;k++){int bs=o+n*k;for(int r=0;r<n;r++){int s=rows[r][c[r]][n];for(int j=0;j<n;j++)s+=D[r][j]*L[bs+j];out[bs+r]=N[s%26];}}
          char pt[98]; pt[97]=0; if(ix==0)memcpy(pt,out,97); else for(int p=0;p<97;p++)pt[p]=out[S[p]];
          printf("S %s n=%d perm=%ld dir=%d ix=%d num=%d o=%d combos=%ld meanQ=%.3f %s\n",lab,n,q,dir,ix,nu,o,prod,best,pt); fflush(stdout);}
      }}}
  printf("C %s n=%d tests=%ld incons=%ld underdet=%ld scored=%ld invertible_combos=%ld best=%.3f range=%ld..%ld/%ld\nH %s",lab,n,tests,incons,under,scored,combos,gbest,lo,hi,st,lab);
  for(int i=0;i<40;i++)printf(" %ld",hist[i]); printf("\n"); return 0;}
