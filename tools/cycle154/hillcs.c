/* Cycle 154 (IDEAS I-012): Hill with the periodic key on the CIPHERTEXT side.
   Decoder: out[t] = sum_j D[r][j] * (L[bs+j] - f[(bs+j) mod k])   (t = bs+r, blocks of n from offset o)
   i.e. encryption = Hill first (E = D^-1), then a period-k Vigenere on the Hill output: L = E.p + f.
   Frames as cycles 141/144/153: direct; bank model Q L[i]=CT[S[i]], pt=out; bank carved order L=CT, pt[p]=out[S[p]];
   both bank directions; A-Z / KRYPTOS numbering; every alignment o.
   The system is bilinear in (D, f). It splits exactly into Z2 x Z13 (CRT). In each field we enumerate whichever side is
   smaller -- all f values on the key residues touched by crib blocks (P^|R|), or all invertible D (P^(n*n)) -- and solve the
   other side by exact Gaussian elimination. Each field yields a list of (D invertible, f) solutions (cap FCAP); the
   configuration survives iff both lists are non-empty; CRT pairs (<= COMBOCAP) are decrypted and quadgram-scored.
   env DROP=1: one-error tolerant mode (direct use): additionally re-solve with each crib-bearing Hill block's equations
   dropped (covers one wrong carved letter or one wrong crib letter); survivors printed as X lines.
   usage: hillcs CT perms.bin|- label lo hi stride n k     env THR (-4.6) COMBOCAP (20000) FCAP (4096) VERB DROP QUAD */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static float *Q; static int ISCRIB[97]; static const char *CRIB="EASTNORTHEASTBERLINCLOCK";
static int cpos[24]; static double THR=-4.6; static long COMBOCAP=20000, FCAP=4096; static int VERB=0, DROP=0;
static const char *NUMS[2]={"ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"};
static int inv13[13]; static int n,K;
/* equations: row r, block start bs, rhs pv */
static int m, er[24], ebs[24], epv[24]; static int L[97];
static int nR, Rmap[64], Rres[64]; /* key residues touched by crib blocks */
typedef struct { unsigned char D[16]; unsigned char f[32]; } Sol;
static Sol *S2, *S13; static long ns2, ns13; static int over2, over13;
static inline int inv(int p,int a){return p==2?1:inv13[a];}
/* generic solve: A (mm x u) x = b over Z_p; returns dim of null space or -1; part, basis */
static int gsolve(int p,int mm,int u,int A[][33],int *b,int *part,int basis[][32]){
  int M[40][34]; for(int i=0;i<mm;i++){for(int j=0;j<u;j++)M[i][j]=A[i][j]; M[i][u]=b[i];}
  int piv[32],r=0; for(int c=0;c<u&&r<mm;c++){int s=-1;for(int i=r;i<mm;i++)if(M[i][c]){s=i;break;} if(s<0)continue;
    if(s!=r)for(int j=0;j<=u;j++){int t=M[r][j];M[r][j]=M[s][j];M[s][j]=t;}
    int iv=inv(p,M[r][c]); if(iv!=1)for(int j=0;j<=u;j++)M[r][j]=M[r][j]*iv%p;
    for(int i=0;i<mm;i++)if(i!=r&&M[i][c]){int f=M[i][c];for(int j=0;j<=u;j++)M[i][j]=(M[i][j]+(p-f)*M[r][j])%p;}
    piv[r]=c;r++;}
  for(int i=r;i<mm;i++)if(M[i][u])return -1;
  int isp[32]={0};for(int i=0;i<r;i++)isp[piv[i]]=1;
  for(int j=0;j<u;j++)part[j]=0; for(int i=0;i<r;i++)part[piv[i]]=M[i][u];
  int d=0; for(int f=0;f<u;f++)if(!isp[f]){for(int j=0;j<u;j++)basis[d][j]=0;basis[d][f]=1;
    for(int i=0;i<r;i++)basis[d][piv[i]]=(p-M[i][f])%p; d++;}
  return d;}
static int detnz(int p,const unsigned char *Dv){int M[4][4];for(int i=0;i<n;i++)for(int j=0;j<n;j++)M[i][j]=Dv[i*n+j]%p;
  for(int c=0;c<n;c++){int s=-1;for(int i=c;i<n;i++)if(M[i][c]){s=i;break;} if(s<0)return 0;
    if(s!=c)for(int j=0;j<n;j++){int t=M[c][j];M[c][j]=M[s][j];M[s][j]=t;}
    int iv=inv(p,M[c][c]); for(int i=c+1;i<n;i++)if(M[i][c]){int f=M[i][c]*iv%p;for(int j=0;j<n;j++)M[i][j]=(M[i][j]+(p-f)*M[c][j])%p;}}
  return 1;}
static void push(int p,const unsigned char *Dv,const unsigned char *fv){
  Sol **SS=p==2?&S2:&S13; long *ns=p==2?&ns2:&ns13; int *ov=p==2?&over2:&over13;
  if(*ns>=FCAP){*ov=1;return;} memcpy((*SS)[*ns].D,Dv,16); memcpy((*SS)[*ns].f,fv,32); (*ns)++;}
static int use[24]; /* equation mask (DROP mode) */
/* f-enumeration mode in field p */
static void fenum(int p){
  unsigned char fv[32]={0}; long tot=1; for(int i=0;i<nR;i++)tot*=p;
  int rows[4][24],nr[4]={0}; for(int e=0;e<m;e++)if(use[e])rows[er[e]][nr[er[e]]++]=e;
  for(long a=0;a<tot;a++){ long z=a; for(int i=0;i<nR;i++){fv[Rres[i]]=z%p;z/=p;}
    int part[4][32],bas[4][32][32],dd[4],ok=1;
    for(int r=0;r<n&&ok;r++){int A[40][33],b[40]; for(int q=0;q<nr[r];q++){int e=rows[r][q];
        for(int j=0;j<n;j++){int pos=ebs[e]+j; A[q][j]=((L[pos]-fv[pos%K])%p+p)%p;} b[q]=epv[e]%p;}
      dd[r]=gsolve(p,nr[r],n,A,b,part[r],bas[r]); if(dd[r]<0)ok=0;}
    if(!ok)continue;
    /* enumerate D = product of row spaces */
    long cnt=1; for(int r=0;r<n;r++)for(int i=0;i<dd[r];i++)cnt*=p;
    if(cnt>FCAP){ if(p==2)over2=1; else over13=1; continue; }
    for(long c=0;c<cnt;c++){unsigned char Dv[16]; long cc=c;
      for(int r=0;r<n;r++){int x[32];for(int j=0;j<n;j++)x[j]=part[r][j];
        for(int i=0;i<dd[r];i++){int co=cc%p;cc/=p;for(int j=0;j<n;j++)x[j]=(x[j]+co*bas[r][i][j])%p;}
        for(int j=0;j<n;j++)Dv[r*n+j]=x[j];}
      if(detnz(p,Dv))push(p,Dv,fv);}
  }}
/* D-enumeration mode in field p: f linear */
static void denum(int p){
  long tot=1; for(int i=0;i<n*n;i++)tot*=p; unsigned char Dv[16];
  for(long a=0;a<tot;a++){long z=a; for(int i=0;i<n*n;i++){Dv[i]=z%p;z/=p;} if(!detnz(p,Dv))continue;
    int A[40][33],b[40],mm=0;
    for(int e=0;e<m;e++){ if(!use[e])continue; int r=er[e]; memset(A[mm],0,sizeof A[mm]); int s=0;
      for(int j=0;j<n;j++){int pos=ebs[e]+j; s+=Dv[r*n+j]*L[pos]; A[mm][Rmap[pos%K]]=(A[mm][Rmap[pos%K]]+Dv[r*n+j])%p;}
      b[mm]=((s-epv[e])%p+p)%p; mm++;}
    int part[32],bas[32][32]; int d=gsolve(p,mm,nR,A,b,part,bas); if(d<0)continue;
    long cnt=1; for(int i=0;i<d;i++)cnt*=p; if(cnt>FCAP){ if(p==2)over2=1; else over13=1; continue;}
    for(long c=0;c<cnt;c++){unsigned char fv[32]={0}; long cc=c; int x[32]; for(int j=0;j<nR;j++)x[j]=part[j];
      for(int i=0;i<d;i++){int co=cc%p;cc/=p;for(int j=0;j<nR;j++)x[j]=(x[j]+co*bas[i][j])%p;}
      for(int j=0;j<nR;j++)fv[Rres[j]]=x[j]; push(p,Dv,fv);}
  }}
/* row-enumeration mode in field p: enumerate one row of D (the row with most crib equations), solve f from that row's
   equations (linear), enumerate the remaining f space, solve the other rows linearly. */
static int rstar_of(void){int c[4]={0};for(int e=0;e<m;e++)if(use[e])c[er[e]]++; int b=0;for(int r=1;r<n;r++)if(c[r]>c[b])b=r; return b;}
static int rowcount(int r){int c=0;for(int e=0;e<m;e++)if(use[e]&&er[e]==r)c++;return c;}
static void renum(int p){
  int rs=rstar_of(); long tot=1; for(int i=0;i<n;i++)tot*=p;
  int rows[4][24],nr[4]={0}; for(int e=0;e<m;e++)if(use[e])rows[er[e]][nr[er[e]]++]=e;
  for(long a=1;a<tot;a++){ int Dr[4]; long z=a; for(int j=0;j<n;j++){Dr[j]=z%p;z/=p;}
    int A[40][33],b[40],mm=0;
    for(int q=0;q<nr[rs];q++){int e=rows[rs][q]; memset(A[mm],0,sizeof A[mm]); int sm=0;
      for(int j=0;j<n;j++){int pos=ebs[e]+j; sm+=Dr[j]*L[pos]; A[mm][Rmap[pos%K]]=(A[mm][Rmap[pos%K]]+Dr[j])%p;}
      b[mm]=((sm-epv[e])%p+p)%p; mm++;}
    int fp[32],fb[32][32]; int d=gsolve(p,mm,nR,A,b,fp,fb); if(d<0)continue;
    long fc=1; for(int i=0;i<d;i++){fc*=p; if(fc>4000000)break;} if(fc>4000000){ if(p==2)over2=1; else over13=1; continue;}
    for(long c=0;c<fc;c++){ unsigned char fv[32]={0}; int x[32]; long cc=c; for(int j=0;j<nR;j++)x[j]=fp[j];
      for(int i=0;i<d;i++){int co=cc%p;cc/=p;for(int j=0;j<nR;j++)x[j]=(x[j]+co*fb[i][j])%p;}
      for(int j=0;j<nR;j++)fv[Rres[j]]=x[j];
      int part[4][32],bas[4][32][32],dd[4],ok=1;
      for(int r=0;r<n&&ok;r++){ if(r==rs){dd[r]=0;for(int j=0;j<n;j++)part[r][j]=Dr[j];continue;}
        int A2[40][33],b2[40]; for(int q=0;q<nr[r];q++){int e=rows[r][q];
          for(int j=0;j<n;j++){int pos=ebs[e]+j; A2[q][j]=((L[pos]-fv[pos%K])%p+p)%p;} b2[q]=epv[e]%p;}
        dd[r]=gsolve(p,nr[r],n,A2,b2,part[r],bas[r]); if(dd[r]<0)ok=0;}
      if(!ok)continue;
      long cnt=1; for(int r=0;r<n;r++)for(int i=0;i<dd[r];i++)cnt*=p;
      if(cnt>FCAP){ if(p==2)over2=1; else over13=1; continue; }
      for(long c2=0;c2<cnt;c2++){unsigned char Dv[16]; long c3=c2;
        for(int r=0;r<n;r++){int y[32];for(int j=0;j<n;j++)y[j]=part[r][j];
          for(int i=0;i<dd[r];i++){int co=c3%p;c3/=p;for(int j=0;j<n;j++)y[j]=(y[j]+co*bas[r][i][j])%p;}
          for(int j=0;j<n;j++)Dv[r*n+j]=y[j];}
        if(detnz(p,Dv))push(p,Dv,fv);}
    }
  }}
/* recursive row mode (exact, used for configurations the other modes leave unresolved): rows of D are fixed one at a time
   (most equations first); each fixed row turns its equations into linear constraints on the affine f-space; when the
   f-space is small (p^d <= RCAP) it is enumerated and the remaining rows solved linearly. */
static long RCAP=200000;
static int rorder[4], rrows[4][24], rnr[4]; static int Dfix[4][4];
static void rec_leaf(int p,int lev,int *fp,int fb[][32],int d){
  long fc=1; for(int i=0;i<d;i++)fc*=p;
  for(long c=0;c<fc;c++){ unsigned char fv[32]={0}; int x[32]; long cc=c; for(int j=0;j<nR;j++)x[j]=fp[j];
    for(int i=0;i<d;i++){int co=cc%p;cc/=p;for(int j=0;j<nR;j++)x[j]=(x[j]+co*fb[i][j])%p;}
    for(int j=0;j<nR;j++)fv[Rres[j]]=x[j];
    int part[4][32],bas[4][32][32],dd[4],ok=1;
    for(int q=0;q<n&&ok;q++){int r=rorder[q]; if(q<lev){dd[r]=0;for(int j=0;j<n;j++)part[r][j]=Dfix[r][j];continue;}
      int A2[40][33],b2[40]; for(int z=0;z<rnr[r];z++){int e=rrows[r][z];
        for(int j=0;j<n;j++){int pos=ebs[e]+j; A2[z][j]=((L[pos]-fv[pos%K])%p+p)%p;} b2[z]=epv[e]%p;}
      dd[r]=gsolve(p,rnr[r],n,A2,b2,part[r],bas[r]); if(dd[r]<0)ok=0;}
    if(!ok)continue;
    long cnt=1; for(int r=0;r<n;r++)for(int i=0;i<dd[r];i++)cnt*=p;
    if(cnt>FCAP){ if(p==2)over2=1; else over13=1; continue; }
    for(long c2=0;c2<cnt;c2++){unsigned char Dv[16]; long c3=c2;
      for(int r=0;r<n;r++){int y[32];for(int j=0;j<n;j++)y[j]=part[r][j];
        for(int i=0;i<dd[r];i++){int co=c3%p;c3/=p;for(int j=0;j<n;j++)y[j]=(y[j]+co*bas[r][i][j])%p;}
        for(int j=0;j<n;j++)Dv[r*n+j]=y[j];}
      if(detnz(p,Dv))push(p,Dv,fv);}
  }}
static void rec(int p,int lev,int *fp,int fb[][32],int d){
  long fc=1; int big=0; for(int i=0;i<d;i++){fc*=p; if(fc>RCAP){big=1;break;}}
  if(!big||lev==n){ if(big){ if(p==2)over2=1; else over13=1; return;} rec_leaf(p,lev,fp,fb,d); return; }
  int r=rorder[lev]; long tot=1; for(int i=0;i<n;i++)tot*=p;
  for(long a=1;a<tot;a++){ long z=a; for(int j=0;j<n;j++){Dfix[r][j]=z%p;z/=p;}
    /* constraints on t: sum_j Dr_j f[col] = Dr.L - pv, f = fp + sum t_i fb_i */
    int A[40][33],b[40],mm=0;
    for(int q=0;q<rnr[r];q++){int e=rrows[r][q]; int cf[32]={0},sm=0;
      for(int j=0;j<n;j++){int pos=ebs[e]+j; sm+=Dfix[r][j]*L[pos]; cf[Rmap[pos%K]]=(cf[Rmap[pos%K]]+Dfix[r][j])%p;}
      int rhs=sm-epv[e]; for(int j=0;j<nR;j++)rhs-=cf[j]*fp[j]; b[mm]=((rhs%p)+p)%p;
      for(int i=0;i<d;i++){int v=0;for(int j=0;j<nR;j++)v+=cf[j]*fb[i][j]; A[mm][i]=v%p;} mm++;}
    int tp[32],tb[32][32]; int d2=gsolve(p,mm,d,A,b,tp,tb); if(d2<0)continue;
    int nfp[32],nfb[32][32]; for(int j=0;j<nR;j++){int v=fp[j];for(int i=0;i<d;i++)v+=tp[i]*fb[i][j];nfp[j]=v%p;}
    for(int u=0;u<d2;u++)for(int j=0;j<nR;j++){int v=0;for(int i=0;i<d;i++)v+=tb[u][i]*fb[i][j];nfb[u][j]=v%p;}
    rec(p,lev+1,nfp,nfb,d2);
  }}
static void recmode(int p){
  for(int r=0;r<n;r++)rnr[r]=0; for(int e=0;e<m;e++)if(use[e])rrows[er[e]][rnr[er[e]]++]=e;
  for(int r=0;r<n;r++)rorder[r]=r; for(int a=0;a<n;a++)for(int b2=a+1;b2<n;b2++)if(rnr[rorder[b2]]>rnr[rorder[a]]){int t=rorder[a];rorder[a]=rorder[b2];rorder[b2]=t;}
  int fp[32]={0},fb[32][32]; for(int i=0;i<nR;i++){for(int j=0;j<nR;j++)fb[i][j]=0;fb[i][i]=1;} rec(p,0,fp,fb,nR);}
static void field(int p){ double cf=1,cd=1,cr=1; for(int i=0;i<nR;i++)cf*=p; for(int i=0;i<n*n;i++)cd*=p;
  int rs=rstar_of(); int fr=nR-rowcount(rs); if(fr<0)fr=0; for(int i=0;i<n;i++)cr*=p; for(int i=0;i<fr;i++)cr*=p; cr*=2;
  if(p==2){ns2=0;over2=0;}else{ns13=0;over13=0;}
  int mode=getenv("MODE")?atoi(getenv("MODE")):0;
  if(mode==1)fenum(p); else if(mode==2)denum(p); else if(mode==3)renum(p); else if(mode==4)recmode(p);
  else if(cf<=cd&&cf<=cr)fenum(p); else if(cd<=cr)denum(p); else renum(p);}
int main(int ac,char**av){
  if(ac<9)return 1; n=atoi(av[7]); K=atoi(av[8]); if(n<2||n>4||K<1||K>32)return 4;
  for(int i=1;i<13;i++)for(int j=1;j<13;j++)if(i*j%13==1)inv13[i]=j;
  if(getenv("THR"))THR=atof(getenv("THR")); if(getenv("COMBOCAP"))COMBOCAP=atol(getenv("COMBOCAP"));
  if(getenv("FCAP"))FCAP=atol(getenv("FCAP")); if(getenv("VERB"))VERB=atoi(getenv("VERB")); if(getenv("DROP"))DROP=atoi(getenv("DROP"));
  S2=malloc(sizeof(Sol)*FCAP); S13=malloc(sizeof(Sol)*FCAP);
  Q=malloc(456976*4);{FILE*f=fopen(getenv("QUAD")?getenv("QUAD"):"/home/box/kryptos_support_backup/quad.bin","rb");if(!f||fread(Q,4,456976,f)!=456976)return 2;fclose(f);}
  {int k=0;for(int i=21;i<=33;i++){ISCRIB[i]=1;cpos[k++]=i;}for(int i=63;i<=73;i++){ISCRIB[i]=1;cpos[k++]=i;}}
  const char*CT=av[1]; const char*lab=av[3]; long lo=atol(av[4]),hi=atol(av[5]),st=atol(av[6]);
  long np=1; short *bank=NULL; if(strcmp(av[2],"-")){FILE*f=fopen(av[2],"rb");fseek(f,0,2);np=ftell(f)/194;fseek(f,0,0);bank=malloc(np*194);if(fread(bank,194,np,f)!=(size_t)np)return 3;fclose(f);}
  if(hi>np)hi=np; if(getenv("RCAP"))RCAP=atol(getenv("RCAP"));
  long *cf=NULL; int ncf=0; if(getenv("CFG")){FILE*g=fopen(getenv("CFG"),"r"); cf=malloc(sizeof(long)*5*100000); while(ncf<100000&&fscanf(g,"%ld %ld %ld %ld %ld",&cf[ncf*5],&cf[ncf*5+1],&cf[ncf*5+2],&cf[ncf*5+3],&cf[ncf*5+4])==5)ncf++; fclose(g);} long tests=0,incons=0,under=0,scored=0,combos=0,surv=0,xsurv=0; double gbest=-99;
  for(long q=lo;q<hi;q+=st)for(int dir=0;dir<(bank?2:1);dir++){
    int S[97]; if(bank){for(int i=0;i<97;i++)S[i]=bank[q*97+i]; if(dir){int T[97];for(int i=0;i<97;i++)T[S[i]]=i;memcpy(S,T,sizeof S);}} else for(int i=0;i<97;i++)S[i]=i;
    for(int ix=0;ix<(bank?2:1);ix++)for(int nu=0;nu<2;nu++){
      const char*N=NUMS[nu]; int idx[26]; for(int i=0;i<26;i++)idx[N[i]-'A']=i; int kp[97]; for(int i=0;i<97;i++)kp[i]=-1;
      if(ix==0){for(int i=0;i<97;i++)L[i]=idx[CT[S[i]]-'A']; for(int k=0;k<24;k++)kp[cpos[k]]=idx[CRIB[k]-'A'];}
      else{for(int i=0;i<97;i++)L[i]=idx[CT[i]-'A']; for(int k=0;k<24;k++)kp[S[cpos[k]]]=idx[CRIB[k]-'A'];}
      for(int o=0;o<n;o++){ if(cf){int hit=0;for(int z=0;z<ncf;z++)if(cf[z*5]==q&&cf[z*5+1]==dir&&cf[z*5+2]==ix&&cf[z*5+3]==nu&&cf[z*5+4]==o){hit=1;break;} if(!hit)continue;} tests++;
        int nb=(97-o)/n; m=0; for(int t=o;t<o+nb*n;t++)if(kp[t]>=0){er[m]=(t-o)%n; ebs[m]=o+((t-o)/n)*n; epv[m]=kp[t]; m++;}
        for(int s=0;s<K;s++)Rmap[s]=-1; nR=0;
        for(int e=0;e<m;e++)for(int j=0;j<n;j++){int s=(ebs[e]+j)%K; if(Rmap[s]<0){Rmap[s]=nR;Rres[nR++]=s;}}
        int nblk=0, blk[24]; for(int e=0;e<m;e++){int f=0;for(int i=0;i<nblk;i++)if(blk[i]==ebs[e])f=1; if(!f)blk[nblk++]=ebs[e];}
        for(int pass=-1;pass<(DROP?nblk:0);pass++){
          for(int e=0;e<m;e++)use[e]=(pass<0||ebs[e]!=blk[pass]);
          field(2); if(ns2==0&&!over2&&!(VERB&&pass<0)){ if(pass<0)incons++; continue;}
          field(13); if(ns2==0&&!over2){ if(VERB)printf("V %s n=%d k=%d nu=%d o=%d n2=0 n13=%ld%s\n",lab,n,K,nu,o,ns13,over13?"+":""); incons++; continue;}
          if(VERB&&pass<0)printf("V %s n=%d k=%d nu=%d o=%d n2=%ld%s n13=%ld%s\n",lab,n,K,nu,o,ns2,over2?"+":"",ns13,over13?"+":"");
          if(ns13==0&&!over13){ if(pass<0)incons++; continue;}
          if(pass<0)surv++; else xsurv++;
          if(over2||over13||(double)ns2*ns13>COMBOCAP){ if(pass<0)under++;
            printf("U %s n=%d k=%d perm=%ld dir=%d ix=%d num=%d o=%d drop=%d n2=%ld%s n13=%ld%s\n",lab,n,K,q,dir,ix,nu,o,pass<0?-1:blk[pass],ns2,over2?"+":"",ns13,over13?"+":""); continue;}
          if(pass<0)scored++; double best=-99; char bpt[98]; bpt[97]=0; int bD[16],bf[32];
          for(long a=0;a<ns2;a++)for(long c=0;c<ns13;c++){ int D[16],fk[32]; combos++;
            for(int j=0;j<n*n;j++)D[j]=(13*S2[a].D[j]+14*S13[c].D[j])%26;
            for(int j=0;j<K;j++)fk[j]=Rmap[j]<0?-1:(13*S2[a].f[j]+14*S13[c].f[j])%26;
            char out[97]; memset(out,0,97);
            for(int bs=o;bs+n<=o+nb*n;bs+=n){int ok=1;for(int j=0;j<n;j++)if(fk[(bs+j)%K]<0)ok=0; if(!ok)continue;
              for(int r=0;r<n;r++){int s=0;for(int j=0;j<n;j++)s+=D[r*n+j]*(L[bs+j]-fk[(bs+j)%K]+26); out[bs+r]=N[s%26];}}
            char pt[97]; if(ix==0)memcpy(pt,out,97); else for(int p=0;p<97;p++)pt[p]=out[S[p]];
            double tot=0;int w=0; for(int i=0;i+4<=97;i++){int g=1,id=0;for(int z=0;z<4;z++){char ch=pt[i+z];if(!ch||ISCRIB[i+z]){g=0;break;}id=id*26+ch-'A';} if(g){tot+=Q[id];w++;}}
            double sc=w>=20?tot/w:-99; if(sc>best){best=sc;for(int i=0;i<97;i++)bpt[i]=pt[i]?pt[i]:'.';memcpy(bD,D,sizeof bD);memcpy(bf,fk,sizeof bf);}
          }
          if(best>gbest)gbest=best;
          if(best>THR||VERB>1){printf("%s %s n=%d k=%d perm=%ld dir=%d ix=%d num=%d o=%d drop=%d sols=%ld meanQ=%.3f D=",pass<0?"S":"X",lab,n,K,q,dir,ix,nu,o,pass<0?-1:blk[pass],ns2*ns13,best);
            for(int j=0;j<n*n;j++)printf("%d%s",bD[j],j<n*n-1?",":""); printf(" f="); for(int j=0;j<K;j++)printf("%d%s",bf[j],j<K-1?",":""); printf(" %s\n",bpt); fflush(stdout);}
        }
      }}}
  printf("C %s n=%d k=%d tests=%ld incons=%ld survivors=%ld underdet=%ld scored=%ld combos=%ld drop_survivors=%ld best=%.3f range=%ld..%ld/%ld drop=%d\n",lab,n,K,tests,incons,surv,under,scored,combos,xsurv,gbest,lo,hi,st,DROP);
  return 0;}
