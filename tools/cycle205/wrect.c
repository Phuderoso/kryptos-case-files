/* Cycle 205, I-259: exact enumeration of 5-separator placements in 97 positions (1-indexed a<b<c<d<e),
   reproducing the published counts of glthr.com (2026-11-11) under explicit definitions.
   EQ: alternating groups equal (a+c+e-b-d == 49).
   RECT: exists width w in 3..48 with a,b on one row, d,e on another row (rows of w), col a == col d, col b == col e.
   SYM:  RECT and the rectangle is centred on the w x R grid (R = floor(97/w)): a+e == R*w+1.
   CEN:  SYM and c within one cell (same row, |col diff|<=1) of the grid centre cell when R*w is odd, else c in the 2 central cells.
   INSET: SYM and a is at row 2, col 2 (1-indexed) of the grid. */
#include <stdio.h>
int main(){ long long tot=0,eq=0,r1=0,sym=0,cen=0,ins=0,eqr1=0,eqsym=0,eqr1s3=0,eqsyms3=0, insc=0;
 for(int a=1;a<=93;a++)for(int b=a+1;b<=94;b++)for(int c=b+1;c<=95;c++)for(int d=c+1;d<=96;d++)for(int e=d+1;e<=97;e++){
  tot++; int E=(a+c+e-b-d==49); eq+=E;
  int s3 = (a-1>=3)&&(b-a-1>=3)&&(c-b-1>=3)&&(d-c-1>=3)&&(e-d-1>=3)&&(97-e>=3);
  int R1=0,S=0,C=0,I=0;
  if(b-a==e-d){ for(int w=3;w<=48;w++){ int ra=(a-1)/w, rb=(b-1)/w, rd=(d-1)/w, re=(e-1)/w;
     if(ra!=rb||rd!=re||ra==rd) continue; if((a-1)%w!=(d-1)%w) continue; R1=1;
     int R=97/w; if(a+e==R*w+1){ S=1; int n=R*w; int ctr=(n+1)/2; /* 1-indexed centre (lower middle if even) */
        int cr=(ctr-1)/w, rc=(c-1)/w; int dc=(c-1)%w-(ctr-1)%w; if(dc<0)dc=-dc;
        int cc = (rc==cr && dc<=1);
        if(cc) C=1;
        if((a-1)/w==1 && (a-1)%w==1){ I=1; if(cc) insc=insc; }
        if(cc && (a-1)/w==1 && (a-1)%w==1) insc++; } } }
  r1+=R1; sym+=S; cen+=C; ins+=I; if(E&&R1)eqr1++; if(E&&S)eqsym++; if(E&&R1&&s3)eqr1s3++; if(E&&S&&s3)eqsyms3++;
 }
 printf("total %lld\nEQ %lld\nRECT %lld\nSYM %lld\nSYM+centre %lld\nSYM+inset %lld\nSYM+inset+centre(width-hits) %lld\nEQ&RECT %lld\nEQ&SYM %lld\nEQ&RECT&seg>=3 %lld\nEQ&SYM&seg>=3 %lld\n",tot,eq,r1,sym,cen,ins,insc,eqr1,eqsym,eqr1s3,eqsyms3);
 int k[5]={21,37,49,59,75}; printf("K4 W check EQ=%d\n", k[0]+k[2]+k[4]-k[1]-k[3]==49); }
