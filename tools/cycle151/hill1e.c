/* Cycle 151: Hill n x n (n = 2..4) under ONE carving error, exact.
   Decoder (same frames as cycles 27/141-144): ix=0 (model Q): L[i]=CT[S[i]], out=Hill(L), pt=out;
   ix=1 (carved order): L=CT, out=Hill(L), pt[p]=out[S[p]]. Direct = identity S, ix=0.
   out[t] = sum_j D[r][j]*L[bs+j] (mod 26), bs = block start (alignment o), r = t-bs.
   A wrong carved letter sits in exactly one Hill block of L, so it breaks only the crib equations of that block
   (a wrong crib letter breaks one equation of one block). Test: for every Hill block b that carries crib equations,
   drop b's equations, solve every row exactly (mod 2 and mod 13, CRT), require D invertible, then require an
   exact ONE-LETTER REPAIR of block b (some position j of the block and some letter v != L[bs+j] such that the
   repaired block reproduces all its crib letters). Counters:
     strict     = configs consistent with all 24 cribs (cycle-27-style, sanity),
     blockdrop  = configs with some block b whose removal makes all rows consistent (covers a wrong crib letter),
     eqdrop     = configs where removing ONE crib equation suffices (exact one-wrong-crib-letter model),
     repair     = (config,b) pairs with an invertible D and an exact one-letter repair of b (one-carved-letter model),
     invertible = invertible D solutions over all block-drop pairs (before the repair check),
     under      = (config,b) pairs whose solution space exceeds COMBOCAP (blind spot, counted, not decoded).
   usage: hill1e CT perms.bin|- label lo hi stride n      env THR (-5.0 print threshold), COMBOCAP (4096), QUAD */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static float *Q; static int ISCRIB[97]; static const char *CRIB="EASTNORTHEASTBERLINCLOCK";
static int cpos[24]; static double THR=-5.0; static long COMBOCAP=4096; static int n;
static const char *NUMS[2]={"ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"};
static int inv13[13];
/* solve A x = b mod p, m eqs, n unknowns; skip row 'skip'. returns -1 inconsistent, else nullity; fills part, basis */
static int solvep(int p,int m,int A[][4],int *b,int skip,int *part,int basis[4][4]){
  int M[24][5],mm=0; for(int i=0;i<m;i++){if(i==skip)continue;for(int j=0;j<n;j++)M[mm][j]=A[i][j]%p; M[mm][n]=b[i]%p; mm++;}
  int piv[4],r=0; for(int c=0;c<n&&r<mm;c++){int s=-1;for(int i=r;i<mm;i++)if(M[i][c]){s=i;break;} if(s<0)continue;
    if(s!=r)for(int j=0;j<=n;j++){int t=M[r][j];M[r][j]=M[s][j];M[s][j]=t;}
    int iv=(p==2)?1:inv13[M[r][c]]; for(int j=0;j<=n;j++)M[r][j]=M[r][j]*iv%p;
    for(int i=0;i<mm;i++)if(i!=r&&M[i][c]){int f=M[i][c];for(int j=0;j<=n;j++)M[i][j]=((M[i][j]-f*M[r][j])%p+p)%p;}
    piv[r]=c;r++;}
  for(int i=r;i<mm;i++)if(M[i][n])return -1;
  if(!part)return n-r;
  int isp[4]={0};for(int i=0;i<r;i++)isp[piv[i]]=1;
  for(int j=0;j<n;j++)part[j]=0; for(int i=0;i<r;i++)part[piv[i]]=M[i][n];
  int d=0; for(int f=0;f<n;f++)if(!isp[f]){for(int j=0;j<n;j++)basis[d][j]=0;basis[d][f]=1;
    for(int i=0;i<r;i++)basis[d][piv[i]]=(p-M[i][f])%p; d++;}
  return d;}
static int detp(int p,int D[4][4]){int M[4][4];for(int i=0;i<n;i++)for(int j=0;j<n;j++)M[i][j]=D[i][j]%p;
  for(int c=0;c<n;c++){int s=-1;for(int i=c;i<n;i++)if(M[i][c]){s=i;break;} if(s<0)return 0;
    if(s!=c)for(int j=0;j<n;j++){int t=M[c][j];M[c][j]=M[s][j];M[s][j]=t;}
    int iv=(p==2)?1:inv13[M[c][c]]; for(int i=c+1;i<n;i++)if(M[i][c]){int f=M[i][c]*iv%p;for(int j=0;j<n;j++)M[i][j]=((M[i][j]-f*M[c][j])%p+p)%p;}}
  return 1;}
/* per-row solution sets (after dropping eq 'skip'), enumerated as full mod-26 rows */
static int rowsols(int m,int A[][4],int *b,int skip,int out[][4],int cap){
  int p2[4],B2[4][4],p13[4],B13[4][4]; int d2=solvep(2,m,A,b,skip,p2,B2); if(d2<0)return -1; int d13=solvep(13,m,A,b,skip,p13,B13); if(d13<0)return -1;
  long n2=1L<<d2,n13=1; for(int i=0;i<d13;i++)n13*=13; if(n2*n13>cap)return -2;
  int k=0; for(long a=0;a<n2;a++)for(long c=0;c<n13;c++){int x2[4],x13[4];for(int j=0;j<n;j++){x2[j]=p2[j];x13[j]=p13[j];}
    for(int t=0;t<d2;t++)if(a>>t&1)for(int j=0;j<n;j++)x2[j]^=B2[t][j];
    long cc=c;for(int t=0;t<d13;t++){int co=cc%13;cc/=13;for(int j=0;j<n;j++)x13[j]=(x13[j]+co*B13[t][j])%13;}
    for(int j=0;j<n;j++)out[k][j]=(13*x2[j]+14*x13[j])%26; k++;}
  return k;}
int main(int ac,char**av){
  if(ac<8)return 1; n=atoi(av[7]); if(n<2||n>4)return 4;
  for(int i=1;i<13;i++)for(int j=1;j<13;j++)if(i*j%13==1)inv13[i]=j;
  if(getenv("THR"))THR=atof(getenv("THR")); if(getenv("COMBOCAP"))COMBOCAP=atol(getenv("COMBOCAP"));
  Q=malloc(456976*4);{FILE*f=fopen(getenv("QUAD")?getenv("QUAD"):"/home/box/kryptos_support_backup/quad.bin","rb");if(!f||fread(Q,4,456976,f)!=456976)return 2;fclose(f);}
  {int k=0;for(int i=21;i<=33;i++){ISCRIB[i]=1;cpos[k++]=i;}for(int i=63;i<=73;i++){ISCRIB[i]=1;cpos[k++]=i;}}
  const char*CT=av[1]; const char*lab=av[3]; long lo=atol(av[4]),hi=atol(av[5]),st=atol(av[6]);
  long np=1; short *bank=NULL; if(strcmp(av[2],"-")){FILE*f=fopen(av[2],"rb");fseek(f,0,2);np=ftell(f)/194;fseek(f,0,0);bank=malloc(np*194);if(fread(bank,194,np,f)!=(size_t)np)return 3;fclose(f);}
  if(hi>np)hi=np;
  long ninv=0,tests=0,nstrict=0,nblock=0,neq=0,nrep=0,nrepcfg=0,under=0,pairs=0; double gbest=-99; char gline[400]="";
  static int sols[4][4096][4];
  for(long q=lo;q<hi;q+=st)for(int dir=0;dir<(bank?2:1);dir++){
    int S[97]; if(bank){for(int i=0;i<97;i++)S[i]=bank[q*97+i]; if(dir){int T[97];for(int i=0;i<97;i++)T[S[i]]=i;memcpy(S,T,sizeof S);}} else for(int i=0;i<97;i++)S[i]=i;
    for(int ix=0;ix<(bank?2:1);ix++)for(int nu=0;nu<2;nu++){
      const char*N=NUMS[nu]; int idx[26]; for(int i=0;i<26;i++)idx[N[i]-'A']=i;
      int L[97],kp[97]; for(int i=0;i<97;i++)kp[i]=-1;
      if(ix==0){for(int i=0;i<97;i++)L[i]=idx[CT[S[i]]-'A']; for(int k=0;k<24;k++)kp[cpos[k]]=idx[CRIB[k]-'A'];}
      else{for(int i=0;i<97;i++)L[i]=idx[CT[i]-'A']; for(int k=0;k<24;k++)kp[S[cpos[k]]]=idx[CRIB[k]-'A'];}
      for(int o=0;o<n;o++){ tests++;
        int nb=(97-o)/n;
        int A[4][24][4],bb[4][24],eb[4][24],m[4]={0};  /* per row: equations, block id */
        int bl[24],nbl=0;
        for(int t=o;t<o+nb*n;t++)if(kp[t]>=0){int blk=(t-o)/n,bs=o+blk*n,r=(t-o)%n; int e=m[r]++;
          for(int j=0;j<n;j++)A[r][e][j]=L[bs+j]; bb[r][e]=kp[t]; eb[r][e]=blk;
          int f=0;for(int z=0;z<nbl;z++)if(bl[z]==blk)f=1; if(!f)bl[nbl++]=blk;}
        int sok[4],dok[4][24]; int allstrict=1;
        for(int r=0;r<n;r++){ sok[r]=(solvep(2,m[r],A[r],bb[r],-1,NULL,NULL)>=0)&&(solvep(13,m[r],A[r],bb[r],-1,NULL,NULL)>=0); if(!sok[r])allstrict=0;
          for(int e=0;e<m[r];e++) dok[r][e]= sok[r] ? 1 : ((solvep(2,m[r],A[r],bb[r],e,NULL,NULL)>=0)&&(solvep(13,m[r],A[r],bb[r],e,NULL,NULL)>=0)); }
        if(allstrict)nstrict++;
        { int bad=0,which=-1; for(int r=0;r<n;r++)if(!sok[r]){bad++;which=r;}
          if(bad==1){int f=0;for(int e=0;e<m[which];e++)if(dok[which][e])f=1; if(f)neq++;} }
        int anyblock=0,anyrep=0;
        for(int z=0;z<nbl;z++){int blk=bl[z]; int ok=1, skip[4];
          for(int r=0;r<n;r++){skip[r]=-1; for(int e=0;e<m[r];e++)if(eb[r][e]==blk)skip[r]=e;
            if(skip[r]>=0){ if(!dok[r][skip[r]]){ok=0;break;} } else if(!sok[r]){ok=0;break;} }
          if(!ok)continue; anyblock=1; pairs++;
          int ns[4]; long prod=1; int und=0;
          for(int r=0;r<n;r++){ns[r]=rowsols(m[r],A[r],bb[r],skip[r],sols[r],(int)COMBOCAP); if(ns[r]==-2){und=1;break;} if(ns[r]<0){und=-1;break;} prod*=ns[r]; if(prod>COMBOCAP){und=1;break;}}
          if(und==1){under++;continue;} if(und<0)continue;
          int bs=o+blk*n; double best=-99; char bpt[98]; bpt[97]=0; int brep=0,bj=-1,bv=-1;
          for(long c=0;c<prod;c++){long cc=c; int D[4][4]; for(int r=0;r<n;r++){int k=cc%ns[r];cc/=ns[r];for(int j=0;j<n;j++)D[r][j]=sols[r][k][j];}
            if(!detp(2,D)||!detp(13,D))continue; ninv++;
            /* one-letter repair of block blk */
            int nrp=0,rj=-1,rv=-1;
            for(int j=0;j<n;j++)for(int v=0;v<26;v++){ if(v==L[bs+j])continue; int good=1;
              for(int r=0;r<n&&good;r++){int t=bs+r; if(kp[t]<0)continue; int s=0; for(int jj=0;jj<n;jj++)s+=D[r][jj]*(jj==j?v:L[bs+jj]); if(s%26!=kp[t])good=0;}
              if(good){nrp++; if(rj<0){rj=j;rv=v;}}}
            if(!nrp)continue;
            int LL[97]; memcpy(LL,L,sizeof LL); LL[bs+rj]=rv;
            char out[97]; memset(out,0,97);
            for(int t=o;t<o+nb*n;t++){int b2=o+((t-o)/n)*n,r=(t-o)%n; int s=0; for(int j=0;j<n;j++)s+=D[r][j]*LL[b2+j]; out[t]=N[s%26];}
            char pt[97]; if(ix==0)memcpy(pt,out,97); else for(int p=0;p<97;p++)pt[p]=out[S[p]];
            double tot=0;int w=0; for(int i=0;i+4<=97;i++){int g=1,id=0;for(int zz=0;zz<4;zz++){char ch=pt[i+zz];if(!ch||ISCRIB[i+zz]){g=0;break;}id=id*26+ch-'A';} if(g){tot+=Q[id];w++;}}
            double sc=w>=20?tot/w:-99; nrep++; anyrep=1;
            if(sc>best){best=sc;brep=nrp;bj=rj;bv=rv;for(int i=0;i<97;i++)bpt[i]=pt[i]?pt[i]:'.';}
          }
          if(best<-90)continue;
          int carvedpos = (ix==0)? S[bs+bj] : bs+bj;
          char line[400]; snprintf(line,sizeof line,"S %s n=%d perm=%ld dir=%d ix=%d num=%d o=%d dropblk=%d fix@carved%d:%c->%c repairs=%d meanQ=%.3f %s",
            lab,n,q,dir,ix,nu,o,blk,carvedpos,CT[carvedpos],N[bv],brep,best,bpt);
          if(best>gbest){gbest=best;strcpy(gline,line);}
          if(best>THR){puts(line);fflush(stdout);}
        }
        if(anyblock)nblock++; if(anyrep)nrepcfg++;
      }}}
  printf("C %s n=%d tests=%ld strict=%ld eqdrop=%ld blockdrop=%ld blockpairs=%ld under=%ld invertible=%ld repair_solutions=%ld repair_configs=%ld best=%.3f range=%ld..%ld/%ld\n",
    lab,n,tests,nstrict,neq,nblock,pairs,under,ninv,nrep,nrepcfg,gbest,lo,hi,st);
  if(gline[0])printf("B %s\n",gline);
  return 0;}
