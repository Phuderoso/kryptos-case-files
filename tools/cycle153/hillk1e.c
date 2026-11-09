/* Cycle 153: Hill n x n (n = 2..5) + optional additive key of period k (k = 0: plain Hill) under ONE carving error, exact.
   Decoder (frames of cycles 141/144/151): ix=0 (model Q): L[i]=CT[S[i]], pt=out; ix=1 (carved order): L=CT, pt[p]=out[S[p]].
     out[t] = sum_j D[r][j]*L[bs+j] + e[t mod k]  (mod 26),  bs = block start for alignment o, r = t-bs.
   All n*n + (#key residues hit by cribs) unknowns are handled JOINTLY, exactly, mod 2 and mod 13 (CRT).
   A wrong carved letter (substitution) sits in exactly ONE Hill block of L, so it can only break that block's crib equations.
   Method (no enumeration on the consistency side):
     1. Reduce [A | b | I] once per configuration and field -> left-null-space H and syndrome s (strict consistent iff s = 0).
     2. Block screen: dropping the equation set E of block B is consistent iff s lies in span(H[:,E]) (both fields).
        Equation screen (one wrong crib letter): same with E = {e}.
     3. Exact one-letter repair of block B: solve the system without E -> x = x0 + N y. Replacing carved letter j of B by
        L[bs+j]+delta (delta 1..25) changes each equation t in E to a_t.x + delta*D[r_t][j] = b_t, which is LINEAR in y.
        Check that small system mod 2 and mod 13 for every (j, delta). Consistent -> repair_cons. Its solution set is then
        enumerated (<= COMBOCAP) for invertible D (repair_inv), decrypted with the repaired letter and quadgram-scored;
        larger sets are counted as repair_under (blind spot: consistent but not decoded).
     4. One wrong crib letter: for each passing single equation e, the solution set without e is enumerated (<= COMBOCAP)
        for invertible D (eq_inv) and scored; larger sets -> eq_under.
   usage: hillk1e CT perms.bin|- label lo hi stride n k       env THR (-5.0), COMBOCAP (4096), QUAD */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MU 40
#define ME 24
static float *Q; static int ISCRIB[97]; static const char *CRIB="EASTNORTHEASTBERLINCLOCK";
static int cpos[24]; static double THR=-5.0; static long COMBOCAP=4096; static int n,K,U;
static const char *NUMS[2]={"ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"};
static int inv13[13];
static inline int md(int a,int p){a%=p;return a<0?a+p:a;}
static inline int ivp(int a,int p){return p==2?1:inv13[a];}
/* generic: solve M (rows x cols, augmented col = cols) mod p. returns -1 or nullity; part[cols], basis[d][cols] */
static int gsolve(int p,int rows,int cols,int M[][MU+1],int *part,int basis[][MU]){
  int piv[MU],r=0; for(int c=0;c<cols&&r<rows;c++){int s=-1;for(int i=r;i<rows;i++)if(M[i][c]){s=i;break;} if(s<0)continue;
    if(s!=r)for(int j=0;j<=cols;j++){int t=M[r][j];M[r][j]=M[s][j];M[s][j]=t;}
    int iv=ivp(M[r][c],p); for(int j=0;j<=cols;j++)M[r][j]=M[r][j]*iv%p;
    for(int i=0;i<rows;i++)if(i!=r&&M[i][c]){int f=M[i][c];for(int j=0;j<=cols;j++)M[i][j]=md(M[i][j]-f*M[r][j],p);}
    piv[r]=c;r++;}
  for(int i=r;i<rows;i++)if(M[i][cols])return -1;
  if(!part)return cols-r;
  int isp[MU]={0};for(int i=0;i<r;i++)isp[piv[i]]=1;
  for(int j=0;j<cols;j++)part[j]=0; for(int i=0;i<r;i++)part[piv[i]]=M[i][cols];
  int d=0; for(int f=0;f<cols;f++)if(!isp[f]){for(int j=0;j<cols;j++)basis[d][j]=0;basis[d][f]=1;
    for(int i=0;i<r;i++)basis[d][piv[i]]=md(-M[i][f],p); d++;}
  return d;}
static int detp(int p,int D[5][5]){int M[5][5];for(int i=0;i<n;i++)for(int j=0;j<n;j++)M[i][j]=D[i][j]%p;
  for(int c=0;c<n;c++){int s=-1;for(int i=c;i<n;i++)if(M[i][c]){s=i;break;} if(s<0)return 0;
    if(s!=c)for(int j=0;j<n;j++){int t=M[c][j];M[c][j]=M[s][j];M[s][j]=t;}
    int iv=ivp(M[c][c],p); for(int i=c+1;i<n;i++)if(M[i][c]){int f=M[i][c]*iv%p;for(int j=0;j<n;j++)M[i][j]=md(M[i][j]-f*M[c][j],p);}}
  return 1;}
/* syndrome: H (h x m), s (h) for A x = b mod p */
static int syndrome(int p,int m,int A[][MU],int *b,int H[][ME],int *s){
  static int M[ME][MU+1+ME]; int W=U+1+m;
  for(int i=0;i<m;i++){for(int j=0;j<U;j++)M[i][j]=md(A[i][j],p); M[i][U]=md(b[i],p); for(int j=0;j<m;j++)M[i][U+1+j]=(i==j);}
  int r=0; for(int c=0;c<U&&r<m;c++){int q=-1;for(int i=r;i<m;i++)if(M[i][c]){q=i;break;} if(q<0)continue;
    if(q!=r)for(int j=0;j<W;j++){int t=M[r][j];M[r][j]=M[q][j];M[q][j]=t;}
    int iv=ivp(M[r][c],p); for(int j=0;j<W;j++)M[r][j]=M[r][j]*iv%p;
    for(int i=0;i<m;i++)if(i!=r&&M[i][c]){int f=M[i][c];for(int j=0;j<W;j++)M[i][j]=md(M[i][j]-f*M[r][j],p);}
    r++;}
  int h=0; for(int i=r;i<m;i++){for(int j=0;j<m;j++)H[h][j]=M[i][U+1+j]; s[h]=M[i][U]; h++;}
  return h;}
/* is s in span of H[:,E]? */
static int inspan(int p,int h,int H[][ME],int *s,int ne,int *E){
  if(h==0)return 1; int M[ME][MU+1]; for(int i=0;i<h;i++){for(int z=0;z<ne;z++)M[i][z]=H[i][E[z]]; M[i][ne]=s[i];}
  return gsolve(p,h,ne,M,NULL,NULL)>=0;}
/* solve system without equations in mask drop[] */
static int masked(int p,int m,int A[][MU],int *b,const int *drop,int *part,int basis[][MU]){
  int M[ME][MU+1],mm=0; for(int i=0;i<m;i++){if(drop[i])continue;for(int j=0;j<U;j++)M[mm][j]=md(A[i][j],p);M[mm][U]=md(b[i],p);mm++;}
  return gsolve(p,mm,U,M,part,basis);}
static int ptpos(int ix,const int*S,int t){if(ix==0)return t; for(int p=0;p<97;p++)if(S[p]==t)return p; return -1;}
static double score(const char*pt){double tot=0;int w=0; for(int i=0;i+4<=97;i++){int g=1,id=0;for(int z=0;z<4;z++){char ch=pt[i+z];if(!ch||ISCRIB[i+z]){g=0;break;}id=id*26+ch-'A';} if(g){tot+=Q[id];w++;}} return w>=20?tot/w:-99;}
int main(int ac,char**av){
  if(ac<9)return 1; n=atoi(av[7]); K=atoi(av[8]); if(n<2||n>5||n*n+K>MU)return 4;
  for(int i=1;i<13;i++)for(int j=1;j<13;j++)if(i*j%13==1)inv13[i]=j;
  if(getenv("THR"))THR=atof(getenv("THR")); if(getenv("COMBOCAP"))COMBOCAP=atol(getenv("COMBOCAP"));
  Q=malloc(456976*4);{FILE*f=fopen(getenv("QUAD")?getenv("QUAD"):"/home/box/kryptos_support_backup/quad.bin","rb");if(!f||fread(Q,4,456976,f)!=456976)return 2;fclose(f);}
  {int k=0;for(int i=21;i<=33;i++){ISCRIB[i]=1;cpos[k++]=i;}for(int i=63;i<=73;i++){ISCRIB[i]=1;cpos[k++]=i;}}
  const char*CT=av[1]; const char*lab=av[3]; long lo=atol(av[4]),hi=atol(av[5]),st=atol(av[6]);
  long np=1; short *bank=NULL; if(strcmp(av[2],"-")){FILE*f=fopen(av[2],"rb");fseek(f,0,2);np=ftell(f)/194;fseek(f,0,0);bank=malloc(np*194);if(fread(bank,194,np,f)!=(size_t)np)return 3;fclose(f);}
  if(hi>np)hi=np;
  long tests=0,nstrict=0,neqcfg=0,neqinv=0,nequnder=0,nblkcfg=0,pairs=0,rcons=0,rconscfg=0,rinv=0,rinvcfg=0,runder=0;
  double gbest=-99,ebest=-99; char gline[700]="",eline[700]="";
  for(long q=lo;q<hi;q+=st)for(int dir=0;dir<(bank?2:1);dir++){
    int S[97]; if(bank){for(int i=0;i<97;i++)S[i]=bank[q*97+i]; if(dir){int T[97];for(int i=0;i<97;i++)T[S[i]]=i;memcpy(S,T,sizeof S);}} else for(int i=0;i<97;i++)S[i]=i;
    for(int ix=0;ix<(bank?2:1);ix++)for(int nu=0;nu<2;nu++){
      const char*N=NUMS[nu]; int idx[26]; for(int i=0;i<26;i++)idx[N[i]-'A']=i;
      int L[97],kp[97]; for(int i=0;i<97;i++)kp[i]=-1;
      if(ix==0){for(int i=0;i<97;i++)L[i]=idx[CT[S[i]]-'A']; for(int k=0;k<24;k++)kp[cpos[k]]=idx[CRIB[k]-'A'];}
      else{for(int i=0;i<97;i++)L[i]=idx[CT[i]-'A']; for(int k=0;k<24;k++)kp[S[cpos[k]]]=idx[CRIB[k]-'A'];}
      for(int o=0;o<n;o++){ tests++;
        int nb=(97-o)/n; int col[24]; int nc=0;
        if(K>0){int hit[24]={0}; for(int t=o;t<o+nb*n;t++)if(kp[t]>=0)hit[t%K]=1; for(int s=0;s<K;s++)col[s]=hit[s]?nc++:-1;}
        U=n*n+nc;
        int A[ME][MU],b[ME],eb[ME],et[ME],m=0;
        for(int t=o;t<o+nb*n;t++)if(kp[t]>=0){int blk=(t-o)/n,bs=o+blk*n,r=(t-o)%n; memset(A[m],0,sizeof A[m]);
          for(int j=0;j<n;j++)A[m][r*n+j]=L[bs+j]; if(K>0)A[m][n*n+col[t%K]]=1; b[m]=kp[t]; eb[m]=blk; et[m]=t; m++;}
        int H2[ME][ME],s2[ME],H13[ME][ME],s13[ME];
        int h13=syndrome(13,m,A,b,H13,s13); int z13=1; for(int i=0;i<h13;i++)if(s13[i])z13=0;
        if(!z13){ /* fast exit: no block (hence no single equation) can be dropped consistently mod 13 */
          int any=0; for(int i=0;i<m&&!any;i++){int E[ME],ne=0; if(i>0&&eb[i]==eb[i-1])continue; for(int z=0;z<m;z++)if(eb[z]==eb[i])E[ne++]=z;
            if(inspan(13,h13,H13,s13,ne,E))any=1;}
          if(!any)continue; }
        int h2=syndrome(2,m,A,b,H2,s2); int z2=1; for(int i=0;i<h2;i++)if(s2[i])z2=0;
        if(z2&&z13){nstrict++;continue;}   /* strict-consistent configs were covered by cycles 141/144 */
        /* one wrong crib letter */
        int anyeq=0;
        for(int e=0;e<m;e++){int E[1]={e}; if(!inspan(2,h2,H2,s2,1,E)||!inspan(13,h13,H13,s13,1,E))continue; anyeq=1;
          int drop[ME]={0}; drop[e]=1; int p2[MU],B2[MU][MU],p13[MU],B13[MU][MU];
          int d2=masked(2,m,A,b,drop,p2,B2), d13=masked(13,m,A,b,drop,p13,B13); if(d2<0||d13<0)continue;
          double cnt=1; for(int i=0;i<d2;i++)cnt*=2; for(int i=0;i<d13;i++)cnt*=13; if(cnt>COMBOCAP){nequnder++;continue;}
          for(long a=0;a<(1L<<d2);a++){long n13=(long)(cnt/(1L<<d2)); for(long c=0;c<n13;c++){int x2[MU],x13[MU],x[MU];
            for(int j=0;j<U;j++){x2[j]=p2[j];x13[j]=p13[j];}
            for(int t=0;t<d2;t++)if(a>>t&1)for(int j=0;j<U;j++)x2[j]^=B2[t][j];
            long cc=c;for(int t=0;t<d13;t++){int co=cc%13;cc/=13;for(int j=0;j<U;j++)x13[j]=(x13[j]+co*B13[t][j])%13;}
            for(int j=0;j<U;j++)x[j]=(13*x2[j]+14*x13[j])%26;
            int D[5][5]; for(int r=0;r<n;r++)for(int j=0;j<n;j++)D[r][j]=x[r*n+j]; if(!detp(2,D)||!detp(13,D))continue; neqinv++;
            char out[97]; memset(out,0,97);
            for(int t=o;t<o+nb*n;t++){if(K>0&&col[t%K]<0)continue; int bs=o+((t-o)/n)*n,r=(t-o)%n; int sm=K>0?x[n*n+col[t%K]]:0; for(int j=0;j<n;j++)sm+=D[r][j]*L[bs+j]; out[t]=N[sm%26];}
            char pt[97]; if(ix==0)memcpy(pt,out,97); else for(int pp=0;pp<97;pp++)pt[pp]=out[S[pp]];
            double sc=score(pt); if(sc>ebest){ebest=sc; char bp[98];for(int i=0;i<97;i++)bp[i]=pt[i]?pt[i]:'.';bp[97]=0;
              snprintf(eline,sizeof eline,"E %s n=%d k=%d perm=%ld dir=%d ix=%d num=%d o=%d dropcrib_pt=%d meanQ=%.3f %s",lab,n,K,q,dir,ix,nu,o,ptpos(ix,S,et[e]),sc,bp);}
            if(sc>THR){printf("E %s n=%d k=%d perm=%ld dir=%d ix=%d num=%d o=%d dropeq=%d meanQ=%.3f\n",lab,n,K,q,dir,ix,nu,o,e,sc);fflush(stdout);}
          }}}
        if(anyeq)neqcfg++;
        /* one wrong carved letter: block drop + exact repair */
        int blks[ME],nbl=0; for(int i=0;i<m;i++){int f=0;for(int z=0;z<nbl;z++)if(blks[z]==eb[i])f=1; if(!f)blks[nbl++]=eb[i];}
        int anyblk=0,anyrc=0,anyri=0;
        for(int zb=0;zb<nbl;zb++){int blk=blks[zb],bs=o+blk*n; int E[ME],ne=0,drop[ME]={0}; for(int i=0;i<m;i++)if(eb[i]==blk){E[ne++]=i;drop[i]=1;}
          if(!inspan(2,h2,H2,s2,ne,E)||!inspan(13,h13,H13,s13,ne,E))continue; anyblk=1; pairs++;
          int p2[MU],B2[MU][MU],p13[MU],B13[MU][MU];
          int d2=masked(2,m,A,b,drop,p2,B2), d13=masked(13,m,A,b,drop,p13,B13); if(d2<0||d13<0)continue;
          for(int j=0;j<n;j++)for(int dl=1;dl<26;dl++){
            /* small systems in y: for t in E: sum_i y_i (a'_t . N_i) = b_t - a'_t . x0, a'_t = a_t + dl*unit(r_t*n+j) */
            int y2p[MU],Y2[MU][MU],y13p[MU],Y13[MU][MU],e2,e13;
            {int M[ME][MU+1]; for(int z=0;z<ne;z++){int i=E[z],r=(et[i]-o)%n,cidx=r*n+j; int ap[MU]; for(int u=0;u<U;u++)ap[u]=A[i][u]; ap[cidx]+=dl;
               for(int d=0;d<d2;d++){int sm=0;for(int u=0;u<U;u++)sm+=ap[u]*B2[d][u]; M[z][d]=sm&1;}
               {int sm=0;for(int u=0;u<U;u++)sm+=ap[u]*p2[u]; M[z][d2]=md(b[i]-sm,2);} }
             e2=gsolve(2,ne,d2,M,y2p,Y2);} if(e2<0)continue;
            {int M[ME][MU+1]; for(int z=0;z<ne;z++){int i=E[z],r=(et[i]-o)%n,cidx=r*n+j; int ap[MU]; for(int u=0;u<U;u++)ap[u]=A[i][u]; ap[cidx]+=dl;
               for(int d=0;d<d13;d++){int sm=0;for(int u=0;u<U;u++)sm+=ap[u]*B13[d][u]; M[z][d]=sm%13;}
               {int sm=0;for(int u=0;u<U;u++)sm+=ap[u]*p13[u]; M[z][d13]=md(b[i]-sm,13);} }
             e13=gsolve(13,ne,d13,M,y13p,Y13);} if(e13<0)continue;
            rcons++; anyrc=1;
            double cnt=1; for(int i=0;i<e2;i++)cnt*=2; for(int i=0;i<e13;i++)cnt*=13; if(cnt>COMBOCAP){runder++;continue;}
            int LL[97]; memcpy(LL,L,sizeof LL); LL[bs+j]=(L[bs+j]+dl)%26;
            long n2=1L<<e2,n13=(long)(cnt/n2);
            for(long a=0;a<n2;a++)for(long c=0;c<n13;c++){int y2[MU],y13[MU],x2[MU],x13[MU],x[MU];
              for(int d=0;d<d2;d++)y2[d]=y2p[d]; for(int t=0;t<e2;t++)if(a>>t&1)for(int d=0;d<d2;d++)y2[d]^=Y2[t][d];
              for(int d=0;d<d13;d++)y13[d]=y13p[d]; long cc=c; for(int t=0;t<e13;t++){int co=cc%13;cc/=13;for(int d=0;d<d13;d++)y13[d]=(y13[d]+co*Y13[t][d])%13;}
              for(int u=0;u<U;u++){int v2=p2[u],v13=p13[u]; for(int d=0;d<d2;d++)if(y2[d])v2^=B2[d][u]; for(int d=0;d<d13;d++)v13+=y13[d]*B13[d][u]; x2[u]=v2&1; x13[u]=v13%13; x[u]=(13*x2[u]+14*x13[u])%26;}
              int D[5][5]; for(int r=0;r<n;r++)for(int jj=0;jj<n;jj++)D[r][jj]=x[r*n+jj]; if(!detp(2,D)||!detp(13,D))continue;
              rinv++; anyri=1;
              char out[97]; memset(out,0,97);
              for(int t=o;t<o+nb*n;t++){if(K>0&&col[t%K]<0)continue; int b2=o+((t-o)/n)*n,r=(t-o)%n; int sm=K>0?x[n*n+col[t%K]]:0; for(int jj=0;jj<n;jj++)sm+=D[r][jj]*LL[b2+jj]; out[t]=N[sm%26];}
              char pt[97]; if(ix==0)memcpy(pt,out,97); else for(int pp=0;pp<97;pp++)pt[pp]=out[S[pp]];
              double sc=score(pt); int carved=(ix==0)?S[bs+j]:bs+j;
              if(sc>gbest||sc>THR){char bp[98];for(int i=0;i<97;i++)bp[i]=pt[i]?pt[i]:'.';bp[97]=0; char Ds[200]="";int w=0;
                for(int r=0;r<n;r++)for(int jj=0;jj<n;jj++)w+=sprintf(Ds+w,"%d%c",D[r][jj],(r==n-1&&jj==n-1)?' ':',');
                char es[100]="";int w2=0; for(int s=0;s<K;s++)w2+=sprintf(es+w2,"%d%c",col[s]<0?-1:x[n*n+col[s]],s==K-1?' ':',');
                char line[700]; snprintf(line,sizeof line,"S %s n=%d k=%d perm=%ld dir=%d ix=%d num=%d o=%d dropblk=%d fix@carved%d:%c->%c D=%s e=%s meanQ=%.3f %s",
                  lab,n,K,q,dir,ix,nu,o,blk,carved,CT[carved],N[LL[bs+j]],Ds,K?es:"-",sc,bp);
                if(sc>gbest){gbest=sc;strcpy(gline,line);} if(sc>THR){puts(line);fflush(stdout);}}
            }
          }
        }
        if(anyblk)nblkcfg++; if(anyrc)rconscfg++; if(anyri)rinvcfg++;
      }}}
  printf("C %s n=%d k=%d tests=%ld strict=%ld eqdrop_cfg=%ld eq_inv=%ld eq_under=%ld blockdrop_cfg=%ld blockpairs=%ld repair_cons=%ld repair_cons_cfg=%ld repair_inv=%ld repair_inv_cfg=%ld repair_under=%ld best=%.3f eqbest=%.3f range=%ld..%ld/%ld\n",
    lab,n,K,tests,nstrict,neqcfg,neqinv,nequnder,nblkcfg,pairs,rcons,rconscfg,rinv,rinvcfg,runder,gbest,ebest,lo,hi,st);
  if(gline[0])printf("B %s\n",gline); if(eline[0])printf("%s\n",eline);
  return 0;}
