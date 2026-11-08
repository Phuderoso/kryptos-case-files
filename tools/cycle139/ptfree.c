/* Cycle 139: plaintext-fed autokey with a FREE plaintext alphabet x, tested only on
   crib-to-crib links (the key letter p_{j-L} is itself a crib letter), so the primer
   never matters and no letter outside the cribs is needed.
     Vigenere: y(c_j) = x(p_j) + z(p_{j-L})   (Beaufort = same test under x -> -x)
     variant : y(c_j) = x(p_j) - z(p_{j-L})
   y = keyed cipher alphabet (word), z in {y, A-Z, KRYPTOS} (x computed outright and checked
   for permutation consistency) or z = x (two-variable equations mod 26, exact solver with
   all-different backtracking).  Layer order: ix=0 model Q (autokey on plaintext order, then
   transposition), ix=1 carved (transposition first, autokey on the carved order).
   usage: ptfree CT words.txt perms.bin label lo hi [pstride]  (env MINCHK, default 5) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
#define MAXW 10100
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PT="EASTNORTHEASTBERLINCLOCK";
static char W[MAXW][32]; static unsigned char INV[MAXW][26]; static unsigned char AZI[26],KRI[26];
static int Plet[24],C[N],MINCHK=5;
int md(int v){v%=26;return v<0?v+26:v;}
static void keyed(const char*w,unsigned char*inv){int u[26]={0},n=0;unsigned char al[26];
 for(const char*p=w;*p;p++){int c=*p-'A';if(c<0||c>25||u[c])continue;u[c]=1;al[n++]=c;}
 for(int c=0;c<26;c++)if(!u[c])al[n++]=c;for(int i=0;i<26;i++)inv[al[i]]=i;}
/* two-variable solver (as cycle 138): edges a=p letter, b=key letter, k=y(c) */
static int ea[24],eb[24],ek[24],ne,form,nodd,neven; static double MINBITS=23.5;
static int sgn[26],off[26],comp[26],ncomp; static unsigned int cmask[26]; static int cverts[26][26],cn[26];
static unsigned int solmask(int coef,int rhs){unsigned int m=0;for(int r=0;r<26;r++)if(md(coef*r)==md(rhs))m|=1u<<r;return m;}
static int bt(int ci,unsigned int used){ if(ci==ncomp)return 1;
  for(int r=0;r<26;r++){ if(!(cmask[ci]>>r&1))continue; unsigned int u=used; int ok=1;
    for(int q=0;q<cn[ci];q++){int v=cverts[ci][q];int val=md(sgn[v]*r+off[v]);if(u>>val&1){ok=0;break;}u|=1u<<val;}
    if(ok&&bt(ci+1,u))return 1;} return 0;}
/* form 0: y = x(a)+x(b); form 1: y = x(a)-x(b) */
static int solve(void){
  int adj[26][48],na[26]; memset(na,0,sizeof na);
  for(int e=0;e<ne;e++){adj[ea[e]][na[ea[e]]++]=e; if(eb[e]!=ea[e]) adj[eb[e]][na[eb[e]]++]=e;}
  for(int v=0;v<26;v++)comp[v]=-1; ncomp=0;
  for(int s=0;s<26;s++){ if(!na[s]||comp[s]>=0)continue; int ci=ncomp++; cn[ci]=0; cmask[ci]=0x3ffffff;
    int stk[26],sp=0; comp[s]=ci;sgn[s]=1;off[s]=0;stk[sp++]=s;cverts[ci][cn[ci]++]=s;
    while(sp){int u=stk[--sp];
      for(int q=0;q<na[u];q++){int e=adj[u][q];int a=ea[e],b=eb[e],k=ek[e];int o=(u==a)?b:a;
        if(comp[o]<0){ if(form==0){sgn[o]=-sgn[u];off[o]=md(k-off[u]);}
          else{ if(u==a){sgn[o]=sgn[u];off[o]=md(off[u]-k);} else {sgn[o]=sgn[u];off[o]=md(off[u]+k);} }
          comp[o]=ci;stk[sp++]=o;cverts[ci][cn[ci]++]=o;}}}}
  nodd=neven=0;
  for(int e=0;e<ne;e++){int a=ea[e],b=eb[e],k=ek[e],ci=comp[a];int coef,rhs;
    if(form==0){coef=sgn[a]+sgn[b];rhs=k-off[a]-off[b];} else {coef=sgn[a]-sgn[b];rhs=k-off[a]+off[b];}
    if(md(coef)==0){} else nodd++;
    cmask[ci]&=solmask(coef,rhs); if(!cmask[ci])return 0;}
  return bt(0,0);}
int main(int argc,char**argv){
  if(argc<7){fprintf(stderr,"usage\n");return 1;}
  for(int i=0;i<N;i++)C[i]=argv[1][i]-'A'; const char*lab=argv[4];
  long lo=atol(argv[5]),hi=atol(argv[6]),pst=argc>7?atol(argv[7]):1;
  if(getenv("MINCHK"))MINCHK=atoi(getenv("MINCHK")); if(getenv("MINBITS"))MINBITS=atof(getenv("MINBITS"));
  FILE*wf=fopen(argv[2],"r");int nw=0;while(nw<MAXW&&fscanf(wf,"%31s",W[nw])==1){keyed(W[nw],INV[nw]);nw++;}fclose(wf);if(hi>nw)hi=nw;
  keyed("A",AZI);keyed("KRYPTOS",KRI);
  for(int t=0;t<24;t++)Plet[t]=PT[t]-'A';
  long np=1; short*Perm;
  if(strcmp(argv[3],"-")){FILE*pf=fopen(argv[3],"rb");fseek(pf,0,SEEK_END);np=ftell(pf)/(2*N);rewind(pf);
    Perm=malloc((size_t)np*N*2);if(fread(Perm,2,(size_t)np*N,pf)!=(size_t)np*N)return 1;fclose(pf);}
  else{Perm=malloc(N*2);for(int i=0;i<N;i++)Perm[i]=i;}
  long long tests=0,hits=0; long npu=0;
  for(long q=0;q<np;q+=pst){npu++;const short*s=Perm+q*N;short u[N];for(int i=0;i<N;i++)u[s[i]]=i;
   for(int dir=0;dir<(np>1?2:1);dir++){const short*S=dir?u:s;
    for(int ix=0;ix<(np>1?2:1);ix++){int layer[N],kp[24],at[N];
      for(int i=0;i<N;i++){layer[i]=ix?C[i]:C[S[i]];at[i]=-1;}
      for(int t=0;t<24;t++){kp[t]=ix?S[CI[t]]:CI[t];at[kp[t]]=t;}
      for(int L=1;L<N;L++){
        int pa[24],pb[24],cc[24],m=0;
        for(int t=0;t<24;t++){int j=kp[t];if(j<L)continue;int t2=at[j-L];if(t2<0)continue;pa[m]=Plet[t];pb[m]=Plet[t2];cc[m]=layer[j];m++;}
        if(m<MINCHK+1)continue;
        unsigned int lm=0;int dl=0;for(int e=0;e<m;e++)if(!(lm>>pa[e]&1)){lm|=1u<<pa[e];dl++;}
        int chk_known=m-dl;
        /* cycles for z=x */
        int par[26];for(int v=0;v<26;v++)par[v]=v; int vm=0,nvv=0,merges=0;
        for(int e=0;e<m;e++){int a=pa[e],b=pb[e];if(!(vm>>a&1)){vm|=1u<<a;nvv++;}if(!(vm>>b&1)){vm|=1u<<b;nvv++;}
          while(par[a]!=a)a=par[a];while(par[b]!=b)b=par[b];if(a!=b){par[a]=b;merges++;}}
        int chk_self=m-merges;
        for(long a=lo;a<hi;a++){const unsigned char*y=INV[a];
          for(int zm=0;zm<4;zm++){
            if(zm<3){ if(chk_known<MINCHK)continue; const unsigned char*z=zm==0?y:zm==1?AZI:KRI;
              for(form=0;form<2;form++){tests++; int val[26];for(int v=0;v<26;v++)val[v]=-1; unsigned int used=0;int ok=1;
                for(int e=0;e<m;e++){int xv=form==0?md(y[cc[e]]-z[pb[e]]):md(y[cc[e]]+z[pb[e]]);
                  if(val[pa[e]]<0){ if(used>>xv&1){ok=0;break;} val[pa[e]]=xv;used|=1u<<xv;} else if(val[pa[e]]!=xv){ok=0;break;}}
                if(ok){hits++;printf("S %s word=%s z=%s form=%s ix=%d L=%d perm=%ld dir=%d m=%d checks=%d\n",lab,W[a],zm==0?"y":zm==1?"AZ":"KRYPTOS",form?"variant":"vig",ix,L,q,dir,m,chk_known);}}
            } else { if(chk_self<MINCHK)continue;
              for(form=0;form<2;form++){tests++; ne=m;for(int e=0;e<m;e++){ea[e]=pa[e];eb[e]=pb[e];ek[e]=y[cc[e]];}
                if(solve()){ int ev=chk_self-nodd; double bits=ev*4.70+nodd*1.0; if(bits<MINBITS)continue; hits++;printf("S %s word=%s z=x form=%s ix=%d L=%d perm=%ld dir=%d m=%d checks=%d even=%d odd=%d bits=%.1f\n",lab,W[a],form?"diff":"sum",ix,L,q,dir,m,chk_self,ev,nodd,bits);}}
            }}}}}}}
  printf("C %s tests %lld hits %lld nperm=%ld words=%ld..%ld minchk=%d\n",lab,tests,hits,npu,lo,hi,MINCHK);
  return 0;}
