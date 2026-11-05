/* Cycle 100b: homophonic (any function) behind EVERY irregular columnar transposition of width w (all w! column orders), map and inverse.
   Columnar: write row-major into w columns (last row short), read columns in key order. Exact crib consistency only.
   Usage: ./homocol CT w [first_col_index_or_-1] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
int crib[N];
int main(int argc,char**argv){ const char*CT=argv[1]; int w=atoi(argv[2]); int fc=argc>3?atoi(argv[3]):-1;
  const char*a="EASTNORTHEAST",*b="BERLINCLOCK"; for(int i=0;i<N;i++)crib[i]=-1;
  for(int i=0;i<13;i++)crib[21+i]=a[i]-65; for(int i=0;i<11;i++)crib[63+i]=b[i]-65;
  int C[N]; for(int i=0;i<N;i++)C[i]=CT[i]-65;
  int ord[16]; for(int i=0;i<w;i++)ord[i]=i; long tot=0,cons=0;
  do{ if(fc>=0 && ord[0]!=fc) goto next;
    { int s[N],k=0; for(int j=0;j<w;j++){int col=ord[j]; for(int r=col;r<N;r+=w) s[r]=k++;} /* plaintext pos r -> cipher pos s[r] */
      for(int inv=0;inv<2;inv++){ int t[N]; if(!inv)memcpy(t,s,sizeof s); else for(int i=0;i<N;i++)t[s[i]]=i;
        tot++; int f[26]; for(int q=0;q<26;q++)f[q]=-1; int ok=1;
        for(int i=21;i<74&&ok;i++){ if(crib[i]<0)continue; int c=C[t[i]]; if(f[c]<0)f[c]=crib[i]; else if(f[c]!=crib[i])ok=0; }
        if(ok){cons++; printf("CONS w=%d inv=%d ord=",w,inv); for(int j=0;j<w;j++)printf("%d,",ord[j]); putchar('\n');} } }
    next:;
    int i=w-2; while(i>=0&&ord[i]>ord[i+1])i--; if(i<0)break; int j=w-1; while(ord[j]<ord[i])j--; int x=ord[i];ord[i]=ord[j];ord[j]=x;
    for(int l=i+1,r=w-1;l<r;l++,r--){x=ord[l];ord[l]=ord[r];ord[r]=x;}
  }while(1);
  fprintf(stderr,"w=%d fc=%d configs %ld consistent %ld\n",w,fc,tot,cons); }
