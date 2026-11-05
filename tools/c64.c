/* Cycle 64: ONE WORD, TWO JOBS. A single English word W (367,184 distinct order/alphabet pairs, length 4-20) sets
   the keyed-columnar column order AND the mixed tableau alphabet (W deduplicated, then the rest of A-Z), as K1-K3's
   economy of keys suggests. The cipher key is FREE: any periodic key of length L <= LMAX (exact against the 24 official
   crib letters; L <= 13 fully over-determined). Layers: columnar (or none) and its inverse, key before or after,
   Vigenere or Beaufort, on the W-mixed tableau (Quagmire III style) plus the A-Z and KRYPTOS tableaux as reference.
   DOUBLE=1: the same word keys BOTH columnar passes (K3 is a double transposition). Geometry and checker identical to cycle 52's dcol.c (s = 0 only). usage: c64 CARVED qg.bin words64.txt part nparts */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char*KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
float*QG; int LMAX=22; const char*car; int num[3][26],den[3][26],cp[24],cl[24];
long cons[3][2][2][27], tests; float best=-99;
static float score(const int*x){float s=0;for(int i=0;i+3<N;i++)s+=QG[((x[i]*26+x[i+1])*26+x[i+2])*26+x[i+3]];return s/(N-3);}
static void check(const int*P,const char*tag,int e0,int e1){int inv[N]; for(int k=0;k<N;k++)inv[P[k]]=k;
 for(int e=e0;e<=e1;e++)for(int m=0;m<2;m++){
  int ct[N]; for(int k=0;k<N;k++) ct[k]=num[e][(m==0? car[P[k]] : car[k])-'A'];
  int ki[24],v[2][24]; for(int j=0;j<24;j++){ki[j]= m==0? cp[j] : inv[cp[j]]; int px=num[e][cl[j]], cx=ct[ki[j]];
    v[0][j]=((cx-px)%26+26)%26; v[1][j]=(cx+px)%26;}
  for(int md=0;md<2;md++)for(int L=1;L<=LMAX;L++){tests++;
    int k[26]; for(int c=0;c<L;c++)k[c]=-1; int ok=1;
    for(int j=0;j<24;j++){int i=ki[j]; int kv=v[md][j]; int c=i%L;
      if(k[c]<0)k[c]=kv; else if(k[c]!=kv){ok=0;break;}}
    if(!ok)continue;
    cons[e][m][md][L]++;
    if(L>13 && !(getenv("PRINTL")&&atoi(getenv("PRINTL"))==L))continue;
    int miss[26],nm=0; for(int c=0;c<L;c++) if(k[c]<0){miss[nm++]=c;k[c]=0;}
    int pt[N],po[N];
    #define DEC() for(int i=0;i<N;i++){int key=k[i%L]; int x= md==0? ((ct[i]-key)%26+26)%26 : ((key-ct[i])%26+26)%26; pt[i]=den[e][x];} \
      if(m==1){for(int i=0;i<N;i++)po[i]=pt[inv[i]];} else memcpy(po,pt,sizeof pt);
    if(nm){ for(int pass=0;pass<3;pass++)for(int u=0;u<nm;u++){int bv=0;float bs=-99; for(int vv=0;vv<26;vv++){k[miss[u]]=vv; DEC(); float t=score(po); if(t>bs){bs=t;bv=vv;}} k[miss[u]]=bv;} }
    DEC(); float sc=score(po); if(sc>best)best=sc;
    char o[N+1];for(int i=0;i<N;i++)o[i]='A'+po[i];o[N]=0;
    printf("HIT %s tab=%c model=%c mode=%c L=%d free=%d score=%.3f pt=%s\n",tag,"AKW"[e],m?'B':'A',md?'B':'V',L,nm,sc,o);}}}
static void col(int w,const int*o,int*P){int k=0; int rows=(N+w-1)/w; for(int j=0;j<w;j++){int c=o[j]; for(int r=0;r<rows;r++){int i=r*w+c; if(i<N)P[i]=k++;}}}
int main(int argc,char**argv){
  car=argv[1]; if(getenv("LMAX"))LMAX=atoi(getenv("LMAX"));
  int part_i=atoi(argv[4]), nparts=atoi(argv[5]);
  QG=malloc(sizeof(float)*456976); FILE*f=fopen(argv[2],"rb"); if(fread(QG,4,456976,f)!=456976)return 1; fclose(f);
  for(int l=0;l<26;l++){num[0][l]=l; num[1][l]=strchr(KA,'A'+l)-KA;}
  const char*cr1="EASTNORTHEAST",*cr2="BERLINCLOCK"; int nc=0;
  for(int i=0;i<13;i++){cp[nc]=21+i;cl[nc++]=cr1[i]-'A';} for(int i=0;i<11;i++){cp[nc]=63+i;cl[nc++]=cr2[i]-'A';}
  FILE*g=fopen(argv[3],"r"); char nm[32]; int w,o[20],idx=0; long nw=0;
  while(fscanf(g,"%31s %d",nm,&w)==2){for(int j=0;j<w;j++)if(fscanf(g,"%d",&o[j])!=1)return 2;
    if((idx++)%nparts!=part_i)continue; nw++;
    char a[27]; int used[26]={0},n=0; for(int j=0;nm[j];j++){int c=nm[j]-'A'; if(!used[c]){used[c]=1;a[n++]=nm[j];}} for(int c=0;c<26;c++)if(!used[c])a[n++]='A'+c;
    for(int l=0;l<26;l++)num[2][a[l]-'A']=l; for(int e=0;e<3;e++)for(int l=0;l<26;l++)den[e][num[e][l]]=l;
    int P[N],Q[N]; col(w,o,P); if(getenv("DOUBLE")){int T[N]; for(int i=0;i<N;i++)T[i]=P[P[i]]; memcpy(P,T,sizeof T);} for(int i=0;i<N;i++)Q[P[i]]=i; char tag[64];
    sprintf(tag,"w=%s inv=0",nm); check(P,tag,0,2);
    sprintf(tag,"w=%s inv=1",nm); check(Q,tag,0,2);
    int I[N]; for(int i=0;i<N;i++)I[i]=i; sprintf(tag,"w=%s notrans",nm); check(I,tag,2,2);}
  printf("SUMMARY part=%d words=%ld tests=%ld best_qg=%.3f\n",part_i,nw,tests,best);
  for(int e=0;e<3;e++)for(int m=0;m<2;m++)for(int md=0;md<2;md++){printf("tab=%c model=%c mode=%c byL","AKW"[e],m?'B':'A',md?'B':'V');for(int L=1;L<=LMAX;L++)printf(" %ld",cons[e][m][md][L]);printf("\n");}
  return 0;}
