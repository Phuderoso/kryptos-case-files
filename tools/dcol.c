/* Cycle 52: DOUBLE KEYED COLUMNAR, exact (new slice: cycles 4-5 only annealed it). Plaintext written row-major
   under keyword 1 (width = word length, incomplete last row), columns read in alphabetic keyword order; the result
   rewritten under keyword 2 and read the same way (K3 is a double transposition). b = -1 means single columnar
   with keyword 1. Keywords: themed Kryptos/K1-K3 words + the most frequent English words (dcol_gen.py).
   Each permutation and its inverse x periodic or progressive keyword key (key_i = k[i mod L] + s*floor(i/L)),
   Vigenere/Beaufort, A-Z or KRYPTOS tableau, key before or after, exact against the 24 official crib letters
   (checker identical to cycles 41/44/46/50).  usage: dcol CARVED qg.bin orders.txt part nparts */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char*KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
float*QG; int SMAX=26, LMAX=22; const char*car; int num[2][26],den[2][26],cp[24],cl[24];
long cons[2][2][2][2], tests, part[27]; float best=-99; long pid=0; int NO; int W[4000],O[4000][14];
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

static void col(int w,const int*o,int*P){int k=0; int rows=(N+w-1)/w; for(int j=0;j<w;j++){int c=o[j]; for(int r=0;r<rows;r++){int i=r*w+c; if(i<N)P[i]=k++;}}}
int main(int argc,char**argv){
  car=argv[1]; if(getenv("SMAX"))SMAX=atoi(getenv("SMAX")); if(getenv("LMAX"))LMAX=atoi(getenv("LMAX"));
  int part_i=atoi(argv[4]), nparts=atoi(argv[5]);
  QG=malloc(sizeof(float)*456976); FILE*f=fopen(argv[2],"rb"); if(fread(QG,4,456976,f)!=456976)return 1; fclose(f);
  for(int l=0;l<26;l++){num[0][l]=l; num[1][l]=strchr(KA,'A'+l)-KA;} for(int e=0;e<2;e++)for(int l=0;l<26;l++)den[e][num[e][l]]=l;
  const char*cr1="EASTNORTHEAST",*cr2="BERLINCLOCK"; int nc=0;
  for(int i=0;i<13;i++){cp[nc]=21+i;cl[nc++]=cr1[i]-'A';} for(int i=0;i<11;i++){cp[nc]=63+i;cl[nc++]=cr2[i]-'A';}
  static char nm[4000][16]; FILE*g=fopen(argv[3],"r"); NO=0; while(fscanf(g,"%15s %d",nm[NO],&W[NO])==2){for(int j=0;j<W[NO];j++)if(fscanf(g,"%d",&O[NO][j])!=1)return 2; NO++;} fclose(g);
  static int PP[4000][N]; for(int a=0;a<NO;a++)col(W[a],O[a],PP[a]);
  long npair=0;
  for(int a=part_i;a<NO;a+=nparts)for(int b=-1;b<NO;b++){ int P[N]; npair++;
    for(int i=0;i<N;i++) P[i]= b<0? PP[a][i] : PP[b][PP[a][i]];
    char tag[96]; sprintf(tag,"k1=%s k2=%s inv=0",nm[a],b<0?"-":nm[b]); check(P,tag);
    int Q[N]; for(int i=0;i<N;i++)Q[P[i]]=i; tag[strlen(tag)-1]='1'; check(Q,tag);}
  printf("SUMMARY part=%d pairs=%ld tests=%ld best_qg=%.3f\n",part_i,npair,tests,best);
  for(int e=0;e<2;e++)for(int m=0;m<2;m++)for(int md=0;md<2;md++)printf("num=%c model=%c mode=%c consistent_s0=%ld consistent_s>0=%ld\n",e?'K':'A',m?'B':'A',md?'B':'V',cons[e][m][md][0],cons[e][m][md][1]);
  printf("PARTIAL_BY_L");for(int L=14;L<=26;L++)printf(" %d:%ld",L,part[L]);printf("\n");
  return 0;}
