/* Cycle 65: Gromark (lagged-Fibonacci digit key, base 10) with BOTH alphabets arbitrary.
   mode census: count primers (length L) feasible against the 24 cribs (weighted union-find + injectivity).
   mode sa: for each feasible primer of length L, anneal (PA,CA) to maximise quadgram score with cribs enforced. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static float *QG; static int N; static int C[200];
static const char *CR1="EASTNORTHEAST",*CR2="BERLINCLOCK"; static int CP[24],CL[24];
static int par[52],pot[52];
static int fnd(int v){ if(par[v]==v) return v; int r=fnd(par[v]); pot[v]=(pot[v]+pot[par[v]])%26; par[v]=r; return r; }
/* note: after fnd, pot[v] = val(v)-val(root) */
static int feasible(const int *k){
  for(int i=0;i<52;i++){par[i]=i;pot[i]=0;}
  for(int j=0;j<24;j++){ int i=CP[j]; int a=CL[j], b=26+C[i]; /* val(b)-val(a)=k */
    int ra=fnd(a), rb=fnd(b); int w=k[i]%26;
    if(ra==rb){ if(((pot[b]-pot[a]-w)%26+26)%26) return 0; }
    else { par[rb]=ra; pot[rb]=((pot[a]+w-pot[b])%26+26)%26; } }
  /* injectivity: same side, same root, same pot => conflict (only nodes that appear) */
  int seen[52][26]; memset(seen,0,sizeof seen); int used[52]={0};
  for(int j=0;j<24;j++){used[CL[j]]=1; used[26+C[CP[j]]]=1;}
  for(int v=0;v<52;v++) if(used[v]){ int r=fnd(v); int side=v>=26; int key=r; 
    if(seen[key][pot[v]] & (1<<side)) return 0; seen[key][pot[v]]|=(1<<side);} 
  return 1; }
static void keygen(const int *pr,int L,int *k){ for(int i=0;i<N;i++) k[i]= i<L? pr[i] : (k[i-L]+k[i-L+1])%10; }
static unsigned long long rs=88172645463325252ULL; static unsigned rnd(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return (unsigned)rs; }
static double frand(void){ return (rnd()&0xffffff)/16777216.0; }
static int x[26],y[26],xi[26];
static double score(const int *k,int *P,int *mis){ for(int a=0;a<26;a++) xi[x[a]]=a;
  for(int i=0;i<N;i++) P[i]=xi[((y[C[i]]-k[i])%26+26)%26];
  int m=0; for(int j=0;j<24;j++) if(P[CP[j]]!=CL[j]) m++; *mis=m;
  double s=0; for(int i=0;i+3<N;i++) s+=QG[((P[i]*26+P[i+1])*26+P[i+2])*26+P[i+3]]; return s/(N-3); }
int main(int argc,char**argv){
  char *ct=argv[2]; N=strlen(ct); for(int i=0;i<N;i++) C[i]=ct[i]-'A';
  for(int j=0;j<13;j++){CP[j]=21+j;CL[j]=CR1[j]-'A';} for(int j=0;j<11;j++){CP[13+j]=63+j;CL[13+j]=CR2[j]-'A';}
  int L=atoi(argv[3]); long lim=1; for(int i=0;i<L;i++) lim*=10; int pr[10],k[200];
  if(!strcmp(argv[1],"census")){ long cnt=0; for(long p=0;p<lim;p++){ long q=p; for(int i=L-1;i>=0;i--){pr[i]=q%10;q/=10;} keygen(pr,L,k);
      if(feasible(k)){ cnt++; if(argc>4) printf("F %0*ld\n",L,p);} } printf("COUNT L=%d %ld\n",L,cnt); return 0; }
  /* sa: hard-constrained annealing. Component offsets keep all 24 crib equations satisfied at every step. */
  QG=malloc(4*456976); FILE*f=fopen(argv[4],"rb"); if(fread(QG,4,456976,f)!=456976) return 1; fclose(f);
  int restarts=atoi(argv[5]); long iters=atol(argv[6]); rs^=(unsigned long long)atoi(argv[7])*2654435761ULL;
  int P[200],best[200]; int part=argc>8?atoi(argv[8]):0, npart=argc>9?atoi(argv[9]):1; long fc=0;
  for(long p=0;p<lim;p++){ long q=p; for(int i=L-1;i>=0;i--){pr[i]=q%10;q/=10;} keygen(pr,L,k); if(!feasible(k)) continue; if((fc++)%npart!=part) continue;
    int used[52]={0}; for(int j=0;j<24;j++){used[CL[j]]=1; used[26+C[CP[j]]]=1;}
    int comp[52],pv[52],nc=0,rootid[52]; for(int v=0;v<52;v++) rootid[v]=-1;
    for(int v=0;v<52;v++){ if(!used[v]){comp[v]=-1;continue;} int r=fnd(v); if(rootid[r]<0) rootid[r]=nc++; comp[v]=rootid[r]; pv[v]=pot[v]; }
    double gb=-1e9;
    for(int r=0;r<restarts;r++){
      int val[52]; int ok=0;
      for(int tries=0;tries<10000 && !ok;tries++){ int occ[2][26]; memset(occ,0,sizeof occ); ok=1;
        for(int c=0;c<nc && ok;c++){ int got=0; for(int t2=0;t2<200 && !got;t2++){ int o=rnd()%26, clash=0;
            for(int v=0;v<52;v++) if(comp[v]==c && occ[v>=26][(o+pv[v])%26]) {clash=1;break;}
            if(!clash){ for(int v=0;v<52;v++) if(comp[v]==c){ val[v]=(o+pv[v])%26; occ[v>=26][val[v]]=1;} got=1; } }
          if(!got) ok=0; }
        if(ok){ for(int s=0;s<2;s++){ int fr[26],nf=0; for(int a=0;a<26;a++) if(!occ[s][a]) fr[nf++]=a;
            for(int a=nf-1;a>0;a--){int b=rnd()%(a+1),t=fr[a];fr[a]=fr[b];fr[b]=t;}
            int z=0; for(int a=0;a<26;a++){ int v=s*26+a; if(comp[v]<0) val[v]=fr[z++]; } } } }
      if(!ok) break;
      for(int a=0;a<26;a++){x[a]=val[a];y[a]=val[26+a];}
      int m; double cur=score(k,P,&m); if(m){fprintf(stderr,"BUG %d\n",m);return 2;}
      for(long it=0;it<iters;it++){ double T=0.04*(1.0-(double)it/iters)+0.001;
        int sv[52]; for(int a=0;a<26;a++){sv[a]=x[a];sv[26+a]=y[a];}
        if(rnd()%3){ /* swap two letters on one side, allowed if both free */
          int s=rnd()&1, a=rnd()%26, b=rnd()%26; if(a==b||comp[s*26+a]>=0||comp[s*26+b]>=0) continue;
          int *A=s?y:x; int t=A[a];A[a]=A[b];A[b]=t; }
        else { /* shift a component by d, displaced free letters take the vacated values */
          if(nc==0) continue; int c=rnd()%nc, d=1+rnd()%25, bad=0;
          for(int s=0;s<2 && !bad;s++){ int *A=s?y:x; int holder[26]; for(int a=0;a<26;a++) holder[A[a]]=a;
            int oldv[26],nwv[26],no=0; int inc[26]={0},inn[26]={0};
            for(int a=0;a<26;a++) if(comp[s*26+a]==c){ oldv[no]=A[a]; nwv[no]=(A[a]+d)%26; inc[oldv[no]]=1; no++; }
            for(int i=0;i<no;i++) inn[nwv[i]]=1;
            int vac[26],nv=0,disp[26],nd=0; for(int i=0;i<no;i++){ if(!inn[oldv[i]]) vac[nv++]=oldv[i]; if(!inc[nwv[i]]){ int h=holder[nwv[i]]; if(comp[s*26+h]>=0){bad=1;break;} disp[nd++]=h; } }
            if(bad) break;
            for(int a=0;a<26;a++) if(comp[s*26+a]==c) A[a]=(A[a]+d)%26;
            for(int i=0;i<nd;i++) A[disp[i]]=vac[i]; }
          if(bad){ for(int a=0;a<26;a++){x[a]=sv[a];y[a]=sv[26+a];} continue; } }
        double s2=score(k,P,&m);
        if(m){fprintf(stderr,"BUG2 %d\n",m);return 2;}
        if(s2>=cur || frand()<exp((s2-cur)/T)){ cur=s2; if(s2>gb){gb=s2;memcpy(best,P,sizeof P);} }
        else for(int a=0;a<26;a++){x[a]=sv[a];y[a]=sv[26+a];} } }
    printf("P %0*ld %.4f ",L,p,gb); for(int i=0;i<N;i++) putchar('A'+best[i]); printf("\n"); fflush(stdout); }
  return 0; }
