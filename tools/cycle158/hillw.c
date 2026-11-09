/* Cycle 158 (IDEAS I-056): key on BOTH sides of the Hill step, both keys VOCABULARY WORDS (phase 0 at the stream start).
   Encryption (one sign convention): x = p (+/-) e_word -> y_block = E.x_block (Hill n x n, blocks from offset o) -> L = y (+/-) f_word.
   Decoder relation used here, per crib position t (block start bs, row r):
       sum_j D[r][j] * (L[bs+j] + sf*F[(bs+j) mod k2])  ==  P[t] + se*E[t mod k1]   (mod 26),  D = E^-1 (unknown, n*n entries)
   sf, se in {+1,-1}; Beaufort on either side = D -> -D (D is free), so the 4 sign pairs cover all Vig/Beau/variant mixes.
   With both words fixed only D is unknown and the rows of D are independent. Exact test, CRT Z26 = Z2 x Z13: in each field and
   for each row, the crib vectors v_q = L+sf*F (n-vectors) have a left null space; every null vector lambda gives a necessary and
   (together) sufficient condition  sum lambda_q (P_q + se*E[t_q mod k1]) == 0.  Checks depend on (frame, f, sf) only; the e word is
   tested against them with early exit. Survivors (consistent mod 2 and mod 13 for every row) are printed; D invertibility,
   full decryption and scoring are done afterwards (solve158.py).
   Frames as hill2s.c (cycle 156): direct; bank model Q L[i]=CT[S[i]] (ix 0); carved order L=CT, crib at S[p] (ix 1); both bank
   directions; A-Z / KRYPTOS numbering (words mapped with the same numbering); every alignment o.
   DROP=1: also every crib-bearing block's equations dropped in turn (exact superset for one wrong carved or crib letter).
   VERB=1: per-(config,row,field) consistency counts for the independent recount.
   usage: hillw CT perms.bin|- label lo hi stride n fwords ewords */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const char *CRIB="EASTNORTHEASTBERLINCLOCK"; static int cpos[24];
static const char *NUMS[2]={"ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"};
#define MAXW 20000
#define KMAX 15
static int nw[2]; static char wtxt[2][MAXW][16]; static int wlen[2][MAXW];
static unsigned char wv[2][2][MAXW][16]; /* [list][nu][word][i] */
static int bylen[2][KMAX+1][MAXW], nbylen[2][KMAX+1];
static int n, DROP=0, VERB=0, EXP=1; static int L[97];
static int m, er[24], ebs[24], ep[24], et[24], use[24];
typedef struct { int p, row, C, nl; int lq[24], la[24]; int have[KMAX+1]; int coef[KMAX+1][KMAX]; } Chk;
static Chk ch[2][64]; static int nch[2]; static int inv13[13];
static long long cons[2][4], consall; static double expct;
static void loadw(int li,const char*fn){FILE*f=fopen(fn,"r"); char b[64]; nw[li]=0; while(fscanf(f,"%63s",b)==1){int k=strlen(b); if(k<1||k>KMAX)continue;
  strcpy(wtxt[li][nw[li]],b); wlen[li][nw[li]]=k; for(int nu=0;nu<2;nu++)for(int i=0;i<k;i++)wv[li][nu][nw[li]][i]=strchr(NUMS[nu],b[i])-NUMS[nu];
  bylen[li][k][nbylen[li][k]++]=nw[li]; nw[li]++;} fclose(f);}
static int V[24][4];
/* left null space per row in field p (fi 0 = mod 13, fi 1 = mod 2); coefficients per key length computed lazily */
static void build(int fi){ int p=fi?2:13; nch[fi]=0;
    for(int r=0;r<n;r++){ int idx[24],mr=0; for(int q=0;q<m;q++)if(use[q]&&er[q]==r)idx[mr++]=q;
      if(mr==0)continue; int M[24][4+24];
      for(int i=0;i<mr;i++){for(int j=0;j<n;j++)M[i][j]=V[idx[i]][j]%p; for(int j=0;j<mr;j++)M[i][n+j]=(i==j);}
      int rk=0; for(int c=0;c<n&&rk<mr;c++){int s=-1; for(int i=rk;i<mr;i++)if(M[i][c]){s=i;break;} if(s<0)continue;
        if(s!=rk)for(int j=0;j<n+mr;j++){int t=M[rk][j];M[rk][j]=M[s][j];M[s][j]=t;}
        int iv=p==2?1:inv13[M[rk][c]]; if(iv!=1)for(int j=0;j<n+mr;j++)M[rk][j]=M[rk][j]*iv%p;
        for(int i=0;i<mr;i++)if(i!=rk&&M[i][c]){int fct=M[i][c]; for(int j=0;j<n+mr;j++)M[i][j]=(M[i][j]+(p-fct)*M[rk][j])%p;}
        rk++;}
      for(int i=rk;i<mr;i++){ Chk*c=&ch[fi][nch[fi]++]; c->p=p; c->row=r; c->C=0; c->nl=0; memset(c->have,0,sizeof c->have);
        for(int j=0;j<mr;j++){int la=M[i][n+j]; if(!la)continue; int q=idx[j]; c->C=(c->C+la*ep[q])%p; c->lq[c->nl]=et[q]; c->la[c->nl++]=la;}}
    }}
static inline const int* coefk(Chk*c,int k){ if(!c->have[k]){ int*cf=c->coef[k]; for(int s=0;s<k;s++)cf[s]=0;
    for(int i=0;i<c->nl;i++)cf[c->lq[i]%k]+=c->la[i]; for(int s=0;s<k;s++)cf[s]%=c->p; c->have[k]=1;} return c->coef[k];}
/* returns surviving sign mask (bit0 se=+1, bit1 se=-1) for word E of length k against checks of field fi (optionally only row r) */
static inline int testw(int fi,int k,const unsigned char*E,int mask,int r){
  for(int i=0;i<nch[fi]&&mask;i++){Chk*c=&ch[fi][i]; if(r>=0&&c->row!=r)continue; int p=c->p; const int*cf=coefk(c,k); int v=0; for(int s=0;s<k;s++)v+=cf[s]*E[s];
    if((mask&1)&&(c->C+v)%p)mask&=~1; if((mask&2)&&((c->C-v)%p+p)%p)mask&=~2;}
  return mask;}
int main(int ac,char**av){
  if(ac<10)return 1; n=atoi(av[7]); for(int i=1;i<13;i++)for(int j=1;j<13;j++)if(i*j%13==1)inv13[i]=j;
  if(getenv("DROP"))DROP=atoi(getenv("DROP")); if(getenv("VERB"))VERB=atoi(getenv("VERB")); if(getenv("EXP"))EXP=atoi(getenv("EXP"));
  loadw(0,av[8]); loadw(1,av[9]);
  {int k=0;for(int i=21;i<=33;i++)cpos[k++]=i;for(int i=63;i<=73;i++)cpos[k++]=i;}
  const char*CT=av[1]; const char*lab=av[3]; long lo=atol(av[4]),hi=atol(av[5]),st=atol(av[6]);
  long np=1; short *bank=NULL; if(strcmp(av[2],"-")){FILE*f=fopen(av[2],"rb");fseek(f,0,2);np=ftell(f)/194;fseek(f,0,0);bank=malloc(np*194);if(fread(bank,194,np,f)!=(size_t)np)return 3;fclose(f);}
  if(hi>np)hi=np;
  long long frames=0, fsets=0, etests=0, surv=0, xsurv=0;
  for(long q0=lo;q0<hi;q0+=st)for(int dir=0;dir<(bank?2:1);dir++){
    int S[97]; if(bank){for(int i=0;i<97;i++)S[i]=bank[q0*97+i]; if(dir){int T[97];for(int i=0;i<97;i++)T[S[i]]=i;memcpy(S,T,sizeof S);}} else for(int i=0;i<97;i++)S[i]=i;
    for(int ix=0;ix<(bank?2:1);ix++)for(int nu=0;nu<2;nu++){
      const char*N=NUMS[nu]; int idx[26]; for(int i=0;i<26;i++)idx[N[i]-'A']=i; int kp[97]; for(int i=0;i<97;i++)kp[i]=-1;
      if(ix==0){for(int i=0;i<97;i++)L[i]=idx[CT[S[i]]-'A']; for(int k=0;k<24;k++)kp[cpos[k]]=idx[CRIB[k]-'A'];}
      else{for(int i=0;i<97;i++)L[i]=idx[CT[i]-'A']; for(int k=0;k<24;k++)kp[S[cpos[k]]]=idx[CRIB[k]-'A'];}
      for(int o=0;o<n;o++){ frames++;
        int nb=(97-o)/n; m=0; for(int t=o;t<o+nb*n;t++)if(kp[t]>=0){er[m]=(t-o)%n; ebs[m]=o+((t-o)/n)*n; ep[m]=kp[t]; et[m]=t; m++;}
        int nblk=0, blk[24]; for(int e=0;e<m;e++){int f=0;for(int i=0;i<nblk;i++)if(blk[i]==ebs[e])f=1; if(!f)blk[nblk++]=ebs[e];}
        for(int fw=0;fw<nw[0];fw++)for(int sfi=0;sfi<2;sfi++){ int sf=sfi?25:1; int k2=wlen[0][fw]; const unsigned char*F=wv[0][nu][fw];
          for(int q=0;q<m;q++)for(int j=0;j<n;j++){int pos=ebs[q]+j; V[q][j]=(L[pos]+sf*F[pos%k2])%26;}
          for(int pass=-1;pass<(DROP?nblk:0);pass++){
            for(int q=0;q<m;q++)use[q]=(pass<0||ebs[q]!=blk[pass]);
            build(0); int built2=0; fsets++;
            if(pass<0&&(EXP||VERB)){build(1); built2=1; int c2=nch[1],c13=nch[0]; double pr=1; for(int i=0;i<c2;i++)pr/=2; for(int i=0;i<c13;i++)pr/=13; expct+=2.0*nw[1]*pr;}
            for(int k=1;k<=KMAX;k++){ int nk=nbylen[1][k]; if(!nk)continue;
              for(int wi=0;wi<nk;wi++){ int ew=bylen[1][k][wi]; const unsigned char*E=wv[1][nu][ew]; etests+=2;
                if(VERB&&pass<0){ for(int sei=0;sei<2;sei++){int okall=1; for(int fi=0;fi<2;fi++)for(int r=0;r<n;r++){
                    if(testw(fi,k,E,1<<sei,r))cons[fi][r]++; else okall=0;} if(okall)consall++;}}
                int mask=testw(0,k,E,3,-1); if(!mask)continue;
                if(!built2){build(1); built2=1;}
                mask=testw(1,k,E,mask,-1);
                for(int sei=0;sei<2;sei++)if(mask&(1<<sei)){ if(pass<0)surv++; else xsurv++;
                  printf("%s %s n=%d perm=%ld dir=%d ix=%d nu=%d o=%d drop=%d f=%s sf=%d e=%s se=%d\n",pass<0?"S":"X",lab,n,bank?q0:-1,dir,ix,nu,o,pass<0?-1:blk[pass],wtxt[0][fw],sfi?-1:1,wtxt[1][ew],sei?-1:1); fflush(stdout);}
              }}
          }}
      }}}
  printf("C %s n=%d frames=%lld fsets=%lld etests=%lld survivors=%lld drop_survivors=%lld expected_chance_strict=%.3e range=%ld..%ld/%ld drop=%d words=%d,%d\n",lab,n,frames,fsets,etests,surv,xsurv,expct,lo,hi,st,DROP,nw[0],nw[1]);
  if(VERB)printf("VC %s n=%d cons13=%lld,%lld,%lld,%lld cons2=%lld,%lld,%lld,%lld all=%lld\n",lab,n,cons[0][0],cons[0][1],cons[0][2],cons[0][3],cons[1][0],cons[1][1],cons[1][2],cons[1][3],consall);
  return 0;}
