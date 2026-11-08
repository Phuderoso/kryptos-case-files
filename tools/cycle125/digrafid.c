/* Cycle 125: Digrafid (ACA; Delastelle-family digraphic fractionation over 27 symbols A-Z + '#').
   Grid1: keyword-1 alphabet written row-wise in 3 rows x 9 cols.  Grid2: keyword-2 alphabet in 9 rows x 3 cols,
   filled down the columns (fill2=0, ACA) or across the rows (fill2=1).  Pair (a,b): a -> (row ra 0-2, col ca 0-8),
   b -> (row rb 0-8, col cb 0-2), triple (ca, 3*ra+cb, rb). Block of p pairs: triples written as columns of a 3 x p
   array, read row by row, regrouped in triples, each triple (x,m,y) -> (grid1[m/3][x], grid2[y][m%3]).
   K4 has 97 letters (odd), so plain Digrafid cannot produce it. Length models:
     A d : carved letter d is a null; drop it -> 96 letters; crib positions after d shift by -1.
     B d : one ciphertext letter is missing before carved position d (98-letter cipher, pt 98); the block holding
           the gap cannot be decrypted, so cribs in that block are skipped (need >= 12 cribs checked).
   usage: digrafid CT keys.txt pairs.txt PMAX DMODE label
     keys.txt: one 27-symbol alphabet per line (name alphabet); pairs.txt: lines "i j" (indices into keys)
     DMODE 0 = all d, 1 = only the natural ends (A 96 drop last, B 97 append).
   output: survivors "S label i j fill2 model d p"; final counts. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const int CRP[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *CRS="EASTNORTHEASTBERLINCLOCK";
#define MAXK 20000
static char alph[MAXK][28]; static char nm[MAXK][40]; static int nk;
static int g1r[27],g1c[27],g2r[27],g2c[27]; static int G1[3][9],G2[9][3];
static int sym(char c){return c=='#'?26:c-'A';}
int main(int argc,char**argv){
  const char*s=argv[1]; int n0=strlen(s); int PMAX=atoi(argv[4]),DM=atoi(argv[5]); const char*lab=argv[6];
  FILE*f=fopen(argv[2],"r"); char b1[64],b2[64]; while(nk<MAXK && fscanf(f,"%39s %63s",b1,b2)==2){strcpy(nm[nk],b1);memcpy(alph[nk],b2,28);nk++;} fclose(f);
  /* build all ciphertext variants: model A drop d, model B gap at d */
  long tests=0,surv=0; int ct[100],L,gap; int pt[100];
  FILE*pf=fopen(argv[3],"r"); int ki,kj;
  while(fscanf(pf,"%d %d",&ki,&kj)==2){
   for(int fill2=0;fill2<2;fill2++){
    for(int t=0;t<27;t++){int x=sym(alph[ki][t]); g1r[x]=t/9; g1c[x]=t%9; G1[t/9][t%9]=x;}
    for(int t=0;t<27;t++){int x=sym(alph[kj][t]); int r,c; if(fill2==0){c=t/9;r=t%9;} else {r=t/3;c=t%3;} g2r[x]=r; g2c[x]=c; G2[r][c]=x;}
    for(int model=0;model<2;model++){
     int dlo=0,dhi=model?97:96; if(DM==1){dlo=dhi;}
     for(int d=dlo;d<=dhi;d++){
      /* build ct */
      if(model==0){ L=0; for(int i=0;i<n0;i++) if(i!=d) ct[L++]=sym(s[i]); gap=-1; }
      else { L=0; for(int i=0;i<n0;i++){ if(i==d) ct[L++]=-1; ct[L++]=sym(s[i]); } if(d==n0) ct[L++]=-1; gap=d; }
      int cp[24]; for(int t=0;t<24;t++) cp[t]= (model==0 && CRP[t]>d)? CRP[t]-1 : CRP[t];
      if(model==0){ int bad=0; for(int t=0;t<24;t++) if(CRP[t]==d) bad=1; if(bad) continue; }
      int np=L/2;
      for(int p=1;p<=PMAX && p<=np;p++){
        tests++; int ok=1,checked=0;
        for(int t=0;t<24 && ok;t++){
          int pos=cp[t], pair=pos/2, blk=pair/p, b0=blk*p, bl=(np-b0<p)?np-b0:p;
          if(gap>=0 && gap/2>=b0 && gap/2<b0+bl) continue; /* gap in this block */
          /* digit sequence of block: triple k = pair b0+k */
          int jj=pair-b0; int dig[3];
          for(int row=0;row<3;row++){ int q=row*bl+jj; int tri=q/3, wi=q%3; int a=ct[2*(b0+tri)], bb=ct[2*(b0+tri)+1];
            int x=g1c[a], m=3*g1r[a]+g2c[bb], y=g2r[bb]; dig[row]= wi==0?x:(wi==1?m:y); }
          int plet = (pos%2==0)? G1[dig[1]/3][dig[0]] : G2[dig[2]][dig[1]%3];
          checked++; if(plet!=CRS[t]-'A') ok=0;
        }
        if(ok && checked>=12){ surv++; printf("S %s %s %s %d %d %d %d chk%d\n",lab,nm[ki],nm[kj],fill2,model,d,p,checked); }
      } } } } }
  printf("C %s tests %ld survivors %ld\n",lab,tests,surv); return 0; }
