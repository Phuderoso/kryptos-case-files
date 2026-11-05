/* Cycle 71: Wheatstone cryptograph (1867), exact crib-consistency test, direct and behind transpositions (model A).
   Device: outer circle of Mo symbols (plaintext), inner circle of Mi symbols (cipher, arbitrary mixed order).
   Both hands advance together one cell per step; to encipher p, step clockwise (>=1 step) until the long hand is on p,
   output the inner symbol under the short hand. Cumulative step count T: outer cell T mod Mo, inner cell T mod Mi.
   G1 (Wheatstone's own): Mo=27 (26 letters + blank inserted in any gap), Mi=26.  G2: Mo=26, Mi=27 (one inner cell unused).
   Within a crib the step increments are fixed by the plaintext, so the inner index of each crib letter is known up to
   one unknown rotation per crib; consistency = same index -> same letter and same letter -> same index.
   Model A: car[P[i]] = Wheatstone(pt)[i]. Direction: clockwise or counter-clockwise (= reversed outer order).
   usage: wheat71 carved.txt perms.bin alph.bin [maxperms] ; prints survivors and summary */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
int main(int argc,char**argv){
  char car[128];FILE*f=fopen(argv[1],"r");if(fscanf(f,"%127s",car)!=1)return 1;fclose(f);
  f=fopen(argv[2],"rb");fseek(f,0,SEEK_END);long sz=ftell(f);fseek(f,0,SEEK_SET);int np=sz/(2*N);
  short*perms=malloc(sz);if(fread(perms,2,(size_t)np*N,f)!=(size_t)np*N)return 1;fclose(f);
  if(argc>4)np=atoi(argv[4]);
  f=fopen(argv[3],"rb");fseek(f,0,SEEK_END);long asz=ftell(f);fseek(f,0,SEEK_SET);int na=asz/26;
  unsigned char*A=malloc(asz);if(fread(A,1,asz,f)!=(size_t)asz)return 1;fclose(f);
  const char*cr1="EASTNORTHEAST",*cr2="BERLINCLOCK";
  /* build configs */
  int maxc=na*(26+1)*2; int (*D1)[13]=malloc(sizeof(int)*13*maxc),(*D2)[11]=malloc(sizeof(int)*11*maxc);
  int *cfa=malloc(4*maxc),*cfg=malloc(4*maxc),*cfd=malloc(4*maxc),*cMi=malloc(4*maxc);int nc=0;
  for(int a=0;a<na;a++)for(int g=-1;g<26;g++)for(int d=0;d<2;d++){
    int pos[27],Mo,Mi; int seq[27],L=0;
    if(g<0){Mo=26;Mi=27;for(int k=0;k<26;k++)seq[L++]=A[a*26+k];}
    else{Mo=27;Mi=26;for(int k=0;k<26;k++){seq[L++]=A[a*26+k];if(k==g)seq[L++]=26;}}
    if(d){for(int k=0;k<L/2;k++){int t=seq[k];seq[k]=seq[L-1-k];seq[L-1-k]=t;}}
    for(int k=0;k<L;k++)pos[seq[k]]=k;
    int T=0;for(int k=0;k<13;k++){if(k){int s=((pos[cr1[k]-'A']-pos[cr1[k-1]-'A'])%Mo+Mo)%Mo;if(!s)s=Mo;T+=s;}D1[nc][k]=T%Mi;}
    T=0;for(int k=0;k<11;k++){if(k){int s=((pos[cr2[k]-'A']-pos[cr2[k-1]-'A'])%Mo+Mo)%Mo;if(!s)s=Mo;T+=s;}D2[nc][k]=T%Mi;}
    cfa[nc]=a;cfg[nc]=g;cfd[nc]=d;cMi[nc]=Mi;nc++;}
  long p1=0,p2=0,p12=0;
  for(int p=0;p<np;p++){short*P=perms+(long)p*N;int c1[13],c2[11];
    for(int k=0;k<13;k++)c1[k]=car[P[21+k]]-'A';for(int k=0;k<11;k++)c2[k]=car[P[63+k]]-'A';
    for(int c=0;c<nc;c++){int Mi=cMi[c];signed char im[27],li[26];memset(im,-1,27);memset(li,-1,26);int ok=1;
      for(int k=0;k<13&&ok;k++){int i=D1[c][k],l=c1[k];
        if(im[i]<0&&li[l]<0){im[i]=l;li[l]=i;} else if(im[i]!=l||li[l]!=i) ok=0;}
      if(!ok)continue; p1++;
      int any=0;
      for(int r=0;r<Mi;r++){signed char im2[27],li2[26];memcpy(im2,im,27);memcpy(li2,li,26);int ok2=1;
        for(int k=0;k<11&&ok2;k++){int i=(D2[c][k]+r)%Mi,l=c2[k];
          if(im2[i]<0&&li2[l]<0){im2[i]=l;li2[l]=i;} else if(im2[i]!=l||li2[l]!=i) ok2=0;}
        if(ok2){any++;printf("SURV perm=%d alpha=%d gap=%d dir=%d Mi=%d r=%d\n",p,cfa[c],cfg[c],cfd[c],Mi,r);}}
      if(any)p12++;}
    /* crib2 alone */
    for(int c=0;c<nc;c++){signed char im[27],li[26];memset(im,-1,27);memset(li,-1,26);int ok=1;
      for(int k=0;k<11&&ok;k++){int i=D2[c][k],l=c2[k];
        if(im[i]<0&&li[l]<0){im[i]=l;li[l]=i;} else if(im[i]!=l||li[l]!=i) ok=0;}
      if(ok)p2++;}
  }
  printf("SUMMARY perms=%d configs=%d tests=%ld crib1_ok=%ld crib2_ok=%ld both_ok=%ld\n",np,nc,(long)np*nc,p1,p2,p12);return 0;}
