/* Cycle 50: NIHILIST TRANSPOSITION (new family). Plaintext written row-major into a 10x10 square (3 empty cells,
   at the end (layout 0) or the start (layout 1)); rows AND columns are reordered by the SAME permutation sigma of
   0..9 (the classic Nihilist transposition keyed by one word); the square is read row-major (read 0) or
   column-major (read 1), skipping empty cells. All 10! sigmas (every 10-letter keyword ordering, plus every shorter
   keyword padded by any completion) x 2 layouts x 2 readings x the map and its inverse.
   On either side of a periodic or progressive keyword key (key_i = k[i mod L] + s*floor(i/L)), Vigenere/Beaufort,
   A-Z or KRYPTOS tableau, exact against the 24 official crib letters (same checker as cycles 41/44/46).
   usage: nihilist CARVED qg.bin first_sigma0 [SMAX env]   (sigma[0] fixed -> 9! sigmas per process) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char*KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
float*QG; int SMAX=26, LMAX=22; const char*car; int num[2][26],den[2][26],cp[24],cl[24];
long cons[2][2][2][2], tests, part[27]; float best=-99; long pid=0;
static float score(const int*x){float s=0;for(int i=0;i+3<N;i++)s+=QG[((x[i]*26+x[i+1])*26+x[i+2])*26+x[i+3]];return s/(N-3);}
static void check(const int*P,const char*tag){int inv[N]; for(int k=0;k<N;k++)inv[P[k]]=k;
 for(int e=0;e<2;e++)for(int m=0;m<2;m++){
  int ct[N]; for(int k=0;k<N;k++) ct[k]=num[e][(m==0? car[P[k]] : car[k])-'A'];
  int ki[24],v[2][24]; for(int j=0;j<24;j++){ki[j]= m==0? cp[j] : inv[cp[j]]; int px=num[e][cl[j]], cx=ct[ki[j]];
    v[0][j]=((cx-px)%26+26)%26; v[1][j]=(cx+px)%26;}
  for(int md=0;md<2;md++)for(int L=1;L<=LMAX;L++)for(int s=0;s<SMAX;s++){tests++;
    int k[26]; for(int c=0;c<L;c++)k[c]=-1; int ok=1;
    for(int j=0;j<24;j++){int i=ki[j]; int kv=((v[md][j]-s*(i/L))%26+26*26)%26; int c=i%L;
      if(k[c]<0)k[c]=kv; else if(k[c]!=kv){ok=0;break;}}
    if(!ok)continue;
    cons[e][m][md][s>0]++;
    if(L>13){part[L]++; if(!(getenv("PRINTL")&&atoi(getenv("PRINTL"))==L))continue;}
    int miss[26],nm=0; for(int c=0;c<L;c++) if(k[c]<0){miss[nm++]=c;k[c]=0;}
    int pt[N],po[N];
    #define DEC() for(int i=0;i<N;i++){int key=(k[i%L]+s*(i/L))%26; int x= md==0? ((ct[i]-key)%26+26)%26 : ((key-ct[i])%26+26)%26; pt[i]=den[e][x];} \
      if(m==1){for(int i=0;i<N;i++)po[i]=pt[inv[i]];} else memcpy(po,pt,sizeof pt);
    if(nm){ for(int pass=0;pass<3;pass++)for(int u=0;u<nm;u++){int bv=0;float bs=-99; for(int vv=0;vv<26;vv++){k[miss[u]]=vv; DEC(); float t=score(po); if(t>bs){bs=t;bv=vv;}} k[miss[u]]=bv;} }
    DEC(); float sc=score(po); if(sc>best)best=sc;
    char o[N+1],kw[27];for(int i=0;i<N;i++)o[i]='A'+po[i];o[N]=0; for(int c=0;c<L;c++)kw[c]= e? KA[k[c]] : 'A'+k[c]; kw[L]=0;
    printf("HIT %s num=%c model=%c mode=%c L=%d s=%d free=%d key=%s score=%.3f pt=%s\n",tag,e?'K':'A',m?'B':'A',md?'B':'V',L,s,nm,kw,sc,o);}}}
int main(int argc,char**argv){
  car=argv[1]; if(getenv("SMAX"))SMAX=atoi(getenv("SMAX")); if(getenv("LMAX"))LMAX=atoi(getenv("LMAX")); int s0=atoi(argv[3]);
  QG=malloc(sizeof(float)*456976); FILE*f=fopen(argv[2],"rb"); if(fread(QG,4,456976,f)!=456976)return 1; fclose(f);
  for(int l=0;l<26;l++){num[0][l]=l; num[1][l]=strchr(KA,'A'+l)-KA;} for(int e=0;e<2;e++)for(int l=0;l<26;l++)den[e][num[e][l]]=l;
  const char*cr1="EASTNORTHEAST",*cr2="BERLINCLOCK"; int nc=0;
  for(int i=0;i<13;i++){cp[nc]=21+i;cl[nc++]=cr1[i]-'A';} for(int i=0;i<11;i++){cp[nc]=63+i;cl[nc++]=cr2[i]-'A';}
  int sg[10]; sg[0]=s0; int rest[9],r=0; for(int x=0;x<10;x++) if(x!=s0) rest[r++]=x;
  /* iterate permutations of rest (Heap-free: lexicographic next_permutation) */
  long nsig=0;
  long MAXS= getenv("MAXSIG")? atol(getenv("MAXSIG")) : 1L<<40;
  do{ for(int i=0;i<9;i++)sg[i+1]=rest[i]; nsig++; if(nsig>MAXS)break;
    for(int lay=0;lay<2;lay++)for(int rd=0;rd<2;rd++){
      /* plaintext cell for pt index i: layout0 cell i; layout1 cell i+3 */
      int occ[100]; for(int c=0;c<100;c++)occ[c]= lay==0? (c<97) : (c>=3);
      /* new grid position of old cell (r,c) is (pos[r],pos[c]) where sigma lists old index at new slot: pos[sg[j]]=j */
      int pos[10]; for(int j=0;j<10;j++)pos[sg[j]]=j;
      int rank[100]; int cnt=0;
      int newocc[100]; for(int c=0;c<100;c++)newocc[c]=0;
      for(int c=0;c<100;c++) if(occ[c]) newocc[pos[c/10]*10+pos[c%10]]=1;
      for(int t=0;t<100;t++){int cell= rd==0? t : (t%10)*10+t/10; if(newocc[cell]) rank[cell]=cnt++;}
      int P[N]; for(int i=0;i<N;i++){int c= lay==0? i : i+3; P[i]=rank[pos[c/10]*10+pos[c%10]];}
      char tag[64]; sprintf(tag,"sigma=%d%d%d%d%d%d%d%d%d%d lay=%d read=%d inv=0",sg[0],sg[1],sg[2],sg[3],sg[4],sg[5],sg[6],sg[7],sg[8],sg[9],lay,rd);
      check(P,tag); int Q[N]; for(int i=0;i<N;i++)Q[P[i]]=i; tag[strlen(tag)-1]='1'; check(Q,tag);}
    int i=7; while(i>=0&&rest[i]>rest[i+1])i--; if(i<0)break; int j=8; while(rest[j]<rest[i])j--;
    int t=rest[i];rest[i]=rest[j];rest[j]=t; for(int a=i+1,b=8;a<b;a++,b--){t=rest[a];rest[a]=rest[b];rest[b]=t;}
  }while(1);
  printf("SUMMARY sigma0=%d sigmas=%ld tests=%ld best_qg=%.3f\n",s0,nsig,tests,best);
  for(int e=0;e<2;e++)for(int m=0;m<2;m++)for(int md=0;md<2;md++)printf("num=%c model=%c mode=%c consistent_s0=%ld consistent_s>0=%ld\n",e?'K':'A',m?'B':'A',md?'B':'V',cons[e][m][md][0],cons[e][m][md][1]);
  printf("PARTIAL_BY_L");for(int L=14;L<=26;L++)printf(" %d:%ld",L,part[L]);printf("\n");
  return 0;}
