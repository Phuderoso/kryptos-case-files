/* Cycle 138: ciphertext-fed autokey where the key letter is read through the
   FREE plaintext alphabet x (any of 26!), cipher side a keyed alphabet y.
     SUM  (Vigenere):           y(c_j) = x(p_j) + x(c_{j-L})
     DIFF (Beaufort = variant): y(c_j) = x(c_{j-L}) - x(p_j)
   (with x free, Beaufort and variant Beaufort coincide under x -> -x).
   Each crib with key index j >= L is a two-variable linear equation mod 26 on
   x.  Exact solver: components with x_v = s_v*r + o_v, root masks from cycles
   (coefficient 0 or +-2), injectivity inside and across components by
   backtracking.  Reports every satisfiable configuration with >= MINCYC
   independent cycles.
   ix=1 carved index (transpose first); ix=0 plaintext index (model Q).
   usage: ctself CT words.txt perms.bin label lo hi LMAX [pstride] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
#define MAXW 12000
static int MINCYC=0; static int MINWIN=4; static double THR=8.0;
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PT="EASTNORTHEASTBERLINCLOCK";
static char W[MAXW][32]; static unsigned char INV[MAXW][26];
static int Plet[24],C[N]; static const char*lab;
static void keyed(const char*w,unsigned char*inv){int u[26]={0},n=0;unsigned char al[26];
 for(const char*p=w;*p;p++){int c=*p-'A';if(c<0||c>25||u[c])continue;u[c]=1;al[n++]=c;}
 for(int c=0;c<26;c++)if(!u[c])al[n++]=c;for(int i=0;i<26;i++)inv[al[i]]=i;}
/* edge: a=p letter, b=key letter, k=y(c) */
static int ea[24],eb[24],ek[24],ne,form;
static int sgn[26],off[26],comp[26],ncomp; static unsigned int cmask[26]; static int cverts[26][26],cn[26];
int md(int v);
static int sol_r[26];
static float *Q; static int ISCRIB[97];
static int cur_ix,cur_L,cur_form,*cur_layer; static const short*cur_S; static const unsigned char*cur_y;
static double best_sc; static int best_x[26]; static long nenum; static int ENUMCAP=300;
static double score_x(const int*xv,char*ps){int inv[26];for(int i=0;i<26;i++)inv[i]=-1;for(int v=0;v<26;v++)if(xv[v]>=0)inv[xv[v]]=v;
  for(int i=0;i<97;i++){int j=cur_ix?cur_S[i]:i;char ch='?';
    if(j>=cur_L&&xv[cur_layer[j-cur_L]]>=0){int xp=cur_form==0?md(cur_y[cur_layer[j]]-xv[cur_layer[j-cur_L]]):md(xv[cur_layer[j-cur_L]]-cur_y[cur_layer[j]]);
      ch=inv[xp]>=0?'A'+inv[xp]:'.';}
    ps[i]=ch;}
  double t=0;int n=0;for(int i=0;i+4<=97;i++){int ok=1,id=0;for(int k=0;k<4;k++){char c=ps[i+k];if(c<'A'||c>'Z'||ISCRIB[i+k]){ok=0;break;}id=id*26+c-'A';}if(ok){t+=Q[id]+5.5;n++;}}
  return n>=MINWIN?t:-99;}
int md(int v){v%=26;return v<0?v+26:v;}
static unsigned int solmask(int coef,int rhs){unsigned int m=0;for(int r=0;r<26;r++)if(md(coef*r)==md(rhs))m|=1u<<r;return m;}
static int bt(int ci,unsigned int used);
static void bte(int ci,unsigned int used){
  if(nenum>=ENUMCAP)return;
  if(ci==ncomp){nenum++;int xv[26];char ps[98];for(int v=0;v<26;v++)xv[v]=comp[v]>=0?md(sgn[v]*sol_r[comp[v]]+off[v]):-1;
    double sc=score_x(xv,ps);if(sc>best_sc){best_sc=sc;memcpy(best_x,xv,sizeof xv);}return;}
  for(int r=0;r<26;r++){ if(!(cmask[ci]>>r&1))continue; unsigned int u=used;int ok=1;
    for(int q=0;q<cn[ci];q++){int v=cverts[ci][q];int val=md(sgn[v]*r+off[v]);if(u>>val&1){ok=0;break;}u|=1u<<val;}
    if(ok){sol_r[ci]=r;bte(ci+1,u);}}}
static int bt(int ci,unsigned int used){
  if(ci==ncomp)return 1;
  for(int r=0;r<26;r++){ if(!(cmask[ci]>>r&1))continue;
    unsigned int u=used; int ok=1;
    for(int q=0;q<cn[ci];q++){int v=cverts[ci][q];int val=md(sgn[v]*r+off[v]);if(u>>val&1){ok=0;break;}u|=1u<<val;}
    if(ok){sol_r[ci]=r; if(bt(ci+1,u))return 1;}
  }
  return 0;}
static int solve(int*cycles){
  int adj[26][48],na[26]; memset(na,0,sizeof na);
  for(int e=0;e<ne;e++){adj[ea[e]][na[ea[e]]++]=e; if(eb[e]!=ea[e]) adj[eb[e]][na[eb[e]]++]=e;}
  for(int v=0;v<26;v++)comp[v]=-1;
  ncomp=0; int nv=0; int tree=0;
  for(int s=0;s<26;s++){ if(!na[s]||comp[s]>=0)continue;
    int ci=ncomp++; cn[ci]=0; cmask[ci]=0x3ffffff;
    int stk[26],sp=0; comp[s]=ci;sgn[s]=1;off[s]=0;stk[sp++]=s;cverts[ci][cn[ci]++]=s;nv++;
    while(sp){int u=stk[--sp];
      for(int q=0;q<na[u];q++){int e=adj[u][q];int a=ea[e],b=eb[e],k=ek[e];
        int other=(u==a)?b:a;
        if(comp[other]<0){ /* tree edge: derive other from u */
          if(form==0){sgn[other]=-sgn[u];off[other]=md(k-off[u]);}
          else{ /* x_b - x_a = k */
            if(u==a){sgn[other]=sgn[u];off[other]=md(off[u]+k);} else {sgn[other]=sgn[u];off[other]=md(off[u]-k);} }
          comp[other]=ci;stk[sp++]=other;cverts[ci][cn[ci]++]=other;nv++;tree++;
        }
      }
    }
  }
  /* check all edges (tree edges pass trivially) */
  for(int e=0;e<ne;e++){int a=ea[e],b=eb[e],k=ek[e],ci=comp[a];
    int coef,rhs;
    if(form==0){coef=sgn[a]+sgn[b];rhs=k-off[a]-off[b];}
    else{coef=sgn[b]-sgn[a];rhs=k-off[b]+off[a];}
    cmask[ci]&=solmask(coef,rhs); if(!cmask[ci])return 0;}
  *cycles=ne-tree;
  /* order components biggest first for backtracking */
  return bt(0,0);
}
int main(int argc,char**argv){
  if(argc<8){fprintf(stderr,"usage\n");return 1;}
  for(int i=0;i<N;i++)C[i]=argv[1][i]-'A';lab=argv[4];
  long lo=atol(argv[5]),hi=atol(argv[6]);int LMAX=atoi(argv[7]);long pst=argc>8?atol(argv[8]):1;
  if(getenv("MINCYC"))MINCYC=atoi(getenv("MINCYC"));
  FILE*wf=fopen(argv[2],"r");int nw=0;while(nw<MAXW&&fscanf(wf,"%31s",W[nw])==1){keyed(W[nw],INV[nw]);nw++;}fclose(wf);if(hi>nw)hi=nw;
  for(int t=0;t<24;t++)Plet[t]=PT[t]-'A';
  FILE*pf=fopen(argv[3],"rb");fseek(pf,0,SEEK_END);long np=ftell(pf)/(2*N);rewind(pf);
  short*Perm=malloc((size_t)np*N*2);if(fread(Perm,2,(size_t)np*N,pf)!=(size_t)np*N)return 1;fclose(pf);
  long long tests=0,sat=0,surv=0; long long hcyc[25]; static long long hsc[100]; Q=malloc(26*26*26*26*4);{FILE*qf=fopen(getenv("QUAD")?getenv("QUAD"):"quad.bin","rb");if(!qf||fread(Q,4,456976,qf)!=456976)return 2;fclose(qf);} for(int i=21;i<=33;i++)ISCRIB[i]=1;for(int i=63;i<=73;i++)ISCRIB[i]=1; if(getenv("THR"))THR=atof(getenv("THR")); if(getenv("MINWIN"))MINWIN=atoi(getenv("MINWIN")); if(getenv("ENUMCAP"))ENUMCAP=atoi(getenv("ENUMCAP")); memset(hcyc,0,sizeof hcyc); long npu=0;
  for(long q=0;q<np;q+=pst){npu++;const short*s=Perm+q*N;short u[N];for(int i=0;i<N;i++)u[s[i]]=i;
    for(int dir=0;dir<2;dir++){const short*S=dir?u:s;
      for(int ix=0;ix<2;ix++){int layer[N],kp[24];
        for(int i=0;i<N;i++)layer[i]=ix?C[i]:C[S[i]];
        for(int t=0;t<24;t++)kp[t]=ix?S[CI[t]]:CI[t];
        for(int L=1;L<=LMAX;L++){
          int cc[24],kk[24],pp[24],m=0;
          for(int t=0;t<24;t++){int j=kp[t];if(j<L)continue;pp[m]=Plet[t];cc[m]=layer[j];kk[m]=layer[j-L];m++;}
          if(m<MINCYC+1)continue;
          for(long a=lo;a<hi;a++){const unsigned char*y=INV[a];
            for(form=0;form<2;form++){tests++;
              ne=m;for(int e=0;e<m;e++){ea[e]=pp[e];eb[e]=kk[e];ek[e]=y[cc[e]];}
              int cyc=0; if(!solve(&cyc))continue; sat++; hcyc[cyc]++;
              if(cyc<MINCYC)continue;
              cur_ix=ix;cur_L=L;cur_form=form;cur_layer=layer;cur_S=S;cur_y=y;best_sc=-99;nenum=0;bte(0,0);
              {int b=(int)(best_sc+50);if(b<0)b=0;if(b>99)b=99;hsc[b]++;}
              if(best_sc<THR)continue; surv++;
              {char ps[98];ps[97]=0;score_x(best_x,ps);
              printf("S %s score=%.3f word=%s form=%s ix=%d L=%d perm=%ld dir=%d cycles=%d ncomp=%d nsol=%ld partial=%s\n",lab,best_sc,W[a],form?"DIFF":"SUM",ix,L,q,dir,cyc,ncomp,nenum,ps);}
            }}}}}}
  for(int b=0;b<100;b++)if(hsc[b])printf("Q %s %d %lld\n",lab,b-50,hsc[b]);
  printf("C %s tests %lld satisfiable %lld survivors %lld alph=%ld..%ld nperm=%ld lmax=%d mincyc=%d\n",lab,tests,sat,surv,lo,hi,npu,LMAX,MINCYC);
  printf("H %s cycles:",lab);for(int i=0;i<25;i++)printf(" %d:%lld",i,hcyc[i]);printf("\n");
  return 0;}
