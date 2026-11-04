/* Cycle 41: PROGRESSIVE KEYWORD substitution (the keyword repeats, but each repetition is shifted by s more:
   key_i = k[i mod L] + s*floor(i/L)), the classic "progressive key" of Kasiski-era manuals, on either side of
   a transposition, A-Z or KRYPTOS tableau, Vigenere (c = p + key) or Beaufort (c = key - p).
   Variant Beaufort (c = p - key) is Vigenere with the key negated, step included, so it is covered.
   s = 0 is the plain periodic key (already excluded in earlier cycles; kept as a sanity check).
   L 1..13: every key class holds at least one letter of EASTNORTHEAST, so a consistent config fixes all 97
   letters in model A.  In model B the crib positions are scattered by the transposition, so a few classes
   can stay unfixed: those key letters are filled by quadgram hill-climbing (free=n in the output).
   L 14..26 is overfit (too many free unknowns): consistent configs are only counted and compared with nulls.
   Index i = plaintext position (model A: carved[P[i]] enciphers pt[i]) or carved position (model B), as in cycle 40.
   usage: progkw CARVED perms.bin qg.bin [start end] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char*KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
float*QG; int SMAX=26;
static float score(const int*x){float s=0;for(int i=0;i+3<N;i++)s+=QG[((x[i]*26+x[i+1])*26+x[i+2])*26+x[i+3]];return s/(N-3);}
int main(int argc,char**argv){
  const char*car=argv[1]; FILE*f=fopen(argv[2],"rb"); fseek(f,0,SEEK_END); long sz=ftell(f); fseek(f,0,SEEK_SET);
  int np=sz/(2*N); short*perms=malloc(sz); if(fread(perms,2,(size_t)np*N,f)!=(size_t)np*N)return 1; fclose(f);
  if(getenv("SMAX"))SMAX=atoi(getenv("SMAX")); int p0=0; if(argc>5){p0=atoi(argv[4]); int m=atoi(argv[5]); if(m<np)np=m;}
  QG=malloc(sizeof(float)*456976); f=fopen(argv[3],"rb"); if(fread(QG,4,456976,f)!=456976)return 1; fclose(f);
  int num[2][26],den[2][26]; for(int l=0;l<26;l++){num[0][l]=l; num[1][l]=strchr(KA,'A'+l)-KA;} for(int e=0;e<2;e++)for(int l=0;l<26;l++)den[e][num[e][l]]=l;
  const char*cr1="EASTNORTHEAST",*cr2="BERLINCLOCK"; int cp[24],cl[24],nc=0;
  for(int i=0;i<13;i++){cp[nc]=21+i;cl[nc++]=cr1[i]-'A';} for(int i=0;i<11;i++){cp[nc]=63+i;cl[nc++]=cr2[i]-'A';}
  long cons[2][2][2][2]={{{{0}}}}; float best=-99; long tests=0, part[27]={0};
  for(int p=p0;p<np;p++){short*P=perms+(long)p*N; int inv[N]; for(int k=0;k<N;k++)inv[P[k]]=k;
   for(int e=0;e<2;e++)for(int m=0;m<2;m++){
    int ct[N]; for(int k=0;k<N;k++) ct[k]=num[e][(m==0? car[P[k]] : car[k])-'A'];
    int ki[24],v[2][24]; for(int j=0;j<24;j++){ki[j]= m==0? cp[j] : inv[cp[j]]; int px=num[e][cl[j]], cx=ct[ki[j]];
      v[0][j]=((cx-px)%26+26)%26; v[1][j]=(cx+px)%26;}
    for(int md=0;md<2;md++)for(int L=1;L<=26;L++)for(int s=0;s<SMAX;s++){tests++;
      int k[26]; for(int c=0;c<L;c++)k[c]=-1; int ok=1;
      for(int j=0;j<24;j++){int i=ki[j]; int kv=((v[md][j]-s*(i/L))%26+26*26)%26; int c=i%L;
        if(k[c]<0)k[c]=kv; else if(k[c]!=kv){ok=0;break;}}
      if(!ok)continue;
      cons[e][m][md][s>0]++;
      if(L>13){if(s>0)part[L]++;continue;}
      int miss[13],nm=0; for(int c=0;c<L;c++) if(k[c]<0){miss[nm++]=c;k[c]=0;}
      int pt[N],po[N];
      #define DEC() for(int i=0;i<N;i++){int key=(k[i%L]+s*(i/L))%26; int x= md==0? ((ct[i]-key)%26+26)%26 : ((key-ct[i])%26+26)%26; pt[i]=den[e][x];} \
        if(m==1){for(int i=0;i<N;i++)po[i]=pt[inv[i]];} else memcpy(po,pt,sizeof pt);
      float sc;
      if(nm){ for(int pass=0;pass<3;pass++)for(int u=0;u<nm;u++){int bv=0;float bs=-99; for(int v=0;v<26;v++){k[miss[u]]=v; DEC(); float t=score(po); if(t>bs){bs=t;bv=v;}} k[miss[u]]=bv;} }
      DEC(); sc=score(po); if(sc>best)best=sc;
      char o[N+1],kw[27];for(int i=0;i<N;i++)o[i]='A'+po[i];o[N]=0; for(int c=0;c<L;c++)kw[c]= e? KA[k[c]] : 'A'+k[c]; kw[L]=0;
      printf("HIT perm=%d num=%c model=%c mode=%c L=%d s=%d free=%d key=%s score=%.3f pt=%s\n",p,e?'K':'A',m?'B':'A',md?'B':'V',L,s,nm,kw,sc,o);}}}
  printf("SUMMARY perms=%d tests=%ld best_qg=%.3f\n",np-p0,tests,best);
  for(int e=0;e<2;e++)for(int m=0;m<2;m++)for(int md=0;md<2;md++)printf("num=%c model=%c mode=%c consistent_s0=%ld consistent_s>0=%ld\n",e?'K':'A',m?'B':'A',md?'B':'V',cons[e][m][md][0],cons[e][m][md][1]);
  printf("PARTIAL_BY_L");for(int L=14;L<=26;L++)printf(" %d:%ld",L,part[L]);printf("\n");
  return 0;}
