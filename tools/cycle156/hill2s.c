/* Cycle 156 (IDEAS I-050): key on BOTH sides of the Hill step.
   Encryption: x = p + e[t mod k1] (Vigenere, period k1)  ->  y = E.x (Hill n x n on blocks from offset o)  ->  L = y + f[t mod k2].
   Decoder:    out[t] = sum_j D[r][j]*(L[bs+j] - f[(bs+j) mod k2]) + e'[t mod k1],  D = E^-1, e' = -e  (t = bs + r).
   Beaufort / variant forms on either side are the same model with D -> -D and/or e, f negated, so they are covered.
   Frames as cycles 141/144/153/154: direct; bank model Q L[i]=CT[S[i]], pt=out (ix 0); carved order L=CT, pt[p]=out[S[p]] (ix 1);
   both bank directions; A-Z / KRYPTOS numbering; every alignment o. Cribs 0-based 21-33, 63-73.
   Exact: Z26 = Z2 x Z13 (CRT). In each field either
     (R) D is fixed row by row (rows with most crib equations first, zero rows skipped); after each fixed row the equations of the
         fixed rows are linear in (f, e) and are solved exactly -- an inconsistent prefix prunes all completions; at the leaf D must be
         invertible and the (f, e) solution space (dim d) contributes p^d solutions;   or
     (F) every f on the touched key residues is enumerated (p^|Rf|) and (D, e) solved linearly; each solution is checked for det != 0.
   Counts are exact numbers of (D invertible, e, f) on the crib-touched residues (capped at CNTCAP); <= FCAP solutions are stored,
   CRT-paired (<= COMBOCAP), decrypted and scored by mean log10 quadgram over decided non-crib letters.
   env DROP=1: also re-solve with each crib-bearing Hill block's equations dropped (exact superset for one wrong carved letter or
   one wrong crib letter); MODE13=R|F forces the mod-13 method (default R for n=2, F for n>=3); VERB=1 prints per-config counts.
   usage: hill2s CT perms.bin|- label lo hi stride n k1 k2 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MC 48
static float *Q; static int ISCRIB[97]; static const char *CRIB="EASTNORTHEASTBERLINCLOCK"; static int cpos[24];
static double THR=-4.6; static long COMBOCAP=20000, FCAP=4096, CNTCAP=100000000, ENUMCAP=1000000; static int VERB=0, DROP=0;
static const char *NUMS[2]={"ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"};
static int inv13[13]; static int n,K1,K2; static char M13='?';
static int m, er[24], ebs[24], epv[24], et[24], use[24]; static int L[97];
static int nRf, Rfm[32], Rfr[32], nRe, Rem[32], Rer[32];
typedef struct { unsigned char D[16], f[32], e[32]; } Sol;
static Sol *SS[2]; static long ns[2], cnt[2]; static int over[2], under[2]; static int FI;
static inline int inv(int p,int a){return p==2?1:inv13[a];}
static int gsolve(int p,int mm,int u,int A[][MC],int *b,int *part,int basis[][MC]){
  static int M[24][MC+1]; for(int i=0;i<mm;i++){for(int j=0;j<u;j++)M[i][j]=A[i][j]; M[i][u]=b[i];}
  int piv[MC],r=0; for(int c=0;c<u&&r<mm;c++){int s=-1;for(int i=r;i<mm;i++)if(M[i][c]){s=i;break;} if(s<0)continue;
    if(s!=r)for(int j=c;j<=u;j++){int t=M[r][j];M[r][j]=M[s][j];M[s][j]=t;}
    int iv=inv(p,M[r][c]); if(iv!=1)for(int j=c;j<=u;j++)M[r][j]=M[r][j]*iv%p;
    for(int i=0;i<mm;i++)if(i!=r&&M[i][c]){int f=M[i][c];for(int j=c;j<=u;j++)M[i][j]=(M[i][j]+(p-f)*M[r][j])%p;}
    piv[r]=c;r++;}
  for(int i=r;i<mm;i++)if(M[i][u])return -1;
  if(!part)return u-r;
  int isp[MC]={0};for(int i=0;i<r;i++)isp[piv[i]]=1;
  for(int j=0;j<u;j++)part[j]=0; for(int i=0;i<r;i++)part[piv[i]]=M[i][u];
  int d=0; for(int f=0;f<u;f++)if(!isp[f]){for(int j=0;j<u;j++)basis[d][j]=0;basis[d][f]=1;
    for(int i=0;i<r;i++)basis[d][piv[i]]=(p-M[i][f])%p; d++;}
  return d;}
static int detnz(int p,const unsigned char *Dv){int M[4][4];for(int i=0;i<n;i++)for(int j=0;j<n;j++)M[i][j]=Dv[i*n+j]%p;
  for(int c=0;c<n;c++){int s=-1;for(int i=c;i<n;i++)if(M[i][c]){s=i;break;} if(s<0)return 0;
    if(s!=c)for(int j=0;j<n;j++){int t=M[c][j];M[c][j]=M[s][j];M[s][j]=t;}
    int iv=inv(p,M[c][c]); for(int i=c+1;i<n;i++)if(M[i][c]){int f=M[i][c]*iv%p;for(int j=0;j<n;j++)M[i][j]=(M[i][j]+(p-f)*M[c][j])%p;}}
  return 1;}
static void push(const unsigned char *Dv,const unsigned char *fv,const unsigned char *ev){
  if(cnt[FI]<CNTCAP)cnt[FI]++; else under[FI]=1;
  if(ns[FI]>=FCAP){over[FI]=1;return;} Sol *s=&SS[FI][ns[FI]++]; memcpy(s->D,Dv,16); memcpy(s->f,fv,32); memcpy(s->e,ev,32);}
/* (R) row-by-row D enumeration; unknowns [f(nRf), e(nRe)] */
static int rord[4], Dcur[4][4];
static void rbuild(int p,int lev,int A[][MC],int *b,int *mm){ *mm=0;
  for(int e=0;e<m;e++){ if(!use[e])continue; int r=er[e],fx=0; for(int q=0;q<lev;q++)if(rord[q]==r)fx=1; if(!fx)continue;
    memset(A[*mm],0,sizeof(int)*MC); int s=0;
    for(int j=0;j<n;j++){int pos=ebs[e]+j; s+=Dcur[r][j]*L[pos]; int c=Rfm[pos%K2]; A[*mm][c]=(A[*mm][c]+(p-1)*Dcur[r][j])%p;}
    A[*mm][nRf+Rem[et[e]%K1]]=(A[*mm][nRf+Rem[et[e]%K1]]+1)%p; b[*mm]=((epv[e]-s)%p+p)%p; (*mm)++;}}
static void rrec(int p,int lev){
  int A[24][MC],b[24],mm,u=nRf+nRe;
  if(lev>0){ rbuild(p,lev,A,b,&mm); if(mm>0&&gsolve(p,mm,u,A,b,NULL,NULL)<0)return; }
  if(lev==n){ unsigned char Dv[16]; for(int r=0;r<n;r++)for(int j=0;j<n;j++)Dv[r*n+j]=Dcur[r][j]; if(!detnz(p,Dv))return;
    int part[MC],bas[MC][MC]; int d=gsolve(p,mm,u,A,b,part,bas); if(d<0)return;
    long c=1; for(int i=0;i<d;i++){c*=p; if(c>ENUMCAP)break;}
    if(c>ENUMCAP||ns[FI]+c>FCAP){ over[FI]=1; if(c>ENUMCAP){under[FI]=1;cnt[FI]=CNTCAP;return;} cnt[FI]+=c; if(cnt[FI]>CNTCAP){cnt[FI]=CNTCAP;under[FI]=1;} return;}
    for(long z=0;z<c;z++){ int x[MC]; long cc=z; for(int j=0;j<u;j++)x[j]=part[j];
      for(int i=0;i<d;i++){int co=cc%p;cc/=p; for(int j=0;j<u;j++)x[j]=(x[j]+co*bas[i][j])%p;}
      unsigned char fv[32]={0},ev[32]={0}; for(int j=0;j<nRf;j++)fv[Rfr[j]]=x[j]; for(int j=0;j<nRe;j++)ev[Rer[j]]=x[nRf+j]; push(Dv,fv,ev);}
    return;}
  int r=rord[lev]; long tot=1; for(int j=0;j<n;j++)tot*=p;
  for(long a=1;a<tot;a++){ long z=a; for(int j=0;j<n;j++){Dcur[r][j]=z%p; z/=p;} rrec(p,lev+1); if(under[FI])return; }}
/* (F) f enumeration; unknowns [D(n*n), e(nRe)] */
static void fenum(int p){
  long tot=1; for(int i=0;i<nRf;i++)tot*=p; int u=n*n+nRe;
  for(long a=0;a<tot;a++){ unsigned char fv[32]={0}; long z=a; for(int i=0;i<nRf;i++){fv[Rfr[i]]=z%p; z/=p;}
    int A[24][MC],b[24],mm=0;
    for(int e=0;e<m;e++){ if(!use[e])continue; memset(A[mm],0,sizeof(int)*MC); int r=er[e];
      for(int j=0;j<n;j++){int pos=ebs[e]+j; A[mm][r*n+j]=((L[pos]-fv[pos%K2])%p+p)%p;}
      A[mm][n*n+Rem[et[e]%K1]]=1; b[mm]=epv[e]%p; mm++;}
    int part[MC],bas[MC][MC]; int d=gsolve(p,mm,u,A,b,part,bas); if(d<0)continue;
    long c=1; for(int i=0;i<d;i++){c*=p; if(c>ENUMCAP)break;} if(c>ENUMCAP){over[FI]=under[FI]=1; return;}
    for(long q=0;q<c;q++){ int x[MC]; long cc=q; for(int j=0;j<u;j++)x[j]=part[j];
      for(int i=0;i<d;i++){int co=cc%p;cc/=p; for(int j=0;j<u;j++)x[j]=(x[j]+co*bas[i][j])%p;}
      unsigned char Dv[16],ev[32]={0}; for(int j=0;j<n*n;j++)Dv[j]=x[j]; if(!detnz(p,Dv))continue;
      for(int j=0;j<nRe;j++)ev[Rer[j]]=x[n*n+j]; push(Dv,fv,ev); if(under[FI])return;}
  }}
static void field(int p){ FI=p==2?0:1; ns[FI]=cnt[FI]=0; over[FI]=under[FI]=0;
  int c[4]={0}; for(int e=0;e<m;e++)if(use[e])c[er[e]]++; for(int r=0;r<n;r++)rord[r]=r;
  for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)if(c[rord[b]]>c[rord[a]]){int t=rord[a];rord[a]=rord[b];rord[b]=t;}
  char md=p==2?'R':(M13!='?'?M13:(n==2?'R':'F')); if(md=='R')rrec(p,0); else fenum(p);}
int main(int ac,char**av){
  if(ac<10)return 1; n=atoi(av[7]); K1=atoi(av[8]); K2=atoi(av[9]); if(n<2||n>4||K1<1||K1>32||K2<1||K2>32)return 4;
  for(int i=1;i<13;i++)for(int j=1;j<13;j++)if(i*j%13==1)inv13[i]=j;
  if(getenv("THR"))THR=atof(getenv("THR")); if(getenv("COMBOCAP"))COMBOCAP=atol(getenv("COMBOCAP")); if(getenv("FCAP"))FCAP=atol(getenv("FCAP"));
  if(getenv("VERB"))VERB=atoi(getenv("VERB")); if(getenv("DROP"))DROP=atoi(getenv("DROP")); if(getenv("MODE13"))M13=getenv("MODE13")[0];
  SS[0]=malloc(sizeof(Sol)*FCAP); SS[1]=malloc(sizeof(Sol)*FCAP);
  Q=malloc(456976*4);{FILE*f=fopen(getenv("QUAD")?getenv("QUAD"):"/home/box/kryptos_support_backup/quad.bin","rb");if(!f||fread(Q,4,456976,f)!=456976)return 2;fclose(f);}
  {int k=0;for(int i=21;i<=33;i++){ISCRIB[i]=1;cpos[k++]=i;}for(int i=63;i<=73;i++){ISCRIB[i]=1;cpos[k++]=i;}}
  const char*CT=av[1]; const char*lab=av[3]; long lo=atol(av[4]),hi=atol(av[5]),st=atol(av[6]);
  long np=1; short *bank=NULL; if(strcmp(av[2],"-")){FILE*f=fopen(av[2],"rb");fseek(f,0,2);np=ftell(f)/194;fseek(f,0,0);bank=malloc(np*194);if(fread(bank,194,np,f)!=(size_t)np)return 3;fclose(f);}
  if(hi>np)hi=np;
  long tests=0,incons=0,surv=0,und=0,scored=0,combos=0,xsurv=0,xund=0; double gbest=-99;
  for(long q=lo;q<hi;q+=st)for(int dir=0;dir<(bank?2:1);dir++){
    int S[97]; if(bank){for(int i=0;i<97;i++)S[i]=bank[q*97+i]; if(dir){int T[97];for(int i=0;i<97;i++)T[S[i]]=i;memcpy(S,T,sizeof S);}} else for(int i=0;i<97;i++)S[i]=i;
    for(int ix=0;ix<(bank?2:1);ix++)for(int nu=0;nu<2;nu++){
      const char*N=NUMS[nu]; int idx[26]; for(int i=0;i<26;i++)idx[N[i]-'A']=i; int kp[97]; for(int i=0;i<97;i++)kp[i]=-1;
      if(ix==0){for(int i=0;i<97;i++)L[i]=idx[CT[S[i]]-'A']; for(int k=0;k<24;k++)kp[cpos[k]]=idx[CRIB[k]-'A'];}
      else{for(int i=0;i<97;i++)L[i]=idx[CT[i]-'A']; for(int k=0;k<24;k++)kp[S[cpos[k]]]=idx[CRIB[k]-'A'];}
      for(int o=0;o<n;o++){ tests++;
        int nb=(97-o)/n; m=0; for(int t=o;t<o+nb*n;t++)if(kp[t]>=0){er[m]=(t-o)%n; ebs[m]=o+((t-o)/n)*n; epv[m]=kp[t]; et[m]=t; m++;}
        for(int s=0;s<32;s++)Rfm[s]=Rem[s]=-1; nRf=nRe=0;
        for(int e=0;e<m;e++){ for(int j=0;j<n;j++){int s=(ebs[e]+j)%K2; if(Rfm[s]<0){Rfm[s]=nRf;Rfr[nRf++]=s;}}
          int s=et[e]%K1; if(Rem[s]<0){Rem[s]=nRe;Rer[nRe++]=s;}}
        int nblk=0, blk[24]; for(int e=0;e<m;e++){int f=0;for(int i=0;i<nblk;i++)if(blk[i]==ebs[e])f=1; if(!f)blk[nblk++]=ebs[e];}
        for(int pass=-1;pass<(DROP?nblk:0);pass++){
          for(int e=0;e<m;e++)use[e]=(pass<0||ebs[e]!=blk[pass]);
          field(2); if(cnt[0]==0&&!under[0]&&!(VERB&&pass<0)){ if(pass<0)incons++; continue;}
          field(13); if(cnt[0]==0&&!under[0]){ printf("V %s n=%d k1=%d k2=%d nu=%d o=%d c2=0 c13=%ld%s\n",lab,n,K1,K2,nu,o,cnt[1],under[1]?"+":""); incons++; continue;}
          if(VERB&&pass<0)printf("V %s n=%d k1=%d k2=%d nu=%d o=%d c2=%ld%s c13=%ld%s\n",lab,n,K1,K2,nu,o,cnt[0],under[0]?"+":"",cnt[1],under[1]?"+":"");
          if(cnt[1]==0&&!under[1]){ if(pass<0)incons++; continue;}
          if(pass<0)surv++; else xsurv++;
          if(over[0]||over[1]||(double)ns[0]*ns[1]>COMBOCAP){ if(pass<0)und++; else xund++;
            printf("U %s n=%d k1=%d k2=%d perm=%ld dir=%d ix=%d num=%d o=%d drop=%d c2=%ld%s c13=%ld%s\n",lab,n,K1,K2,q,dir,ix,nu,o,pass<0?-1:blk[pass],cnt[0],under[0]?"+":"",cnt[1],under[1]?"+":""); continue;}
          if(pass<0)scored++; double best=-99; char bpt[98]; bpt[97]=0; int bD[16],bf[32],be[32];
          for(long a=0;a<ns[0];a++)for(long c=0;c<ns[1];c++){ int D[16],fk[32],ek[32]; combos++;
            for(int j=0;j<n*n;j++)D[j]=(13*SS[0][a].D[j]+14*SS[1][c].D[j])%26;
            for(int j=0;j<K2;j++)fk[j]=Rfm[j]<0?-1:(13*SS[0][a].f[j]+14*SS[1][c].f[j])%26;
            for(int j=0;j<K1;j++)ek[j]=Rem[j]<0?-1:(13*SS[0][a].e[j]+14*SS[1][c].e[j])%26;
            char out[97]; memset(out,0,97);
            for(int bs=o;bs+n<=o+nb*n;bs+=n){int ok=1;for(int j=0;j<n;j++)if(fk[(bs+j)%K2]<0)ok=0; if(!ok)continue;
              for(int r=0;r<n;r++){ if(ek[(bs+r)%K1]<0)continue; int s=ek[(bs+r)%K1];
                for(int j=0;j<n;j++)s+=D[r*n+j]*(L[bs+j]-fk[(bs+j)%K2]+26); out[bs+r]=N[s%26];}}
            char pt[97]; if(ix==0)memcpy(pt,out,97); else for(int p=0;p<97;p++)pt[p]=out[S[p]];
            double tot=0;int w=0; for(int i=0;i+4<=97;i++){int g=1,id=0;for(int z=0;z<4;z++){char ch=pt[i+z];if(!ch||ISCRIB[i+z]){g=0;break;}id=id*26+ch-'A';} if(g){tot+=Q[id];w++;}}
            double sc=w>=20?tot/w:-99; if(sc>best){best=sc;for(int i=0;i<97;i++)bpt[i]=pt[i]?pt[i]:'.';memcpy(bD,D,sizeof bD);memcpy(bf,fk,sizeof bf);memcpy(be,ek,sizeof be);}
          }
          if(best>gbest)gbest=best;
          if(best>THR||VERB>1){printf("%s %s n=%d k1=%d k2=%d perm=%ld dir=%d ix=%d num=%d o=%d drop=%d sols=%ld meanQ=%.3f D=",pass<0?"S":"X",lab,n,K1,K2,q,dir,ix,nu,o,pass<0?-1:blk[pass],ns[0]*ns[1],best);
            for(int j=0;j<n*n;j++)printf("%d%s",bD[j],j<n*n-1?",":""); printf(" e="); for(int j=0;j<K1;j++)printf("%d%s",be[j],j<K1-1?",":"");
            printf(" f="); for(int j=0;j<K2;j++)printf("%d%s",bf[j],j<K2-1?",":""); printf(" %s\n",bpt); fflush(stdout);}
        }
      }}}
  printf("C %s n=%d k1=%d k2=%d tests=%ld incons=%ld survivors=%ld underdet=%ld scored=%ld combos=%ld drop_survivors=%ld drop_underdet=%ld best=%.3f range=%ld..%ld/%ld drop=%d\n",lab,n,K1,K2,tests,incons,surv,und,scored,combos,xsurv,xund,gbest,lo,hi,st,DROP);
  return 0;}
