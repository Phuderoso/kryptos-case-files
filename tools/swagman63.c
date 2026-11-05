/* Cycle 63: exact Swagman (ACA Latin-square transposition, 7-row key square) + periodic Vigenere/Beaufort
   (themed alphabets) before or after. Usage: swagman63 alpha.bin nalpha ct.txt pmax [maxprint]
   Configs: 98-symbol block (K4 with '?' at start or end of carved text; one unknown PT null at start or end),
   forward Swagman or its inverse; plus the irregular 97-letter block (last cell empty, forward).
   Key slot: case A = 97-letter PT index mod p (sub before transposition); case B = K4 carved index mod p.
   Vig and variant Beaufort are equivalent for consistency checks with one tableau, so only vig/beau run. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const char *CR1="EASTNORTHEAST",*CR2="BERLINCLOCK";
typedef struct { int nc; int q[24]; int pl[24]; int pt97[24]; } Cribs;
static unsigned char AL[2000][26];
typedef struct {
  int ct[98]; int ctslot[98]; int n; /* CT symbols (alpha idx later), -1 for ? ; slot = K4 index or -1 */
  int irregular, inverse;
  int ncr; int cq[24], cpl[24], cs97[24];
  int kcr[7][8], nk[7]; /* crib indices per key column */
} Cfg;
static long long solcount; static int maxprint, printed;
typedef struct { const Cfg *C; const unsigned char *al; int idx[26]; int beau, p, caseB; int slot[200]; int used[7][7]; int tau[7][7]; } St;
static int ctpos(const St *S,int ci){ const Cfg*C=S->C; int q=C->cq[ci];
  if(!C->inverse){ int r=q/14,c=q%14,k=c%7; int v=S->tau[k][r];
    if(C->irregular && c==13){ int m=S->tau[6][6]; return 91 + v - (m<v); }
    return c*7+v; }
  else { int c=q/7,s=q%7,k=c%7; return S->tau[k][s]*14+c; } }
static int rowsfor(const Cfg*C,int k,int*rows){ int nr=0,seen[7]={0};
  for(int i=0;i<C->nk[k];){ int q=C->cq[C->kcr[k][i]]; int a=C->inverse? q%7 : q/14; if(!seen[a]){seen[a]=1;rows[nr++]=a;} i++; }
  if(C->irregular && k==6 && !seen[6]) rows[nr++]=6;
  return nr; }
static void dfs(St*S,int k);
static void assign(St*S,int k,int*rows,int nr,int d){
  if(d==nr){ /* check cribs of column k */
    const Cfg*C=S->C; int undo[8],nu=0,ok=1;
    for(int i=0;i<C->nk[k]&&ok;i++){ int ci=C->kcr[k][i]; int pos=ctpos(S,ci); int cl=C->ct[pos];
      if(cl<0){ok=0;break;} int sl = S->caseB ? C->ctslot[pos] : C->cs97[ci]; if(sl<0){ok=0;break;} sl%=S->p;
      int pi=S->idx[C->cpl[ci]], ci2=S->idx[cl]; int sh = S->beau ? (ci2+pi)%26 : (ci2-pi+26)%26;
      if(S->slot[sl]<0){S->slot[sl]=sh;undo[nu++]=sl;} else if(S->slot[sl]!=sh) ok=0; }
    if(ok) dfs(S,k+1);
    for(int i=0;i<nu;i++) S->slot[undo[i]]=-1; return; }
  int r=rows[d];
  for(int v=0;v<7;v++){ if(S->used[r][v]) continue; int clash=0; for(int e=0;e<d;e++) if(S->tau[k][rows[e]]==v) clash=1; if(clash) continue;
    S->used[r][v]=1; S->tau[k][r]=v; assign(S,k,rows,nr,d+1); S->used[r][v]=0; S->tau[k][r]=-1; } }
static void dfs(St*S,int k){
  if(k==7){ long long c; 
    #pragma omp atomic capture
    c=++solcount;
    if(c<=maxprint){ printf("  HIT %s %s p=%d tau:",S->beau?"beau":"vig",S->caseB?"B":"A",S->p);
      for(int a=0;a<7;a++){printf(" ");for(int b=0;b<7;b++)printf("%c",S->tau[a][b]<0?'.':'1'+S->tau[a][b]);} printf("\n"); }
    return; }
  int rows[8]; int nr=rowsfor(S->C,k,rows); assign(S,k,rows,nr,0); }
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"rb"); int na=atoi(argv[2]); fread(AL,26,na,f); fclose(f);
  char k4[200]; f=fopen(argv[3],"r"); fscanf(f,"%199s",k4); fclose(f); int pmax=atoi(argv[4]); maxprint=argc>5?atoi(argv[5]):5;
  if(strlen(k4)!=97){fprintf(stderr,"need 97\n");return 1;}
  int crq[24],crl[24],nc=0; for(int i=0;i<13;i++){crq[nc]=21+i;crl[nc++]=CR1[i]-'A';} for(int i=0;i<11;i++){crq[nc]=63+i;crl[nc++]=CR2[i]-'A';}
  Cfg cfgs[9]; int ncfg=0; const char*names[9];
  static char nb[9][64];
  for(int qs=0;qs<2;qs++) for(int ns=0;ns<2;ns++) for(int inv=0;inv<2;inv++){ Cfg*C=&cfgs[ncfg]; memset(C,0,sizeof*C);
    C->n=98; C->inverse=inv; for(int i=0;i<98;i++){ int j = qs==0 ? i-1 : i; if(j<0||j>=97){C->ct[i]=-1;C->ctslot[i]=-1;} else {C->ct[i]=k4[j]-'A';C->ctslot[i]=j;} }
    C->ncr=24; for(int i=0;i<24;i++){C->cq[i]=crq[i]+(ns==0?1:0); C->cpl[i]=crl[i]; C->cs97[i]=crq[i];}
    sprintf(nb[ncfg],"98 ?%s nullPT%s %s",qs?"end":"start",ns?"end":"start",inv?"inverse":"forward"); names[ncfg]=nb[ncfg]; ncfg++; }
  { Cfg*C=&cfgs[ncfg]; memset(C,0,sizeof*C); C->n=97; C->irregular=1; for(int i=0;i<97;i++){C->ct[i]=k4[i]-'A';C->ctslot[i]=i;}
    C->ncr=24; for(int i=0;i<24;i++){C->cq[i]=crq[i];C->cpl[i]=crl[i];C->cs97[i]=crq[i];} names[ncfg]="97 irregular (last cell empty) forward"; ncfg++; }
  for(int g=0;g<ncfg;g++){ Cfg*C=&cfgs[g]; for(int i=0;i<C->ncr;i++){ int q=C->cq[i]; int k = C->inverse ? (q/7)%7 : (q%14)%7; C->kcr[k][C->nk[k]++]=i; } }
  long long total=0;
  for(int g=0;g<ncfg;g++) for(int caseB=0;caseB<2;caseB++) for(int beau=0;beau<2;beau++) for(int p=1;p<=pmax;p++){
    solcount=0;
    #pragma omp parallel for schedule(dynamic)
    for(int a=0;a<na;a++){ St S; memset(&S,0,sizeof S); S.C=&cfgs[g]; S.al=AL[a]; for(int i=0;i<26;i++) S.idx[AL[a][i]]=i;
      S.beau=beau;S.p=p;S.caseB=caseB; for(int i=0;i<200;i++)S.slot[i]=-1; memset(S.tau,-1,sizeof S.tau); dfs(&S,0); }
    if(solcount) printf("%s case %c %s p=%d: %lld partial-square solutions\n",names[g],caseB?'B':'A',beau?"beau":"vig",p,solcount);
    total+=solcount; fflush(stdout); }
  printf("TOTAL %lld\n",total); return 0; }
