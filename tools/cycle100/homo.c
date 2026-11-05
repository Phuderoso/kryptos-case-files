/* Cycle 100: homophonic (many-to-one) substitution, alone and behind a transposition.
   Model: P_i = f(C_{s(i)}), f: 26 cipher letters -> 26 plain letters, ANY function (several cipher letters may share a plain letter).
   Covers both layer orders (a letter-wise substitution commutes with a transposition).
   Step 1: exact crib consistency.  Step 2: for consistent configs, anneal the free values of f for quadgram score (cribs hard).
   Usage: ./homo CT qg.bin restarts perms.bin...  (identity perm always tested first) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
float*QG; int crib[N];
static float score(const int*x){float s=0;for(int i=0;i+3<N;i++)s+=QG[((x[i]*26+x[i+1])*26+x[i+2])*26+x[i+3]];return s/(N-3);}
static unsigned rs=12345; static inline unsigned rnd(){rs^=rs<<13;rs^=rs>>17;rs^=rs<<5;return rs;}
long tot=0,cons=0; float bestall=-99; int R;
void test(const char*CT,const int*s,const char*tag,long n,int inv){
  int c[N],f[26],fixed[26]; for(int i=0;i<N;i++)c[i]=CT[s[i]]-65; tot++;
  for(int k=0;k<26;k++){f[k]=-1;fixed[k]=0;}
  for(int i=0;i<N;i++) if(crib[i]>=0){ if(f[c[i]]<0){f[c[i]]=crib[i];fixed[c[i]]=1;} else if(f[c[i]]!=crib[i]) return; }
  cons++; int nfree=0,used[26]={0}; for(int i=0;i<N;i++)used[c[i]]=1; for(int k=0;k<26;k++) if(used[k]&&!fixed[k])nfree++;
  float bs=-99; int bf[26];
  for(int r=0;r<R;r++){ int g[26]; for(int k=0;k<26;k++) g[k]=fixed[k]?f[k]:rnd()%26;
    int p[N]; for(int i=0;i<N;i++)p[i]=g[c[i]]; float cur=score(p); int imp=1;
    while(imp){imp=0; for(int k=0;k<26;k++){ if(fixed[k]||!used[k])continue; int old=g[k],bv=old;
        for(int v=0;v<26;v++){ if(v==old)continue; g[k]=v; for(int i=0;i<N;i++)p[i]=g[c[i]]; float sc=score(p); if(sc>cur+1e-6){cur=sc;bv=v;imp=1;} }
        g[k]=bv; for(int i=0;i<N;i++)p[i]=g[c[i]]; } }
    if(cur>bs){bs=cur;memcpy(bf,g,sizeof g);} }
  if(bs>bestall)bestall=bs;
  printf("CONS %s n=%ld inv=%d free=%d qg=%.3f ",tag,n,inv,nfree,bs); for(int i=0;i<N;i++)putchar(65+bf[c[i]]); putchar('\n');
}
int main(int argc,char**argv){ const char*CT=argv[1]; R=atoi(argv[3]);
  QG=malloc(4*456976); FILE*q=fopen(argv[2],"rb"); fread(QG,4,456976,q); fclose(q);
  const char*a="EASTNORTHEAST",*b="BERLINCLOCK"; for(int i=0;i<N;i++)crib[i]=-1;
  for(int i=0;i<13;i++)crib[21+i]=a[i]-65; for(int i=0;i<11;i++)crib[63+i]=b[i]-65;
  int id[N]; for(int i=0;i<N;i++)id[i]=i; test(CT,id,"identity",0,0);
  for(int A=4;A<argc;A++){ FILE*fp=fopen(argv[A],"rb"); fseek(fp,0,2); long np=ftell(fp)/194; fseek(fp,0,0); short*S=malloc(np*194); fread(S,194,np,fp); fclose(fp);
    for(long n=0;n<np;n++) for(int inv=0;inv<2;inv++){ int s[N]; if(!inv)for(int i=0;i<N;i++)s[i]=S[n*N+i]; else for(int i=0;i<N;i++)s[S[n*N+i]]=i; test(CT,s,argv[A],n,inv);} free(S);}
  fprintf(stderr,"configs %ld crib-consistent %ld best_qg %.3f\n",tot,cons,bestall); }
